import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os

def charging_time(chargeNeeded, chargerType):
    if chargerType == 'low':
        chargingSpeed = 7
    elif chargerType == 'semifast':
        chargingSpeed = 20
    elif chargerType == 'fast':
        chargingSpeed = 60
    else:
        print('')
    hourChargingTime = chargeNeeded / chargingSpeed
    return round(hourChargingTime, 2)

def percentage_preference_type_charger(df):
    annualVehicles = [list(df["EV"])[i] + list(df["PHEV"])[i] for i in range(len(list(df["EV"])))]
    BL1 = []
    BL2 = []
    BL3 = []
    BL1_sum = []
    BL2_sum = []
    BL3_sum = []
    for i in range(len(annualVehicles)):
        np.random.seed(0)
        B = np.random.random((1,annualVehicles[i]))
        # B = [[0.9]*annualVehicles[i]]
        L2 = np.random.random((1,annualVehicles[i]))
        L3 = []
        for j in range(len(B[0])):
            L3.append(1 - L2[0][j])
            BL1.append(1-B[0][j])
            BL2.append(B[0][j] * L2[0][j])
            BL3.append(B[0][j] * L3[j])
        BL1_sum.append(sum(BL1))
        BL2_sum.append(sum(BL2))
        BL3_sum.append(sum(BL3))
    return BL1_sum, BL2_sum, BL3_sum

def cp_technical_metrics(demand, BL1, BL2, BL3, P, T):
    chargersLow, chargersSemifast, chargersFast = [], [], []
    utilization_low, utilization_semifast, utilization_fast = [], [], []
    emission_low, emission_semifast, emission_fast = [], [], []
    gwp = [82.52, 91.58, 111.02]
    for i in range(len(BL1)):
        low     = (demand * BL1[i]) / (P[0] * T[0])
        semifast= (demand * BL2[i]) / (P[1] * T[1])
        fast    = (demand * BL3[i]) / (P[2] * T[2])
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
        u_low =  ((demand * BL1[i]) / P[0] ) * 100 / (low * T[0])
        u_semifast =  ((demand * BL2[i]) / P[1] ) * 100 / (semifast * T[1])
        u_fast =  ((demand * BL2[i]) / P[1] ) * 100 / (semifast * T[1])
        e_low = (demand * BL1[i]) * gwp[0] 
        e_semifast = (demand * BL2[i]) * gwp[1] 
        e_fast = (demand * BL3[i]) * gwp[2] 
        chargersLow.append(math.ceil(low))
        chargersSemifast.append(math.ceil(semifast))
        chargersFast.append(math.ceil(fast))
        utilization_low.append(math.ceil(u_low))
        utilization_semifast.append(math.ceil(u_semifast))
        utilization_fast.append(math.ceil(u_fast))
        emission_low.append(math.ceil(e_low))
        emission_semifast.append(math.ceil(e_semifast))
        emission_fast.append(math.ceil(e_fast))

    return chargersLow, chargersSemifast, chargersFast, utilization_low, utilization_semifast, utilization_fast, emission_low, emission_semifast, emission_fast

