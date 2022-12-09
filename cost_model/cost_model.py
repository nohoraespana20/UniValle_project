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

def totalAnnualCostTrips(VACATIONS):
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

if __name__ == '__main__':

    import numpy as np
    import json

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
    Cd = 2401.01
    Ctx = 84.17
    Cti = 194.88
    Cr = 1446.22
    Ci = 250.2
    Cc = 730.31
    Cp = 167.07
    Cen = 0.05
    Dt = [3.2, 5.3, 6.6]
    Da = [46800, 54600, 62400]

    #Ecuación de costo
    Ctco = [] #Costo total de propiedad por carrera
    for i in range(len(Dt)):
        for j in range(len(Da)): 
            cto= Dt[i] * (((Cd + Ctx + Cti + Cr + Ci + Cc + Cp) / Da[j]) - Cen)
            Ctco.append(cto)
    Ctco = np.reshape(Ctco, (3,3))

    ### DEFINICIÓN DE PRECIO, COSTO DE VIAJES Y GANANCIA NETA ###
    VACATIONS = True
    HOLIDAYS = True

    print('Price COP')
    print(totalPriceAnnualTrips(VACATIONS, HOLIDAYS)[1])
    print('Ganancia bruta = ', sum(totalPriceAnnualTrips(VACATIONS, HOLIDAYS)[1]))

    print('\nCost COP')
    print(totalAnnualCostTrips(VACATIONS)[1])
    print('Costo total = ', sum(totalAnnualCostTrips(VACATIONS)[1]))

    print('\nGanancia neta COP')
    print('Ganancia neta = ', sum(totalPriceAnnualTrips(VACATIONS, HOLIDAYS)[1]) - sum(totalAnnualCostTrips(VACATIONS)[1]))