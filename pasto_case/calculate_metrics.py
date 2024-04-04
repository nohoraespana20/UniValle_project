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
    total_fuel = route_class["FuelConsumption"].sum()*(0.000264) #Fuel in gallons
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

def consumption_metric(vehType, distance, consumption):
    '''
    Efficiency is quantified in terms of consumption per kilometer traveled 
    vehType: EV (Electric Vehicle) or ICE (Internal Combustion Engine)
    distance: paths in km
    consumption: fuel or kwh consumed in paths
    '''
    if vehType == "ICE":
        E_100km = (consumption*3.785*10.7*100)/distance
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
        consumption = (E_100km/(100*3.785*10.7))
        autonomy = capacity / consumption
    elif vehType == "EV":
        autonomy = capacity * 0.85 / (E_100km/100)
    else:
        print('Vehicle type is not defined')
    return round(autonomy, 2)

        # self.createBox(cfgFrame, "Divisa", self.currency, ('', 'USD', 'COP'), 1)
        # self.createBox(cfgFrame, "Modo de transporte", self.modeTransport, (" ", "Taxi", "Bus"), 2)
        # self.createEntry(cfgFrame, "Años", self.time, "", 3)
        # self.createEntry(cfgFrame, "Distancia anual [km]", self.annualDistance, "", 4)
        # self.createEntry(cfgFrame, "Distancia diaria [km]", self.dailyDistance, "", 5)

        # self.createEntry(cFrame, "Costo de compra", self.combustionCost, "", 1)
        # self.createEntry(cFrame, "Costo galón de combustible", self.fuelCost, "", 2)
        # self.createEntry(cFrame, "% Incremento anual combustible", self.fuelRaise, "", 3)
        # self.createEntry(cFrame, "Consumo diario [gl]", self.dailyConsumption, "", 4)
        # self.createEntry(cFrame, "Costo anual mantenimiento", self.combustionMaintenanceCost, "", 5)
        # self.createEntry(cFrame, "Costo anual SOAT", self.soatCost, "", 6)
        # self.createEntry(cFrame, "Costo anual otros seguros", self.otherInsurance, "", 7)
        # self.createEntry(cFrame, "Costo revisión tecnomecánica", self.checkCost, "", 8)
        # self.createEntry(cFrame, "% Incremento anual seguros", self.insuranceRaise, "", 9)
        # self.createEntry(cFrame, "Reparaciones por año", self.repairs, "", 10)

        # self.createEntry(eFrame, "Costo de compra", self.electricCost, "", 1)
        # self.createEntry(eFrame, "Costo kWh", self.kWhCost, "", 2)
        # self.createEntry(eFrame, "% Incremento anual kWh", self.kWhRaise, "", 3)
        # self.createEntry(eFrame, "Consumo diario [kWh]", self.dailykWh, "", 4)
        # self.createEntry(eFrame, "Capacidad de batería [kWh]", self.bateryCapacity, "", 5)

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

def accumulatedCost(configuration, combustion, electric, vehType, E_100km):
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

    if vehType == 'ICE':
        powerConsumption = (E_100km/(100*3.785*10.7))*configuration[3]
            
        totalCost[0] = combustion[0] 
        taxCost = combustion[0] * 0.01 # Based on "Ley 1964 de 2019, Congreso de Colombia"
        annualPowerCost = powerConsumption * combustion[1]
        annualPowerCostRaise  = combustion[2] / 100
        maintenanceCost = combustion[4]
        soatCost = combustion[5]
        otherInsurance = combustion[6] # Contractual insuarence and all damages insurance
        checkCost = combustion[7]
    elif vehType == 'EV':
        powerConsumption = (E_100km/100)*configuration[3]
            
        totalCost[0] = electric[0]
        taxCost = combustion[0] * 0.01 * 0.4 # Based on "Ley 1964 de 2019, Congreso de Colombia"
        annualPowerCost = powerConsumption * electric[1]
        annualPowerCostRaise  = electric[2] / 100
        maintenanceCost = combustion[4] * 0.4
        soatCost = combustion[5] * 0.9
        checkCost = combustion[7] * 0.7 
        bateryCost = electric[4] * 156 / 5000 # Batery cost in COP
        batteryYearlyRaise = -0.0967 # According to technology reduction cost trend
    else:
        print('vehType parameter is not defined ')

    for i in range(1,configuration[2],1):
        totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + taxCost
        if i >= 2:
        #Annual variance of parameters costs
            taxCost = taxCost * (1 + insuranceCostRaise)
            annualPowerCost = annualPowerCost * (1 + annualPowerCostRaise)
            maintenanceCost = maintenanceCost * (1 + ipc)
            soatCost = soatCost * (1 + insuranceCostRaise)
            otherInsurance = otherInsurance * (1 + insuranceCostRaise)
            checkCost = checkCost * (1 + insuranceCostRaise)
            totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + \
            taxCost + checkCost
            if vehType == 'EV':
                bateryCost = bateryCost * (1 + batteryYearlyRaise)
                if i==8 or i==16 or i==24:
                    totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance \
                        + checkCost + taxCost + bateryCost

    for i in range(len(totalCost)):
        totalCost[i] = round(totalCost[i] / currency , 2)
        
    return totalCost

