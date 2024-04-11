def readJson(file):
    with open(file) as file:
        data = json.load(file)
    return data

def importData():
    dataConfig = readJson('config_files/data_config.json')
    dataCombustion = readJson('config_files/data_combustion.json')
    dataElectric = readJson('config_files/data_electric.json')

    currency = dataConfig['Currency']
    vehicle = dataConfig['Mode of transport']
    year = dataConfig['Years']
    annualDistance = dataConfig['Annual distance']
    dailyDistance = dataConfig['Daily distance']

    vciCost = dataCombustion['Vehicle cost']
    galonCost = dataCombustion['Galon cost']
    fuelRaise = dataCombustion['Fuel raise']
    dailyFuel = dataCombustion['Daily consumption']
    maintenanceCombustionCost = dataCombustion['Maintenance cost']
    soatCost = dataCombustion['SOAT cost']
    otherInsurance = dataCombustion['Other insurances']
    checkCost = dataCombustion['Annual check']
    insuranceRaise = dataCombustion['Insurance raise']
    repairs = dataCombustion['Repairs per year']

    evCost = dataElectric['Vehicle cost']
    kWhCost =  dataElectric['kWh cost']
    kWhRaise =  dataElectric['kWh raise']
    dailykWh =  dataElectric['Daily consumption']
    bateryCapacity =  dataElectric['Batery capacity [kWh]']

    configuration = [currency, vehicle, year, annualDistance, dailyDistance]
    combustion = [vciCost, galonCost, fuelRaise, dailyFuel, maintenanceCombustionCost, soatCost, otherInsurance, checkCost, insuranceRaise, repairs]
    electric = [evCost, kWhCost, kWhRaise, dailykWh, bateryCapacity]

    return configuration, combustion, electric

def total_per_trip(data, route, emission_class):
    '''
    Sum all data for each category data and express in km for distance, kg for emissions, gallon for fuel, kWh for electricity and mean dB for noise.
    '''
    routee = data[data["route"] == route]
    route_class = routee[routee["emission_class"] == emission_class]

    step_route = route_class.iloc[-1, route_class.columns.get_loc("step")]
    distance_route = route_class.iloc[-1, route_class.columns.get_loc("distance")]/1E3 #Distance in km
    
    total_CO2 = route_class["CO2Emission"].sum()/1E6 #Emission in kg
    total_CO = route_class["COEmission"].sum()/1E6 #Emission in kg
    total_HC = route_class["HCEmission"].sum()/1E6 #Emission in kg
    total_PMx = route_class["PMxEmission"].sum()/1E6 #Emission in kg
    total_NOx = route_class["NOxEmission"].sum()/1E6 #Emission in kg 
    total_fuel = route_class["FuelConsumption"].sum()/(1000) #Fuel in liters
    total_energy = route_class["ElectricityConsumption"].sum()/1E3 #Energy in kWh
    total_noise = route_class["NoiseEmission"].sum()/step_route  # Mean noise in dB
    return [route, emission_class, distance_route, total_CO2, total_CO, total_HC, total_PMx, total_NOx, total_fuel, total_energy, total_noise]

def generate_data_frame(emission_classes, file):
    '''
    Organize vehicles data in a data frame
    '''
    data = pd.read_csv(file)
    routes = [1, 2, 3, 4, 5, 6]
    category = ['route','emission_class','distance [km]', 'CO2 [kg]', 'CO [kg]', 'HC [kg]', 'PMx [kg]', 'NOx [kg]', 'fuel [gl]', 'energy [kWh]', 'noise [dB]']
    total_data = []
    for route in routes:
        for emission in emission_classes:
            total_route = total_per_trip(data, route, emission)
            total_data.append(total_route)
    total_data_frame = pd.DataFrame(total_data,columns=category)
    data_frame = total_data_frame.iloc[:, :]#[0,1,3,4,5,6,7,8,9,10]]
    return data_frame

