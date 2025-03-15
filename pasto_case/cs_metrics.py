import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

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
    normLevelPreference = []
    for i in range(len(annualVehicles)):
        np.random.seed(0)
        publicPreference = np.random.random((1, annualVehicles[i]))
        levelPreference = np.random.random((1,2))
        sumLevelPreference = sum(levelPreference[0])
        normLevelPreference.append([round(levelPreference[0][0]/ sumLevelPreference ,2), 
                                    round(levelPreference[0][1]/ sumLevelPreference ,2)])
    return publicPreference, normLevelPreference

def number_chargers(demand, b, L, P, T, E100km, dailyDistance):
    chargersLow = []
    chargersSemifast = []
    chargersFast = []
    results = []
    
    for i in range(len(demand)):
        low = round((demand[i] * (1 - b[0][i])) / (E100km * dailyDistance))
        semifast = round((demand[i] * b[0][i] * L[i][0]) / (P[1] * T[1]))
        fast = round((demand[i] * b[0][i] * L[i][0]) / (P[2] * T[2]))
        
        if i > 0:
            low = max(low, chargersLow[i-1])
            semifast = max(semifast, chargersSemifast[i-1])
            fast = max(fast, chargersFast[i-1])
        
        chargersLow.append(low)
        chargersSemifast.append(semifast)
        chargersFast.append(fast)
        results.append([low, semifast, fast])
    
    df_chargers = pd.DataFrame(results, columns=["Low Charge", "Semifast Charge", "Fast Charge"])
    df_chargers.to_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections.csv')
    return chargersLow, chargersSemifast, chargersFast

def charging_stations_metrics(total_demand, numberChargers, P, T, chargerType):
    if chargerType == 'low':
        gwp = 82.52
    elif chargerType == 'semifast':
        gwp = 91.58
    elif chargerType == 'fast':
        gwp = 111.02
    utilizationRate1 = []
    utilizationRate2 = []
    utilizationRate3 = []
    emissions1 = []
    emissions2 = []
    emissions3 = []
    for i in range(31):
        utilizationRate1.append(math.ceil(total_demand / (P[0] * numberChargers[0][i]) * 100 / T[0]))
        utilizationRate2.append(math.ceil(total_demand / (P[1] * numberChargers[1][i]) * 100 / T[1]))
        utilizationRate3.append(math.ceil(total_demand / (P[2] * numberChargers[2][i]) * 100 / T[2]))
        emissions1.append(math.ceil((total_demand * gwp)))
    return utilizationRate1, emissions1

def plot_charger_scenarios(df_electricity, df_vehicles, P, T, E100km, dailyDistance, save_path):
    fig, axes = plt.subplots(3, 1, figsize=(8, 8))
    scenarios = ["Scenario 1", "Scenario 2", "Scenario 3"]

    for i, scenario in enumerate(scenarios):
        df_electricity_s = df_electricity[df_electricity["Scenario"] == scenario]
        df_vehicles_s = df_vehicles[df_vehicles["Scenario"] == scenario]

        b, L = percentage_preference_type_charger(df_vehicles_s)
        low, semifast, fast = number_chargers(list(df_electricity_s['Electricity [kWh]']), b, L, P, T, E100km, dailyDistance)
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

if __name__ == '__main__':
    fuel_demand = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/fuel_demand.csv')
    projections = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_projections.csv')

    df_electricity = fuel_demand[["Year", "Scenario", "Electricity [kWh]"]]
    df_vehicles = projections[["Year", "Scenario", "EV", "PHEV"]]

    P = [7, 20, 60]  
    T = [24, 8, 12]  
    E100km = 0.1103
    dailyDistance = 175
    plot_charger_scenarios(df_electricity, df_vehicles, P, T, E100km, dailyDistance, 'C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections.jpg')