def ICR_metric(powerCost, consumption, distance):
    '''
    Relates the duration of the trip to the fuel or electricity expenditure during that trip. 
    powerCost: cost per gallon of fuel or cost per kWh.
    consumption: fuel consumption in gallons or electricity consumption in kWh.
    distance: the distance traveled in kilometers.
    '''
    icr = powerCost * consumption / distance
    return round(icr,2)

def emission_metric(co2Emission, consumption, distance, vehType):
    '''
    Expressed in grams of CO2 per kilometer for both ICEVs and EVs. 
    '''
    if vehType == 'ICE':
        emissionPerKilometer = co2Emission * 1000 / distance
    elif vehType == 'EV':
        emissionPerKilometer = 164.38 * consumption / distance
    else:
        print('Vehicle type is not defined')
    return round(emissionPerKilometer, 2)

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


if __name__ == '__main__':
    import matplotlib.pyplot as plt
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

    #Calculate the consumption metric - E100km - Rush hour
    # print('RUSH HOUR\n')
    E100km_ICE = consumption_metric('ICE', mean_daily('ICE', rush_df_ICE, 35, 2), mean_daily('ICE', rush_df_ICE, 35, 8))
    E100km_EV = consumption_metric('EV', mean_daily('EV', rush_df_EV, 35, 2), mean_daily('EV', rush_df_EV, 35, 9))
    # print('E100km_ICE [kWh/100km] = ', E100km_ICE, '\nE100km_EV [kWh/100km] = ', E100km_EV)

    # autonomy_ICE = autonomy_metric('ICE', E100km_ICE, 9.35) #View KIA grand EKO Taxi datasheet (tank capacity)
    # autonomy_EV = autonomy_metric('EV', E100km_EV, 53.5) #View BYD D1 datasheet (battery capacity)
    # print('Autonomy ICE [km]= ', autonomy_ICE, '\nAutonomy EV [km]= ', autonomy_EV)

    # icr_ICE = ICR_metric(combustion[1] , mean_daily('ICE', rush_df_ICE, 35, 8) , mean_daily('ICE', rush_df_ICE, 35, 2))
    # icr_EV = ICR_metric(electric[1] , mean_daily('EV', rush_df_EV, 35, 9) , mean_daily('EV', rush_df_EV, 35, 2))
    # print('ICR ICE = ', icr_ICE, '\nICR EV = ', icr_EV)

    # accumulatedCost_ICE = accumulatedCost(configuration, combustion, electric, 'ICE', E100km_ICE)
    # accumulatedCost_EV = accumulatedCost(configuration, combustion, electric, 'EV', E100km_EV)
    # print('Cost ICE = ', accumulatedCost_ICE, '\nCost EV = ', accumulatedCost_EV)

    # emission_ICE = emission_metric(mean_daily('ICE', rush_df_ICE, 35, 3), mean_daily('ICE', rush_df_ICE, 35, 8), mean_daily('ICE', rush_df_ICE, 35, 2), 'ICE')
    # emission_EV = emission_metric(mean_daily('EV', rush_df_EV, 35, 3), mean_daily('EV', rush_df_EV, 35, 9), mean_daily('EV', rush_df_EV, 35, 2), 'EV')
    # print('CO2/km ICE = ', emission_ICE, '\nCO2/km EV = ', emission_EV)

    # socialCost_ICE = socialCost_metric(mean_daily('ICE', rush_df_ICE, 35, 3))
    # socialCost_EV = socialCost_metric(mean_daily('EV', rush_df_EV, 35, 3))
    # print('Social Cost Emission ICE = ', socialCost_ICE, '\nSocial Cost Emission EV = ', socialCost_EV)

    availabilityFactor_ICE = chargingTime_metric(9.25, 951.02, mean_daily('ICE', rush_df_ICE, 35, 2), 9.25, E100km_ICE)
    print('Availability factor ICE = ', availabilityFactor_ICE)

    availabilityFactor_EV = chargingTime_metric(53.5, 1, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV)
    print('Availability factor EV = ', availabilityFactor_EV)

    availabilityFactor_EV = chargingTime_metric(53.5, 6, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV)
    print('Availability factor EV = ', availabilityFactor_EV)

    availabilityFactor_EV = chargingTime_metric(53.5, 50, mean_daily('EV', rush_df_EV, 35, 2), 53.5, E100km_EV)
    print('Availability factor EV = ', availabilityFactor_EV)