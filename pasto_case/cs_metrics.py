import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
import seaborn as sns

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
        u_low =         ((demand * BL1[i]) / P[0] ) * 100 / (low * T[0])
        u_semifast =    ((demand * BL2[i]) / P[1] ) * 100 / (semifast * T[1])
        u_fast =        ((demand * BL3[i]) / P[2] ) * 100 / (fast * T[2])
        e_low =     (demand * BL1[i]) * gwp[0] /1000
        e_semifast = (demand * BL2[i]) * gwp[1] /1000
        e_fast =    (demand * BL3[i]) * gwp[2] /1000
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

def ev_per_CP(scenario_selected_v, cL1, cL2, cL3):
    ev_cs = [[],[],[]]
    annualVehicles = [list(scenario_selected_v["EV"])[i] + list(scenario_selected_v["PHEV"])[i] for i in range(len(list(scenario_selected_v["EV"])))]
    for i in range(len(annualVehicles)):
        ev_cs[0].append(math.ceil(annualVehicles[i] / cL1[i]))
        ev_cs[1].append(math.ceil(annualVehicles[i] / cL2[i]))
        ev_cs[2].append(math.ceil(annualVehicles[i] / cL3[i]))
    return ev_cs

def get_real_discount_rate(year):
    """Retorna la tasa de descuento real según el horizonte del proyecto (DNP Documento 490)."""
    if year <= 5:
        return 0.095  # 9.5% para los primeros 5 años
    elif year <= 25:
        return 0.064  # 6.4% entre 6 y 25 años
    else:
        return 0.035  # 3.5% después de 25 años

def discounted_accumulated_cost(years, initial_cost, maintenance_rate, retrofit_rate, charger_points):
    annualInvestment = [initial_cost]
    annualMaintenance = [0]
    annualRetrofit = [0]

    numberCSnew = [charger_points[0] / 2]
    maintenance = [0]
    retrofit = [0]
    annual = [initial_cost]
    discountedAccumulatedCost = [initial_cost]
    AccumulatedCost = [initial_cost]

    for i in range(1, len(years)):
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
    return discountedAccumulatedCost, AccumulatedCost, annual

def job_charging_station(portsPerCH, totalChargerPoints):
    jobsPerCS = 5
    jobs_CS = []
    for i in range(len(totalChargerPoints[0])):
        jobs_CS.append(math.ceil(((totalChargerPoints[2][i] + totalChargerPoints[2][i]) * jobsPerCS / portsPerCH)))
    return jobs_CS

def land_area_metric(cL, parkingArea):
    gamma = [0, 0.1, 0.5]
    landArea_L1 = []
    landArea_L2 = []
    landArea_L3 = []
    for i in range(len(cL[0])):
        landArea_L1.append((cL[0][i] * gamma[0] ) + (parkingArea[0])) #14m2 every EV
        landArea_L2.append((cL[1][i] * gamma[1] ) + (parkingArea[1])) #14m2 every EV
        landArea_L3.append((cL[2][i] * gamma[2] / 2) + (2 * parkingArea[2])) #14m2 every EV
        landArea = [landArea_L1, landArea_L2, landArea_L3]
    return landArea

