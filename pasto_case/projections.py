import random

def ice_to_ev(vehicleSeed, penetrationPercentage):
    evPenetration = []
    for i in range(len(penetrationPercentage)):
        evPenetration.append(vehicleSeed * (i * 2) * penetrationPercentage[i] / 100)
    return evPenetration

def annual_consumption_per_penetration(annualVehicles, annualConsumption):
    annualConsumptionperPenetration = []
    for i in range(len(penetrationPercentage)):
        annualConsumptionperPenetration.append(annualVehicles[i] * annualConsumption)
    return annualConsumptionperPenetration

def charging_time(chargeNeeded, chargingSpeed):
    hourChargingTime = chargeNeeded / chargingSpeed
    return round(hourChargingTime, 2)

def demand(C , P, T, N):
    demand = []
    for i in range(N):
        b = random.random()
        Pref = random.random()
        demand.append(C * b * Pref)
    totalDemand = sum(demand)/ (P * T)
    return totalDemand

if __name__ == '__main__':
    import calculate_metrics as cm

    penetrationPercentage = [0.5, 1, 1.5, 2.0, 3.0, 10, 25, 50, 80, 100] 
    vehicleSeed = 3016 # Number of taxis in Pasto (year = 2024)

    annualVehicles = ice_to_ev(vehicleSeed, penetrationPercentage)
    print('Annual EV = ', annualVehicles)

    emissionClasses = ['Energy/unknown']
    dataframe = cm.generate_data_frame(emissionClasses,"./results/rush/data_emissions_EV.csv")
    annualConsumption = cm.mean_daily('EV', dataframe, 35, 9) * 365
    annualConsumptionTotal = annual_consumption_per_penetration(annualVehicles, annualConsumption)
    print('Annual demand kWh per penetration percentage = ', annualConsumptionTotal)

    print('Hour charging per year L1 = ', charging_time(annualConsumptionTotal[2], 1.9)/24)
    print('Hour charging per year L2 = ', charging_time(annualConsumptionTotal[2], 7)/24)
    print('Hour charging per year L3 = ', charging_time(annualConsumptionTotal[2], 50)/24)

    C = 53.5 * cm.mean_daily('EV', dataframe, 35, 2) / 417.20
    P = 11
    T = 24
    print(demand(C , 11, T, 3016))
    print(demand(C , 22, T, 3016))
    print(demand(C , 50, T, 3016))