import numpy as np
import matplotlib.pyplot as plt
import math

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

def charging_time(chargeNeeded, chargerType):
    if chargerType == 'low':
        chargingSpeed = 1
    elif chargerType == 'semifast1':
        chargingSpeed = 11
    elif chargerType == 'semifast2':
        chargingSpeed = 22
    elif chargerType == 'fast':
        chargingSpeed = 50
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
    # print('Mean public preference = ', round(np.mean(publicPreference), 2))
    return publicPreference[0], normLevelPreference

def demand_power_charge(demandPerVehicle , annualVehicles, chargerType, b, P):
    powerNeeded = []
    for i in range(annualVehicles):
        if chargerType == 'low':
            powerNeeded.append(demandPerVehicle * (1 - b))
        elif chargerType == 'semifast1':
            powerNeeded.append(demandPerVehicle * b * P[0])
        elif chargerType == 'semifast2':
            powerNeeded.append(demandPerVehicle * b * P[1])
        elif chargerType == 'fast':
            powerNeeded.append(demandPerVehicle * b * P[2])
    return sum(powerNeeded)

def vehicle_projection(years, initialYear, vehicleSeed):
    taxisProjection, taxisProjectionSub, penetrationPercentageSub, annualVehiclesSub, yearCalendar, yearCalendarSub = [], [], [], [], [], []
    penetrationPercentage = [0.03, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 10.0, 
                             12.0, 15.0, 18.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 
                             56.0, 62.0, 68.0, 75.0, 80.0, 85.0, 88.0, 92.0, 96.0, 100.0]
    for year in range(0, years):
        
        if year == 0:
            yearCalendar.append(initialYear + 1)
            taxisProjection.append(math.ceil(vehicleSeed * 1.009))
        else:
            yearCalendar.append(initialYear + year + 1)
            taxisProjection.append(math.ceil(taxisProjection[year-1] * 1.009))
    annualVehicles = ice_to_ev(taxisProjection, penetrationPercentage)
    for year in range(years):
        if year == 0 or year == 1 or year == 2 or year == 3 or year == 4 or year == 9 or year == 14 or year == 19 or year == 24 or year == 29:
            taxisProjectionSub.append(taxisProjection[year])
            penetrationPercentageSub.append(penetrationPercentage[year])
            annualVehiclesSub.append(annualVehicles[year])
            yearCalendarSub.append(yearCalendar[year])
    print('Taxis projection = ', taxisProjection)
    print('Penetration percetage = ', penetrationPercentageSub)
    print('EV projection = ', annualVehicles)
    print('Year = ', yearCalendarSub)
    return taxisProjection, penetrationPercentage, annualVehicles, yearCalendar

def charging_stations_metrics(annualVehicles, demandPerVehicle, timeAvailability, chargerType, b, P):
    if chargerType == 'low':
        gwp = 82.52
        powerCharging = 1.8
    elif chargerType == 'semifast1':
        gwp = 91.58
        powerCharging = 11.0
    elif chargerType == 'semifast2':
        gwp = 91.58
        powerCharging = 22.0
    elif chargerType == 'fast':
        gwp = 111.02
        powerCharging = 50.0
    
    totalDemand = demand_power_charge(demandPerVehicle, annualVehicles, chargerType, b, P)
    if chargerType == 'low':
        numberChargers = math.ceil(totalDemand / demandPerVehicle)
    else:
        numberChargers = math.ceil((totalDemand / (powerCharging * timeAvailability)) )
    utilizationRate = math.ceil(totalDemand / (powerCharging * numberChargers) * 100 / timeAvailability)
    emissions = math.ceil((totalDemand * gwp))
    print(f'Utilization rate - {chargerType} =', utilizationRate, ' %') 
    print(f'Number of chargers - {chargerType} =', numberChargers) 
    print(f'Emissions - {chargerType} =', emissions, ' g CO2e/kWh') 
    return utilizationRate, numberChargers, emissions, totalDemand

