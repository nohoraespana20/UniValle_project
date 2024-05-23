import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def readJson(file):
    with open(file) as file:
        data = json.load(file)
    return data

def importData():
    dataConfig = readJson('config_files/data_config.json')
    dataCombustion = readJson('config_files/data_combustion.json')
    dataGas = readJson('config_files/data_gas.json')
    dataElectric = readJson('config_files/data_electric.json')
    dataHybrid = readJson('config_files/data_hybrid.json')

    currency = dataConfig['Currency']
    vehicle = dataConfig['Mode of transport']
    year = dataConfig['Years']
    annualDistance = dataConfig['Annual distance']
    dailyDistance = dataConfig['Daily distance']
    configuration = [currency, vehicle, year, annualDistance, dailyDistance]

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
    combustion = [vciCost, galonCost, fuelRaise, dailyFuel, maintenanceCombustionCost, soatCost, otherInsurance, checkCost, insuranceRaise, repairs]

    hybridCost = dataHybrid['Vehicle cost']
    galonCost = dataHybrid['Galon cost']
    fuelRaise = dataHybrid['Fuel raise']
    maintenanceCombustionCost = dataCombustion['Maintenance cost']
    kWhCost =  dataHybrid['kWh cost']
    kWhRaise =  dataHybrid['kWh raise']
    bateryCapacity = dataHybrid['Batery capacity [kWh]']
    hybrid = [hybridCost, galonCost, fuelRaise, maintenanceCombustionCost, kWhCost, kWhRaise, bateryCapacity]

    gasCost = dataGas['Vehicle cost']
    m3Cost = dataGas['m3 cost']
    m3Raise = dataGas['m3 raise']
    dailyFuel = dataGas['Daily consumption']
    gas = [gasCost, m3Cost, m3Raise, dailyFuel]

    evCost = dataElectric['Vehicle cost']
    kWhCost =  dataElectric['kWh cost']
    kWhRaise =  dataElectric['kWh raise']
    dailykWh =  dataElectric['Daily consumption']
    bateryCapacity =  dataElectric['Batery capacity [kWh]']
    electric = [evCost, kWhCost, kWhRaise, dailykWh, bateryCapacity]

    return configuration, combustion, gas, electric, hybrid

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
    total_fuel = route_class["FuelConsumption"].sum()/1E3 #Fuel in liters
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

    elif vehType == "EV" or vehType == 'CNG':
        route1 = dataFrame.iloc[0, category]
        route2 = dataFrame.iloc[2, category]
        route3 = dataFrame.iloc[5, category]
        if vehType == 'CNG':
            print('CNG ', route1, category)
        else:
            print('EV ', route1, category)
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
        E_100km = (consumption*9.67*100)/distance
    elif vehType == 'CNG':
        E_100km = (consumption*10.70*100)/distance
    elif vehType == 'Diesel':
        E_100km = (consumption*10.69*100)/distance
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
        consumption = E_100km/(100*9.67)
        autonomy = capacity * 3.785 / consumption
    elif vehType == 'CNG':
        consumption = E_100km/(100*10.70)
        autonomy = capacity * 3.785 / consumption
    elif vehType == "EV":
        autonomy = capacity * 0.85 / (E_100km/100)
    elif vehType == "PHEV":
        battCapacity = 8
        EkWh_100km = 16.85
        autonomy = (capacity * 3.785 / (E_100km/(100*9.67))) + (battCapacity * 0.85 / (EkWh_100km/100))
    else:
        print('Vehicle type is not defined')
    return round(autonomy, 2)

