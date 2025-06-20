from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus
from pymoo.indicators.igd import IGD
from pymoo.indicators.igd_plus import IGDPlus
from pymoo.util.ref_dirs import get_reference_directions
import numpy as np
import pandas as pd
import os
import math
import time
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

# Parámetros técnicos
E100km = 11.03
Cev = (E100km / 100) * 175
Cphev = (E100km / 100) * 175 * 0.7
P = [7, 20, 60]

# Cargar promedios de EV y PHEV
df_vehicles = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_projections.csv')
scenario = 'Scenario 3'
df_scenario = df_vehicles[df_vehicles['Scenario'] == scenario]
ev_list = list(df_scenario["EV"])
phev_list = list(df_scenario["PHEV"])

def percentage_preference_type_charger(vehicles):
    np.random.seed(0)
    BL1, BL2, BL3 = [], [], []

    B = np.random.random(vehicles)
    L2 = np.random.random(vehicles)
    L3 = []
    for j in range(len(B)):
        L3.append(1 - L2[j])
        BL1.append(1-B[j])
        BL2.append(B[j] * L2[j])
        BL3.append(B[j] * L3[j])
    return np.sum(BL1), np.sum(BL2), np.sum(BL3)

def cp_technical_metrics(Cev, Cphev, BL1ev, BL1phev, BL2ev, BL2phev, BL3ev, BL3phev, P, T, initial_cp):

    demand_L1 = ((Cev * BL1ev) + (Cphev * BL1phev))
    demand_L2 = ((Cev * BL2ev) + (Cphev * BL2phev))
    demand_L3 = ((Cev * BL3ev) + (Cphev * BL3phev))

    L1 = ((Cev * BL1ev) + (Cphev * BL1phev)) / (P[0] * T[0])
    L2 = ((Cev * BL2ev) + (Cphev * BL2phev)) / (P[1] * T[1])
    L3 = ((Cev * BL3ev) + (Cphev * BL3phev)) / (P[2] * T[2])

    chargersLow     = max( L1, initial_cp[0])
    chargersSemifast= max( L2, initial_cp[1])
    chargersFast    = max( L3, initial_cp[2])

    return chargersLow, chargersSemifast, chargersFast, demand_L1+demand_L2+demand_L3

def power_generated(area_available):
    powerPanelPV = 550
    areaPanelPV = 3
    hps = 3.5
    numberPanelPV = math.ceil(area_available / areaPanelPV)
    powerPlantPV = numberPanelPV * 0.9 * powerPanelPV * hps / 1000
    return round(powerPlantPV)

def sizing_battery_system(powerPlantPV):
    autonomy_days = 20/24
    nominal_voltage = 24
    discharge_depth = 0.7
    batCapacity = (powerPlantPV)* autonomy_days * nominal_voltage / (nominal_voltage * discharge_depth)
    Cbat = 60.6
    num_batteries = batCapacity / Cbat
    return round(batCapacity)

def calculate_reinforcement(P_base, P_max, P_VE, P_DER):
    FP_red = 0.9
    FP_VE = 0.9
    FP_DER = 0.95
    S_base = np.sqrt((P_base**2) + ((P_base * math.tan(math.acos(FP_red)))**2))
    S_max = np.sqrt((P_max**2) + ((P_max * math.tan(math.acos(FP_red)))**2))
    f_utilizacion = 0.9
    delta_P = P_VE - P_DER
    delta_Q = (P_VE * math.tan(math.acos(FP_VE))) - (P_DER * math.tan(math.acos(FP_DER)))
    S_total = np.sqrt(delta_P**2 + delta_Q**2)
    S_refor = (((S_base + S_total) / (f_utilizacion)) - S_max  ) 
    S_refor_percentage = S_refor / S_max
    return S_refor_percentage

def job_charging_station(totalChargerPoints):
    jobsPerCS = 5
    jobs_CS = ( (((totalChargerPoints[0] + totalChargerPoints[1]) * jobsPerCS / 2)))
    return jobs_CS

def calcular_emisiones_CO2(P_pv, P_red):
    CO2paneles = (P_pv * 24 * 365) * 40  # g CO2 eq por año
    CO2electricidad = P_red * 164.38  # g CO2 eq anual
    CO2total_anual = CO2paneles + CO2electricidad
    return CO2total_anual

# NUEVAS FUNCIONES PARA MÉTRICAS DE RENDIMIENTO

