from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
import numpy as np
import pandas as pd
import os

def percentage_preference_type_charger(annualVehicles):
    beta, lx2, lx3 = [], [], []
    BL1, BL2, BL3 = [], [], []
    BL1_sum, BL2_sum, BL3_sum = [], [], []
    for i in range(len(annualVehicles)):
        np.random.seed(0)
        B = np.random.random((1,int(round(annualVehicles[i]))))
        beta.append(B)
        L2 = np.random.random((1,int(round(annualVehicles[i]))))
        lx2.append(L2)
        L3 = []
        for j in range(len(B[0])):
            L3.append(1 - L2[0][j])
            BL1.append(1-B[0][j])
            BL2.append(B[0][j] * L2[0][j])
            BL3.append(B[0][j] * L3[j])
        lx3.append(L3)
        BL1_sum.append(sum(BL1))
        BL2_sum.append(sum(BL2))
        BL3_sum.append(sum(BL3))
    return BL1_sum, BL2_sum, BL3_sum

def cp_technical_metrics(Cev, Cphev, BL1ev, BL1phev, BL2ev, BL2phev, BL3ev, BL3phev, P, T):
    chargersLow, chargersSemifast, chargersFast = [], [], []
    demand_L1, demand_L2, demand_L3 = [], [], []
    for i in range(len(BL1ev)):
        low     = (((Cev * BL1ev[i]) + (Cphev * BL1phev[i])) / (P[0] * T[0]))
        demand_L1.append(low)
        semifast= (((Cev * BL2ev[i]) + (Cphev * BL2phev[i])) / (P[1] * T[1]))
        demand_L2.append(semifast)
        fast    = (((Cev * BL3ev[i]) + (Cphev * BL3phev[i])) / (P[2] * T[2]))
        demand_L3.append(fast)
        if low < 1:
            low = 1
        if semifast < 1:
            semifast = 1
        if fast < 1:
            fast = 1
        if i > 0:
            low      = max(low, chargersLow[i-1])
            semifast = max(semifast, chargersSemifast[i-1])
            fast     = max(fast, chargersFast[i-1])
        chargersLow.append((low))
        chargersSemifast.append((semifast))
        chargersFast.append((fast))
    return chargersLow , chargersSemifast , chargersFast

def guardar_soluciones_individuales(res, problem, carpeta_salida="C:/Nohora/UniValle_project/pasto_case/"):
    n_years = int((problem.n_var - 2) / 2)

    # Crear carpeta si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for i in range(len(res.X)):
        x = [int(round(val)) for val in res.X[i]]

        x1 = x[:n_years]
        x2 = x[n_years:2*n_years]
        tL2, tL3 = x[-2:]

        # Calcular métricas técnicas
        BL1ev, BL2ev, BL3ev = percentage_preference_type_charger(x1)
        BL1phev, BL2phev, BL3phev = percentage_preference_type_charger(x2)

        cpl1, cpl2, cpl3 = cp_technical_metrics(
            Cev, Cphev,
            BL1ev, BL1phev,
            BL2ev, BL2phev,
            BL3ev, BL3phev,
            P, [24, tL2, tL3]
        )

        # Crear DataFrame con columnas x1, x2, x3, x4, cpl1, cpl2, cpl3
        data = {
            "x1": x1,
            "x2": x2,
            "x3": [tL2] * n_years,  # Asumimos que x3 y x4 son tL2 y tL3 replicados por año
            "x4": [tL3] * n_years,
            "cpl1": cpl1,
            "cpl2": cpl2,
            "cpl3": cpl3
        }

        df_sol = pd.DataFrame(data)
        filename = os.path.join(carpeta_salida, f"solucion_{i}.csv")
        df_sol.to_csv(filename, index=False)

    print(f"{len(res.X)} soluciones guardadas en la carpeta: {carpeta_salida}")

E100km = 11.03 # EV's performance (kwh/100km)
Cev = (E100km / 100) * 175 # electric demand daily per vehicle
Cphev = (E100km / 100) * 175 * 0.7 # electric demand daily per vehicle
P = [7, 20, 60] # charge speed

df_vehicles = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_projections.csv')
scenario = 'Scenario 1'
scenario_selected_v = df_vehicles.loc[df_vehicles.loc[:, 'Scenario'] == scenario]
ev_min = list(scenario_selected_v["ICEV"])
ev_max = list(scenario_selected_v["Total"])
phev_min = list(scenario_selected_v["PHEV"])
scenario = 'Scenario 3'
scenario_selected_v = df_vehicles.loc[df_vehicles.loc[:, 'Scenario'] == scenario]
phev_max = list(scenario_selected_v["PHEV"])
total_proj = list(scenario_selected_v["Total"])

n_years = len(ev_min)

# 2. Definición del problema
class EVChargingPlanningProblem(ElementwiseProblem):
    def __init__(self):
        self.n_var = 2 * n_years + 2
        self.xl = np.array(ev_min + phev_min + [8, 8])
        self.xu = np.array(ev_max + phev_max + [24, 24])

        super().__init__(
            n_var=self.n_var,
            n_obj=3,
            n_constr=(n_years - 1) + n_years,
            xl=self.xl,
            xu=self.xu
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Forzar enteros manualmente
        x = [int(round(val)) for val in x]

        x1 = x[:n_years]                # EVs por año
        x2 = x[n_years:2*n_years]       # PHEVs por año
        tL2, tL3 = x[-2:]               # Tiempos de carga

        BL1ev, BL2ev, BL3ev = percentage_preference_type_charger(x1)
        BL1phev, BL2phev, BL3phev = percentage_preference_type_charger(x2)

        cpl1, cpl2, cpl3 = cp_technical_metrics(
            Cev, Cphev,
            BL1ev, BL1phev,
            BL2ev, BL2phev,
            BL3ev, BL3phev,
            P, [24, tL2, tL3]
        )

        f1 = max(cpl1)
        f2 = max(cpl2)
        f3 = max(cpl3)

        out["F"] = [int(round(f1)), int(round(f2)), int(round(f3))]

        # Restricciones:
        g1 = [x1[i] - x1[i+1] for i in range(n_years - 1)]  # EV crecientes
        g2 = [abs(x1[i] + x2[i] - total_proj[i]) - 0.05 * total_proj[i] for i in range(n_years)]  # suma total exacta

        out["G"] = np.array(g1 + g2)

# Configurar el algoritmo NSGA-II
algorithm = NSGA2(
    pop_size=100,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True
)

# # Ejecutar la optimización
problem = EVChargingPlanningProblem()
res = minimize(problem, algorithm, ("n_gen", 50), seed=1, verbose=True)

if res.X is None:
    print("No se encontraron soluciones factibles.")
else:
    for i in range(min(5, len(res.X))):
        print(f"x = {res.X[i]}, F = {res.F[i]}")

    guardar_soluciones_individuales(res, problem, carpeta_salida="C:/Nohora/UniValle_project/pasto_case/")