def accumulatedCost(configuration, combustion, electric, gas, hybrid, vehType, E_100km, annualDistance, levelCharge):
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
        if vehType == 'PHEV':
            batteryReplacementYear = 8
        else:
            batteryReplacementYear = round(8 * annualDistance / 160000)
    elif levelCharge == 'Level3':
        if vehType == 'PHEV':
            batteryReplacementYear = round(8 * 0.9)
        else:
            batteryReplacementYear = round(8 * 0.9 * annualDistance / 160000)
    else:
        print('Level Charge is not defined')

    if vehType == 'ICE':
        powerConsumption = (E_100km / (100 * 9.67)) * annualDistance
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
    elif vehType == 'CNG':
        powerConsumption = (E_100km / (100 * 10.70)) * annualDistance
        gas[1] = gas[1] / 1000
        totalCost[0] = gas[0]
        annualCost[0] = gas[0] 
        taxCost = combustion[0] * 0.01 * 0.4 # Based on "LEY 2128 DE 2021, Congreso de Colombia"
        annualPowerCost = powerConsumption * gas[1] 
        annualPowerCostRaise  = gas[2] / 100
        maintenanceCost = combustion[4]
        soatCost = combustion[5] * 0.9 # Based on "LEY 2128 DE 2021, Congreso de Colombia"
        otherInsurance = combustion[6] * 0.9 # Contractual insuarence and all damages insurance # Based on "LEY 2128 DE 2021, Congreso de Colombia"
        checkCost = combustion[7] * 0.7 
    elif vehType == 'PHEV':
        EkWh_100km = 16.85
        powerConsumptionICE = (E_100km / (100 * 9.67)) * annualDistance * 0.7
        powerConsumptionEV = (EkWh_100km/100) * annualDistance * 0.3
        hybrid_1 = hybrid[1] / 3.785
        totalCost[0] = hybrid[0]
        annualCost[0] = hybrid[0]
        taxCost = hybrid[0] * 0.01 # Based on "Ley 1964 de 2019, Congreso de Colombia"
        annualPowerCost = (powerConsumptionICE * hybrid_1) + (powerConsumptionEV * hybrid[4])
        annualPowerCostRaise  = hybrid[2] / 100
        maintenanceCost = combustion[4]
        soatCost = combustion[5] *0.9
        otherInsurance = combustion[6] *0.9 # Contractual insuarence and all damages insurance
        checkCost = combustion[7] *0.7
        batteryCost = hybrid[6] * 156 * 4000  # Batery cost in COP
        batteryYearlyRaise = -0.0967 # According to technology reduction cost trend
    elif vehType == 'EV':
        powerConsumption = (E_100km/100) * annualDistance
        totalCost[0] = electric[0]
        annualCost[0] = electric[0]
        taxCost = combustion[0] * 0.01 * 0.4 # Based on "Ley 1964 de 2019, Congreso de Colombia"
        annualPowerCost = powerConsumption * electric[1]
        annualPowerCostRaise  = electric[2] / 100
        maintenanceCost = combustion[4] * 0.4
        soatCost = combustion[5] * 0.9
        otherInsurance = combustion[6] * 0.9 # Contractual insuarence and all damages insurance
        checkCost = combustion[7] * 0.7 
        batteryCost = electric[4] * 156 * 4000  # Batery cost in COP
        batteryYearlyRaise = -0.0967 # According to technology reduction cost trend
    else:
        print('vehType parameter is not defined ')
    del hybrid
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
            if vehType == 'EV' or vehType == 'PHEV':
                batteryCost = batteryCost * (1 + batteryYearlyRaise)
                if i==batteryReplacementYear or i==2*batteryReplacementYear or i==3*batteryReplacementYear or i==4*batteryReplacementYear or i==5*batteryReplacementYear or i==6*batteryReplacementYear:
                    annualCost[i] = annualPowerCost + maintenanceCost + soatCost + otherInsurance \
                        + checkCost + taxCost + batteryCost
                    totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance \
                        + checkCost + taxCost + batteryCost

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
    if vehType == 'ICE' or vehType == 'CNG':
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
    if vehType == 'ICE' or vehType == 'CNG':
        productionEmission = mass * e_body
    elif vehType == 'EV' or vehType == 'PHEV':
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
    if vehType == 'ICE' or vehType == 'CNG':
        productionEmission = mass * e_body
    elif vehType == 'EV' or vehType == 'PHEV':
        productionEmission = (mass * e_body) + (capacity * e_bat)
    else:
        print('Vehicle type is not defined')
    return round(productionEmission, 2)

