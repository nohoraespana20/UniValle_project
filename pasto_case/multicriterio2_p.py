from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
# Importar métricas de rendimiento
from pymoo.indicators.hv import HV
from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus
from pymoo.indicators.igd import IGD
from pymoo.indicators.igd_plus import IGDPlus
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
import numpy as np
import pandas as pd
import os
import math
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def run_doper_model(demand_scale=None, pv_scale=None, battery_capacities=None):
    import gc
    import os
    import pandas as pd
    from pyomo.environ import Objective, minimize
    from doper import DOPER
    from doper.models.basemodel import base_model, default_output_list
    from doper.models.battery import add_battery
    from doper.models.network import add_network
    from doper_parameter_simply import parameters, ts_inputs

    # Control model
    def control_model(inputs, parameter):
        model = base_model(inputs, parameter)
        model = add_battery(model, inputs, parameter)
        model = add_network(model, inputs, parameter)

        def objective_function(model):
            return model.sum_energy_cost * parameter['objective']['weight_energy'] \
                   + model.sum_demand_cost * parameter['objective']['weight_demand'] \
                   + model.sum_export_revenue * parameter['objective']['weight_export'] \
                   + model.fuel_cost_total * parameter['objective']['weight_energy']
        model.objective = Objective(rule=objective_function, sense=minimize, doc='objective function')
        return model

    # Crear parámetros
    parameter = parameters()

    # Modificar capacidades de baterías si se proporcionan
    if battery_capacities is not None:
        for i, cap in enumerate(battery_capacities):
            parameter['batteries'][i]['capacity'] = cap

    # Crear datos multinodo
    data4 = ts_inputs(parameter, load='B90', scale_load=demand_scale * 0.30, scale_pv=pv_scale * 0.15)
    data5 = ts_inputs(parameter, load='B90', scale_load=demand_scale * 0.22, scale_pv=pv_scale * 0.13)
    data6 = ts_inputs(parameter, load='B90', scale_load=demand_scale * 0.48, scale_pv=pv_scale * 0.72)

    data = data5.copy().drop(['load_demand', 'generation_pv'], axis=1)
    data['pf_demand_node4'] = data4['load_demand']
    data['pf_demand_node18'] = data5['load_demand']
    data['pf_demand_node27'] = data6['load_demand']
    data['pf_pv_node4'] = data4['generation_pv']
    data['pf_pv_node18'] = data5['generation_pv']
    data['pf_pv_node27'] = data6['generation_pv']

    # Ejecutar optimización
    solver_path = "C:\\Nohora\\UniValle_project\\pasto_case\\DOPER\\doper\\solvers\\Windows64\\cbc.exe"
    smartDER = DOPER(model=control_model,
                     parameter=parameter,
                     solver_path=solver_path,
                     output_list=default_output_list(parameter))
    
    res = smartDER.do_optimization(data)
    duration, objective, df, model, result, termination, parameter = res

    # Si es correcto, continúa
    P_red = df['Export Power [kW]'].max()
    E_export = df['Export Power [kW]'].sum()
    E_pv = df['PV Power [kW]'].sum()
    print('Resultados DOPER \nP_red = ', P_red, ' E_export = ', E_export, ' E_pv = ', E_pv)
    return P_red, E_export, E_pv

def calculate_iip(E_export, year, E_pv):
    profit  = E_export * 0.12 * 365 / 1000
    discount_rate = 0.09
    discounted_profit = profit / ((1 + discount_rate) ** year)
    iip = discounted_profit / (E_pv*365)

    return iip

# NUEVAS FUNCIONES PARA MÉTRICAS DE RENDIMIENTO

def normalize_objectives(F, f_min=None, f_max=None):
    """Normalizar objetivos entre 0 y 1 para cálculo de métricas"""
    if f_min is None:
        f_min = np.min(F, axis=0)
    if f_max is None:
        f_max = np.max(F, axis=0)
    
    # Evitar división por cero
    range_f = f_max - f_min
    range_f[range_f == 0] = 1
    
    F_norm = (F - f_min) / range_f
    return F_norm, f_min, f_max

def generate_reference_set(problem, n_samples=10000):
    """Generar conjunto de referencia mediante muestreo aleatorio"""
    np.random.seed(42)  # Para reproducibilidad
    
    # Generar muestras aleatorias
    samples = np.random.uniform(
        low=problem.xl, 
        high=problem.xu, 
        size=(n_samples, problem.n_var)
    )
    
    # Evaluar muestras
    F_ref = []
    for x in samples:
        out = {}
        problem._evaluate(x, out)
        F_ref.append(out["F"])
    
    F_ref = np.array(F_ref)
    
    # Encontrar frente de Pareto del conjunto de referencia
    nds = NonDominatedSorting()
    pareto_front_indices = nds.do(F_ref, only_non_dominated_front=True)
    
    return F_ref[pareto_front_indices]

