import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
import seaborn as sns

def percentage_preference_type_charger(annualVehicles):
    # annualVehicles = [list(df["EV"])[i] + list(df["PHEV"])[i] for i in range(len(list(df["EV"])))] #arreglar para PHEV, se tiene en cuenta la carga total de un EV
    beta, lx2, lx3 = [], [], []
    BL1, BL2, BL3 = [], [], []
    BL1_sum, BL2_sum, BL3_sum = [], [], []
    for i in range(len(annualVehicles)):
        np.random.seed(0)
        B = np.random.random((1,annualVehicles[i]))
        # B = [[0.9]*annualVehicles[i]]
        beta.append(B)
        L2 = np.random.random((1,annualVehicles[i]))
        # L2 = [[0.5]*annualVehicles[i]]
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
    return BL1_sum, BL2_sum, BL3_sum, beta, lx2, lx3

def cp_technical_metrics(Cev, Cphev, BL1ev, BL1phev, BL2ev, BL2phev, BL3ev, BL3phev, P, T, importPower):
    chargersLow, chargersSemifast, chargersFast = [], [], []
    utilization_low, utilization_semifast, utilization_fast = [], [], []
    emission_low, emission_semifast, emission_fast = [], [], []
    demand_L1, demand_L2, demand_L3 = [], [], []
    gwp = [82.52, 91.58, 111.02]
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
        
        u_low =         (((Cev * BL1ev[i]) + (Cphev * BL1phev[i])) / P[0] ) * 100 / (low * T[0])
        u_semifast =    (((Cev * BL2ev[i]) + (Cphev * BL2phev[i])) / P[1] ) * 100 / (semifast * T[1])
        u_fast =        (((Cev * BL3ev[i]) + (Cphev * BL3phev[i])) / P[2] ) * 100 / (fast * T[2])
        if not importPower:
            e_low =      ((Cev * BL1ev[i]) + (Cphev * BL1phev[i])) * (gwp[0] + 164.38)  /1000
            e_semifast = ((Cev * BL2ev[i]) + (Cphev * BL2phev[i])) * (gwp[1] + 164.38)  /1000
            e_fast =     ((Cev * BL3ev[i]) + (Cphev * BL3phev[i])) * (gwp[2] + 164.38)  /1000
        else:
            e_low =      importPower[i] * (BL1ev[i] + BL1phev[i]) * (gwp[0] + 164.38)  /1000
            e_semifast = importPower[i] * (BL2ev[i] + BL2phev[i]) * (gwp[1] + 164.38)  /1000
            e_fast =     importPower[i] * (BL2ev[i] + BL2phev[i]) * (gwp[2] + 164.38)  /1000

        chargersLow.append((low))
        chargersSemifast.append((semifast))
        chargersFast.append((fast))
        utilization_low.append( (u_low))
        utilization_semifast.append( (u_semifast))
        utilization_fast.append( (u_fast))
        emission_low.append( (e_low))
        emission_semifast.append( (e_semifast))
        emission_fast.append( (e_fast))
    return chargersLow, chargersSemifast, chargersFast, utilization_low, utilization_semifast, utilization_fast, emission_low, emission_semifast, emission_fast, demand_L1, demand_L2, demand_L3

def ev_per_CP(scenario_selected_v, cL1, cL2, cL3):
    ev_cs = [[],[],[]]
    annualVehicles = [list(scenario_selected_v["EV"])[i] + list(scenario_selected_v["PHEV"])[i] for i in range(len(list(scenario_selected_v["EV"])))]
    for i in range(len(annualVehicles)):
        ev_cs[0].append( (annualVehicles[i] / cL1[i]))
        ev_cs[1].append( (annualVehicles[i] / cL2[i]))
        ev_cs[2].append( (annualVehicles[i] / cL3[i]))
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
    #Values for year = 0
    numberCSnew = charger_points[0] / 2
    maintenance = 0
    retrofit = 0
    annualMaintenance = initial_cost * maintenance_rate
    annualRetrofit = initial_cost * retrofit_rate
    
    annual = [initial_cost]
    discountedAccumulatedCost = [initial_cost]
    AccumulatedCost = [initial_cost]

    for i in range(1, len(years)):
        discount_rate = get_real_discount_rate(i)

        numberCSnew = (charger_points[i] - charger_points[i-1]) / 2
        maintenance = annualMaintenance * numberCSnew
        retrofit = annualRetrofit * numberCSnew

        if i == 10 or i == 20 or i == 30:
            annual.append( (maintenance + retrofit))
        else:
            annual.append( (maintenance))

        discountedAccumulatedCost.append( (discountedAccumulatedCost[i-1] + (annual[i] / ((1 + discount_rate) ** i))))
        AccumulatedCost.append( (AccumulatedCost[i-1] + annual[i]))
    return discountedAccumulatedCost, AccumulatedCost, annual