def plot_charger_scenarios(df_electricity, df_vehicles, low, semifast, fast, save_path):
    fig, axes = plt.subplots(3, 1, figsize=(8, 8))
    scenarios = ["Scenario 1", "Scenario 2", "Scenario 3"]

    for i, scenario in enumerate(scenarios):
        df_electricity_s = df_electricity[df_electricity["Scenario"] == scenario]
        df_vehicles_s = df_vehicles[df_vehicles["Scenario"] == scenario]

        year = list(df_electricity_s["Year"])

        axes[i].plot(year, low, label='Low charge', color="#bda5ad")
        axes[i].plot(year, semifast, label='Semifast charge', color="#00a099")
        axes[i].plot(year, fast, label='Fast charge', color="#a4165f")
        axes[i].set_title(f'{scenario}')
        axes[i].grid()
        axes[i].legend()
        if i != len(scenarios) - 1:
            axes[i].set_xticklabels([])
        else:
            axes[i].set_xlabel("Year")
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_charger(df_electricity, low, semifast, fast, save_path):
    scenario = "Scenario 3"
    df_electricity_s = df_electricity[df_electricity["Scenario"] == scenario]
    year = list(df_electricity_s["Year"])

    plt.plot(year, low, label='Low charge', color="#bda5ad")
    plt.plot(year, semifast, label='Semifast charge', color="#00a099")
    plt.plot(year, fast, label='Fast charge', color="#a4165f")
    plt.title(f'Charging points in base case - {scenario}')
    plt.grid()
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Number charging points")
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_charger_bar(df_electricity, low, semifast, fast, save_path):
    scenario = "Scenario 3"
    df_electricity_s = df_electricity[df_electricity["Scenario"] == scenario]
    year = list(df_electricity_s["Year"])

    plt.bar(year, low, label='Low charge', color="#bda5ad")
    plt.bar(year, semifast, label='Semifast charge', color="#00a099", bottom=low)
    plt.bar(year, fast, label='Fast charge', color="#a4165f", bottom=[i + j for i, j in zip(low, semifast)])
    
    plt.title(f'Charging points in base case - {scenario}')
    plt.grid()
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Number charging points")
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_csv_data(directory):
    files = sorted([f for f in os.listdir(directory) if f.startswith("cs_projections_") and f.endswith(".csv") and "base" not in f], key=lambda x: int(x.split('_')[2].split('.')[0]) if x.split('_')[2].isdigit() else 0)
    data = {} 
    for file in files:
        df = pd.read_csv(os.path.join(directory, file))
        label = file.split('_')[2].split('.')[0]
        data[label] = df
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True)
    
    for label, df in data.items():
        axes[0].plot(df.index, df.iloc[:, 2], label=label)  # L1
        axes[1].plot(df.index, df.iloc[:, 5], label=label)  # L2
        axes[2].plot(df.index, df.iloc[:, 8], label=label)  # L3
    
    axes[0].set_title("Charging points L1")
    axes[0].set_xlabel("Year")
    axes[0].grid()
    axes[1].set_title("Charging points L2")
    axes[1].set_xlabel("Year")
    axes[1].grid()
    axes[2].set_title("Charging points L3")
    axes[2].set_xlabel("Year")
    axes[2].grid()
    
    for ax in axes:
        ax.legend()
        ax.set_ylabel("Number charging points")
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cases_preference.jpg')
    plt.close()