def mean_daily(vehType, dataFrame, numberPaths, category):
    '''
    Calculate the mean daily for all categories in vehicle data.
    vehType: EV (Electric Vehicle) or ICE (Internal Combustion Engine)
    dataFrame: local variable for data frame from vehicle data
    numberPaths: number of paths done daily
    category: number corresponding to list of categories [0:'route', 1:'emission_class',
    2:'distance [km]', 3:'CO2 [kg]', 4:'CO [kg]', 5:'HC [kg]', 6:'PMx [kg]', 7:'NOx [kg]', 
    8:'fuel [gl]', 9:'energy [kWh]', 10:'noise [dB]']
    '''
    np_np = numberPaths * 0.5
    np_p = numberPaths * 0.3
    p_p = numberPaths * 0.2

    if vehType == "ICE":
        route1_tot = list(dataFrame.iloc[0:5, category])
        route2_tot = list(dataFrame.iloc[10:15, category])
        route3_tot = list(dataFrame.iloc[25:30, category])

        route1 = (route1_tot[0]*0.25)+(route1_tot[0]*0.20)+(route1_tot[0]*0.20)+(route1_tot[0]*0.20)+(route1_tot[0]*0.15)
        route2 = (route2_tot[0]*0.25)+(route2_tot[0]*0.20)+(route2_tot[0]*0.20)+(route2_tot[0]*0.20)+(route2_tot[0]*0.15)
        route3 = (route3_tot[0]*0.25)+(route3_tot[0]*0.20)+(route3_tot[0]*0.20)+(route3_tot[0]*0.20)+(route3_tot[0]*0.15)

    elif vehType == "EV":
        route1 = dataFrame.iloc[0, category]
        route2 = dataFrame.iloc[2, category]
        route3 = dataFrame.iloc[5, category]
    else:
        print('Vehicle type is not defined')
    mean = route1*np_np + route2*np_p + route3*p_p
    return round(mean,2)

def consumption_metric(vehType, distance, consumption):
    '''
    Efficiency is quantified in terms of consumption per 100 kilometer traveled 
    vehType: EV (Electric Vehicle) or ICE (Internal Combustion Engine)
    distance: paths in km
    consumption: fuel or kwh consumed in paths
    '''
    if vehType == "ICE":
        # E_100km = (consumption*3.785*8.9*100)/distance
        E_100km = (consumption*8.9*100)/distance
    elif vehType == "EV":
        E_100km = (consumption*100)/distance
    else:
        print('Vehicle type is not defined')
    return round(E_100km, 2)

def autonomy_metric(vehType, E_100km, capacity):
    '''
    Return driving range in km.
    vehType: EV (Electric Vehicle) or ICE (Internal Combustion Engine)
    E_100km: Efficiency is quantified in terms of consumption per 100 kilometer traveled
    capacity: tank (gallons) or battery (kWh) capacity depends from vehType
    '''
    if vehType == "ICE":
        consumption = (E_100km/(100*8.9))
        autonomy = capacity / consumption
    elif vehType == "EV":
        autonomy = capacity * 0.85 / (E_100km/100)
    else:
        print('Vehicle type is not defined')
    return round(autonomy, 2)

