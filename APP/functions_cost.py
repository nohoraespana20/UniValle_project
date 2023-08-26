import numpy as np
import json
import matplotlib.pyplot as plt

def meanFuelPerKM_C(file):
    with open(file) as file:
        fuelConsumption = json.load(file)
    fuel = []
    for i in range(2):
        for j in range(4):
            fuel.append(fuelConsumption[i][j][1]) # Solo EURO 3

    fuel = np.reshape(fuel,(2,4))
    fuelPerTypePeakOff = fuel[0][0:]
    fuelPerTypePeak = fuel[1][0:]
    
    #Distance data from results of emissions simulation
    distances = [24.5*6, 31.4*6, 25.0*6, 18.1*6] # C1, C16, E1, E2
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
        for j in range(4):
            fuel.append(fuelConsumption[i][j][0]) 
    fuel = np.reshape(fuel,(2,4))
    fuelPerTypePeakOff = fuel[0][0:]
    fuelPerTypePeak = fuel[1][0:]
    
    #Distance data from results of emissions simulation
    distances = [24.5*6, 31.4*6, 25.0*6, 18.1*6] # C1, C16, E1, E2
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

# def accumulatedCost2(initialCost_C, initialCost_E, currency, year, yearlyRaise_C,yearlyRaise_E,IPC,yearlyRaise_batery,yearlyRaise_others, Cen_C, Cen_E, Cm_C, Cm_E, othersC, othersE, otherC, otherE, Ec, Ee, batery_capacity):
def accumulatedCost2(initialCost_C, yearlyRaise_C, Cen_C, Cm_C, othersC, otherC, yearlyRaise_others,
                     initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, Cm_E, othersE, otherE, batery_capacity, 
                     currency, year, IPC, Ec):
    
    initialCost_C =  initialCost_C / currency
    Cm_C = Cm_C / currency 
    Cen_C = Cen_C / currency
    othersC = othersC / currency
    otherC = otherC / currency

    initialCost_E = initialCost_E / currency
    Cen_E = Cen_E / currency
    Cm_E = Cm_E / currency
    othersE = otherE / currency
    otherE = otherE / currency

    Ee = Ec 
    totalC = []
    totalE = []
    totalC = [*range(0, year, 1)]
    totalE = [*range(0, year, 1)]
    totalC[0] = initialCost_C
    totalE[0] = initialCost_E
    #capacidad bateria: 53.6 kWh # USD 156/kWh # tasa de cambio dolar 4997.9 # USD cambio a millones de pesos
    bateryCost = batery_capacity * 156 * 4997.9 / currency 
    for i in range(1,year,1):
        Cen_C = Cen_C + (Cen_C * yearlyRaise_C)
        Cen_E = Cen_E + (Cen_E * yearlyRaise_E)
        Cm_C = Cm_C + (Cm_C * IPC)
        Cm_E = Cm_E + (Cm_E * IPC)
        bateryCost = bateryCost + (bateryCost * yearlyRaise_batery)
        if i > 2:
            combustionCost = (Ec * Cen_C)
            electricCost = (Ee * Cen_E)
            combustionMaintenance = Cm_C
            electricMaintenance = Cm_E
            totalC[i] = totalC[i-1] + combustionCost + combustionMaintenance + othersC + otherC
            if i==8 or i==16 or i==24:
                totalE[i] = totalE[i-1] + electricCost + electricMaintenance + othersE + otherE + bateryCost
            else:
                totalE[i] = totalE[i-1] + electricCost + electricMaintenance + othersE + otherE
            othersC = othersC + (othersC * yearlyRaise_others)
            othersE = othersE + (othersE * yearlyRaise_others)
            otherC = otherC + (otherC * yearlyRaise_others)
            otherE = otherE + (otherE * yearlyRaise_others)
        else:
            combustionCost = (Ec * Cen_C)
            electricCost = (Ee * Cen_E)
            combustionMaintenance = Cm_C
            electricMaintenance = Cm_E
            totalC[i] = totalC[i-1] + combustionCost + combustionMaintenance + othersC
            totalE[i] = totalE[i-1] + electricCost + electricMaintenance + othersE
            othersC = othersC + (othersC * yearlyRaise_others)
            othersE = othersE + (othersE * yearlyRaise_others)
            otherC = otherC + (otherC * yearlyRaise_others)
            otherE = otherE + (otherE * yearlyRaise_others)
    return totalC, totalE, i

def accumulatedPerYear(initialCost_C, yearlyRaise_C, Cen_C, Cm_C, othersC, otherC, yearlyRaise_others,
                     initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, Cm_E, othersE, otherE, batery_capacity, 
                     currency, year, IPC, Ec):
    
    initialCost_C =  initialCost_C / currency
    Cm_C = Cm_C / currency 
    Cen_C = Cen_C / currency
    othersC = othersC / currency
    otherC = otherC / currency

    initialCost_E = initialCost_E / currency
    Cen_E = Cen_E / currency
    Cm_E = Cm_E / currency
    othersE = otherE / currency
    otherE = otherE / currency

    Ee = Ec 
    totalC = []
    totalE = []
    totalC = [*range(0, year, 1)]
    totalE = [*range(0, year, 1)]
    totalC[0] = initialCost_C
    totalE[0] = initialCost_E
    #capacidad bateria: 53.6 kWh # USD 156/kWh # tasa de cambio dolar 4997.9 # USD cambio a millones de pesos
    bateryCost = batery_capacity * 156 * 4997.9 / currency 
    for i in range(1,year,1):
        Cen_C = Cen_C + (Cen_C * yearlyRaise_C)
        Cen_E = Cen_E + (Cen_E * yearlyRaise_E)
        Cm_C = Cm_C + (Cm_C * IPC)
        Cm_E = Cm_E + (Cm_E * IPC)
        bateryCost = bateryCost + (bateryCost * yearlyRaise_batery)
        if i > 2:
            combustionCost = (Ec * Cen_C)
            electricCost = (Ee * Cen_E)
            combustionMaintenance = Cm_C
            electricMaintenance = Cm_E
            totalC[i] = totalC[i] + combustionCost + combustionMaintenance + othersC + otherC
            if i==8 or i==16 or i==24:
                totalE[i] = totalE[i] + electricCost + electricMaintenance + othersE + otherE + bateryCost
            else:
                totalE[i] = totalE[i] + electricCost + electricMaintenance + othersE + otherE
            othersC = othersC + (othersC * yearlyRaise_others)
            othersE = othersE + (othersE * yearlyRaise_others)
            otherC = otherC + (otherC * yearlyRaise_others)
            otherE = otherE + (otherE * yearlyRaise_others)
        else:
            combustionCost = (Ec * Cen_C)
            electricCost = (Ee * Cen_E)
            combustionMaintenance = Cm_C
            electricMaintenance = Cm_E
            totalC[i] = totalC[i] + combustionCost + combustionMaintenance + othersC
            totalE[i] = totalE[i] + electricCost + electricMaintenance + othersE
            othersC = othersC + (othersC * yearlyRaise_others)
            othersE = othersE + (othersE * yearlyRaise_others)
            otherC = otherC + (otherC * yearlyRaise_others)
            otherE = otherE + (otherE * yearlyRaise_others)
    return totalC, totalE, i