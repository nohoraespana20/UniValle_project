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

def demand(C , P, T, N):
    demand = []
    np.random.seed(0)
    b = np.random.random((1,N))
    Pref = np.random.random((1,N))
    for i in range(N):
        demand.append(C * b[0][i] * Pref[0][i])
    totalDemand = sum(demand)/ (P * T)
    return round(totalDemand, 2)

if __name__ == '__main__':
    import calculate_metrics as cm

    vehicleSeed = 3016 # Number of taxis in Pasto (year = 2024)
    taxisProjection = [3043, 3071, 3098, 3126, 3154, 3299, 3450, 3608, 3773, 3946]
    penetrationPercentage = [0.03, 0.5, 1.0, 2.0, 3.0, 10.0, 25.0, 50.0, 80.0, 100.0] 
    
    annualVehicles = ice_to_ev(taxisProjection, penetrationPercentage)
    print('Annual EV = ', annualVehicles)

    emissionClasses = ['Energy/unknown']
    dataframe = cm.generate_data_frame(emissionClasses,"./results/rush/data_emissions_EV.csv")
    annualConsumption = cm.mean_daily('EV', dataframe, 35, 9) * 365
    annualConsumptionTotal = annual_consumption_per_penetration(annualVehicles, annualConsumption)
    print('Annual demand kWh per penetration percentage = ', annualConsumptionTotal)

    # print('Hour charging per year L1 = ', charging_time(annualConsumptionTotal[2], 1.8))
    # print('Hour charging per year L2 - M1 = ', charging_time(annualConsumptionTotal[2], 11.0))
    # print('Hour charging per year L2 - M2&3 = ', charging_time(annualConsumptionTotal[2], 22.0))
    # print('Hour charging per year L3 = ', charging_time(annualConsumptionTotal[2], 50.0))

    C = 53.5 * cm.mean_daily('EV', dataframe, 35, 2) / 417.20
    P = [11, 22, 50]
    T = 24

    demandPerYear11kW = []
    demandPerYear22kW = []
    demandPerYear50kW = []
    
    for i in range(len(annualVehicles)):
        demandPerYear11kW.append(demand(C , P[0], T, annualVehicles[i]))
        demandPerYear22kW.append(demand(C , P[1], T, annualVehicles[i]))
        demandPerYear50kW.append(demand(C , P[2], T, annualVehicles[i]))
    # print('Demand per year - 11 kW =', demandPerYear11kW)
    # print('Demand per year - 22 kW =', demandPerYear22kW)
    # print('Demand per year - 50 kW =', demandPerYear50kW)

    # print('11 kW ', round(annualVehicles[-1]/demandPerYear11kW[-1]))
    # print('22 kW ', round(annualVehicles[-1]/demandPerYear22kW[-1]))
    # print('50 kW ', round(annualVehicles[-1]/demandPerYear50kW[-1]))

    cs11kW = round(demandPerYear11kW[-1])
    cs22kW = round(demandPerYear22kW[-1])
    cs50kW = round(demandPerYear50kW[-1])
    print('# CS 11 kW = ', cs11kW, '# CS 22 kW = ', cs22kW, '# CS 50 kW = ', cs50kW)

    csUtilizationRateL1 = []
    csUtilizationRateL2M1 = []
    csUtilizationRateL2M2_3 = []
    csUtilizationRateL3M4 = []


    for i in range(len(annualConsumptionTotal)):
        csUtilizationRateL1.append(round( (charging_time(annualConsumptionTotal[i], 1.8) / 12) * 100 / (24 * 30 * 91),2))
        csUtilizationRateL2M1.append(round((charging_time(annualConsumptionTotal[i], 11.0) / 12) * 100 / (24 * 30 * 46),2))
        csUtilizationRateL2M2_3.append(round((charging_time(annualConsumptionTotal[i], 22.0) / 12) * 100 / (24 * 30 * 46),2))
        csUtilizationRateL3M4.append(round((charging_time(annualConsumptionTotal[i], 50.0) / 12) * 100 / (24 * 30 * 20),2))

    print('CS Utilization Rate')
    print('CS 11 kW = ', csUtilizationRateL1)
    print('CS 22 kW = ', csUtilizationRateL2M1)
    print('CS 22 kW = ', csUtilizationRateL2M2_3)
    print('CS 50 kW = ', csUtilizationRateL3M4)

    year = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30]
    plt.plot(year, csUtilizationRateL1)
    plt.plot(year, csUtilizationRateL2M1)
    plt.plot(year, csUtilizationRateL2M2_3)
    plt.plot(year, csUtilizationRateL3M4)
    plt.legend(['L1 - 11 kW', 'L2 M1 - 22 kW', 'L2 M2&3 - 22kW', 'L3 M4 - 50 kW'])
    plt.title('Charging Station Utilization Rate')
    plt.xlabel('Year')
    plt.ylabel('%')
    plt.grid()
    plt.show()