def calculate_performance_metrics(F_obtained, F_reference=None, normalize=True):
    """Calcular métricas de rendimiento del algoritmo"""
    metrics = {}
    
    # Normalizar si es necesario
    if normalize:
        if F_reference is not None:
            # Usar rango del conjunto de referencia para normalización
            f_min = np.min(F_reference, axis=0)
            f_max = np.max(F_reference, axis=0)
            F_norm, _, _ = normalize_objectives(F_obtained, f_min, f_max)
            F_ref_norm, _, _ = normalize_objectives(F_reference, f_min, f_max)
        else:
            F_norm, f_min, f_max = normalize_objectives(F_obtained)
            F_ref_norm = None
    else:
        F_norm = F_obtained
        F_ref_norm = F_reference
    
    # 1. Hypervolume (HV)
    try:
        ref_point = np.ones(F_norm.shape[1]) * 1.1  # Punto de referencia
        hv = HV(ref_point=ref_point)
        metrics['hypervolume'] = hv(F_norm)
    except Exception as e:
        print(f"Error calculando Hypervolume: {e}")
        metrics['hypervolume'] = None
    
    # 2. Número de soluciones no dominadas
    nds = NonDominatedSorting()
    fronts = nds.do(F_obtained)
    metrics['n_nondominated'] = len(fronts[0])
    metrics['total_solutions'] = len(F_obtained)
    metrics['nondominated_ratio'] = metrics['n_nondominated'] / metrics['total_solutions']
    
    # 3. Métricas que requieren conjunto de referencia
    if F_ref_norm is not None:
        try:
            # Generational Distance (GD)
            gd = GD(F_ref_norm)
            metrics['generational_distance'] = gd(F_norm)
            
            # Generational Distance Plus (GD+)
            gd_plus = GDPlus(F_ref_norm)
            metrics['generational_distance_plus'] = gd_plus(F_norm)
            
            # Inverted Generational Distance (IGD)
            igd = IGD(F_ref_norm)
            metrics['inverted_generational_distance'] = igd(F_norm)
            
            # Inverted Generational Distance Plus (IGD+)
            igd_plus = IGDPlus(F_ref_norm)
            metrics['inverted_generational_distance_plus'] = igd_plus(F_norm)
            
        except Exception as e:
            print(f"Error calculando métricas con conjunto de referencia: {e}")
            metrics['generational_distance'] = None
            metrics['generational_distance_plus'] = None
            metrics['inverted_generational_distance'] = None
            metrics['inverted_generational_distance_plus'] = None
    
    # 4. Métricas de diversidad
    if len(F_obtained) > 1:
        # Distancia promedio entre soluciones
        distances = []
        for i in range(len(F_norm)):
            for j in range(i+1, len(F_norm)):
                distances.append(np.linalg.norm(F_norm[i] - F_norm[j]))
        
        metrics['avg_distance'] = np.mean(distances) if distances else 0
        metrics['std_distance'] = np.std(distances) if distances else 0
        
        # Extensión (spread) del frente
        metrics['range_objectives'] = np.max(F_norm, axis=0) - np.min(F_norm, axis=0)
        metrics['volume_coverage'] = np.prod(metrics['range_objectives'])
    
    return metrics

def plot_pareto_front_3d(F, title="Frente de Pareto", save_path=None):
    """Visualizar frente de Pareto en 3D (primeros 3 objetivos)"""
    if F.shape[1] >= 3:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.scatter(F[:, 0], F[:, 1], F[:, 2], c='red', marker='o', s=50, alpha=0.7)
        ax.set_xlabel('Objetivo 1')
        ax.set_ylabel('Objetivo 2')
        ax.set_zlabel('Objetivo 3')
        ax.set_title(title)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

def save_performance_metrics(metrics, filepath):
    """Guardar métricas en archivo CSV"""
    df_metrics = pd.DataFrame([metrics])
    df_metrics.to_csv(filepath, index=False)
    return df_metrics

