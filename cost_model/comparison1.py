def priceTrips(tripsDayWeekendPerType , tripsDayWeekPerType, businessDays, holidays, HOLIDAYS):
    if HOLIDAYS:
        priceWeek = []
        priceWeekend = []
        totalPrice = []
        #Precio por tipo de carrera
        pricePerType = [1.10, 1.28, 1.50] 
        for k in range(len(pricePerType)):
            priceWeek.append(tripsDayWeekPerType[k] * pricePerType[k] * businessDays)
            pricePerType[k] = pricePerType[k] + 0.12
            priceWeekend.append(tripsDayWeekendPerType[k] * pricePerType[k] * holidays)
            totalPrice.append(round(priceWeek[k] + priceWeekend[k]))
    else:
        #Precio anual de las carreras realizadas
        priceWeek = []
        priceWeekend = []
        totalPrice = []
        #Precio por tipo de carrera
        pricePerType = [1.10, 1.28, 1.50]
        for k in range(len(pricePerType)):
            priceWeek.append(tripsDayWeekPerType[k] * pricePerType[k] * businessDays)
            priceWeekend.append(tripsDayWeekendPerType[k] * pricePerType[k] * holidays)
            totalPrice.append(round(priceWeek[k] + priceWeekend[k]))
    
    return totalPrice

def totalPriceAnnualTrips(VACATIONS, HOLIDAYS):
    # Número de carreras diarias promedio realizadas
    tripsDayWeekend = 33 
    tripsDayWeek = 27
    tripsDayWeekendPerType = [round(tripsDayWeekend * tripsNP), round(tripsDayWeekend * tripsNPP), round(tripsDayWeekend * tripsP)]
    tripsDayWeekPerType = [round(tripsDayWeek * tripsNP), round(tripsDayWeek * tripsNPP), round(tripsDayWeek * tripsP)]

    if VACATIONS:
        tripsDayWeekend = tripsDayWeekend + 10
        tripsDayWeek = tripsDayWeek + 10
        tripsDayWeekendPerType = [round(tripsDayWeekend * tripsNP), round(tripsDayWeekend * tripsNPP), round(tripsDayWeekend * tripsP)]
        tripsDayWeekPerType = [round(tripsDayWeek * tripsNP), round(tripsDayWeek * tripsNPP), round(tripsDayWeek * tripsP)]

        #Días trabajados por tipo
        holidaysVacations = 3 #Sunday and Holidays annual
        vacationsDays = 38 #december + 7 days january carnival
        businessDaysVacations = vacationsDays - holidaysVacations

        holidays = 67 #Sunday and Holidays annual
        retrictedDays = 48
        businessDays = 365 - holidays - vacationsDays - retrictedDays

        #Precio anual de los viajes
        priceTripsVacations = priceTrips(tripsDayWeekendPerType , tripsDayWeekPerType,businessDaysVacations, holidaysVacations, HOLIDAYS)
        priceTripsNoVacations = priceTrips(tripsDayWeekendPerType , tripsDayWeekPerType,businessDays, holidays, HOLIDAYS)
        totalPriceUSD = []
        totalPriceCOP = []
        for l in range(len(priceTripsVacations)):
            totalPriceUSD.append(priceTripsNoVacations[l] + priceTripsVacations[l])
            totalPriceCOP.append((priceTripsNoVacations[l] + priceTripsVacations[l])*4998)

        return totalPriceUSD, totalPriceCOP
    else: 
        #Días trabajados por tipo
        holidays = 70 #Sunday and Holidays annual
        retrictedDays = 52
        businessDays = 365 - holidays - retrictedDays

        #Precio anual de los viajes
        totalPriceUSD = []
        totalPriceCOP = []
        totalPriceUSD = priceTrips(tripsDayWeekendPerType , tripsDayWeekPerType, businessDays, holidays, HOLIDAYS)
        for i in range(len(totalPriceUSD)):
            totalPriceCOP.append(totalPriceUSD[i]*4998)
        return totalPriceUSD, totalPriceCOP