def accumulatedCost(configuration, combustion, electric, vehType, E_100km, annualDistance, levelCharge):
    '''
    Initial investment plus the sum of operating costs (insurance, vehicle tax, 
    technical-mechanical inspection, fuel), and maintenance, including annual increases. 
    In the case of EVs, governmental incentives must be included. 
    '''
    if configuration[0] == "USD":
        currency = 1000
    elif configuration[0] == "COP":
        currency = 1000000
    else:
        print("currency parameter is not defined")

    ipc = 0.0457 # Average value of IPC in Colombia
    otherInsurance = combustion[6]
    insuranceCostRaise = combustion[8] / 100 
    totalCost = []
    totalCost = [*range(0, configuration[2], 1)]
    annualCost = []
    annualCost = [*range(0, configuration[2], 1)]
    if levelCharge == 'Level1' or levelCharge == 'Level2':
        batteryReplacementYear = round(8 / (150000 / annualDistance))
    elif levelCharge == 'Level3':
        batteryReplacementYear = round(8 * 0.9 / (150000 / annualDistance))
    else:
        print('Level Charge is not defined')
    print(levelCharge, batteryReplacementYear)

    if vehType == 'ICE':
        powerConsumption = (E_100km / (100 * 8.9)) * annualDistance
        combustion[1] = combustion[1] / 3.785
        totalCost[0] = combustion[0] 
        annualCost[0] = combustion[0] 
        taxCost = combustion[0] * 0.01 # Based on "Ley 1964 de 2019, Congreso de Colombia"
        annualPowerCost = powerConsumption * combustion[1] 
        annualPowerCostRaise  = combustion[2] / 100
        maintenanceCost = combustion[4]
        soatCost = combustion[5]
        otherInsurance = combustion[6] # Contractual insuarence and all damages insurance
        checkCost = combustion[7]
    elif vehType == 'EV':
        powerConsumption = (E_100km/100)*annualDistance
        totalCost[0] = electric[0]
        annualCost[0] = electric[0]
        taxCost = combustion[0] * 0.01 * 0.4 # Based on "Ley 1964 de 2019, Congreso de Colombia"
        annualPowerCost = powerConsumption * electric[1]
        annualPowerCostRaise  = electric[2] / 100
        maintenanceCost = combustion[4] * 0.4
        soatCost = combustion[5] * 0.9
        checkCost = combustion[7] * 0.7 
        bateryCost = electric[4] * 156 * 4000  # Batery cost in COP
        batteryYearlyRaise = -0.0967 # According to technology reduction cost trend
    else:
        print('vehType parameter is not defined ')

    for i in range(1,configuration[2],1):
        annualCost[i] = annualPowerCost + maintenanceCost + soatCost + otherInsurance + taxCost
        totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + taxCost
        if i >= 2:
        #Annual variance of parameters costs
            taxCost = taxCost * (1 + insuranceCostRaise)
            annualPowerCost = annualPowerCost * (1 + annualPowerCostRaise)
            maintenanceCost = maintenanceCost * (1 + ipc)
            soatCost = soatCost * (1 + insuranceCostRaise)
            otherInsurance = otherInsurance * (1 + insuranceCostRaise)
            checkCost = checkCost * (1 + insuranceCostRaise)
            annualCost[i] = annualPowerCost + maintenanceCost + soatCost + otherInsurance + \
                taxCost + checkCost
            totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + \
                taxCost + checkCost
            if vehType == 'EV':
                bateryCost = bateryCost * (1 + batteryYearlyRaise)
                if i==batteryReplacementYear or i==2*batteryReplacementYear or i==3*batteryReplacementYear or i==4*batteryReplacementYear or i==5*batteryReplacementYear or i==6*batteryReplacementYear:
                    annualCost[i] = annualPowerCost + maintenanceCost + soatCost + otherInsurance \
                        + checkCost + taxCost + bateryCost
                    totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance \
                        + checkCost + taxCost + bateryCost

    for i in range(len(totalCost)):
        totalCost[i] = round(totalCost[i] / currency , 2)
        annualCost[i] = round(annualCost[i] / currency , 2)
        
    return totalCost, annualCost

def ICR_metric(powerCost, consumption, distance):
    '''
    Relates the duration of the trip to the fuel or electricity expenditure during that trip. 
    powerCost: cost per gallon of fuel or cost per kWh.
    consumption: fuel consumption in gallons or electricity consumption in kWh.
    distance: the distance traveled in kilometers.
    '''
    icr = powerCost * consumption  / distance
    return round(icr,2)

def emission_metric(co2Emission, consumption, distance, vehType):
    '''
    Expressed in kilograms of CO2 per kilometer for both ICEVs and EVs. 
    '''
    if vehType == 'ICE':
        emissionPerKilometer = (co2Emission * 1000) / distance
    elif vehType == 'EV':
        emissionPerKilometer = 164.38 * consumption / distance
    else:
        print('Vehicle type is not defined')
    return round(emissionPerKilometer / 1000, 2)

def socialCost_metric(co2Emission):
    '''
    Refers to the economic and environmental impact attributed to the 
    release of CO2 and other greenhouse gasses into the atmosphere. 
    co2Emission: CO2 per trip in kg. 
    '''
    socialEmission = co2Emission * 1000 * 199 / 1000000
    return round(socialEmission, 2)

def chargingTime_metric(chargeNeeded, chargingSpeed, distance, capacity, E100km):
    consumption = E100km / 100
    annualDistance = distance * 365
    hourChargingTime = chargeNeeded / chargingSpeed
    numberCharges = (consumption * annualDistance) / capacity
    availability_factor = (365 - (hourChargingTime * numberCharges / 24))*100/365
    return round(availability_factor, 2)

