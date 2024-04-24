def ice_to_ev(vehicleSeed, penetrationPercentage):
    evPenetration = []
    for i in range(len(penetrationPercentage)):
        evPenetration.append(vehicleSeed * penetrationPercentage[i] / 100)
    return evPenetration

def annual_consumption_per_penetration(annualVehicles, annualConsumption):
    annualConsumptionperPenetration = []
    for i in range(len(penetrationPercentage)):
        annualConsumptionperPenetration.append(annualVehicles[i] * annualConsumption)
    return annualConsumptionperPenetration

def charging_time(chargeNeeded, chargingSpeed):
    hourChargingTime = chargeNeeded / chargingSpeed
    return round(hourChargingTime, 2)

if __name__ == '__main__':
    import pandas as pd
    import calculate_metrics as cm
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    
    import numpy as np
    import json

    penetrationPercentage = [1, 5, 10, 25, 50, 80, 100] 
    vehicleSeed = 3016 # Number of taxis in Pasto

    annualVehicles = ice_to_ev(vehicleSeed, penetrationPercentage)
    print('Annual EV = ', annualVehicles)

    emissionClasses = ['Energy/unknown']
    dataframe = cm.generate_data_frame(emissionClasses,"./results/rush/data_emissions_EV.csv")
    annualConsumption = cm.mean_daily('EV', dataframe, 35, 9) * 365
    annualConsumptionTotal = annual_consumption_per_penetration(annualVehicles, annualConsumption)
    print('Annual demand kWh per penetration percentage = ', annualConsumptionTotal)

    print('Hour charging per year L1 = ', charging_time(annualConsumptionTotal[0], 1)/24)
    print('Hour charging per year L2 = ', charging_time(annualConsumptionTotal[0], 6)/24)
    print('Hour charging per year L3 = ', charging_time(annualConsumptionTotal[0], 50)/24)