def totalAnnualCostTrips(VACATIONS, Ctco):
    # Número de carreras diarias promedio realizadas
    tripsDayWeekend = 33 
    tripsDayWeek = 27
    tripsDayWeekendPerType = [round(tripsDayWeekend * tripsNP), round(tripsDayWeekend * tripsNPP), round(tripsDayWeekend * tripsP)]
    tripsDayWeekPerType = [round(tripsDayWeek * tripsNP), round(tripsDayWeek * tripsNPP), round(tripsDayWeek * tripsP)]

    if VACATIONS:
        tripsWeekendPerType = [round(tripsDayWeekend * tripsNP), round(tripsDayWeekend * tripsNPP), round(tripsDayWeekend * tripsP)]
        tripsWeekPerType = [round(tripsDayWeek * tripsNP), round(tripsDayWeek * tripsNPP), round(tripsDayWeek * tripsP)]

        tripsDayWeekend = tripsDayWeekend + 10
        tripsDayWeek = tripsDayWeek + 10
        
        tripsDayWeekendPerType = [round(tripsDayWeekend * tripsNP), round(tripsDayWeekend * tripsNPP), round(tripsDayWeekend * tripsP)]
        tripsDayWeekPerType = [round(tripsDayWeek * tripsNP), round(tripsDayWeek * tripsNPP), round(tripsDayWeek * tripsP)]

        #Días trabajados por tipo
        holidaysVacations = 3 #Sunday and Holidays annual
        vacationsDays = 38 #december + 7 days january carnival
        businessDaysVacations = vacationsDays - holidaysVacations

        holidays = 67 #Sunday and Holidays annual
        retrictedDays = 48
        businessDays = 365 - holidays - vacationsDays - retrictedDays

        #Precio anual de los viajes
        totalCostUSD = []
        totalCostCOP = []
        for l in range(len(tripsDayWeekendPerType)):
            costTripsVacations = (businessDaysVacations + holidaysVacations) * (tripsDayWeekPerType[l] + tripsDayWeekendPerType[l])
            costTripsNoVacations = (businessDays + holidays) * (tripsWeekPerType[l] + tripsWeekendPerType[l])
            totalCostUSD.append(round((costTripsNoVacations + costTripsVacations)* Ctco[l][l]))
            totalCostCOP.append(round((costTripsNoVacations + costTripsVacations)* Ctco[l][l])*4998)
        return totalCostUSD, totalCostCOP
    else: 
        tripsWeekendPerType = [round(tripsDayWeekend * tripsNP), round(tripsDayWeekend * tripsNPP), round(tripsDayWeekend * tripsP)]
        tripsWeekPerType = [round(tripsDayWeek * tripsNP), round(tripsDayWeek * tripsNPP), round(tripsDayWeek * tripsP)]

        #Días trabajados por tipo
        holidays = 70 #Sunday and Holidays annual
        retrictedDays = 52
        businessDays = 365 - holidays - retrictedDays

        #Precio anual de los viajes
        totalCostUSD = []
        totalCostCOP = []
        for l in range(len(tripsDayWeekendPerType)):
            totalCostUSD.append(round((businessDays + holidays) * (tripsWeekPerType[l] + tripsWeekendPerType[l]) * Ctco[l][l]))
            totalCostCOP.append(round((businessDays + holidays) * (tripsWeekPerType[l] + tripsWeekendPerType[l]) * Ctco[l][l])*4998)
        return totalCostUSD, totalCostCOP

def meanFuelPerKM_C(file):
    with open(file) as file:
        fuelConsumption = json.load(file)
    fuel = []
    for i in range(2):
        for j in range(6):
            fuel.append(fuelConsumption[i][j][2]) # Solo EURO 4
    fuel = np.reshape(fuel,(2,6))
    fuelPerTypePeak = [np.mean(fuel[0][0:2]), np.mean(fuel[0][2:4]), np.mean(fuel[0][4:])]
    fuelPerTypePeakOff = [np.mean(fuel[1][0:2]), np.mean(fuel[1][2:4]), np.mean(fuel[1][4:])]
    
    #Distance data from results of emissions simulation
    distances = [(4022.095899057417+2415.0392316822504)/2000, (6938.748453744248+3465.652911930644)/2000, (5978.676979676662+7116.311075331374)/2000]
    fuelPerKMPeak = []
    fuelPerKMPeakOff = []
    for i in range(len(distances)):
        fuelPerKMPeak.append(fuelPerTypePeak[i]/distances[i])
        fuelPerKMPeakOff.append(fuelPerTypePeakOff[i]/distances[i])
    
    meanFuelPerKMPeak = np.mean(fuelPerKMPeak)
    meanFuelPerKMPeakOff = np.mean(fuelPerKMPeakOff)

    return meanFuelPerKMPeak, meanFuelPerKMPeakOff