def production_emission(vehType, mass, capacity):
    e_body = 4.56
    e_bat = 83.5
    if vehType == 'ICE':
        productionEmission = mass * e_body
    elif vehType == 'EV':
        productionEmission = (mass * e_body) + (capacity * e_bat)
    else:
        print('Vehicle type is not defined')
    return round(productionEmission, 2)

def utilization_emission(emission, annualDistance):
    
    # if vehType == 'ICE':
    #     E100km = E100km / 8.9 
    #     e_wtw = 2.83
    # elif vehType == 'EV': 
    #     if elecType == 'conventional':
    #         e_wtw = 0.401
    #     elif elecType == 'renewable':
    #         e_wtw = 0.036
    #     else:
    #         print('Electricity type is not defined')
    # else:
    #     print('Vehicle type is not defined')
    # utilizationEmission = E100km * e_wtw * annualDistance / 100
    utilizationEmission = emission * annualDistance
    return round(utilizationEmission, 2)

def recycling_emission(vehType, mass, capacity):
    e_body = -2.93
    e_bat = -48.4
    if vehType == 'ICE':
        productionEmission = mass * e_body
    elif vehType == 'EV':
        productionEmission = (mass * e_body) + (capacity * e_bat)
    else:
        print('Vehicle type is not defined')
    return round(productionEmission, 2)

def lifecycle_emissions(vehType, mass, capacity, emission, annualDistance):
    production = production_emission(vehType, mass, capacity)
    utilization = utilization_emission(emission, annualDistance)
    recycling = recycling_emission(vehType, mass, capacity)
    lifecycleTotalEmissions = production + utilization + recycling
    return round(lifecycleTotalEmissions, 2)

def ahp_attributes(ahp_df):
    sum_array = np.array(ahp_df.sum(numeric_only=True))
    cell_by_sum = ahp_df.div(sum_array,axis=1)
    priority_df = pd.DataFrame(cell_by_sum.mean(axis=1),
                               index=ahp_df.index,columns=['priority index'])
    priority_df = priority_df.transpose()
    return priority_df

def consistency_ratio(priority_index,ahp_df):
    random_matrix = {1:0,2:0,3:0.58,4:0.9,5:1.12,6:1.24,7:1.32,
                     8:1.14,9:1.45,10:1.49,11:1.51,12:1.48,13:1.56,
                     14:1.57,15:1.59,16:1.605,17:1.61,18:1.615,19:1.62,20:1.625}
    consistency_df = ahp_df.multiply(np.array(priority_index.loc['priority index']),axis=1)
    consistency_df['sum_of_col'] = consistency_df.sum(axis=1)
    lambda_max_df = consistency_df['sum_of_col'].div(np.array(priority_index.transpose()
                                                              ['priority index']),axis=0)
    lambda_max = lambda_max_df.mean()
    consistency_index = round((lambda_max-len(ahp_df.index))/(len(ahp_df.index)-1),3)
    # print(f'The Consistency Index is: {consistency_index}')
    consistency_ratio = round(consistency_index/random_matrix[len(ahp_df.index)],3)
    # print(f'The Consistency Ratio is: {consistency_ratio}')
    if consistency_ratio<0.1:
        print('The model is consistent')
    else:
        print('The model is not consistent')

def supplier_priority_index(suppl_attr_df,num_attr,attr_name):
    data_dict = {}
    data_dict[f"ahp_df_suppl_{attr_name}"] = suppl_attr_df.loc[attr_name]
    data_dict[f"sum_array_suppl_{attr_name}"] = np.array(data_dict[
        f"ahp_df_suppl_{attr_name}"].sum(numeric_only=True))
    data_dict[f"norm_mat_suppl_{attr_name}"] = data_dict[
        f"ahp_df_suppl_{attr_name}"].div(data_dict[f"sum_array_suppl_{attr_name}"],axis=1)
    priority_df = pd.DataFrame(data_dict[
        f"norm_mat_suppl_{attr_name}"].mean(axis=1),
                               index=suppl_attr_df.loc[attr_name].index,columns=[attr_name])
    return priority_df