def calculate_spacing_metric(pareto_front):
    """
    Calcula la métrica de espaciado (Spacing) del frente de Pareto.
    Mide la uniformidad de la distribución de soluciones.
    """
    if len(pareto_front) < 2:
        return 0.0
    
    distances = []
    for i, sol in enumerate(pareto_front):
        min_dist = float('inf')
        for j, other_sol in enumerate(pareto_front):
            if i != j:
                dist = np.linalg.norm(sol - other_sol)
                min_dist = min(min_dist, dist)
        distances.append(min_dist)
    
    mean_dist = np.mean(distances)
    spacing = np.sqrt(np.mean([(d - mean_dist)**2 for d in distances]))
    return spacing

def calculate_extent_metric(pareto_front):
    """
    Calcula la métrica de extensión (Extent) del frente de Pareto.
    Mide el rango cubierto por las soluciones en cada objetivo.
    """
    if len(pareto_front) < 2:
        return [0.0] * pareto_front.shape[1]
    
    extents = []
    for obj in range(pareto_front.shape[1]):
        extent = np.max(pareto_front[:, obj]) - np.min(pareto_front[:, obj])
        extents.append(extent)
    return extents

def calculate_convergence_rate(history_f):
    """
    Calcula la tasa de convergencia basada en el historial de mejores soluciones.
    """
    if len(history_f) < 2:
        return 0.0
    
    # Calcular el hypervolume en cada generación
    hv_values = []
    ref_point = np.max(history_f[-1], axis=0) + 1  # Punto de referencia
    
    for gen_f in history_f:
        if len(gen_f) > 0:
            hv = HV(ref_point=ref_point)
            hv_val = hv(gen_f)
            hv_values.append(hv_val)
        else:
            hv_values.append(0.0)
    
    # Calcular la tasa de mejora
    improvements = []
    for i in range(1, len(hv_values)):
        if hv_values[i-1] > 0:
            improvement = (hv_values[i] - hv_values[i-1]) / hv_values[i-1]
            improvements.append(improvement)
    
    return np.mean(improvements) if improvements else 0.0

def calculate_diversity_metric(pareto_front):
    """
    Calcula una métrica de diversidad basada en la distancia promedio entre soluciones.
    """
    if len(pareto_front) < 2:
        return 0.0
    
    distances = pdist(pareto_front)
    return np.mean(distances)

def generate_reference_front(problem, n_points=100):
    """
    Genera un frente de referencia usando muestreo aleatorio para calcular IGD.
    """
    # Muestreo aleatorio en el espacio de variables
    np.random.seed(42)  # Para reproducibilidad
    X_ref = np.random.uniform(problem.xl, problem.xu, (n_points * 10, problem.n_var))
    
    # Evaluar todas las soluciones
    F_ref = []
    for x in X_ref:
        out = {}
        problem._evaluate(x, out)
        F_ref.append(out["F"])
    
    F_ref = np.array(F_ref)
    
    # Encontrar soluciones no dominadas
    from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
    nds = NonDominatedSorting()
    I = nds.do(F_ref, only_non_dominated_front=True)
    
    return F_ref[I]

class PerformanceTracker:
    """
    Clase para rastrear métricas de rendimiento durante la optimización.
    """
    def __init__(self, reference_front=None):
        self.reference_front = reference_front
        self.metrics_history = []
        self.execution_times = []
        self.hypervolume_history = []
        
    def calculate_metrics(self, result, execution_time, generation=None):
        """
        Calcula todas las métricas de rendimiento para un resultado dado.
        """
        metrics = {}
        
        if result.F is not None and len(result.F) > 0:
            # Métricas básicas
            metrics['n_solutions'] = len(result.F)
            metrics['execution_time'] = execution_time
            
            # Hypervolume
            ref_point = np.max(result.F, axis=0) + 1
            hv = HV(ref_point=ref_point)
            metrics['hypervolume'] = hv(result.F)
            
            # Spacing (uniformidad)
            metrics['spacing'] = calculate_spacing_metric(result.F)
            
            # Extent (rango de objetivos)
            extents = calculate_extent_metric(result.F)
            for i, ext in enumerate(extents):
                metrics[f'extent_obj_{i+1}'] = ext
            
            # Diversidad
            metrics['diversity'] = calculate_diversity_metric(result.F)
            
            # Métricas que requieren frente de referencia
            if self.reference_front is not None:
                # IGD (Inverted Generational Distance)
                igd = IGD(self.reference_front)
                metrics['igd'] = igd(result.F)
                
                # IGD+
                igd_plus = IGDPlus(self.reference_front)
                metrics['igd_plus'] = igd_plus(result.F)
                
                # GD (Generational Distance)
                gd = GD(self.reference_front)
                metrics['gd'] = gd(result.F)
                
                # GD+
                gd_plus = GDPlus(self.reference_front)
                metrics['gd_plus'] = gd_plus(result.F)
        
        else:
            # Si no hay soluciones válidas
            metrics = {
                'n_solutions': 0,
                'execution_time': execution_time,
                'hypervolume': 0,
                'spacing': 0,
                'diversity': 0,
                'igd': float('inf') if self.reference_front is not None else None,
                'gd': float('inf') if self.reference_front is not None else None
            }
        
        if generation is not None:
            metrics['generation'] = generation
            
        self.metrics_history.append(metrics)
        return metrics