# Problema de optimización ajustado a cada año
class EVChargingYearlyProblem(ElementwiseProblem):
    def __init__(self, ev, phev, initial_cp, min_area, year):
        super().__init__(
            n_var=3,
            n_obj=5,
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
        jobs = -job_charging_station([cpl1, cpl2, cpl3])
        out["F"] = [math.ceil(cpl1), math.ceil(cpl2), math.ceil(cpl3), round(S_refor,2), math.ceil(jobs)]

# Crear carpeta de salida si no existe
carpeta_salida = "C:/Nohora/UniValle_project/pasto_case/"
os.makedirs(carpeta_salida, exist_ok=True)

# Crear carpeta para métricas de rendimiento
carpeta_metricas = os.path.join(carpeta_salida, "performance_metrics2")
os.makedirs(carpeta_metricas, exist_ok=True)

# Inicializar archivos CSV para las 5 mejores soluciones
archivos_csv = [os.path.join(carpeta_salida, f"problem2_solucion_{i+1}.csv") for i in range(5)]
columnas = ["Año", "EV", "PHEV", "tL2", "tL3", "area", "cpl1", "cpl2", "cpl3", "S_refor", "Empleos"]
for ruta in archivos_csv:
    if not os.path.exists(ruta):
        pd.DataFrame(columns=columnas).to_csv(ruta, index=False)

# Archivo para métricas de rendimiento por año
archivo_metricas = os.path.join(carpeta_metricas, "performance_metrics_by_year.csv")
columnas_metricas = ["Año", "EV", "PHEV", "execution_time", "n_evaluations", 
                    "hypervolume", "n_nondominated", "total_solutions", "nondominated_ratio",
                    "generational_distance", "generational_distance_plus", 
                    "inverted_generational_distance", "inverted_generational_distance_plus",
                    "avg_distance", "std_distance", "volume_coverage"]

if not os.path.exists(archivo_metricas):
    pd.DataFrame(columns=columnas_metricas).to_csv(archivo_metricas, index=False)

initial_cp = [0, 0, 0]
min_area = 11000

# Ejecutar optimización por año con métricas de rendimiento
for year, (ev, phev) in enumerate(zip(ev_list, phev_list), start=1):
    # Ejecutar solo para años específicos si se descomenta la línea siguiente
    # if year == 5 or year == 15 or year == 25 or year == 30:
    print(f"\n=== Año {year} ===")
    problem = EVChargingYearlyProblem(ev, phev, initial_cp, min_area, year)

    # Generar conjunto de referencia (solo para el primer año o cuando sea necesario)
    if year == 1:
        print("Generando conjunto de referencia...")
        reference_set = generate_reference_set(problem, n_samples=5000)
        print(f"Conjunto de referencia generado con {len(reference_set)} soluciones")

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

    if res.X is not None:
        # Calcular métricas de rendimiento
        print("Calculando métricas de rendimiento...")
        metrics = calculate_performance_metrics(res.F, reference_set)
        
        # Agregar información adicional
        metrics['Año'] = year
        metrics['EV'] = ev
        metrics['PHEV'] = phev
        metrics['execution_time'] = execution_time
        metrics['n_evaluations'] = res.algorithm.evaluator.n_eval
        
        # Guardar métricas
        df_metrics = pd.DataFrame([metrics])
        df_metrics.to_csv(archivo_metricas, mode='a', header=False, index=False)
        
        # Mostrar métricas principales
        print(f"Tiempo de ejecución: {execution_time:.2f} segundos")
        print(f"Evaluaciones: {res.algorithm.evaluator.n_eval}")
        print(f"Hypervolume: {metrics.get('hypervolume', 'N/A')}")
        print(f"Soluciones no dominadas: {metrics['n_nondominated']}/{metrics['total_solutions']}")
        print(f"IGD: {metrics.get('inverted_generational_distance', 'N/A')}")
        
        # Visualizar frente de Pareto cada 5 años
        if year % 5 == 0:
            plot_path = os.path.join(carpeta_metricas, f"pareto_front_year_{year}.png")
            plot_pareto_front_3d(res.F, f"Frente de Pareto - Año {year}", plot_path)

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
                "S_refor": f[3],
                "jobs": -f[4]
            }

            df_fila = pd.DataFrame([fila])
            df_fila.to_csv(archivos_csv[i], mode='a', header=False, index=False)
    else:
        print(f"No se encontraron soluciones factibles para el año {year}.")

    print(f"Año {year} completado.")

# Análisis final de rendimiento
print("\n=== ANÁLISIS DE RENDIMIENTO COMPLETADO ===")
print(f"Métricas guardadas en: {archivo_metricas}")
print(f"Gráficos guardados en: {carpeta_metricas}")

# Leer y mostrar resumen de métricas
try:
    df_all_metrics = pd.read_csv(archivo_metricas)
    print("\nResumen de métricas:")
    print(f"Tiempo promedio de ejecución: {df_all_metrics['execution_time'].mean():.2f} ± {df_all_metrics['execution_time'].std():.2f} segundos")
    print(f"Evaluaciones promedio: {df_all_metrics['n_evaluations'].mean():.0f} ± {df_all_metrics['n_evaluations'].std():.0f}")
    print(f"Hypervolume promedio: {df_all_metrics['hypervolume'].mean():.4f} ± {df_all_metrics['hypervolume'].std():.4f}")
    print(f"Ratio de soluciones no dominadas: {df_all_metrics['nondominated_ratio'].mean():.3f} ± {df_all_metrics['nondominated_ratio'].std():.3f}")
except Exception as e:
    print(f"Error leyendo métricas finales: {e}")