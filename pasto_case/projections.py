import numpy as np
import matplotlib.pyplot as plt

def ice_to_ev(taxisProjection, penetrationPercentage):
    evPenetration = []
    for i in range(len(penetrationPercentage)):
        evPenetration.append(round(taxisProjection[i] * penetrationPercentage[i] / 100))
    return evPenetration

def annual_consumption_per_penetration(annualVehicles, annualConsumption):
    annualConsumptionperPenetration = []
    for i in range(len(penetrationPercentage)):
        annualConsumptionperPenetration.append(round(annualVehicles[i] * annualConsumption, 2))
    return annualConsumptionperPenetration

def charging_time(chargeNeeded, chargingSpeed):
    hourChargingTime = chargeNeeded / chargingSpeed
    return round(hourChargingTime, 2)

def demandPowerCharge(C , T, N):
    powerNeeded_1 = []
    powerNeeded_11 = []
    powerNeeded_22 = []
    powerNeeded_50 = []
    np.random.seed(0)
    b = np.random.random((1,N))
    for i in range(N):
        Pref_r = np.random.random((1,3))
        suma = sum(Pref_r[0])
        Pref_norm = [Pref_r[0][0]/ suma, Pref_r[0][1]/ suma, Pref_r[0][2]/ suma]
        powerNeeded_1.append(C * (1 - b[0][i]))
        powerNeeded_11.append(C * b[0][i] * Pref_norm[0])
        powerNeeded_22.append(C * b[0][i] * Pref_norm[1])
        powerNeeded_50.append(C * b[0][i] * Pref_norm[2])
    return sum(powerNeeded_1), sum(powerNeeded_11), sum(powerNeeded_22), sum(powerNeeded_50), np.mean(b[0])

if __name__ == '__main__':
    import calculate_metrics as cm

    vehicleSeed = 3016 # Number of taxis in Pasto (year = 2024)
    taxisProjection = [3043, 3071, 3098, 3126, 3154, 3299, 3450, 3608, 3773, 3946]
    penetrationPercentage = [0.03, 0.5, 1.0, 2.0, 3.0, 10.0, 25.0, 50.0, 80.0, 100.0] 
    
    annualVehicles = ice_to_ev(taxisProjection, penetrationPercentage)
    print('Annual vehicles = ', annualVehicles)

    emissionClasses = ['HBEFA4/PC_BEV']
    dataframe = cm.generate_data_frame(emissionClasses,"./results/rush/data_emissions_EV.csv")
    annualConsumption = cm.mean_daily('EV', dataframe, 35, 9) * 365
    annualConsumptionTotal = annual_consumption_per_penetration(annualVehicles, annualConsumption)

    dailyDistance = cm.mean_daily('EV', dataframe, 35, 2)
    C = 53.5 * dailyDistance / 417.20
    P = [1.8 ,11, 22, 50]
    T = 24

    tu_1kW = []
    tu_11kW = []
    tu_22kW = []
    tu_50kW = []
    numberChargers1kW = []
    numberChargers11kW = []
    numberChargers22kW = []
    numberChargers50kW = []
    csUtilizationRateL1 = []
    csUtilizationRateL2M1 = []
    csUtilizationRateL2M2_3 = []
    csUtilizationRateL3M4 = []
    b_index = []


    for i in range(len(annualVehicles)):
        nCS = demandPowerCharge(C, T, annualVehicles[i])
        tu_1kW.append(nCS[0] / P[0])
        tu_11kW.append(nCS[1] / P[1])
        tu_22kW.append(nCS[2] / P[2])
        tu_50kW.append(nCS[3] / P[3])
        numberChargers1kW.append(round(nCS[0] / (P[0] * T), 2))
        numberChargers11kW.append(round(nCS[1] / (P[1] * T), 2))
        numberChargers22kW.append(round(nCS[2] / (P[2] * T), 2))
        numberChargers50kW.append(round(nCS[3] / (P[3] * T), 2))
        b_index.append(round(nCS[4], 2))
    print('Preference private station = ', b_index, 'Mean preference = ', round(np.mean(b_index), 2))
    print('Number of chargers - 1.8 kW =', numberChargers1kW)
    print('Number of chargers - 11 kW =', numberChargers11kW)
    print('Number of chargers - 22 kW =', numberChargers22kW)
    print('Number of chargers - 50 kW =', numberChargers50kW)

    print('11 kW ', round(annualVehicles[-1]/numberChargers11kW[-1]))
    print('22 kW ', round(annualVehicles[-1]/numberChargers22kW[-1]))
    print('50 kW ', round(annualVehicles[-1]/numberChargers50kW[-1]))


    print('Number CS 1 kW = ', round(numberChargers1kW[-1]), 
          'Number CS 11 kW = ', round(numberChargers11kW[-1]), 
          'Number CS 22 kW = ', round(numberChargers22kW[-1]), 
          'Number CS 50 kW = ', round(numberChargers50kW[-1]))
    
    ta_1kw = numberChargers1kW[-1] * T
    ta_11kw = numberChargers11kW[-1] * T
    ta_22kw = numberChargers22kW[-1] * T
    ta_50kw = numberChargers50kW[-1] * T

    for i in range(len(annualVehicles)):
        csUtilizationRateL1.append(round(tu_1kW[i] * 100 / ta_1kw , 2))
        csUtilizationRateL2M1.append(round(tu_11kW[i] * 100 / ta_11kw , 2))
        csUtilizationRateL2M2_3.append(round(tu_22kW[i] * 100 / ta_22kw , 2))
        csUtilizationRateL3M4.append(round(tu_50kW[i] * 100 / ta_50kw , 2))


    year = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30]
    plt.plot(year, csUtilizationRateL1)
    plt.plot(year, csUtilizationRateL2M1)
    plt.plot(year, csUtilizationRateL2M2_3)
    plt.plot(year, csUtilizationRateL3M4)
    plt.legend(['L1 - 1.8 kW', 'L2 M1 - 11 kW', 'L2 M2&3 - 22kW', 'L3 M4 - 50 kW'])
    plt.title('Charging Station Utilization Rate')
    plt.xlabel('Year')
    plt.ylabel('%')
    plt.grid()
    plt.show()

    year = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30]
    plt.plot(year, numberChargers1kW)
    plt.plot(year, numberChargers11kW)
    plt.plot(year, numberChargers22kW)
    plt.plot(year, numberChargers50kW)
    plt.legend([ '#CS - 1.8 kW', '#CS - 11 kW', '#CS - 22kW', '#CS - 50 kW'])
    plt.title('Number of Charging Station')
    plt.xlabel('Year')
    plt.ylabel('%')
    plt.grid()
    plt.show()