def ev_per_charging_point(annualVehicles, numberChargers, chargerType):
    EVperCP = math.ceil(annualVehicles / numberChargers)
    print(f'1 charger point {chargerType} per ', EVperCP, ' EV')
    return EVperCP

def land_area_metric(EVperCP, parkingArea, chargerType):
    if chargerType == "low":
        gamma = 0 # asumme parking available
    elif chargerType == "semifast1" or chargerType == "semifast2":
        gamma = 1 # 100 m2 every 100 EV
    elif chargerType == "fast":
        gamma = 2 # 200 m2 every 100 EV
    else:
        print("Type charger is not defined")
    landArea = EVperCP * (gamma + parkingArea) #14m2 every EV
    print(f"Land area for {chargerType} charger = ", landArea, " m^2")
    return landArea

def charging_stations_metrics_per_year(annualVehicles, demandPerVehicle, timeAvailability, chargerTypes, parkingArea):
    b, P, = percentage_preference_type_charger(annualVehicles[-1])
    print('Preference porcentage\nb = ', b[-1], '\nP = ', P[-1])
    utilizationRateYear, numberChargersYear, emissionChargersYear, EVperCPYear, landAreaYear, demandChargersYear = [], [], [], [], [], []
    for j in range(len(annualVehicles)):
        utilizationRate, numberChargers, emissionChargers, EVperCP, landArea, demandChargers = [], [], [], [], [], []
        for i in range(len(chargerTypes)):
            print(f'\nMetrics for charger type {chargerTypes[i]} {j}')
            uR, nC, eC, dC = charging_stations_metrics(annualVehicles[j], demandPerVehicle, timeAvailability[i], chargerTypes[i], b[j], P[j])
            ev = ev_per_charging_point(annualVehicles[j], nC, chargerTypes[i])
            lArea= land_area_metric(ev, parkingArea[i], chargerTypes[i])
            utilizationRate.append(uR)
            numberChargers.append(nC)
            emissionChargers.append(eC)
            EVperCP.append(ev)
            landArea.append(lArea)
            demandChargers.append(dC)
        utilizationRateYear.append(utilizationRate)
        numberChargersYear.append(numberChargers)
        emissionChargersYear.append(emissionChargers)
        EVperCPYear.append(EVperCP)
        landAreaYear.append(landArea)
        demandChargersYear.append(demandChargers)
    return utilizationRateYear, numberChargersYear, emissionChargersYear, EVperCPYear, landAreaYear, demandChargersYear

def job_charging_station(portsPerCH, annualVehicles, numberChargersYear):
    jobsPerCS = 5
    totalChargerPoints = []
    jobs_CS = []
    for i in range(len(annualVehicles)):
        totalChargerPoints.append((numberChargersYear[i][1]) + round(numberChargersYear[i][2]) + round(numberChargersYear[i][3]))
        jobs_CS.append(math.ceil((totalChargerPoints[i] * jobsPerCS / portsPerCH)))
    print('\nJobs generated per Year = ', jobs_CS, '\nTotal jobs generated = ', sum(jobs_CS))
    return jobs_CS

def number_charging_station(numberChargersYear, chargerTypes):
        numberChargingStationsPerType = []
        for j in range(len(chargerTypes)):
            numberChargingStations = []
            for i in range(len(numberChargersYear)):
                if chargerTypes[j] == 'low':
                    numberChargingStations.append(math.ceil(numberChargersYear[i][j]))
                else:
                    numberChargingStations.append(math.ceil(numberChargersYear[i][j] / 6))
                if i > 0:
                    if numberChargingStations[i] < numberChargingStations[i-1]:
                        numberChargingStations[i] = numberChargingStations[i-1]
            numberChargingStationsPerType.append(numberChargingStations)
        print('\nnumberChargingStationsPerType ', numberChargingStationsPerType)
        return numberChargingStationsPerType

