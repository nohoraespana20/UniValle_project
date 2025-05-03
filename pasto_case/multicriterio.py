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
print(ev_list)

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
    demand_L1 = ((Cev * BL1ev) + (Cphev * BL1phev)) / (P[0] * T[0])
    demand_L2 = ((Cev * BL2ev) + (Cphev * BL2phev)) / (P[1] * T[1])
    demand_L3 = ((Cev * BL3ev) + (Cphev * BL3phev)) / (P[2] * T[2])

    chargersLow     = max( demand_L1, initial_cp[0])
    chargersSemifast= max( demand_L2, initial_cp[1])
    chargersFast    = max( demand_L3, initial_cp[2])

    return chargersLow, chargersSemifast, chargersFast

# Guardar solución como CSV
def guardar_solucion_individual(x, f, carpeta_salida="C:/Nohora/UniValle_project/pasto_case/"):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    df = pd.DataFrame({
        "tL2": [x[0]],
        "tL3": [x[1]],
        "cpl1": [f[0]],
        "cpl2": [f[1]],
        "cpl3": [f[2]]
    })
    df.to_csv(os.path.join(carpeta_salida, "solucion_unica.csv"), index=False)
    print(f"Solución guardada en {carpeta_salida}")

# Problema de optimización ajustado a cada año
class EVChargingYearlyProblem(ElementwiseProblem):
    def __init__(self, ev, phev, initial_cp):
        super().__init__(
            n_var=2,
            n_obj=3,
            n_constr=0,
            xl=np.array([8, 8]),
            xu=np.array([24, 24])
        )
        self.ev = ev
        self.phev = phev
        self.initial_cp = initial_cp

    def _evaluate(self, x, out, *args, **kwargs):
        tL2, tL3 = x

        BL1ev, BL2ev, BL3ev = percentage_preference_type_charger(self.ev)
        BL1phev, BL2phev, BL3phev = percentage_preference_type_charger(self.phev)

        cpl1, cpl2, cpl3 = cp_technical_metrics(
            Cev, Cphev,
            BL1ev, BL1phev,
            BL2ev, BL2phev,
            BL3ev, BL3phev,
            P, [24, tL2, tL3], self.initial_cp
        )

        out["F"] = [math.ceil(cpl1), math.ceil(cpl2), math.ceil(cpl3)]

# Ejecutar optimización para cada año
resultados = []
initial_cp = [1,1,1]
for year, (ev, phev) in enumerate(zip(ev_list, phev_list), start=1):  
    problem = EVChargingYearlyProblem(ev, phev, initial_cp)
    algorithm = NSGA2(
        pop_size=20,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

    res = minimize(problem, algorithm, ("n_gen", 10), seed=1, verbose=False)

    if res.X is not None:
        x = res.X[0]
        f = res.F[0]
        initial_cp = f
        resultados.append({
            "Año": year,
            "EV": ev,
            "PHEV": phev,
            "tL2": x[0],
            "tL3": x[1],
            "cpl1": f[0],
            "cpl2": f[1],
            "cpl3": f[2]
        })
    else:
        print(f"No se encontraron soluciones factibles para el año {year}.")

# Guardar todos los resultados en un único archivo
df_resultados = pd.DataFrame(resultados)
ruta_salida = "C:/Nohora/UniValle_project/pasto_case/soluciones_todos_los_anios.csv"
df_resultados.to_csv(ruta_salida, index=False)
print(f"\nTodas las soluciones fueron guardadas en: {ruta_salida}")