def meanFuelPerKM_E(file):
    with open(file) as file:
        fuelConsumption = json.load(file)
    fuel = []
    for i in range(2):
        for j in range(6):
            fuel.append(fuelConsumption[i][j][0]) 
    fuel = np.reshape(fuel,(2,6))
    fuelPerTypePeak = [np.mean(fuel[0][0:2]), np.mean(fuel[0][2:4]), np.mean(fuel[0][4:])]
    fuelPerTypePeakOff = [np.mean(fuel[1][0:2]), np.mean(fuel[1][2:4]), np.mean(fuel[1][4:])]
    
    #Distance data from results of emissions simulation
    distances = [(4022.095899057417+2415.0392316822504)/2000, (6938.748453744248+3465.652911930644)/2000, (5978.676979676662+7116.311075331374)/2000]
    fuelPerKMPeak = []
    fuelPerKMPeakOff = []
    for i in range(len(distances)):
        fuelPerKMPeak.append(fuelPerTypePeak[i]/distances[i])
        fuelPerKMPeakOff.append(fuelPerTypePeakOff[i]/distances[i])
    
    meanFuelPerKMPeak = np.mean(fuelPerKMPeak)
    meanFuelPerKMPeakOff = np.mean(fuelPerKMPeakOff)

    return meanFuelPerKMPeak, meanFuelPerKMPeakOff

def costEquation(CenPeak,  CenPeakOff):
    Cd = 2401.01
    Ctx = 84.17
    Cti = 194.88
    Cr = 1446.22
    Ci = 250.2
    Cc = 730.31
    Cp = 167.07
    Cen = (CenPeak+CenPeakOff)/2
    Dt = [3.2, 5.3, 6.6]
    Da = [46800, 54600, 62400]

    #Ecuación de costo
    Ctco = [] #Costo total de propiedad por carrera
    for i in range(len(Dt)):
        for j in range(len(Da)): 
            cto= Dt[i] * (((Cd + Ctx + Cti + Cr + Ci + Cc + Cp) / Da[j]) - Cen)
            Ctco.append(cto)
    Ctco = np.reshape(Ctco, (3,3))
    return Ctco

def accumulatedCost1(Cen_C, Cen_E, E):
    year = 30
    totalC = [*range(0, year, 1)]
    totalE = [*range(0, year, 1)]
    totalC[0] = initialCost_C
    totalE[0] = initialCost_E
    for i in range(1,year,1):
        Cen_C = Cen_C + Cen_C * yearlyRaise_C
        Cen_E = Cen_E + Cen_E * yearlyRaise_E
        combustionCost = (E * Cen_C)
        electricCost = (E * Cen_E)
        totalC[i] = initialCost_C + combustionCost
        totalE[i] = initialCost_E + electricCost
    return totalC, totalE, i

def accumulatedCost2(Cen_C, Cen_E, Cm_C, Cm_E, othersC, othersE, otherC, otherE, E):
    year = 30
    totalC = [*range(0, year, 1)]
    totalE = [*range(0, year, 1)]
    totalC[0] = initialCost_C
    totalE[0] = initialCost_E
    bateryCost = 156 * 4997.9 / USD
    for i in range(1,year,1):
        Cen_C = Cen_C + (Cen_C * yearlyRaise_C)
        Cen_E = Cen_E + (Cen_E * yearlyRaise_E)
        Cm_C = Cm_C + (Cm_C * IPC)
        Cm_E = Cm_E + (Cm_E * IPC)
        bateryCost = bateryCost + (bateryCost * yearlyRaise_batery)
        if i > 2:
            combustionCost = (E * Cen_C)
            electricCost = (E * Cen_E)
            combustionMaintenance = Cm_C
            electricMaintenance = Cm_E
            totalC[i] = initialCost_C + combustionCost + combustionMaintenance + othersC + otherC
            if i==8 or i==16 or i==24:
                totalE[i] = initialCost_E + electricCost + electricMaintenance + othersE + otherE + bateryCost
            else:
                totalE[i] = initialCost_E + electricCost + electricMaintenance + othersE + otherE
            othersC = othersC + (othersC * yearlyRaise_others)
            othersE = othersE + (othersE * yearlyRaise_others)
            otherC = otherC + (otherC * yearlyRaise_others)
            otherE = otherE + (otherE * yearlyRaise_others)
        else:
            combustionCost = (E * Cen_C)
            electricCost = (E * Cen_E)
            combustionMaintenance = Cm_C
            electricMaintenance = Cm_E
            totalC[i] = initialCost_C + combustionCost + combustionMaintenance + othersC
            totalE[i] = initialCost_E + electricCost + electricMaintenance + othersE
            othersC = othersC + (othersC * yearlyRaise_others)
            othersE = othersE + (othersE * yearlyRaise_others)
            otherC = otherC + (otherC * yearlyRaise_others)
            otherE = otherE + (otherE * yearlyRaise_others)
    return totalC, totalE, i

def saveFigure(totalC, totalE, i, E, name):
    years = [*range(0, i+1, 1)]
    plt.plot(years, totalC, label = "convencional")
    plt.plot(years, totalE, label = "eléctrico")
    plt.xlabel('Año')
    plt.ylabel('Costo acumulado [millones COP]')
    plt.title('%d km/año' %E )
    plt.legend()
    plt.grid()
    plt.savefig('comparison/%s.png' %name)
    plt.close()