def discounted_accumulated_cost2(years, initial_cost, maintenance_rate, retrofit_rate, charger_points, energy_cost):
    #Values for year = 0
    numberCSnew = charger_points[0] / 2
    maintenance = 0
    retrofit = 0
    annualMaintenance = initial_cost * maintenance_rate
    annualRetrofit = initial_cost * retrofit_rate
    
    annual = [initial_cost + (energy_cost[0] * 365)]
    discountedAccumulatedCost = [initial_cost + (energy_cost[0] * 365)]
    AccumulatedCost = [initial_cost + (energy_cost[0] * 365)]

    for i in range(1, len(years)):
        discount_rate = get_real_discount_rate(i)

        numberCSnew = (charger_points[i] - charger_points[i-1]) / 2
        maintenance = annualMaintenance * numberCSnew
        retrofit = annualRetrofit * numberCSnew

        if i == 10 or i == 20 or i == 30:
            annual.append( (maintenance + retrofit + (energy_cost[i] * 365)))
        else:
            annual.append( (maintenance + (energy_cost[i] * 365)))

        discountedAccumulatedCost.append( (discountedAccumulatedCost[i-1] + (annual[i] / ((1 + discount_rate) ** i))))
        AccumulatedCost.append( (AccumulatedCost[i-1] + annual[i]))
    return discountedAccumulatedCost, AccumulatedCost, annual

def job_charging_station(portsPerCH, totalChargerPoints):
    jobsPerCS = 5
    jobs_CS = []
    for i in range(len(totalChargerPoints[0])):
        jobs_CS.append( (((totalChargerPoints[2][i] + totalChargerPoints[2][i]) * jobsPerCS / portsPerCH)))
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
    plt.ylabel('Number Charger Ports')
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/chargers_{case}.jpg')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['Utilization L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['Utilization L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['Utilization L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('Utilization Rate (%)')
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/utilization_{case}.jpg')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['Emission L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['Emission L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['Emission L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('kg CO2')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/emissions_{case}_withPV.jpg')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['EV/CP L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['EV/CP L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['EV/CP L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('EV per Charging Port')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/EVcp_{case}.jpg')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['DAC L1 case1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['DAC L2 case1'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['DAC L3 case1'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('Discounted Accumulated Cost [USD]')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/discountedCost_{case}.jpg')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['Area L1'], color=colors[0], label='L1')
    plt.plot(years, df_chargers['Area L2'], color=colors[1], label='L2')
    plt.plot(years, df_chargers['Area L3'], color=colors[2], label='L3')
    plt.xlabel('Year')
    plt.ylabel('Land Area Required $m^2$')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/area_{case}.jpg')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(years, df_chargers['Jobs'])
    plt.xlabel('Year')
    plt.ylabel('Jobs generated')
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/jobs_{case}.jpg')
    plt.close()

def subplot_ev_metrics(years, df_chargers, case):
    colors = ["#bda5ad", "#00a099", "#a4165f"]
    fig, axs = plt.subplots(4, 2, figsize=(16, 16))
    axs = axs.flatten()

    # 1. Charger ports (stacked bar)
    axs[0].bar(years, df_chargers['L1'], color=colors[0], label='L1')
    axs[0].bar(years, df_chargers['L2'], bottom=df_chargers['L1'], color=colors[1], label='L2')
    axs[0].bar(years, df_chargers['L3'], bottom=df_chargers['L1'] + df_chargers['L2'], color=colors[2], label='L3')
    axs[0].set_ylabel('Number Public Charging Ports')
    axs[0].set_title('Public Charging Ports')
    axs[0].legend()
    axs[0].grid(True, linestyle="--", alpha=0.7)

    # 4. EV per Charging Port
    axs[1].plot(years, df_chargers['EV/CP L1'], color=colors[0], label='L1')
    axs[1].plot(years, df_chargers['EV/CP L2'], color=colors[1], label='L2')
    axs[1].plot(years, df_chargers['EV/CP L3'], color=colors[2], label='L3')
    axs[1].set_ylabel('EV per Charging Port')
    axs[1].set_title('Vehicles per Charging Point ')
    axs[1].legend()
    axs[1].grid(True, linestyle="--", alpha=0.7)

    # 2. Utilization
    axs[2].plot(years, df_chargers['Utilization L1'], color=colors[0], label='L1')
    axs[2].plot(years, df_chargers['Utilization L2'], color=colors[1], label='L2')
    axs[2].plot(years, df_chargers['Utilization L3'], color=colors[2], label='L3')
    axs[2].set_ylabel('Utilization Rate (%)')
    axs[2].set_title('Charging Station Utilization Rate ')
    axs[2].legend()
    axs[2].grid(True, linestyle="--", alpha=0.7)

    # 5. Discounted Cost
    axs[3].plot(years, df_chargers['DAC L1 case1'], color=colors[0], label='L1')
    axs[3].plot(years, df_chargers['DAC L2 case1'], color=colors[1], label='L2')
    axs[3].plot(years, df_chargers['DAC L3 case1'], color=colors[2], label='L3')
    axs[3].set_ylabel('Cost [USD]')
    axs[3].set_title('Discounted Accumulated Cost')
    axs[3].legend()
    axs[3].grid(True, linestyle="--", alpha=0.7)

    # 6. Land Area
    axs[4].plot(years, df_chargers['Area L1'], color=colors[0], label='L1')
    axs[4].plot(years, df_chargers['Area L2'], color=colors[1], label='L2')
    axs[4].plot(years, df_chargers['Area L3'], color=colors[2], label='L3')
    axs[4].set_ylabel('Land Area ($m^2$)')
    axs[4].set_title('Land Area Required')
    axs[4].legend()
    axs[4].grid(True, linestyle="--", alpha=0.7)

    # 3. Emissions
    axs[5].plot(years, df_chargers['Emission L1'], color=colors[0], label='L1')
    axs[5].plot(years, df_chargers['Emission L2'], color=colors[1], label='L2')
    axs[5].plot(years, df_chargers['Emission L3'], color=colors[2], label='L3')
    axs[5].set_ylabel('kg CO2')
    axs[5].set_title('Environmental Factor')
    axs[5].legend()
    axs[5].grid(True, linestyle="--", alpha=0.7)

    # 7. Jobs
    axs[6].plot(years, df_chargers['Jobs'], color='gray')
    axs[6].set_ylabel('Number of jobs')
    axs[6].set_title('Job creation ')
    axs[6].grid(True, linestyle="--", alpha=0.7)

    # 8. Turn off unused subplot
    data = {
    "": ["Number Ports", "EV per CS", "Utilization rate [%]", "Cost [USD]", "Land Area [$m^3]$ ", "kg $CO_2$", "Number jobs"],
    "Low charging": ['2,485', '2', '100', '37,230', '0', '26,691', ""],
    "Semi fast charging": ['1,299', '4', '100', '260,857', '130', '13,775', '2,210'],
    "Fast charging": ['442', '11', '100', '1,064,471', '139', '15,111', ""]
    }

    table_df = pd.DataFrame(data)

    # Remove axis and add table
    axs[7].axis('off')
    table = axs[7].table(cellText=table_df.values,
                        colLabels=table_df.columns,
                        cellLoc='center',
                        loc='center')

    table.scale(1, 1.5)  # optional: increase row height
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    axs[7].set_title("Summary of results for the last year in the projection horizon")

    # Set common X label
    for ax in axs:
        ax.set_xlabel('Year')

    plt.tight_layout()
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/figures/all_metrics_{case}.jpg')
    plt.close()

def extract_import_power_doper(folder_path):
    all_data = []
    csv_files = sorted([f for f in os.listdir(folder_path) if f.startswith("doperRes") and f.endswith(".csv")],
                        key=lambda x: int(x.replace("doperRes", "").replace(".csv", "")))
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path) 
        all_data.append(list(df['Import Power [kW]']))
    importPower = []
    for i in range(len(all_data)):
        # importPower.append( (0.0833 * sum(all_data[i])))
        importPower.append( (sum(all_data[i])))
    return importPower

if __name__ == '__main__':
    fuel_demand = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/fuel_demand.csv')
    projections = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_projections.csv')

    df_electricity = fuel_demand[["Year", "Scenario", "Electricity [kWh]"]]
    df_vehicles = projections[["Year", "Scenario", "EV", "PHEV"]]

    P = [7, 20, 60] # charge speed
    E100km = 11.03 # EV's performance (kwh/100km)
    dailyDistance = 175 # EV's daily distance (km)
    Cev = (E100km / 100) * 175 # electric demand daily per vehicle
    Cphev = (E100km / 100) * 175 * 0.7 # electric demand daily per vehicle
    initial_cost = [800, 6500, 75000]
    maintenance_rate = [0.1, 0.1, 0.1]
    retrofit_rate = [0.05, 0.5, 0.5]
    energy_cost = 0.22 #USD/kWh extract to CEDENAR march 2025 - kWh cost for comercial in tension 2
    portsPerCH = 2
    parkingArea = [0, 0, 14]

    scenario = 'Scenario 3'
    scenario_selected_v = df_vehicles.loc[df_vehicles.loc[:, 'Scenario'] == scenario]
    scenario_selected_e = df_electricity.loc[df_electricity.loc[:, 'Scenario'] == scenario]
    years = list(scenario_selected_v['Year'])

    T_cases = [[24, 8, 8], [24, 10, 12], [24, 12, 15], [24, 16, 18], [24, 24, 24]] # time available
    list_cases = ['case1', 'case2', 'case3', 'case4', 'case5']

    energy_cost_file = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/costEnergyCompare.csv')
    energy_cost2 = list(energy_cost_file['Energy Cost [$]'])
    energy_cost3 = list(energy_cost_file['PV Cost [$]'])

    doper_results_directory = "C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper_withoutIncrease"
    import_power_with_pv = [0]
    import_power = extract_import_power_doper(doper_results_directory)
    v = []
    for i in range(len(list(scenario_selected_v['EV']))):
        v.append(list(scenario_selected_v['EV'])[i]+(list(scenario_selected_v['PHEV'])[i] * 0.7))
    
    for i in range(1, len(import_power)):
        import_power_with_pv.append( (import_power[i] / (v[i])) ) 
    # print('C = ', C)
    # print('import power =' ,  import_power)
    # print('vehiculos = ', v)
    # print('import power with pv =' , import_power_with_pv)

    for j in range(len(list_cases)):
    # for j in range(1):
        T = T_cases[j]
        case = list_cases[j]
        ev = list(scenario_selected_v["EV"])
        bL1ev, bL2ev, bL3ev, betaev, lx2ev, lx3ev = percentage_preference_type_charger(ev)
        phev = list(scenario_selected_v["PHEV"])
        bL1phev, bL2phev, bL3phev, betaphev, lx2phev, lx3ephv = percentage_preference_type_charger(phev)

        # year_index = 30
        # beta_year = np.array(beta[year_index][0])
        # lx2_year = np.array(lx2[year_index][0])
        # lx3_year = np.array(lx3[year_index])
        # vehicles = np.arange(len(beta_year))  # Eje x: índice de vehículos
        # fig, axs = plt.subplots(1, 2, figsize=(10, 4), sharex=True)
        # axs[0].bar(vehicles, beta_year, color='#a4165f', width=0.5)
        # axs[0].set_title(f'β distribution')
        # axs[0].set_xlabel('Vehicle')
        # axs[1].bar(vehicles, lx2_year, label='L2', color='#c0fcf7', width=0.5)
        # axs[1].bar(vehicles, lx3_year, bottom=lx2_year, label='L3', color='#005ecc', width=0.5)
        # axs[1].set_xlabel('Vehicle')
        # axs[1].set_title('$\\alpha^{L_2}$ and $\\alpha^{L_3}$ distribution')
        # axs[1].legend()
        # plt.show()

        cL1, cL2, cL3, uL1, uL2, uL3, eL1, eL2, eL3, demand_L1, demand_L2, demand_L3 = cp_technical_metrics(Cev, Cphev, bL1ev, bL1phev, bL2ev, bL2phev, bL3ev, bL3phev, P, T, import_power_with_pv)
        totalChargerPoints = [cL1, cL2, cL3]
        ev_cs = ev_per_CP(scenario_selected_v, cL1, cL2, cL3)
        discountedAC_L1_1, accumulatedC_L1_1, annualC_L1_1 = discounted_accumulated_cost(years, initial_cost[0], maintenance_rate[0], retrofit_rate[0], cL1)
        discountedAC_L2_1, accumulatedC_L2_1, annualC_L2_1 = discounted_accumulated_cost(years, initial_cost[1], maintenance_rate[1], retrofit_rate[1], cL2)
        discountedAC_L3_1, accumulatedC_L3_1, annualC_L3_1 = discounted_accumulated_cost(years, initial_cost[2], maintenance_rate[2], retrofit_rate[2], cL3)

        discountedAC_L1_2, accumulatedC_L1_2, annualC_L1_2 = discounted_accumulated_cost2(years, initial_cost[0], maintenance_rate[0], retrofit_rate[0], cL1, energy_cost2)
        discountedAC_L2_2, accumulatedC_L2_2, annualC_L2_2 = discounted_accumulated_cost2(years, initial_cost[1], maintenance_rate[1], retrofit_rate[1], cL2, energy_cost2)
        discountedAC_L3_2, accumulatedC_L3_2, annualC_L3_2 = discounted_accumulated_cost2(years, initial_cost[2], maintenance_rate[2], retrofit_rate[2], cL3, energy_cost2)

        discountedAC_L1_3, accumulatedC_L1_3, annualC_L1_3 = discounted_accumulated_cost2(years, initial_cost[0], maintenance_rate[0], retrofit_rate[0], cL1, energy_cost3)
        discountedAC_L2_3, accumulatedC_L2_3, annualC_L2_3 = discounted_accumulated_cost2(years, initial_cost[1], maintenance_rate[1], retrofit_rate[1], cL2, energy_cost3)
        discountedAC_L3_3, accumulatedC_L3_3, annualC_L3_3 = discounted_accumulated_cost2(years, initial_cost[2], maintenance_rate[2], retrofit_rate[2], cL3, energy_cost3)

        jobs = job_charging_station(portsPerCH, totalChargerPoints)
        landArea = land_area_metric(totalChargerPoints, parkingArea)

        df_chargers = pd.DataFrame()
        df = pd.DataFrame({'Year': years,
                        'L1': cL1, 'L2': cL2, 'L3': cL3,
                        'Utilization L1': uL1, 'Utilization L2': uL2, 'Utilization L3': uL3,
                        'Emission L1': eL1, 'Emission L2': eL2, 'Emission L3': eL3,
                        'EV/CP L1': ev_cs[0], 'EV/CP L2': ev_cs[1], 'EV/CP L3': ev_cs[2],
                        'Area L1': landArea[0], 'Area L2': landArea[1], 'Area L3': landArea[2],
                        'Jobs': jobs,
                        'DAC L1 case1': discountedAC_L1_1, 'DAC L2 case1': discountedAC_L2_1, 'DAC L3 case1': discountedAC_L3_1,
                        'DAC L1 case2': discountedAC_L1_2, 'DAC L2 case2': discountedAC_L2_2, 'DAC L3 case2': discountedAC_L3_2,
                        'DAC L1 case3': discountedAC_L1_3, 'DAC L2 case3': discountedAC_L2_3, 'DAC L3 case3': discountedAC_L3_3})

        df_chargers = pd.concat([df_chargers, df])
        df_chargers.to_csv(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/change_percentage_preference/cs_projections_{case}_withPV.csv')
        plot_ev_metrics(years, df_chargers, f'{case}')
        subplot_ev_metrics(years, df_chargers, f'{case}')

    