def lifecycle_emissions(vehType, mass, capacity, emission, aDistance):
    if vehType == 'PHEV':
        annualDistance = aDistance * 0.7
    else:
        annualDistance = aDistance
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
        print('The AHP model is consistent')
    else:
        print('The AHP model is not consistent')

def priority_index(suppl_attr_df,attr_name):
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

def generate_alternative_matrix(availability, autonomy, cost, incentives, emissions):
    df = pd.DataFrame({
    "Criteria":['Availability Factor', 'Availability Factor', 'Availability Factor', 'Availability Factor', 'Availability Factor', 'Availability Factor', 'Availability Factor', 'Availability Factor', 
                'Driving Range', 'Driving Range', 'Driving Range', 'Driving Range', 'Driving Range', 'Driving Range', 'Driving Range', 'Driving Range', 
                'Accumulated Cost', 'Accumulated Cost', 'Accumulated Cost', 'Accumulated Cost', 'Accumulated Cost', 'Accumulated Cost', 'Accumulated Cost', 'Accumulated Cost', 
                'Incentives', 'Incentives', 'Incentives', 'Incentives', 'Incentives', 'Incentives', 'Incentives', 'Incentives', 
                'Emissions', 'Emissions', 'Emissions', 'Emissions', 'Emissions', 'Emissions', 'Emissions', 'Emissions'],
    "Alternative": ['ICE', 'EVL1', 'EVL2', 'EVL3', 'CNG', 'PHEVL1', 'PHEVL2', 'PHEVL3', 'ICE', 'EVL1', 'EVL2', 'EVL3', 'CNG', 'PHEVL1', 'PHEVL2', 'PHEVL3',
                    'ICE', 'EVL1', 'EVL2', 'EVL3', 'CNG', 'PHEVL1', 'PHEVL2', 'PHEVL3', 'ICE', 'EVL1', 'EVL2', 'EVL3', 'CNG', 'PHEVL1', 'PHEVL2', 'PHEVL3', 
                    'ICE', 'EVL1', 'EVL2', 'EVL3', 'CNG', 'PHEVL1', 'PHEVL2', 'PHEVL3']})
    index = pd.MultiIndex.from_frame(df)  
    data = []
    for i in range(len(availability)):
        availabilityFactor, drivingRangeFactor, costFactor, incentivesFactor, emissionsFactor = [], [], [], [], []
        for j in range(len(availability)):
            availabilityFactor.append(availability[j] / availability[i])
            drivingRangeFactor.append(autonomy[j] / autonomy[i])
            costFactor.append(cost[i] / cost[j])
            incentivesFactor.append(incentives[j] / incentives[i])
            emissionsFactor.append(emissions[i] / emissions[j])
        data.append(availabilityFactor + drivingRangeFactor + costFactor + incentivesFactor + emissionsFactor)
    data = np.array(data).T.tolist()
    ahp_df = pd.DataFrame(data, index=index, columns=['ICE','EVL1', 'EVL2', 'EVL3', 'CNG','PHEVL1', 'PHEVL2', 'PHEVL3'])
    print(ahp_df.round(3))
    scaled_df = MinMaxScaler().fit_transform(ahp_df)
    scaled_df = pd.DataFrame(scaled_df, index=index, columns=['ICE','EVL1', 'EVL2', 'EVL3', 'CNG','PHEVL1', 'PHEVL2', 'PHEVL3'])
    print(scaled_df.round(3))
    return scaled_df