def plot_ev_metrics(years, df_chargers, case):
    colors = ["#bda5ad", "#00a099", "#a4165f"]
    
    plt.figure(figsize=(10, 6))
    plt.bar(years, df_chargers['L1'], color=colors[0], label='L1')
    plt.bar(years, df_chargers['L2'], bottom=df_chargers['L1'], color=colors[1], label='L2')
    plt.bar(years, df_chargers['L3'], bottom=df_chargers['L1'] + df_chargers['L2'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('Number charger points')
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/chargers_{case}.jpg')
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['Utilization L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['Utilization L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['Utilization L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('Utilization Rate (%)')
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/utilization_{case}.jpg')
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['Emission L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['Emission L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['Emission L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('kg CO2')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/emissions_{case}.jpg')
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['EV/CP L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['EV/CP L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['EV/CP L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('EV per Charging Point')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/EVcp_{case}.jpg')

    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['DAC L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['DAC L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['DAC L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('Discounted accumulated cost [USD]')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/discountedCost_{case}.jpg')

    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['Area L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['Area L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['Area L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('Land area required $m^2$')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/area_{case}.jpg')

    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['Jobs'])
    plt.xlabel('Year')
    plt.ylabel('Jobs generated')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/jobs_{case}.jpg')

def plot_comparative(years, df_case1, df_case2, df_case3, df_case4, df_case5):   
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case1['L1'], label="Case 1", color="black")
    axes[0].plot(years, df_case2['L1'], label="Case 2", color="#a4165f")
    axes[0].plot(years, df_case3['L1'], label="Case 3", color="#ea694e")
    axes[0].plot(years, df_case4['L1'], label="Case 4", color="#516bc5")
    axes[0].plot(years, df_case5['L1'], label="Case 5", color="#00aea7")
    axes[0].set_title('L1')
    axes[0].set_ylabel("Number of charging ports")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case1['L2'], label="Case 1", color="black")
    axes[1].plot(years, df_case2['L2'], label="Case 2", color="#a4165f")
    axes[1].plot(years, df_case3['L2'], label="Case 3", color="#ea694e")
    axes[1].plot(years, df_case4['L2'], label="Case 4", color="#516bc5")
    axes[1].plot(years, df_case5['L2'], label="Case 5", color="#00aea7")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case1['L3'], label="Case 1", color="black")
    axes[2].plot(years, df_case2['L3'], label="Case 2", color="#a4165f")
    axes[2].plot(years, df_case3['L3'], label="Case 3", color="#ea694e")
    axes[2].plot(years, df_case4['L3'], label="Case 4", color="#516bc5")
    axes[2].plot(years, df_case5['L3'], label="Case 5", color="#00aea7")
    axes[2].set_title('L3')
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)   
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/chargingPorts_comparative.jpg')

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case1['Utilization L1'], label="Case 1", color="black")
    axes[0].plot(years, df_case2['Utilization L1'], label="Case 2", color="#a4165f")
    axes[0].plot(years, df_case3['Utilization L1'], label="Case 3", color="#ea694e")
    axes[0].plot(years, df_case4['Utilization L1'], label="Case 4", color="#516bc5")
    axes[0].plot(years, df_case5['Utilization L1'], label="Case 5", color="#00aea7")
    axes[0].set_title('L1')
    axes[0].set_ylabel("Utilization rate [%]")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case1['Utilization L2'], label="Case 1", color="black")
    axes[1].plot(years, df_case2['Utilization L2'], label="Case 2", color="#a4165f")
    axes[1].plot(years, df_case3['Utilization L2'], label="Case 3", color="#ea694e")
    axes[1].plot(years, df_case4['Utilization L2'], label="Case 4", color="#516bc5")
    axes[1].plot(years, df_case5['Utilization L2'], label="Case 5", color="#00aea7")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case1['Utilization L3'], label="Case 1", color="black")
    axes[2].plot(years, df_case2['Utilization L3'], label="Case 2", color="#a4165f")
    axes[2].plot(years, df_case3['Utilization L3'], label="Case 3", color="#ea694e")
    axes[2].plot(years, df_case4['Utilization L3'], label="Case 4", color="#516bc5")
    axes[2].plot(years, df_case5['Utilization L3'], label="Case 5", color="#00aea7")
    axes[2].set_title('L3')
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/utilization_comparative.jpg')

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case1['EV/CP L1'], label="Case 1", color="black")
    axes[0].plot(years, df_case2['EV/CP L1'], label="Case 2", color="#a4165f")
    axes[0].plot(years, df_case3['EV/CP L1'], label="Case 3", color="#ea694e")
    axes[0].plot(years, df_case4['EV/CP L1'], label="Case 4", color="#516bc5")
    axes[0].plot(years, df_case5['EV/CP L1'], label="Case 5", color="#00aea7")
    axes[0].set_title('L1')
    axes[0].set_ylabel("EV per CP")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case1['EV/CP L2'], label="Case 1", color="black")
    axes[1].plot(years, df_case2['EV/CP L2'], label="Case 2", color="#a4165f")
    axes[1].plot(years, df_case3['EV/CP L2'], label="Case 3", color="#ea694e")
    axes[1].plot(years, df_case4['EV/CP L2'], label="Case 4", color="#516bc5")
    axes[1].plot(years, df_case5['EV/CP L2'], label="Case 5", color="#00aea7")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case1['EV/CP L3'], label="Case 1", color="black")
    axes[2].plot(years, df_case2['EV/CP L3'], label="Case 2", color="#a4165f")
    axes[2].plot(years, df_case3['EV/CP L3'], label="Case 3", color="#ea694e")
    axes[2].plot(years, df_case4['EV/CP L3'], label="Case 4", color="#516bc5")
    axes[2].plot(years, df_case5['EV/CP L3'], label="Case 5", color="#00aea7")
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].set_title('L3')
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/ev_cp_comparative.jpg')

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case1['DAC L1'], label="Case 1", color="black")
    axes[0].plot(years, df_case2['DAC L1'], label="Case 2", color="#a4165f")
    axes[0].plot(years, df_case3['DAC L1'], label="Case 3", color="#ea694e")
    axes[0].plot(years, df_case4['DAC L1'], label="Case 4", color="#516bc5")
    axes[0].plot(years, df_case5['DAC L1'], label="Case 5", color="#00aea7")
    axes[0].set_title('L1')
    axes[0].set_ylabel("Cost [USD]")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case1['DAC L2'], label="Case 1", color="black")
    axes[1].plot(years, df_case2['DAC L2'], label="Case 2", color="#a4165f")
    axes[1].plot(years, df_case3['DAC L2'], label="Case 3", color="#ea694e")
    axes[1].plot(years, df_case4['DAC L2'], label="Case 4", color="#516bc5")
    axes[1].plot(years, df_case5['DAC L2'], label="Case 5", color="#00aea7")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case1['DAC L3'], label="Case 1", color="black")
    axes[2].plot(years, df_case2['DAC L3'], label="Case 2", color="#a4165f")
    axes[2].plot(years, df_case3['DAC L3'], label="Case 3", color="#ea694e")
    axes[2].plot(years, df_case4['DAC L3'], label="Case 4", color="#516bc5")
    axes[2].plot(years, df_case5['DAC L3'], label="Case 5", color="#00aea7")
    axes[2].set_title('L3')
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/dac_comparative.jpg')

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case1['Area L1'], label="Case 1", color="black")
    axes[0].plot(years, df_case2['Area L1'], label="Case 2", color="#a4165f")
    axes[0].plot(years, df_case3['Area L1'], label="Case 3", color="#ea694e")
    axes[0].plot(years, df_case4['Area L1'], label="Case 4", color="#516bc5")
    axes[0].plot(years, df_case5['Area L1'], label="Case 5", color="#00aea7")
    axes[0].set_title('L1')
    axes[0].set_ylabel("Area [$m^2$]")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case1['Area L2'], label="Case 1", color="black")
    axes[1].plot(years, df_case2['Area L2'], label="Case 2", color="#a4165f")
    axes[1].plot(years, df_case3['Area L2'], label="Case 3", color="#ea694e")
    axes[1].plot(years, df_case4['Area L2'], label="Case 4", color="#516bc5")
    axes[1].plot(years, df_case5['Area L2'], label="Case 5", color="#00aea7")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case1['Area L3'], label="Case 1", color="black")
    axes[2].plot(years, df_case2['Area L3'], label="Case 2", color="#a4165f")
    axes[2].plot(years, df_case3['Area L3'], label="Case 3", color="#ea694e")
    axes[2].plot(years, df_case4['Area L3'], label="Case 4", color="#516bc5")
    axes[2].plot(years, df_case5['Area L3'], label="Case 5", color="#00aea7")
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].set_title('L3')
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/area_comparative.jpg')

def plot_comparative_preference(years, df_case10, df_case20, df_case30, df_case40, df_case50, df_case60, df_case70, df_case80, df_case90):   
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case10['L1'], label="10%")
    axes[0].plot(years, df_case20['L1'], label="20%")
    axes[0].plot(years, df_case30['L1'], label="30%")
    axes[0].plot(years, df_case40['L1'], label="40%")
    axes[0].plot(years, df_case50['L1'], label="50%")
    axes[0].plot(years, df_case60['L1'], label="60%")
    axes[0].plot(years, df_case70['L1'], label="70%")
    axes[0].plot(years, df_case80['L1'], label="80%")
    axes[0].plot(years, df_case90['L1'], label="90%")
    axes[0].set_title('L1')
    axes[0].set_ylabel("Number of charging ports")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case10['L2'], label="10%")
    axes[1].plot(years, df_case20['L2'], label="20%")
    axes[1].plot(years, df_case30['L2'], label="30%")
    axes[1].plot(years, df_case40['L2'], label="40%")
    axes[1].plot(years, df_case50['L2'], label="50%")
    axes[1].plot(years, df_case60['L2'], label="60%")
    axes[1].plot(years, df_case70['L2'], label="70%")
    axes[1].plot(years, df_case80['L2'], label="80%")
    axes[1].plot(years, df_case90['L2'], label="90%")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case10['L3'], label="10%")
    axes[2].plot(years, df_case20['L3'], label="20%")
    axes[2].plot(years, df_case30['L3'], label="30%")
    axes[2].plot(years, df_case40['L3'], label="40%")
    axes[2].plot(years, df_case50['L3'], label="50%")
    axes[2].plot(years, df_case60['L3'], label="60%")
    axes[2].plot(years, df_case70['L3'], label="70%")
    axes[2].plot(years, df_case80['L3'], label="80%")
    axes[2].plot(years, df_case90['L3'], label="90%")
    axes[2].set_title('L3')
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)   
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/chargingPorts_comparative.jpg')

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case10['Utilization L1'], label="10%")
    axes[0].plot(years, df_case20['Utilization L1'], label="20%")
    axes[0].plot(years, df_case30['Utilization L1'], label="30%")
    axes[0].plot(years, df_case40['Utilization L1'], label="40%")
    axes[0].plot(years, df_case50['Utilization L1'], label="50%")
    axes[0].plot(years, df_case60['Utilization L1'], label="60%")
    axes[0].plot(years, df_case70['Utilization L1'], label="70%")
    axes[0].plot(years, df_case80['Utilization L1'], label="80%")
    axes[0].plot(years, df_case90['Utilization L1'], label="90%")
    axes[0].set_title('L1')
    axes[0].set_ylabel("Utilization rate [%]")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case10['Utilization L2'], label="10%")
    axes[1].plot(years, df_case20['Utilization L2'], label="20%")
    axes[1].plot(years, df_case30['Utilization L2'], label="30%")
    axes[1].plot(years, df_case40['Utilization L2'], label="40%")
    axes[1].plot(years, df_case50['Utilization L2'], label="50%")
    axes[1].plot(years, df_case60['Utilization L2'], label="60%")
    axes[1].plot(years, df_case70['Utilization L2'], label="70%")
    axes[1].plot(years, df_case80['Utilization L2'], label="80%")
    axes[1].plot(years, df_case90['Utilization L2'], label="90%")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case10['Utilization L3'], label="10%")
    axes[2].plot(years, df_case20['Utilization L3'], label="20%")
    axes[2].plot(years, df_case30['Utilization L3'], label="30%")
    axes[2].plot(years, df_case40['Utilization L3'], label="40%")
    axes[2].plot(years, df_case50['Utilization L3'], label="50%")
    axes[2].plot(years, df_case60['Utilization L3'], label="60%")
    axes[2].plot(years, df_case70['Utilization L3'], label="70%")
    axes[2].plot(years, df_case80['Utilization L3'], label="80%")
    axes[2].plot(years, df_case90['Utilization L3'], label="90%")
    axes[2].set_title('L3')
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/utilization_comparative.jpg')

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case10['EV/CP L1'], label="10%")
    axes[0].plot(years, df_case20['EV/CP L1'], label="20%")
    axes[0].plot(years, df_case30['EV/CP L1'], label="30%")
    axes[0].plot(years, df_case40['EV/CP L1'], label="40%")
    axes[0].plot(years, df_case50['EV/CP L1'], label="50%")
    axes[0].plot(years, df_case60['EV/CP L1'], label="60%")
    axes[0].plot(years, df_case70['EV/CP L1'], label="70%")
    axes[0].plot(years, df_case80['EV/CP L1'], label="80%")
    axes[0].plot(years, df_case90['EV/CP L1'], label="90%")
    axes[0].set_title('L1')
    axes[0].set_ylabel("EV per CP")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case10['EV/CP L2'], label="10%")
    axes[1].plot(years, df_case20['EV/CP L2'], label="20%")
    axes[1].plot(years, df_case30['EV/CP L2'], label="30%")
    axes[1].plot(years, df_case40['EV/CP L2'], label="40%")
    axes[1].plot(years, df_case50['EV/CP L2'], label="50%")
    axes[1].plot(years, df_case60['EV/CP L2'], label="60%")
    axes[1].plot(years, df_case70['EV/CP L2'], label="70%")
    axes[1].plot(years, df_case80['EV/CP L2'], label="80%")
    axes[1].plot(years, df_case90['EV/CP L2'], label="90%")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case10['EV/CP L3'], label="10%")
    axes[2].plot(years, df_case20['EV/CP L3'], label="20%")
    axes[2].plot(years, df_case30['EV/CP L3'], label="30%")
    axes[2].plot(years, df_case40['EV/CP L3'], label="40%")
    axes[2].plot(years, df_case50['EV/CP L3'], label="50%")
    axes[2].plot(years, df_case60['EV/CP L3'], label="60%")
    axes[2].plot(years, df_case70['EV/CP L3'], label="70%")
    axes[2].plot(years, df_case80['EV/CP L3'], label="80%")
    axes[2].plot(years, df_case90['EV/CP L3'], label="90%")
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].set_title('L3')
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/ev_cp_comparative.jpg')

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case10['DAC L1'], label="10%")
    axes[0].plot(years, df_case20['DAC L1'], label="20%")
    axes[0].plot(years, df_case30['DAC L1'], label="30%")
    axes[0].plot(years, df_case40['DAC L1'], label="40%")
    axes[0].plot(years, df_case50['DAC L1'], label="50%")
    axes[0].plot(years, df_case60['DAC L1'], label="60%")
    axes[0].plot(years, df_case70['DAC L1'], label="70%")
    axes[0].plot(years, df_case80['DAC L1'], label="80%")
    axes[0].plot(years, df_case90['DAC L1'], label="90%")
    axes[0].set_title('L1')
    axes[0].set_ylabel("Cost [USD]")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case10['DAC L2'], label="10%")
    axes[1].plot(years, df_case20['DAC L2'], label="20%")
    axes[1].plot(years, df_case30['DAC L2'], label="30%")
    axes[1].plot(years, df_case40['DAC L2'], label="40%")
    axes[1].plot(years, df_case50['DAC L2'], label="50%")
    axes[1].plot(years, df_case60['DAC L2'], label="60%")
    axes[1].plot(years, df_case70['DAC L2'], label="70%")
    axes[1].plot(years, df_case80['DAC L2'], label="80%")
    axes[1].plot(years, df_case90['DAC L2'], label="90%")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case10['DAC L3'], label="10%")
    axes[2].plot(years, df_case20['DAC L3'], label="20%")
    axes[2].plot(years, df_case30['DAC L3'], label="30%")
    axes[2].plot(years, df_case40['DAC L3'], label="40%")
    axes[2].plot(years, df_case50['DAC L3'], label="50%")
    axes[2].plot(years, df_case60['DAC L3'], label="60%")
    axes[2].plot(years, df_case70['DAC L3'], label="70%")
    axes[2].plot(years, df_case80['DAC L3'], label="80%")
    axes[2].plot(years, df_case90['DAC L3'], label="90%")
    axes[2].set_title('L3')
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/dac_comparative.jpg')

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].plot(years, df_case10['Area L1'], label="10%")
    axes[0].plot(years, df_case20['Area L1'], label="20%")
    axes[0].plot(years, df_case30['Area L1'], label="30%")
    axes[0].plot(years, df_case40['Area L1'], label="40%")
    axes[0].plot(years, df_case50['Area L1'], label="50%")
    axes[0].plot(years, df_case60['Area L1'], label="60%")
    axes[0].plot(years, df_case70['Area L1'], label="70%")
    axes[0].plot(years, df_case80['Area L1'], label="80%")
    axes[0].plot(years, df_case90['Area L1'], label="90%")
    axes[0].set_title('L1')
    axes[0].set_ylabel("Area [$m^2$]")
    axes[0].set_xlabel("Year")  
    axes[0].grid(True, linestyle="--", alpha=0.7)
    axes[0].legend()

    axes[1].plot(years, df_case10['Area L2'], label="10%")
    axes[1].plot(years, df_case20['Area L2'], label="20%")
    axes[1].plot(years, df_case30['Area L2'], label="30%")
    axes[1].plot(years, df_case40['Area L2'], label="40%")
    axes[1].plot(years, df_case50['Area L2'], label="50%")
    axes[1].plot(years, df_case60['Area L2'], label="60%")
    axes[1].plot(years, df_case70['Area L2'], label="70%")
    axes[1].plot(years, df_case80['Area L2'], label="80%")
    axes[1].plot(years, df_case90['Area L2'], label="90%")
    axes[1].set_title('L2')
    axes[1].set_xlabel("Year")  
    axes[1].grid(True, linestyle="--", alpha=0.7)
    axes[1].legend()

    axes[2].plot(years, df_case10['Area L3'], label="10%")
    axes[2].plot(years, df_case20['Area L3'], label="20%")
    axes[2].plot(years, df_case30['Area L3'], label="30%")
    axes[2].plot(years, df_case40['Area L3'], label="40%")
    axes[2].plot(years, df_case50['Area L3'], label="50%")
    axes[2].plot(years, df_case60['Area L3'], label="60%")
    axes[2].plot(years, df_case70['Area L3'], label="70%")
    axes[2].plot(years, df_case80['Area L3'], label="80%")
    axes[2].plot(years, df_case90['Area L3'], label="90%")
    axes[2].set_xlabel("Year")  
    axes[2].grid(True, linestyle="--", alpha=0.7)
    axes[2].set_title('L3')
    axes[2].legend()
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/area_comparative.jpg')

if __name__ == '__main__':
    fuel_demand = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/fuel_demand.csv')
    projections = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_projections.csv')

    df_electricity = fuel_demand[["Year", "Scenario", "Electricity [kWh]"]]
    df_vehicles = projections[["Year", "Scenario", "EV", "PHEV"]]

    P = [7, 20, 60] # charge speed
    T = [24, 8, 12] # time available
    case = 'Case1_90'
    E100km = 11.03 # EV's performance (kwh/100km)
    dailyDistance = 175 # EV's daily distance (km)
    C = (E100km / 100) * 175 # electric demand daily per vehicle
    initial_cost = [800, 6500, 75000]
    maintenance_rate = [0.1, 0.1, 0.1]
    retrofit_rate = [0.05, 0.5, 0.5]
    portsPerCH = 2
    parkingArea = [0, 0, 14]

    scenario = 'Scenario 3'
    scenario_selected_v = df_vehicles.loc[df_vehicles.loc[:, 'Scenario'] == scenario]
    scenario_selected_e = df_electricity.loc[df_electricity.loc[:, 'Scenario'] == scenario]
    years = list(scenario_selected_v['Year'])

    bL1, bL2, bL3 = percentage_preference_type_charger(scenario_selected_v)
    cL1, cL2, cL3, uL1, uL2, uL3, eL1, eL2, eL3 = cp_technical_metrics(C, bL1, bL2, bL3, P, T)
    totalChargerPoints = [cL1, cL2, cL3]
    ev_cs = ev_per_CP(scenario_selected_v, cL1, cL2, cL3)
    discountedAC_L1, accumulatedC_L1, annualC_L1 = discounted_accumulated_cost(years, initial_cost[0], maintenance_rate[0], retrofit_rate[0], cL1)
    discountedAC_L2, accumulatedC_L2, annualC_L2 = discounted_accumulated_cost(years, initial_cost[1], maintenance_rate[1], retrofit_rate[1], cL2)
    discountedAC_L3, accumulatedC_L3, annualC_L3 = discounted_accumulated_cost(years, initial_cost[2], maintenance_rate[2], retrofit_rate[2], cL3)
    jobs = job_charging_station(portsPerCH, totalChargerPoints)
    landArea = land_area_metric(totalChargerPoints, parkingArea)

    df_chargers = pd.DataFrame()
    df = pd.DataFrame({'L1': cL1, 'L2': cL2, 'L3': cL3,
                       'Utilization L1': uL1, 'Utilization L2': uL2, 'Utilization L3': uL3,
                       'Emission L1': eL1, 'Emission L2': eL2, 'Emission L3': eL3,
                       'EV/CP L1': ev_cs[0], 'EV/CP L2': ev_cs[1], 'EV/CP L3': ev_cs[2],
                       'DAC L1': discountedAC_L1, 'DAC L2': discountedAC_L2, 'DAC L3': discountedAC_L3,
                       'Area L1': landArea[0], 'Area L2': landArea[1], 'Area L3': landArea[2],
                       'Jobs': jobs})

    df_chargers = pd.concat([df_chargers, df])
    # df_chargers.to_csv(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_{case}.csv')
    # plot_ev_metrics(years, df_chargers, f'{case}')

    # df_case1 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_Case1.csv')
    # df_case2 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_Case2.csv')
    # df_case3 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_Case3.csv')
    # df_case4 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_Case4.csv')
    # df_case5 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/cs_projections_Case5.csv')
    # plot_comparative(years, df_case1, df_case2, df_case3, df_case4, df_case5)

    df_case10 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_10.csv')
    df_case20 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_20.csv')
    df_case30 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_30.csv')
    df_case40 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_40.csv')
    df_case50 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_50.csv')
    df_case60 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_60.csv')
    df_case70 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_70.csv')
    df_case80 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_80.csv')
    df_case90 = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_Case1_90.csv')

    plot_comparative_preference(years, df_case10, df_case20, df_case30, df_case40, df_case50, df_case60, df_case70, df_case80, df_case90)