# Problema de optimización ajustado a cada año
class EVChargingYearlyProblem(ElementwiseProblem):
    def __init__(self, ev, phev, initial_cp, min_area, year):
        super().__init__(
            n_var=3,
            n_obj=4,
            n_constr=0,
            xl=np.array([8, 8, min_area]),
            xu=np.array([24, 24, 40000])
        )
        self.ev = ev
        self.phev = phev
        self.initial_cp = initial_cp
        self.year = year

    def _evaluate(self, x, out, *args, **kwargs):
        x1, x2, x3 = x

        BL1ev, BL2ev, BL3ev = percentage_preference_type_charger(self.ev)
        BL1phev, BL2phev, BL3phev = percentage_preference_type_charger(self.phev)

        cpl1, cpl2, cpl3, demand = cp_technical_metrics(
            Cev, Cphev,
            BL1ev, BL1phev,
            BL2ev, BL2phev,
            BL3ev, BL3phev,
            P, [24, x1, x2], self.initial_cp
        )
        P_pv = power_generated(x3)
        S_refor = calculate_reinforcement(100000, 104000, demand, P_pv)
        out["F"] = [math.ceil(cpl1), math.ceil(cpl2), math.ceil(cpl3), round(S_refor,2)]

# Crear carpeta de salida si no existe
carpeta_salida = "C:/Nohora/UniValle_project/pasto_case/"
os.makedirs(carpeta_salida, exist_ok=True)

# Inicializar archivos CSV para las 5 mejores soluciones
archivos_csv = [os.path.join(carpeta_salida, f"problem1_solucion_{i+1}.csv") for i in range(5)]
columnas = ["Año", "EV", "PHEV", "tL2", "tL3", "area", "cpl1", "cpl2", "cpl3", "S_refor"]
for ruta in archivos_csv:
    if not os.path.exists(ruta):
        pd.DataFrame(columns=columnas).to_csv(ruta, index=False)

# Archivo para métricas de rendimiento
metricas_csv = os.path.join(carpeta_salida, "metricas_rendimiento_1.csv")
columnas_metricas = ["Año", "n_solutions", "execution_time", "hypervolume", "spacing", 
                    "diversity", "extent_obj_1", "extent_obj_2", "extent_obj_3", "extent_obj_4",
                    "igd", "igd_plus", "gd", "gd_plus", "convergence_rate"]

if not os.path.exists(metricas_csv):
    pd.DataFrame(columns=columnas_metricas).to_csv(metricas_csv, index=False)

initial_cp = [0, 0, 0]
min_area = 11000