if __name__ == '__main__':

    import numpy as np
    import json
    import matplotlib.pyplot as plt

    #####################################################################################
    ####### MODELO DE COSTO - TRANSPORTE PUBLICO INDIVIDUAL - MOTOR DE COMBUSTIÓN #######
    #####################################################################################

    ### DEFINICIÓN DE ESCENARIOS - Entregable 2.1.5 Escenarios de simulación ###
    # Porcentaje de carreras diarias promedio por tipo
    tripsNP = 0.5   #trips no periferal to no periferal
    tripsNPP = 0.35 #trips no periferal to periferal / periferal to no periferal
    tripsP = 0.15   #trips periferal to periferal

    # Porcentaje de carreras diarias promedio por hora
    tripsAM = 0.2 #trips in peak AM
    tripsM = 0.1  #trips in peak M
    tripsPM = 0.2 #trips in peak PM
    tripsPO = 0.5 #trips in peak-off

    ### PARÁMETROS - ECUACIÓN MODELO DE COSTO - Entregable 2.1.5 Tabla 5 ###
    # Costos en dólares - Tasa de cambio 1USD = 4997.9 COP - 3/11/2022
    # USD = 4997.9
    USD = 1000000
    costGalonFuel = 8032 / USD
    costkWh = 670.55 / USD
    yearlyRaise_C = 0.0712
    yearlyRaise_E = 0.0660

    costMaintenance_C = 29262970 / USD
    costMaintenance_E = costMaintenance_C * 0.35

    yearlyRaise_others = 0.1
    yearlyRaise_batery = -0.0967

    IPC = 0.0434

    initialCost_C =  65000000 / USD
    initialCost_E = 145000000 / USD

    SOAT_C = 285100  / USD
    tax_C = initialCost_C * 0.01
    otherC = 255682  / USD

    SOAT_E = SOAT_C * 0.9
    tax_E = initialCost_E * 0.01 * 0.4
    otherE = otherC * 0.7

    othersC = SOAT_C + tax_C 
    othersE = SOAT_E + tax_E

    file_C = 'figures/Fuel_mean.json'
    file_E = 'figures/kWh_mean.json'

    #Costo energético promedio por kilómetro - combustion
    CenPeak_C,  CenPeakOff_C =  meanFuelPerKM_C(file_C)
    CenPeak_C = CenPeak_C * costGalonFuel
    CenPeakOff_C =  CenPeakOff_C * costGalonFuel
    Cen_C = (CenPeak_C + CenPeakOff_C)/2

    #Costo energético promedio por kilómetro - electrico
    CenPeak_E,  CenPeakOff_E =  meanFuelPerKM_E(file_E)
    CenPeak_E = CenPeak_E * costkWh
    CenPeakOff_E =  CenPeakOff_E * costkWh
    Cen_E = (CenPeak_E + CenPeakOff_E)/2

    E1 = 35000
    E2 = 60000
    E3 = 84000
    E4 = 51000
    E5 = 208000

    totalC_E11, totalE_E11, i = accumulatedCost1(Cen_C, Cen_E, E1)
    totalC_E21, totalE_E21, i = accumulatedCost1(Cen_C, Cen_E, E2)
    totalC_E31, totalE_E31, i = accumulatedCost1(Cen_C, Cen_E, E3)
    totalC_E41, totalE_E41, i = accumulatedCost1(Cen_C, Cen_E, E4)
    totalC_E51, totalE_E51, i = accumulatedCost1(Cen_C, Cen_E, E5)

    saveFigure(totalC_E11, totalE_E11, i, E1, 'E1')
    saveFigure(totalC_E21, totalE_E21, i, E2, 'E2')
    saveFigure(totalC_E31, totalE_E31, i, E3, 'E3')
    saveFigure(totalC_E41, totalE_E41, i, E4, 'E4')
    saveFigure(totalC_E51, totalE_E51, i, E5, 'E5')

    totalC_E12, totalE_E12, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, E1)
    totalC_E22, totalE_E22, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, E2)
    totalC_E32, totalE_E32, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, E3)
    totalC_E42, totalE_E42, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, E4)
    totalC_E52, totalE_E52, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, E5)

    saveFigure(totalC_E12, totalE_E12, i, E1, 'E1_maintenance')
    saveFigure(totalC_E22, totalE_E22, i, E2, 'E2_maintenance')
    saveFigure(totalC_E32, totalE_E32, i, E3, 'E3_maintenance')
    saveFigure(totalC_E42, totalE_E42, i, E4, 'E4_maintenance')
    saveFigure(totalC_E52, totalE_E52, i, E5, 'E5_maintenance')