def demand_daily_power_charging_station(numberChargingStationsPerType, numberChargersYear, demandChargersYear):
    #demand per type of charging
    demandPowerPerTypeCS = []
    for i in range(len(numberChargingStationsPerType)): #(0 - 4)
        demandPower = []
        for j in range(len(numberChargingStationsPerType[0])): #(0 - 30)
            demandPower.append(math.ceil(numberChargersYear[j][i] * demandChargersYear[j][i] * 365 /  numberChargingStationsPerType[i][j]))
        demandPowerPerTypeCS.append(demandPower)
    # print('\ndemandPowerPerTypeCS daily', demandPowerPerTypeCS)
    return demandPowerPerTypeCS

if __name__ == '__main__':
    import calculate_metrics as cm
    import pandas as pd
    years = 30
    taxisProjection, penetrationPercentage, annualVehicles, yearCalendar = vehicle_projection(years, initialYear = 2025, vehicleSeed = 3016)
    
    costkWh = cm.readJson('config_files/data_electric.json')['kWh cost']
    emissionClasses = ['Energy/unknown']
    dataframe = cm.generate_data_frame(emissionClasses,"./results/rush/data_emissions_EV.csv")
    dailyDistance = cm.mean_daily('EV', dataframe, 35, 2)

    capacityBat = 53.5
    autonomy = 417.20
    demandPerVehicle = (capacityBat * dailyDistance / autonomy) 
    chargerTypes = ['low', 'semifast1', 'semifast2', 'fast']
    timeAvailability = [24, 8, 8, 12] # Service hours per type CS
    parkingArea = [0, 0, 0, 14]
    portsPerCS = 6

    utilizationRateYear, numberChargersYear, emissionChargersYear, EVperCPYear, landAreaYear, demandChargersYear = charging_stations_metrics_per_year(annualVehicles, demandPerVehicle, timeAvailability, chargerTypes, parkingArea)
    numberChargingStationsPerType = number_charging_station(numberChargersYear, chargerTypes)  
    demandDailyPowerCS = demand_daily_power_charging_station(numberChargingStationsPerType, numberChargersYear, demandChargersYear)
    print('demand Yearly PowerCS Level1', demandDailyPowerCS[0])
    print('demand Yearly PowerCS Level2M1', demandDailyPowerCS[1])
    print('demand Yearly PowerCS Level2M23', demandDailyPowerCS[2])
    print('demand Yearly PowerCS Level3', demandDailyPowerCS[3])
    jobsGenerateCS = job_charging_station(portsPerCS, annualVehicles, numberChargersYear)

    kWhCostResidential = [round(681.3 / 5000, 2)]
    kWhCostCommercial = [round(853.6 / 5000, 2)]
    ipc = 0.0457 # Average value of IPC in Colombia
    annualIncremental = 1 + ipc
    investmentResidential = [0, 1000, 1800]
    investmentCommercial = [3800, 9200, 220000]

    annualCostResidentialperType, accumulatedCostResidentialperType = [], []
    for k in range(len(investmentResidential)):
        numberCSnew = [numberChargingStationsPerType[0][0]]

        investment = [investmentResidential[k]]
        maintenance = [investmentResidential[k] * 0.1]
        retrofit = [investmentResidential[k] * 0.5]

        annualInvestment = [investmentResidential[k]]
        annualMaintenance = [investmentResidential[k] * 0.1]
        annualretrofit = [investmentResidential[k] * 0.5]

        annualCostkWhResidential = [round(kWhCostResidential[0] * demandDailyPowerCS[0][0] , 2)]
        annualCostResidential = [investmentResidential[k] + annualCostkWhResidential[0]]
        accumulatedCostResidential = [investmentResidential[k] + annualCostkWhResidential[0]]

        for i in range(1, years):
            kWhCostResidential.append(round(kWhCostResidential[i-1] * (1 + (7.5 / 100)) , 2))
            kWhCostCommercial.append(round(kWhCostCommercial[i-1] * (1 + (7.2 / 100)) , 2))
            
            annualCostkWhResidential.append(round(kWhCostResidential[i] * demandDailyPowerCS[0][i] , 2))
            annualInvestment.append(annualInvestment[i-1] * annualIncremental)
            annualMaintenance.append(annualMaintenance[i-1] * annualIncremental)
            annualretrofit.append(annualretrofit[i-1] * annualIncremental)

            if numberChargingStationsPerType[0][i] - numberChargingStationsPerType[0][i-1] > 0: 
                numberCSnew.append(numberChargingStationsPerType[0][i] - numberChargingStationsPerType[0][i-1])
                investment.append(annualInvestment[i] * numberCSnew[i])
                maintenance.append(annualMaintenance[i-1] * numberCSnew[i-1])
                retrofit.append(annualretrofit[i-1] * numberCSnew[i-1])
            else:
                numberCSnew.append(1)
                investment.append(0)
                maintenance.append(annualMaintenance[i-1] * numberCSnew[i-1])
                retrofit.append(annualretrofit[i-1] * numberCSnew[i-1]) 
            if i == 10 or i == 20 or i == 30:
                annualCostResidential.append(math.ceil(investment[i] + maintenance[i] + retrofit[i] + annualCostkWhResidential[i]))
                accumulatedCostResidential.append(accumulatedCostResidential[i-1] + annualCostResidential[i])
            else:
                annualCostResidential.append(math.ceil(investment[i] + maintenance[i] + annualCostkWhResidential[i]))
                accumulatedCostResidential.append(accumulatedCostResidential[i-1] + annualCostResidential[i])
        annualCostResidentialperType.append(annualCostResidential) 
        accumulatedCostResidentialperType.append(accumulatedCostResidential) 
   
    annualCostCommercialperType, accumulatedCostCommercialperType = [], []
    for k in range(len(investmentCommercial)):
        numberCSnew = [numberChargingStationsPerType[k][0]]

        investment = [investmentCommercial[k]]
        maintenance = [investmentCommercial[k] * 0.1]
        retrofit = [investmentCommercial[k] * 0.25]

        annualInvestment = [investmentCommercial[k]]
        annualMaintenance = [investmentCommercial[k] * 0.1]
        annualretrofit = [investmentCommercial[k] * 0.25]

        annualCostkWhCommercial = [round(kWhCostCommercial[0] * demandDailyPowerCS[k+1][0] , 2)]
        annualCostCommercial = [investmentCommercial[k] + annualCostkWhCommercial[0]]
        accumulatedCostCommercial = [investmentCommercial[k] + annualCostkWhCommercial[0]]

        for i in range(1, years):
            annualInvestment.append(annualInvestment[i-1] * annualIncremental)
            annualMaintenance.append(annualMaintenance[i-1] * annualIncremental)
            annualretrofit.append(annualretrofit[i-1] * annualIncremental)
            annualCostkWhCommercial.append(round(kWhCostCommercial[i] * demandDailyPowerCS[k+1][i] , 2))

            if numberChargingStationsPerType[k+1][i] - numberChargingStationsPerType[k+1][i-1] > 0: 
                numberCSnew.append(numberChargingStationsPerType[k+1][i] - numberChargingStationsPerType[k+1][i-1])
                investment.append(annualInvestment[i] * numberCSnew[i])
                maintenance.append(annualMaintenance[i-1] * numberCSnew[i-1])
                retrofit.append(annualretrofit[i-1] * numberCSnew[i-1])
            else:
                numberCSnew.append(1)
                investment.append(0)
                maintenance.append(annualMaintenance[i-1] * numberCSnew[i-1])
                retrofit.append(annualretrofit[i-1] * numberCSnew[i-1]) 
            if i == 10 or i == 20 or i == 30:
                annualCostCommercial.append(math.ceil(investment[i] + maintenance[i] + retrofit[i] + annualCostkWhCommercial[i]))
                accumulatedCostCommercial.append(accumulatedCostCommercial[i-1] + annualCostCommercial[i])
            else:
                annualCostCommercial.append(math.ceil(investment[i] + maintenance[i] + annualCostkWhCommercial[i]))
                accumulatedCostCommercial.append(accumulatedCostCommercial[i-1] + annualCostCommercial[i])
        annualCostCommercialperType.append(annualCostCommercial) 
        accumulatedCostCommercialperType.append(accumulatedCostCommercial) 

    for i in range(len(annualCostCommercialperType)):
        for j in range(len(annualCostCommercialperType[0])):
            annualCostResidentialperType[i][j] = round(annualCostResidentialperType[i][j] / 1000, 2)
            annualCostCommercialperType[i][j] = round(annualCostCommercialperType[i][j] / 1000, 2)
            accumulatedCostResidentialperType[i][j] = round(accumulatedCostResidentialperType[i][j] / 1000, 2)
            accumulatedCostCommercialperType[i][j] = round(accumulatedCostCommercialperType[i][j] / 1000, 2)
    # print('\nannualCostResidentialperType = ', annualCostResidentialperType)
    # print('\nannualCostCommercialperType = ', annualCostCommercialperType)

    interestRate = 0.1125

    npcCommercialperType = []
    npcResidentialperType = []
    lcocResidentialperType = []
    lcocCommercialperType = []

    for k in range(3):
        npcCommercialyearly = []
        npcResidentialyearly = []
        lcocResidentialyearly = []
        lcocCommercialyearly = []
        for i in range(years-1):
            npcResidentialyearly.append(annualCostResidentialperType[k][i] / ((1 + interestRate)**i))
            npcCommercialyearly.append(annualCostCommercialperType[k][i] / ((1 + interestRate)**i))
            lcocResidentialyearly.append(demandDailyPowerCS[0][i] / ((1 + interestRate)**i))
            lcocCommercialyearly.append(demandDailyPowerCS[k+1][i] / ((1 + interestRate)**i))
        npcResidentialperType.append(math.ceil(sum(npcResidentialyearly)))
        npcCommercialperType.append(math.ceil(sum(npcCommercialyearly)))
        lcocResidentialperType.append(round(math.ceil(sum(npcResidentialyearly)) * 1000 / sum(lcocResidentialyearly), 2))
        lcocCommercialperType.append(round(math.ceil(sum(npcCommercialyearly)) * 1000 / sum(lcocCommercialyearly), 2))

    print('\nnpcResidential = ', npcResidentialperType)
    print('\nnpcCommercial = ', npcCommercialperType)
    print('\nlcocResidential = ', lcocResidentialperType)
    print('\nlcoCommercial = ', lcocCommercialperType)
    

    years_p = [*range(0, years, 1)]
    Y = [str(x) for x in years_p]
    slow1 = annualCostResidentialperType[0]
    slow2 = annualCostResidentialperType[1]
    slow3 = annualCostResidentialperType[2]
    semifast1 = annualCostCommercialperType[0]
    semifast2 = annualCostCommercialperType[1]
    fast = annualCostCommercialperType[2]
    df = pd.DataFrame({'Slow charging with access': slow1, 'Slow charging without access': slow2, 'Slow charging commercial': slow3, 'Semifast residential':semifast1, 'Semifast commercial':semifast2, 'Fast':fast}, index=Y)
    df.plot( kind = 'bar', rot=0, color=['#444444', '#adff2f', "#38761d", "#512647", "#ddcd82", "#89cff0"])
    plt.xlabel("Year")
    plt.ylabel("Thousands of USD")
    plt.title("Annual cost - EV charging infrastructure")
    plt.grid()
    plt.legend()
    plt.show()

    year = list(range(years))
    plt.plot(year, accumulatedCostResidentialperType[0], "#444444", label="Slow with access")
    plt.plot(year, accumulatedCostResidentialperType[1], "#adff2f", label="Slow without access")
    plt.plot(year, accumulatedCostResidentialperType[2], "#38761d", label="Slow commercial")
    plt.plot(year, accumulatedCostCommercialperType[0], "#512647", label="Semifast residential")
    plt.plot(year, accumulatedCostCommercialperType[1], "#ddcd82", label="Semifast commercial")
    plt.plot(year, accumulatedCostCommercialperType[2], "#89cff0", label="Fast")
    plt.xlabel("Year")
    plt.ylabel("Thousands of USD")
    plt.title("Accumulated cost - EV charging infrastructure")
    plt.grid()
    plt.legend()
    plt.show()