# Ejecutar optimización por año con tracking de rendimiento
for year, (ev, phev) in enumerate(zip(ev_list, phev_list), start=1):
    print(f"Año {year}")
    problem = EVChargingYearlyProblem(ev, phev, initial_cp, min_area, year)
    
    # Generar frente de referencia para este problema específico
    reference_front = generate_reference_front(problem, n_points=200)
    
    # Inicializar tracker de rendimiento
    tracker = PerformanceTracker(reference_front)
    
    algorithm = NSGA2(
        pop_size=20,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

    # Medir tiempo de ejecución
    start_time = time.time()
    
    res = minimize(problem, algorithm, ("n_gen", 50), seed=1, verbose=False)
    
    execution_time = time.time() - start_time
    
    # Calcular métricas de rendimiento
    metrics = tracker.calculate_metrics(res, execution_time)
    
    print(f"Métricas de rendimiento para el año {year}:")
    print(f"  - Tiempo de ejecución: {execution_time:.2f} segundos")
    print(f"  - Número de soluciones: {metrics['n_solutions']}")
    print(f"  - Hypervolume: {metrics['hypervolume']:.4f}")
    print(f"  - Spacing: {metrics['spacing']:.4f}")
    print(f"  - Diversidad: {metrics['diversity']:.4f}")
    if 'igd' in metrics and metrics['igd'] is not None:
        print(f"  - IGD: {metrics['igd']:.4f}")
        print(f"  - GD: {metrics['gd']:.4f}")

    if res.X is not None:
        # Asegurar que hay al menos 5 soluciones
        n_sols = min(5, len(res.X))

        for i in range(n_sols):
            x = res.X[i]
            f = res.F[i]

            if i == 0:
                # Solo actualizar si es la mejor solución
                initial_cp = f
                min_area = x[2]

            fila = {
                "Año": year,
                "EV": ev,
                "PHEV": phev,
                "tL2": round(x[0], 1),
                "tL3": round(x[1], 1),
                "area": round(x[2], 1),
                "cpl1": f[0],
                "cpl2": f[1],
                "cpl3": f[2],
                "S_refor": f[3]
            }

            df_fila = pd.DataFrame([fila])
            df_fila.to_csv(archivos_csv[i], mode='a', header=False, index=False)
    else:
        print(f"No se encontraron soluciones factibles para el año {year}.")

    # Guardar métricas de rendimiento
    fila_metricas = {
        "Año": year,
        "n_solutions": metrics['n_solutions'],
        "execution_time": metrics['execution_time'],
        "hypervolume": metrics['hypervolume'],
        "spacing": metrics['spacing'],
        "diversity": metrics['diversity'],
        "extent_obj_1": metrics.get('extent_obj_1', 0),
        "extent_obj_2": metrics.get('extent_obj_2', 0),
        "extent_obj_3": metrics.get('extent_obj_3', 0),
        "extent_obj_4": metrics.get('extent_obj_4', 0),
        "igd": metrics.get('igd', None),
        "igd_plus": metrics.get('igd_plus', None),
        "gd": metrics.get('gd', None),
        "gd_plus": metrics.get('gd_plus', None),
        "convergence_rate": 0  # Se podría calcular con múltiples ejecuciones
    }
    
    df_metricas = pd.DataFrame([fila_metricas])
    df_metricas.to_csv(metricas_csv, mode='a', header=False, index=False)

    print(f"Año {year} completado.")
    print("-" * 50)

print("\nOptimización completada. Métricas guardadas en:", metricas_csv)

# Crear visualización de métricas
def plot_performance_metrics():
    """
    Crea gráficos de las métricas de rendimiento a lo largo de los años.
    """
    df_metrics = pd.read_csv(metricas_csv)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Hypervolume
    axes[0,0].plot(df_metrics['Año'], df_metrics['hypervolume'], 'b-o')
    axes[0,0].set_title('Hypervolume')
    axes[0,0].set_xlabel('Año')
    axes[0,0].grid(True)
    
    # Tiempo de ejecución
    axes[0,1].plot(df_metrics['Año'], df_metrics['execution_time'], 'r-o')
    axes[0,1].set_title('Tiempo de Ejecución (s)')
    axes[0,1].set_xlabel('Año')
    axes[0,1].grid(True)
    
    # Spacing
    axes[0,2].plot(df_metrics['Año'], df_metrics['spacing'], 'g-o')
    axes[0,2].set_title('Spacing (Uniformidad)')
    axes[0,2].set_xlabel('Año')
    axes[0,2].grid(True)
    
    # Diversidad
    axes[1,0].plot(df_metrics['Año'], df_metrics['diversity'], 'm-o')
    axes[1,0].set_title('Diversidad')
    axes[1,0].set_xlabel('Año')
    axes[1,0].grid(True)
    
    # IGD (si está disponible)
    if 'igd' in df_metrics.columns and not df_metrics['igd'].isnull().all():
        axes[1,1].plot(df_metrics['Año'], df_metrics['igd'], 'c-o')
        axes[1,1].set_title('IGD (Inverted Generational Distance)')
        axes[1,1].set_xlabel('Año')
        axes[1,1].grid(True)
    
    # Número de soluciones
    axes[1,2].plot(df_metrics['Año'], df_metrics['n_solutions'], 'k-o')
    axes[1,2].set_title('Número de Soluciones')
    axes[1,2].set_xlabel('Año')
    axes[1,2].grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, 'metricas_rendimiento_1.png'), dpi=300, bbox_inches='tight')
    plt.show()

# Ejecutar visualización (descomenta la siguiente línea si quieres generar los gráficos)
plot_performance_metrics()