def social_metric(altenativeMatrix):
    comparisonMatrix = {}
    comparisonMatrix['Availability Factor'] =   [1, 1/4, 1/5, 1/6, 1/7]
    comparisonMatrix['Driving Range'] =         [4, 1,   1/2, 1/3, 1/4]
    comparisonMatrix['Accumulated Cost'] =      [5, 2,   1,   1/2, 1/3]
    comparisonMatrix['Incentives'] =            [6, 3,   2,   1,   1/2]
    comparisonMatrix['Emissions'] =             [7, 4,   3,   2,   1]

    ahp_df = pd.DataFrame(comparisonMatrix, index=['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', 'Emissions'])
    priority_index_attr = ahp_attributes(ahp_df)
    consistency_ratio(priority_index_attr,ahp_df)

    ahp_df_1 = altenativeMatrix
    
    AF_df = priority_index(ahp_df_1,'Availability Factor')
    DR_df = priority_index(ahp_df_1,'Driving Range')
    AC_df = priority_index(ahp_df_1,'Accumulated Cost')
    I_df = priority_index(ahp_df_1,'Incentives')
    E_df = priority_index(ahp_df_1,'Emissions')

    alternative_df = pd.concat([AF_df,DR_df,AC_df, I_df, E_df],axis=1)
    norm_df = alternative_df.multiply(np.array(priority_index_attr.loc['priority index']),axis=1) 
    norm_df['Sum'] = norm_df.sum(axis=1)
    print(round(norm_df,3))
    print('Max Score = ', round(norm_df['Sum'].max(),3), 'Best alternative = ', norm_df['Sum'].idxmax())
    return norm_df

def plot_cost():
    #Plot Accumulated and Annual Cost
    year = list(range(20))
    plt.plot(year, accumulatedCost_ICE, "#444444", label="ICE")
    plt.plot(year, accumulatedCost_EV1, "#adff2f", label="EV-L1&2")
    plt.plot(year, accumulatedCost_EV3, "#38761d", label="EV_L3")
    plt.plot(year, accumulatedCost_PHEV1, "#512647", label="EV-L1&2")
    plt.plot(year, accumulatedCost_PHEV3, "#ddcd82", label="EV_L3")
    plt.plot(year, accumulatedCost_CNG, "#89cff0", label="CNG")
    plt.xlabel("Year")
    plt.ylabel("Accumulated Cost")
    plt.title("Accumulated Cost ICE, EV, PHEV and CNG")
    plt.grid()
    plt.legend()
    plt.show()

    years = [*range(0, 20, 1)]
    Y = [str(x) for x in years]
    conventional = annualCost_ICE
    electric1 = annualCost_EV1
    electric3 = annualCost_EV3
    gas = annualCost_CNG
    phev1 = annualCost_PHEV1
    phev3 = annualCost_PHEV3
    df = pd.DataFrame({'ICE': conventional, 'EV-L2': electric1, 'EV-L3': electric3, 'PHEV-L2': phev1, 'PHEV-L3': phev3,'CNG': gas}, index=Y)
    df.plot( kind = 'bar', rot=0, color=['#444444', '#adff2f', "#38761d", "#512647", "#ddcd82", "#89cff0"])
    plt.show()

