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

def demand(C , T, N):
    tu_11 = []
    tu_22 = []
    tu_50 = []
    Pref = []
    np.random.seed(0)
    b = np.random.random((1,N))

    for i in range(N):
        Pref_r = np.random.random((1,3))
        suma = sum(Pref_r[0])
        Pref_norm = [Pref_r[0][0]/ suma, Pref_r[0][1]/ suma, Pref_r[0][2]/ suma]
        Pref.append(Pref_norm)

    for i in range(N):
        tu_11.append(C * b[0][i] * Pref[i][0])
        tu_22.append(C * b[0][i] * Pref[i][1])
        tu_50.append(C * b[0][i] * Pref[i][2])

    totalDemand11 = sum(tu_11)/ (11 * T)
    totalDemand22 = sum(tu_22)/ (22 * T)
    totalDemand50 = sum(tu_50)/ (50 * T)
    
    return round(sum(tu_11), 2), round(sum(tu_22), 2), round(sum(tu_50), 2), round(totalDemand11, 2), round(totalDemand22, 2), round(totalDemand50, 2)

if __name__ == '__main__':
    import calculate_metrics as cm

    vehicleSeed = 3016 # Number of taxis in Pasto (year = 2024)
    taxisProjection = [3043, 3071, 3098, 3126, 3154, 3299, 3450, 3608, 3773, 3946]
    penetrationPercentage = [0.03, 0.5, 1.0, 2.0, 3.0, 10.0, 25.0, 50.0, 80.0, 100.0] 
    
    annualVehicles = ice_to_ev(taxisProjection, penetrationPercentage)
    print('Annual EV = ', annualVehicles)

    emissionClasses = ['HBEFA4/PC_BEV']
    dataframe = cm.generate_data_frame(emissionClasses,"./results/rush/data_emissions_EV.csv")
    annualConsumption = cm.mean_daily('EV', dataframe, 35, 9) * 365
    annualConsumptionTotal = annual_consumption_per_penetration(annualVehicles, annualConsumption)
    print('Annual demand kWh per penetration percentage = ', annualConsumptionTotal)

    # print('Hour charging per year L1 = ', charging_time(annualConsumptionTotal[2], 1.8))
    # print('Hour charging per year L2 - M1 = ', charging_time(annualConsumptionTotal[2], 11.0))
    # print('Hour charging per year L2 - M2&3 = ', charging_time(annualConsumptionTotal[2], 22.0))
    # print('Hour charging per year L3 = ', charging_time(annualConsumptionTotal[2], 50.0))

    C = 53.5 * cm.mean_daily('EV', dataframe, 35, 2) / 417.20
    # print('C = ', C, 'distance = ', cm.mean_daily('EV', dataframe, 35, 2))
    P = [11, 22, 50]
    T = 24

    numberChargers11kW = []
    numberChargers22kW = []
    numberChargers50kW = []
    
    for i in range(len(annualVehicles)):
        numberChargers11kW.append(demand(C, T, annualVehicles[i])[3])
        numberChargers22kW.append(demand(C, T, annualVehicles[i])[4])
        numberChargers50kW.append(demand(C, T, annualVehicles[i])[5])
    print('Number of chargers - 11 kW =', numberChargers11kW)
    print('Number of chargers - 22 kW =', numberChargers22kW)
    print('Number of chargers - 50 kW =', numberChargers50kW)

    # print('11 kW ', round(annualVehicles[-1]/numberChargers11kW[-1]))
    # print('22 kW ', round(annualVehicles[-1]/numberChargers22kW[-1]))
    # print('50 kW ', round(annualVehicles[-1]/numberChargers50kW[-1]))

    print('Number of chargers')
    cs11kW = round(numberChargers11kW[-1])
    cs22kW = round(numberChargers22kW[-1])
    cs50kW = round(numberChargers50kW[-1])
    print('Number CS 11 kW = ', cs11kW, 'Number CS 22 kW = ', cs22kW, 'Number CS 50 kW = ', cs50kW)

    csUtilizationRateL1 = []
    csUtilizationRateL2M1 = []
    csUtilizationRateL2M2_3 = []
    csUtilizationRateL3M4 = []


    TU = demand(C, T, annualVehicles[-1])[0]
    TA = 24 * cs11kW
    print('TU = ', TU)
    csUtilizationRateL2M1 = TU * 100 / TA
    # for i in range(len(annualConsumptionTotal)):
    #     TU = charging_time(annualConsumptionTotal[i] / 365, 11.0)
    #     TA = 24 * cs11kW
        # print('TU = ', TU, 'TA = ', TA)
        # csUtilizationRateL2M1.append(round((TU) * 100 / (TA),2))
        # csUtilizationRateL2M2_3.append(round((charging_time(annualConsumptionTotal[i], 22.0) / 12) * 100 / (24 * 30 * 22),2))
        # csUtilizationRateL3M4.append(round((charging_time(annualConsumptionTotal[i], 50.0) / 12) * 100 / (24 * 30 * 14),2))

    print('CS Utilization Rate')
    print('CS 11 kW = ', csUtilizationRateL2M1)
    # print('CS 22 kW = ', csUtilizationRateL2M2_3)
    # print('CS 50 kW = ', csUtilizationRateL3M4)

    # year = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30]
    # plt.plot(year, csUtilizationRateL2M1)
    # plt.plot(year, csUtilizationRateL2M2_3)
    # plt.plot(year, csUtilizationRateL3M4)
    # plt.legend([ 'L2 M1 - 11 kW', 'L2 M2&3 - 22kW', 'L3 M4 - 50 kW'])
    # plt.title('Charging Station Utilization Rate')
    # plt.xlabel('Year')
    # plt.ylabel('%')
    # plt.grid()
    # plt.show()