def calcule_plot_evCP(scenario_selected_v, cL1, cL2, cL3, name):
    ev_cs = [[],[],[]]
    annualVehicles = [list(scenario_selected_v["EV"])[i] + list(scenario_selected_v["PHEV"])[i] for i in range(len(list(scenario_selected_v["EV"])))]
    for i in range(len(annualVehicles)):
        ev_cs[0].append(math.ceil(annualVehicles[i] / cL1[i]))
        ev_cs[1].append(math.ceil(annualVehicles[i] / cL2[i]))
        ev_cs[2].append(math.ceil(annualVehicles[i] / cL3[i]))
    df = pd.DataFrame({ "L1": ev_cs[0], "L2": ev_cs[1], "L3": ev_cs[2]})
    df.to_csv(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_cp_{name}.csv')
    years = scenario_selected_v["Year"]
    plt.plot(years, ev_cs[0], label='L1', color='#bda5ad')
    plt.plot(years, ev_cs[1], label='L2', color='#00a099')
    plt.plot(years, ev_cs[2], label='L3', color='#a4165f')
    plt.title('EV per Charging point')
    plt.xlabel('Year')
    plt.ylabel('Number EV/CP')
    plt.legend()
    plt.grid()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_cp_{name}.jpg')
    plt.close()
    return ev_cs

def get_real_discount_rate(year):
    """Retorna la tasa de descuento real según el horizonte del proyecto (DNP Documento 490)."""
    if year <= 5:
        return 0.095  # 9.5% para los primeros 5 años
    elif year <= 25:
        return 0.064  # 6.4% entre 6 y 25 años
    else:
        return 0.035  # 3.5% después de 25 años

def discounted_accumulated_cost(years, initial_cost, maintenance_rate, retrofit_rate, path, typeCS):
    file = pd.read_csv(path)
    charger_points = list(file[typeCS])

    annualInvestment = [initial_cost]
    annualMaintenance = [0]
    annualRetrofit = [0]

    numberCSnew = [charger_points[0] / 2]
    maintenance = [0]
    retrofit = [0]
    annual = [initial_cost]
    discountedAccumulatedCost = [initial_cost]
    AccumulatedCost = [initial_cost]

    for i in range(1, len(charger_points)):
        discount_rate = get_real_discount_rate(i)  

        annualInvestment.append(initial_cost)  
        annualMaintenance.append(initial_cost * maintenance_rate)
        annualRetrofit.append(initial_cost * retrofit_rate)

        numberCSnew.append((charger_points[i] - charger_points[i-1]) / 2)   
        maintenance.append(annualMaintenance[i-1] * numberCSnew[i-1])
        retrofit.append(annualRetrofit[i-1] * numberCSnew[i-1])

        if i == 10 or i == 20 or i == 30:
            annual.append(math.ceil(maintenance[i] + retrofit[i]))
        else:
            annual.append(math.ceil(maintenance[i]))

        discountedAccumulatedCost.append(math.ceil(discountedAccumulatedCost[i-1] + (annual[i] / ((1 + discount_rate) ** i))))
        AccumulatedCost.append(math.ceil(AccumulatedCost[i-1] + annual[i]))

    df = pd.DataFrame({ 
        f"AC {typeCS}": AccumulatedCost, 
        f'DAC {typeCS}': discountedAccumulatedCost, 
        f'Annual {typeCS}': annual
        })
    if len(df) != len(file):
        raise ValueError("El nuevo DataFrame tiene un número diferente de filas, lo que causará desalineación.")
    file = pd.concat([file, df], axis=1)  
    file.to_csv(path, index=False)

if __name__ == '__main__':
    fuel_demand = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/fuel_demand.csv')
    projections = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_projections.csv')
    
    df_electricity = fuel_demand[["Year", "Scenario", "Electricity [kWh]"]]
    df_vehicles = projections[["Year", "Scenario", "EV", "PHEV"]]
    
    P = [7, 20, 60] # charge speed
    T = [24, 8, 12] # time available
    E100km = 0.1103 # EV's performance (kwh/100km)
    dailyDistance = 175 # EV's daily distance (km)
    C = (E100km * 1) * 175 # electric demand daily per vehicle
    
    df_chargers = pd.DataFrame()
    scenarios = ['Scenario 1']#, 'Scenario 2', 'Scenario 3']
    for scenario in scenarios:
        scenario_selected_v = df_vehicles.loc[df_vehicles.loc[:, 'Scenario'] == scenario]
        scenario_selected_e = df_electricity.loc[df_electricity.loc[:, 'Scenario'] == scenario]
        bL1, bL2, bL3 = percentage_preference_type_charger(scenario_selected_v)
        cL1, cL2, cL3, uL1, uL2, uL3, eL1, eL2, eL3 = cp_technical_metrics(C, bL1, bL2, bL3, P, T)
        df = pd.DataFrame({ "L1": cL1, 'Utilization L1': uL1, 'Emission L1': eL1,
                            "L2": cL2, 'Utilization L2': uL2, 'Emission L2': eL2, 
                            "L3": cL3, 'Utilization L3': uL3, 'Emission L3': eL3})
        scenario_tag = [scenario]*len(list(scenario_selected_e["Electricity [kWh]"]))
        df.insert(0, 'Scenario', scenario)
        df_chargers = pd.concat([df_chargers, df])

    years = scenario_selected_v['Year']
    plt.plot(years, uL1, label='L1', color="#bda5ad")
    plt.plot(years, uL2, label='L2', color="#00a099")
    plt.plot(years, uL3, label='L3', color="#a4165f")
    plt.title(f'Utilization rate of charging points')
    plt.grid()
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("%")
    
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/UR_case1.jpg')
    plt.close()

    ec_cs = calcule_plot_evCP(scenario_selected_v, cL1, cL2, cL3, 'case1')
    df_chargers.to_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_case1.csv')
    plot_charger_bar(df_electricity, cL1, cL2, cL3, 'C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_bar_case1.jpg')
    plot_csv_data('C:/Nohora/UniValle_project/pasto_case/results_netherlands')

    path = 'C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_case1.csv'
    initial_cost = 800  
    maintenance_rate = 0.1  
    retrofit_rate = 0.05  
    discounted_accumulated_cost(years, initial_cost, maintenance_rate, retrofit_rate, path, 'L1')
    initial_cost = 6500  
    maintenance_rate = 0.1  
    retrofit_rate = 0.5
    discounted_accumulated_cost(years, initial_cost, maintenance_rate, retrofit_rate, path, 'L2')
    initial_cost = 75000  
    maintenance_rate = 0.1  
    retrofit_rate = 0.5
    discounted_accumulated_cost(years, initial_cost, maintenance_rate, retrofit_rate, path, 'L3')

    file = pd.read_csv(path)
    discountedAC_L1 = list(file['DAC L1'])
    discountedAC_L2 = list(file['DAC L2'])
    discountedAC_L3 = list(file['DAC L3'])
    plt.plot(years, discountedAC_L1, label = 'L1', color="#bda5ad")
    plt.plot(years, discountedAC_L2, label = 'L2', color="#00a099")
    plt.plot(years, discountedAC_L3, label = 'L3', color="#a4165f")
    plt.grid()
    plt.xlabel('Year')
    plt.ylabel('Cost [USD]')
    plt.legend()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/discountAC_case1.jpg')
    plt.close()