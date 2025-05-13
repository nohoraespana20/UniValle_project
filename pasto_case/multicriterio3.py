from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
import numpy as np
import pandas as pd
import os
import math

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



# Guardar solución como CSV
def guardar_solucion_individual(x, f, carpeta_salida="C:/Nohora/UniValle_project/pasto_case/"):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    df = pd.DataFrame({
        "tL2": [x[0]],
        "tL3": [x[1]],
        "area": [x[2]],
        "cpl1": [f[0]],
        "cpl2": [f[1]],
        "cpl3": [f[2]],
        "S_refor": [f[3]],
        "jobs": [f[4]],
        "emisiones":[f[5]],
        "incentivos":[f[6]]
    })
    df.to_csv(os.path.join(carpeta_salida, "solucion_unica.csv"), index=False)
    print(f"Solución guardada en {carpeta_salida}")

# Problema de optimización ajustado a cada año
class EVChargingYearlyProblem(ElementwiseProblem):
    def __init__(self, ev, phev, initial_cp, min_area, year):
        super().__init__(
            n_var=3,
            n_obj=7,
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
        P_bat = sizing_battery_system(P_pv)

        capacidades = [P_bat*0.15, P_bat*0.13, P_bat*0.72]  # Nuevos valores de capacidad por nodo
        P_red, E_export, E_pv = run_doper_model(demand_scale=demand, pv_scale=P_pv, battery_capacities=capacidades)
        emisiones = calcular_emisiones_CO2(P_pv, P_red)
        S_refor = calculate_reinforcement(100000, 104000, demand, P_pv)
        jobs = -job_charging_station([cpl1, cpl2, cpl3])

        ipp = -calculate_iip(E_export, self.year, E_pv)
        out["F"] = [math.ceil(cpl1), math.ceil(cpl2), math.ceil(cpl3), round(S_refor,2), math.ceil(jobs), round(emisiones,2), round(ipp,2)]

# Crear carpeta de salida si no existe
carpeta_salida = "C:/Nohora/UniValle_project/pasto_case/"
os.makedirs(carpeta_salida, exist_ok=True)

initial_cp = [0, 0, 0]
min_area = 11000

# Inicializar listas de resultados por solución
archivos_csv = [os.path.join(carpeta_salida, f"solucion_{i+1}.csv") for i in range(5)]

# Crear encabezados en los archivos si no existen
columnas = [
    "Año", "EV", "PHEV", "tL2", "tL3", "area",
    "cpl1", "cpl2", "cpl3", "S_refor", "jobs", "emisiones", "incentivos"
]
for ruta in archivos_csv:
    if not os.path.exists(ruta):
        pd.DataFrame(columns=columnas).to_csv(ruta, index=False)

# Ejecutar optimización por año
for year, (ev, phev) in enumerate(zip(ev_list, phev_list), start=1):
    # if year == 5 or year == 15 or year == 25 or year == 30:
    if year == 31:
        print(f"Año {year}")
        problem = EVChargingYearlyProblem(ev, phev, initial_cp, min_area, year)

        algorithm = NSGA2(
            pop_size=20,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=0.9, eta=15),
            mutation=PM(eta=20),
            eliminate_duplicates=True
        )

        res = minimize(problem, algorithm, ("n_gen", 50), seed=1, verbose=False)

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
                    "S_refor": f[3],
                    "jobs": -f[4],
                    "emisiones": f[5],
                    "incentivos": -f[6]
                }

                df_fila = pd.DataFrame([fila])
                df_fila.to_csv(archivos_csv[i], mode='a', header=False, index=False)
        else:
            print(f"No se encontraron soluciones factibles para el año {year}.")

        print(f"Año {year} completado.")