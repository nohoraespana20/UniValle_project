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
    BL1 = []
    BL2 = []
    BL3 = []
    BL1_sum = []
    BL2_sum = []
    BL3_sum = []
    for i in range(len(annualVehicles)):
        np.random.seed(0)
        B = np.random.random((1,annualVehicles[i]))
        L2 = np.random.random((1,annualVehicles[i]))
        L3 = []
        for j in range(len(B[0])):
            L3.append(1 - L2[0][j])
            BL1.append(1-B[0][j])
            BL2.append(B[0][j] * L2[0][j])
            BL3.append(B[0][j] * L3[j])
            if j == 2:
                print('1-B = ', BL1[j])
                print('B = ', B[0][j])
                print('L2 = ', L2[0][j])
                print('L3 = ', L3[j])
        BL1_sum.append(round(sum(BL1), 2))
        BL2_sum.append(round(sum(BL2), 2))
        BL3_sum.append(round(sum(BL3), 2))
    return BL1_sum, BL2_sum, BL3_sum

def number_chargers(demand, BL1, BL2, BL3, P, T):
    chargersLow = []
    chargersSemifast = []
    chargersFast = []
    results = []

    for i in range(len(demand)):
        low = round((demand[i] * (BL1[i])) / (P[0] * T[0]))
        semifast = round((demand[i] * BL2[i]) / (P[1] * T[1]))
        fast = round((demand[i] * BL3[i]) / (P[2] * T[2]))
            
        if i > 0:
            low = max(low, chargersLow[i-1])
            semifast = max(semifast, chargersSemifast[i-1])
            fast = max(fast, chargersFast[i-1])
            
        chargersLow.append(low)
        chargersSemifast.append(semifast)
        chargersFast.append(fast)
        results.append([low, semifast, fast])
    return results

def charging_stations_metrics(total_demand, numberChargers, P, T):
    gwp = [82.52, 91.58, 111.02]
    utilizationRate = []
    emissions = []
    for i in range(31):
        for k in range(3):
            utilizationRate.append(math.ceil(total_demand[i] / (P[k] * numberChargers[k][i]) * 100 / T[k]))
            emissions.append(math.ceil((total_demand[i] * gwp[k])))
    return utilizationRate, emissions

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
    
    # plot_charger_scenarios(df_electricity, df_vehicles, P, T, E100km, dailyDistance, 'C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections.jpg')
    bL1, bL2, bL3 = percentage_preference_type_charger(df_vehicles.loc[df_vehicles.loc[:, 'Scenario'] == 'Scenario 1'])
    # print('bl 1 = ', bL1, '\nb L2 = ', bL2, '\nbL3 = ', bL3)
    # df = pd.DataFrame()

    # scenario_select = df_electricity.loc[:, 'Scenario'] == 'Scenario 1'
    # df_electricity_scenario = df_electricity.loc[scenario_select]
    # total_chargers = number_chargers(list(df_electricity_scenario["Electricity [kWh]"]), bL1, bL2,bL3, P, T)
    # df_chargers = pd.DataFrame(total_chargers, columns=["Low Charge", "Semifast Charge", "Fast Charge"])
    # scenario = ['Scenario 1']*len(list(df_electricity_scenario["Electricity [kWh]"]))
    # df_chargers.insert(0, 'Scenario', scenario)
    # df = pd.concat([df, df_chargers])
    # print(df)

    # scenario_select = df_electricity.loc[:, 'Scenario'] == 'Scenario 2'
    # df_electricity_scenario = df_electricity.loc[scenario_select]
    # total_chargers = number_chargers(list(df_electricity_scenario["Electricity [kWh]"]), b, L, P, T, E100km, dailyDistance)
    # df_chargers = pd.DataFrame(total_chargers, columns=["Low Charge", "Semifast Charge", "Fast Charge"])
    # scenario = ['Scenario 2']*len(list(df_electricity_scenario["Electricity [kWh]"]))
    # df_chargers.insert(0, 'Scenario', scenario)
    # df = pd.concat([df, df_chargers])
    # print(df)


    # # df_chargers.to_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections.csv')
    # # number_chargers = [low, semifast, fast]
    # # utilization, emissions = charging_stations_metrics(list(df_electricity_scenario["Electricity [kWh]"]), number_chargers, P, T)
    # # print(utilization)