def social_metric(availability, autonomy, cost, incentives, emissions):
    ahp_df = pd.read_csv('pair_wise_comparison.csv')
    ahp_df.set_index('Unnamed: 0', inplace=True)

    comparisonMatrix = {}
    comparisonMatrix['Availability Factor'] = [1, 4, 5, 6, 7]
    comparisonMatrix['Driving Range'] = [1, 4, 5, 6, 7]

    priority_index_attr = ahp_attributes(ahp_df)
    consistency_ratio(priority_index_attr,ahp_df)

    ahp_df_1 = pd.read_csv('alternative_attribute.csv',header=[0], index_col=[0,1]) 

    # alternativesMatrix = [[],
    #                       [],
    #                       [],
    #                       [],
    #                       []]

    suppl_AF_df = supplier_priority_index(ahp_df_1,3,'Availability Factor')
    suppl_DR_df = supplier_priority_index(ahp_df_1,3,'Driving Range')
    suppl_AC_df = supplier_priority_index(ahp_df_1,3,'Accumulated Cost')
    suppl_I_df = supplier_priority_index(ahp_df_1,5,'Incentives')
    suppl_E_df = supplier_priority_index(ahp_df_1,5,'Emissions')

    suppl_df = pd.concat([suppl_AF_df,suppl_DR_df,suppl_AC_df, suppl_I_df, suppl_E_df],axis=1)
    suppl_norm_df = suppl_df.multiply(np.array(priority_index_attr.loc['priority index']),axis=1)
    suppl_norm_df['Sum'] = suppl_norm_df.sum(axis=1)
    print(round(suppl_norm_df,2))



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    import pandas as pd
    import numpy as np
    import json

    # Load configuration data 
    configuration, combustion, electric = importData()
    #Generate data frame for EV
    emission_classes_EV = ['Energy/unknown']
    rush_df_EV = generate_data_frame(emission_classes_EV,"./results/rush/data_emissions_EV.csv")
    offPeak_df_EV = generate_data_frame(emission_classes_EV,"./results/off_peak/data_emissions_EV.csv")
    #Generate data frame for ICE
    emission_classes_ICE = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6d']
    rush_df_ICE = generate_data_frame(emission_classes_ICE,"./results/rush/data_emissions_ICE.csv")
    offPeak_df_ICE = generate_data_frame(emission_classes_ICE,"./results/off_peak/data_emissions_ICE.csv")

    #category=[0:'route', 1:'emission_class', 2:'distance [km]', 3:'CO2 [kg]', 4:'CO [kg]', 5:'HC [kg]', 6:'PMx [kg]', 7:'NOx [kg]', 8:'fuel [gl]', 9:'energy [kWh]', 10:'noise [dB]']
    annualDistance = mean_daily('ICE', rush_df_ICE, 35, 2) * 365

    #Calculate the E100k metric - Rush hour
    E100km_ICE = consumption_metric('ICE', mean_daily('ICE', rush_df_ICE, 35, 2), mean_daily('ICE', rush_df_ICE, 35, 8))
    E100km_EV = consumption_metric('EV', mean_daily('EV', rush_df_EV, 35, 2), mean_daily('EV', rush_df_EV, 35, 9))
    print('E100km_ICE [kWh/100km] = ', E100km_ICE, ' - E100km_EV [kWh/100km] = ', E100km_EV)

    #Calculate the Driving Range metric -Rush hour
    autonomy_ICE = autonomy_metric('ICE', E100km_ICE, 9.35) #View KIA grand EKO Taxi datasheet (tank capacity)
    autonomy_EV = autonomy_metric('EV', E100km_EV, 53.5) #View BYD D1 datasheet (battery capacity)
    print('Autonomy ICE [km]= ', autonomy_ICE, ' - Autonomy EV [km]= ', autonomy_EV)

    #Calculate the ICR metric - Rush hour
    icr_ICE = ICR_metric(combustion[1]/3.785 , mean_daily('ICE', rush_df_ICE, 35, 8) , mean_daily('ICE', rush_df_ICE, 35, 2))
    icr_EV = ICR_metric(electric[1] , mean_daily('EV', rush_df_EV, 35, 9) , mean_daily('EV', rush_df_EV, 35, 2))
    print('ICR ICE = ', icr_ICE, '- ICR EV = ', icr_EV)

    #Calculate the Accumulated cost and Annual cost metric - Rush hour
    accumulatedCost_ICE, annualCost_ICE= accumulatedCost(configuration, combustion, electric, 'ICE', E100km_ICE, annualDistance, 'Level1')
    accumulatedCost_EV1, annualCost_EV1 = accumulatedCost(configuration, combustion, electric, 'EV', E100km_EV, annualDistance, 'Level1')
    accumulatedCost_EV3, annualCost_EV3 = accumulatedCost(configuration, combustion, electric, 'EV', E100km_EV, annualDistance, 'Level3')
    print('Accum ICE = ', accumulatedCost_ICE,'\nAnnua ICE = ', annualCost_ICE,
          '\nAccum EV L1 = ', accumulatedCost_EV1,'\nAnnua EV1 = ', annualCost_EV1,
          '\nAccum EV L3 = ', accumulatedCost_EV3,'\nAnnua EV3 = ', annualCost_EV3)

    #Calculate the emission per kilometer metric - Rush hour
    emission_ICE = emission_metric(mean_daily('ICE', rush_df_ICE, 35, 3), mean_daily('ICE', rush_df_ICE, 35, 8), mean_daily('ICE', rush_df_ICE, 35, 2), 'ICE')
    emission_EV = emission_metric(mean_daily('EV', rush_df_EV, 35, 3), mean_daily('EV', rush_df_EV, 35, 9), mean_daily('EV', rush_df_EV, 35, 2), 'EV')
    print('CO2/km ICE = ', emission_ICE, ' - CO2/km EV = ', emission_EV)

    #Calculate the Social cost metric - Rush hour
    socialCost_ICE = socialCost_metric(mean_daily('ICE', rush_df_ICE, 35, 3))
    socialCost_EV = socialCost_metric(mean_daily('EV', rush_df_EV, 35, 3))
    print('Social Cost Emission ICE = ', socialCost_ICE, ' - Social Cost Emission EV = ', socialCost_EV)

    #Calculate the availability factor metric - Rush hour
    availabilityFactor_ICE = chargingTime_metric(9.25, 951.02, mean_daily('ICE', rush_df_ICE, 35, 2), 9.25, E100km_ICE)
    availabilityFactor_EV1 = chargingTime_metric(53.5, 1, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV)
    availabilityFactor_EV2 = chargingTime_metric(53.5, 6, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV)
    availabilityFactor_EV3 = chargingTime_metric(53.5, 50, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV)
    print('Availability factor ICE = ', availabilityFactor_ICE, ' - Availability factor EV1 = ', availabilityFactor_EV1, ' - Availability factor EV2 = ', 
          availabilityFactor_EV2, ' - Availability factor EV3 = ', availabilityFactor_EV3)

    #Calculate the LifeCycle Emission metric - Rush hour
    utilization_ICE = utilization_emission(emission_ICE, annualDistance)
    utilization_EV = utilization_emission(emission_EV, annualDistance)

    lifecycleEmissions_ICE = lifecycle_emissions('ICE', 894, 0, emission_ICE, annualDistance)
    lifecycleEmissions_EV = lifecycle_emissions('EV', 1640, 53.5, emission_EV, annualDistance)
    print('LC Emissions ICE = ', lifecycleEmissions_ICE, ' - LC Emissions EV = ', lifecycleEmissions_EV)

    #Calculate the Social metric - Rush hour
    availability = [availabilityFactor_ICE, availabilityFactor_EV1, availabilityFactor_EV2, availabilityFactor_EV3]
    autonomy = [autonomy_ICE, autonomy_EV]
    cost = [accumulatedCost_ICE, accumulatedCost_EV1, accumulatedCost_EV3]
    incentives = [0 , 9]
    emissions = [lifecycleEmissions_ICE, lifecycleEmissions_EV]
    social_metric(availability, autonomy, cost, incentives, emissions)

    #Plot Accumulated and Annual Cost
    year = list(range(20))
    plt.plot(year, accumulatedCost_ICE, "#A0A0A0", label="ICE")
    plt.plot(year, accumulatedCost_EV1, "#33FF33", label="EV")
    plt.xlabel("Year")
    plt.ylabel("Accumulated Cost")
    plt.title("Accumulated Cost ICE and EV")
    plt.grid()
    plt.legend()
    plt.show()

    years = [*range(0, 20, 1)]
    Y = [str(x) for x in years]
    conventional = annualCost_ICE
    electric = annualCost_EV1
    df = pd.DataFrame({'ICE': conventional, 'EV': electric}, index=Y)
    df.plot( kind = 'bar', rot=0, color=['#A0A0A0', '#33FF33'])
    plt.show()