def save_metrics_data(consumption, autonomy, cpt, cost, eco, emissions, socialCost, social, availability):
    socialSum = social['Sum']
    df = pd.DataFrame({
    "Criteria":['Technical', 'Technical', 'Economic', 'Economic', 'Environmental', 'Environmental', 'Social', 'Social', 'Social'],
    "Metrics": ['E100km', 'Driving Range', 'Cost per trip', 'Accumulated cost', 
                'Emissions per kilometer', 'Lifecycle emissions', 
                'Social cost', 'Willingness-to-pay', 'Availability factor']})
    index = pd.MultiIndex.from_frame(df)  
    data =  [[consumption[0], autonomy[0], cpt[0], cost[0], eco[0], emissions[0], socialCost[0], socialSum[0], availability[0]], 
             [consumption[1], autonomy[1], cpt[1], cost[1], eco[1], emissions[1], socialCost[1], socialSum[1], availability[1]],
             [consumption[1], autonomy[2], cpt[1], cost[2], eco[1], emissions[1], socialCost[1], socialSum[2], availability[2]],
             [consumption[1], autonomy[3], cpt[1], cost[3], eco[1], emissions[1], socialCost[1], socialSum[3], availability[3]],
             [consumption[2], autonomy[4], cpt[2], cost[4], eco[2], emissions[2], socialCost[2], socialSum[4], availability[4]],
             [consumption[3], autonomy[5], cpt[1], cost[5], eco[3], emissions[3], socialCost[3], socialSum[5], availability[5]],
             [consumption[3], autonomy[6], cpt[1], cost[6], eco[3], emissions[3], socialCost[3], socialSum[6], availability[6]],
             [consumption[3], autonomy[7], cpt[2], cost[7], eco[3], emissions[3], socialCost[3], socialSum[7], availability[7]]]
    data = np.array(data).T.tolist()
    metrics_df = pd.DataFrame(data, index=index, columns=['ICE','EVL1', 'EVL2', 'EVL3', 'CNG', 'PHEVL1', 'PHEVL2', 'PHEVL3'])

    metrics_df.to_csv('./results/metrics_data.csv')


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    import pandas as pd
    import numpy as np
    import json

    # Load configuration data 
    configuration, combustion, gas, electric, hybrid = importData()
    trips = 35

    #Generate data frame for EV
    emission_classes_EV = ['Energy/unknown']#['HBEFA4/PC_BEV']
    rush_df_EV = generate_data_frame(emission_classes_EV,"./results/rush/data_emissions_EV.csv")

    #Generate data frame for ICE
    emission_classes_ICE = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6d']
    rush_df_ICE = generate_data_frame(emission_classes_ICE,"./results/rush/data_emissions_ICE.csv")

    #Generate data frame for CNG
    emission_classes_CNG = ['HBEFA4/PC_CNG_petrol_Euro-6_(CNG)']
    rush_df_CNG = generate_data_frame(emission_classes_CNG,"./results/rush/data_emissions_CNG.csv")
    print('Emissions CNG')
    print(rush_df_CNG)

    #category=[0:'route', 1:'emission_class', 2:'distance [km]', 3:'CO2 [kg]', 4:'CO [kg]', 5:'HC [kg]', 6:'PMx [kg]', 7:'NOx [kg]', 8:'fuel [gl]', 9:'energy [kWh]', 10:'noise [dB]']
    
    dailyDistance = mean_daily('ICE', rush_df_ICE, trips, 2)
    annualDistance = dailyDistance * 365

    #Calculate the E100k metric - Rush hour
    E100km_ICE = consumption_metric('ICE', dailyDistance, mean_daily('ICE', rush_df_ICE, trips, 8))
    E100km_EV = consumption_metric('EV', dailyDistance, mean_daily('EV', rush_df_EV, trips, 9))
    E100km_CNG = consumption_metric('CNG', dailyDistance, mean_daily('CNG', rush_df_CNG, trips, 8))
    E100km_PHEV = (E100km_ICE * 0.7) + (E100km_EV * 0.3)
    
    #Calculate the Driving Range metric -Rush hour
    autonomy_ICE = autonomy_metric('ICE', E100km_ICE, 9.25) #View KIA grand EKO Taxi datasheet (tank capacity)
    autonomy_EV = autonomy_metric('EV', E100km_EV, 53.5) #View BYD D1 datasheet (battery capacity)
    autonomy_CNG = autonomy_metric('CNG', E100km_CNG, 5.28) #Without datasheet (tank capacity in gallons)
    autonomy_PHEV = (autonomy_ICE * 0.7 + autonomy_EV * 0.3) 
    
    #Calculate the ICR metric - Rush hour
    icr_ICE = ICR_metric(combustion[1]/3.785 , mean_daily('ICE', rush_df_ICE, trips, 8) , dailyDistance)
    icr_EV = ICR_metric(electric[1] , mean_daily('EV', rush_df_EV, trips, 9) , dailyDistance)
    icr_CNG = ICR_metric(gas[1] , mean_daily('CNG', rush_df_CNG, trips, 9) , dailyDistance)
    icr_PHEV = (icr_ICE * 0.7) + (icr_EV * 0.3)
    
    #Calculate the Accumulated cost and Annual cost metric - Rush hour
    accumulatedCost_ICE, annualCost_ICE= accumulatedCost(configuration, combustion, electric, gas, hybrid, 'ICE', E100km_ICE, annualDistance, 'Level1')
    accumulatedCost_EV1, annualCost_EV1 = accumulatedCost(configuration, combustion, electric, gas, hybrid,'EV', E100km_EV, annualDistance, 'Level1')
    accumulatedCost_EV3, annualCost_EV3 = accumulatedCost(configuration, combustion, electric, gas, hybrid,'EV', E100km_EV, annualDistance, 'Level3')
    accumulatedCost_CNG, annualCost_CNG = accumulatedCost(configuration, combustion, electric, gas, hybrid,'CNG', E100km_CNG, annualDistance, 'Level1')
    accumulatedCost_PHEV1, annualCost_PHEV1 = accumulatedCost(configuration, combustion, electric, gas, hybrid,'PHEV', E100km_ICE, annualDistance, 'Level1')
    accumulatedCost_PHEV3, annualCost_PHEV3 = accumulatedCost(configuration, combustion, electric, gas, hybrid,'PHEV', E100km_ICE, annualDistance, 'Level3')
   
    #Calculate the emission per kilometer metric - Rush hour
    emission_ICE = emission_metric(mean_daily('ICE', rush_df_ICE, trips, 3), mean_daily('ICE', rush_df_ICE, trips, 8), dailyDistance, 'ICE')
    emission_EV = emission_metric(mean_daily('EV', rush_df_EV, trips, 3), mean_daily('EV', rush_df_EV, trips, 9), dailyDistance, 'EV')
    emission_CNG = emission_metric(mean_daily('CNG', rush_df_CNG, trips, 3), mean_daily('CNG', rush_df_CNG, trips, 8), dailyDistance, 'CNG')
    emission_PHEV = (emission_ICE * 0.7) + (emission_EV * 0.3)
    
    #Calculate the Social cost metric - Rush hour
    socialCost_ICE = socialCost_metric(mean_daily('ICE', rush_df_ICE, trips, 3))
    socialCost_EV = socialCost_metric(mean_daily('EV', rush_df_EV, trips, 3))
    socialCost_CNG = socialCost_metric(mean_daily('CNG', rush_df_CNG, trips, 3))
    socialCost_PHEV = (socialCost_ICE * 0.7) + (socialCost_EV * 0.3)
    
    #Calculate the availability factor metric - Rush hour
    availabilityFactor_ICE = chargingTime_metric(9.25, 951.02, annualDistance / 365 , 9.25, E100km_ICE)
    availabilityFactor_EV1 = chargingTime_metric(53.5, 1.8, annualDistance / 365, 53.5, E100km_EV)
    availabilityFactor_EV2 = chargingTime_metric(53.5, 22.0, annualDistance / 365, 53.5, E100km_EV)
    availabilityFactor_EV3 = chargingTime_metric(53.5, 50.0, annualDistance / 365, 53.5, E100km_EV)
    availabilityFactor_CNG = chargingTime_metric(5.28, 55.0, annualDistance / 365, 5.28, E100km_CNG)
    availabilityFactor_PHEV1 = (chargingTime_metric(9.25, 951.02, dailyDistance * 0.7 , 9.25, E100km_ICE)) + chargingTime_metric(53.5, 1.8, dailyDistance * 0.3, 8.0, E100km_EV)
    availabilityFactor_PHEV2 = (chargingTime_metric(9.25, 951.02, dailyDistance * 0.7 , 9.25, E100km_ICE)) + chargingTime_metric(53.5, 22.0, dailyDistance * 0.3, 8.0, E100km_EV)
    availabilityFactor_PHEV3 = (chargingTime_metric(9.25, 951.02, dailyDistance * 0.7 , 9.25, E100km_ICE)) + chargingTime_metric(53.5, 50.0, dailyDistance * 0.3, 8.0, E100km_EV)
    
    #Calculate the LifeCycle Emission metric - Rush hour
    lifecycleEmissions_ICE = lifecycle_emissions('ICE', 894, 0, emission_ICE, annualDistance)
    lifecycleEmissions_EV = lifecycle_emissions('EV', 1640, 53.5, emission_EV, annualDistance)
    lifecycleEmissions_CNG = lifecycle_emissions('CNG', 894, 0, emission_CNG, annualDistance)
    lifecycleEmissions_PHEV = lifecycle_emissions('PHEV', 1640, 8.0, emission_PHEV, annualDistance)

    #Calculate the Social metric - Rush hour
    availability = [availabilityFactor_ICE, 
                    availabilityFactor_EV1, availabilityFactor_EV2, availabilityFactor_EV3, 
                    availabilityFactor_CNG, 
                    availabilityFactor_PHEV1, availabilityFactor_PHEV2, availabilityFactor_PHEV3]
    autonomy = [autonomy_ICE, autonomy_EV, autonomy_EV, autonomy_EV, autonomy_CNG, autonomy_PHEV, autonomy_PHEV, autonomy_PHEV]
    cost = [accumulatedCost_ICE[-1], accumulatedCost_EV1[-1], accumulatedCost_EV1[-1], accumulatedCost_EV3[-1], accumulatedCost_CNG[-1], 
            accumulatedCost_PHEV1[-1], accumulatedCost_PHEV1[-1], accumulatedCost_PHEV3[-1]]
    incentives = [1, 9, 9, 9, 9, 4, 4, 4]
    emissions = [lifecycleEmissions_ICE, lifecycleEmissions_EV, lifecycleEmissions_EV, lifecycleEmissions_EV, lifecycleEmissions_CNG, lifecycleEmissions_PHEV, lifecycleEmissions_PHEV, lifecycleEmissions_PHEV]

    social = social_metric(generate_alternative_matrix(availability, autonomy, cost, incentives, emissions))
    plot_cost()
    consumption = [E100km_ICE, E100km_EV, E100km_CNG, E100km_PHEV]
    cpt = [icr_ICE, icr_EV, icr_CNG, icr_PHEV]
    eco = [emission_ICE, emission_EV, emission_CNG, emission_PHEV]
    emissions = [lifecycleEmissions_ICE, lifecycleEmissions_EV, lifecycleEmissions_CNG, lifecycleEmissions_PHEV]
    socialCost = [socialCost_ICE, socialCost_EV, socialCost_CNG, socialCost_PHEV]

    save_metrics_data(consumption, autonomy, cpt, cost, eco, emissions, socialCost, social, availability)

    # # print('L1 (1.2 kW) = ', chargingTime_metric(53.5, 1.2, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV))
    # # print('L1 (1.8 kW) = ', chargingTime_metric(53.5, 1.8, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV))
    # # print('L2 (3.6 kW) = ', chargingTime_metric(53.5, 3.6, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV))
    # # print('L2 (11 kW) = ', chargingTime_metric(53.5, 11.0, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV))
    # # print('L2 (22 kW) = ', chargingTime_metric(53.5, 22.0, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV))
    # # print('L3 (50 kW) = ', chargingTime_metric(53.5, 50.0, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV))