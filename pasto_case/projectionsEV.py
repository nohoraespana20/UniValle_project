import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def escenario_1(start_year=2025, end_year=2055):
    years = np.arange(start_year, end_year + 1)
    total_vehicles = [3016, 3056, 3097, 3138, 3180, 3222, 3265, 3308, 3352, 3397, 3442, 3488, 3534, 3581, 3629, 
                      3677, 3726, 3776, 3826, 3877, 3928, 3980, 4033, 4087, 4141, 4196, 4252, 4309, 4366, 4424, 4483 ]
    icev = [2976, 3015, 3041, 3065, 3075, 3084, 3095, 3071, 3081, 3090,
            3066, 3042, 2982, 2923, 2896, 2764, 2630, 2492, 2353, 2211,
            2066, 1883, 1695, 1504, 1271, 1111, 947, 759, 457, 266, 0]
    cng = [40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 46, 46, 47, 47, 48, 49, 49, 50,
           51, 51, 52, 53, 53, 54, 55, 56, 56, 57, 58, 59, 59]
    phev = [0]*31
    ev = [0, 1, 15, 31, 63, 95, 127, 193, 227, 262, 330, 400, 505, 611, 685, 
         864, 1047, 1233, 1422, 1614, 1810, 2045, 2285, 2529, 2815, 3030, 
         3249, 3493, 3851, 4100, 4424]

    return pd.DataFrame({'Year': years, 'Total': total_vehicles, 'ICEV': icev, 'CNG': cng, 'PHEV': phev, 'EV': ev})

def escenario_2(start_year=2025, end_year=2055):
    years = np.arange(start_year, end_year + 1)
    total_vehicles = [3016, 3056, 3097, 3138, 3180, 3222, 3265, 3308, 3352, 3397, 3442, 3488, 3534, 3581, 3629, 
                      3677, 3726, 3776, 3826, 3877, 3928, 3980, 4033, 4087, 4141, 4196, 4252, 4309, 4366, 4424, 4483 ]
    icev = [2976, 3015, 3041, 3065, 3075, 3084, 3095, 3071, 3081, 3090,
            3066, 3042, 2982, 2923, 2896, 2764, 2630, 2492, 2353, 2211,
            2066, 1883, 1695, 1504, 1271, 1111, 947, 759, 457, 266, 0]
    cng = [40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 46, 46, 47, 47, 48, 49, 49, 50,
           51, 51, 52, 53, 53, 54, 55, 56, 56, 57, 58, 59, 59]
    phev = [0, 1, 8, 16, 32, 48, 64, 97, 114, 131, 165, 200, 253, 306, 343, 
            432, 524, 617, 711, 807, 905, 1023, 1143, 1265, 1408, 1515, 1625, 
            1747, 1926, 2050, 2212]
    ev = phev

    return pd.DataFrame({'Year': years, 'Total': total_vehicles, 'ICEV': icev, 'CNG': cng, 'PHEV': phev, 'EV': ev})

def escenario_3(start_year=2025, end_year=2055):
    years = np.arange(start_year, end_year + 1)
    total_vehicles = [3016, 3056, 3097, 3138, 3180, 3222, 3265, 3308, 3352, 3397, 3442, 3488, 3534, 3581, 3629, 
                      3677, 3726, 3776, 3826, 3877, 3928, 3980, 4033, 4087, 4141, 4196, 4252, 4309, 4366, 4424, 4483 ]
    icev = [2976, 3015, 3041, 3065, 3075, 3084, 3095, 3071, 3081, 3090,
            3066, 3042, 2982, 2923, 2896, 2764, 2630, 2492, 2353, 2211,
            2066, 1883, 1695, 1504, 1271, 1111, 947, 759, 457, 266, 0]
    cng = [40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 46, 46, 47, 47, 48, 49, 49, 50,
           51, 51, 52, 53, 53, 54, 55, 56, 56, 57, 58, 59, 59]
    phev = [0, 1, 11, 23, 47, 71, 95, 145, 170, 197, 248, 298, 304, 306, 310, 
            312, 316, 320, 326, 330, 334, 339, 342, 349, 356, 363, 370, 378, 
            385, 393, 401]
    ev = [0, 1, 4, 8, 16, 24, 32, 48, 57, 66, 83, 100, 201, 305, 375, 552, 
         731, 913, 1096, 1284, 1476, 1706, 1943, 2180, 2459, 2667, 
         2879, 3115, 3466, 3707, 4023]

    return pd.DataFrame({'Year': years, 'Total': total_vehicles, 'ICEV': icev, 'CNG': cng, 'PHEV': phev, 'EV': ev})

def plot_escenario(df, title, ax):
    sns.set_style("whitegrid")

    ax.plot(df["Year"], df["ICEV"], label="ICEV", linestyle="--", color="#a4165f")
    ax.plot(df["Year"], df["CNG"], label="CNG", linestyle="--", color="#0088d1")
    ax.plot(df["Year"], df["PHEV"], label="PHEV", linestyle="-", color="#516bc5")
    ax.plot(df["Year"], df["EV"], label="EV", linestyle=":", color="#00aea7")
    ax.plot(df["Year"], df["Total"], label="Total", linestyle=":", color="black")

    ax.set_ylabel("Number of vehicles")
    ax.set_title(title)
    ax.legend()
    ax.grid()
    if ax != axes[-1]:
        ax.set_xticklabels([])  
    else:
        ax.set_xlabel("Year")  
    if ax == axes[-1]:
        ax.legend()

def calculate_demand(icev, cng, ev, phev, phev_g_ratio=0.3):
    gasoline = [round(i * 3.785 * 65.43 * 175.4 / (10.69 * 100), 2) for i in icev]
    cng_demand = [round(c * 3.785 * 52.33 * 175.4 / (10.70 * 100), 2) for c in cng]
    ev_demand = [round(e * 11.03 * 175.4 / 100, 2) for e in ev]
    phev_g = [round(p * 3.785 * 65.43 * (175.4 * phev_g_ratio) / (10.69 * 100), 2) for p in phev]
    phev_e = [round(p * 11.03 * (175.4 * (1 - phev_g_ratio)) / 100, 2) for p in phev]
    total_gasoline = [gasoline[i] + phev_g[i] for i in range(len(phev_g))]
    total_ev = [ev_demand[i] + phev_e[i] for i in range(len(phev_e))]
    return total_gasoline, cng_demand, total_ev

def plot_daily_demand(years, fuel_data, save_path):
    """
    Genera una gráfica de la demanda diaria de energía por escenario.
    Parámetros:
    - years: Lista de años.
    - fuel_data: Lista de tuplas (fuel, linestyle, label_prefix), donde:
        * fuel: Lista con los valores de combustibles [Petrol, CNG, Electricity].
        * linestyle: Tipo de línea ('--', 'dotted', '-').
        * label_prefix: Nombre del escenario ('Scenario 1', 'Scenario 2', etc.).
    - save_path: Ruta donde se guardará la imagen.
    """
    plt.figure(figsize=(10, 6))

    colors = ['#ff7900', '#00c6ce', '#00bc45']  
    labels = ['Petrol [l]', 'CNG [l]', 'Electricity [kWh]']

    for fuel, linestyle, label_prefix in fuel_data:
        for i in range(3): 
            plt.plot(years, fuel[i], linestyle=linestyle, color=colors[i],
                     label=f"{labels[i]} - {label_prefix}")

    plt.xlabel('Year')
    plt.ylabel('Daily demand')
    plt.title('Power daily demand per scenarios')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(save_path)

def charging_time(chargeNeeded, chargerType):
    if chargerType == 'low':
        chargingSpeed = 7
    elif chargerType == 'semifast1':
        chargingSpeed = 20
    elif chargerType == 'fast':
        chargingSpeed = 60
    else:
        print('')
    hourChargingTime = chargeNeeded / chargingSpeed
    return round(hourChargingTime, 2)

def percentage_preference_type_charger(annualVehicles):
    np.random.seed(0)
    publicPreference = np.random.random((1, annualVehicles))
    normLevelPreference = []
    for i in range(annualVehicles):
        levelPreference = np.random.random((1,3))
        sumLevelPreference = sum(levelPreference[0])
        normLevelPreference.append([levelPreference[0][0]/ sumLevelPreference, levelPreference[0][1]/ sumLevelPreference, levelPreference[0][2]/ sumLevelPreference])
    return publicPreference[0], normLevelPreference

def demand_power_charge(demandPerVehicle , annualVehicles, chargerType, b, P):
    powerNeeded = []
    for i in range(annualVehicles):
        if chargerType == 'low':
            powerNeeded.append(demandPerVehicle * (1 - b))
        elif chargerType == 'semifast':
            powerNeeded.append(demandPerVehicle * b * P[0])
        elif chargerType == 'fast':
            powerNeeded.append(demandPerVehicle * b * P[1])
    return sum(powerNeeded)



if __name__ == '__main__':
    df_1 = escenario_1()
    df_2 = escenario_2()
    df_3 = escenario_3()

    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    plot_escenario(df_1, "Scenario 1", axes[0])
    plot_escenario(df_2, "Scenario 2", axes[1])
    plot_escenario(df_3, "Scenario 3", axes[2])
    plt.tight_layout()
    plt.savefig('C:/Users/noluc/OneDrive/Escritorio/Univalle/Avances2025/paper_netherland/projections.jpg')

    # Calcular demanda
    fuel_1 = calculate_demand(df_1["ICEV"], df_1["CNG"], df_1["EV"], df_1["PHEV"], 0)
    fuel_2 = calculate_demand(df_2["ICEV"], df_2["CNG"], df_2["EV"], df_2["PHEV"], 0.3)
    fuel_3 = calculate_demand(df_3["ICEV"], df_3["CNG"], df_3["EV"], df_3["PHEV"], 0.3)

    fuel_data = [(fuel_1, '--', 'Scenario 1'),
                (fuel_2, 'dotted', 'Scenario 2'),
                (fuel_3, '-', 'Scenario 3')]

    plot_daily_demand(df_1["Year"], fuel_data, 'C:/Users/noluc/OneDrive/Escritorio/Univalle/Avances2025/paper_netherland/daily_demand.jpg')