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

def accumulatedCost1(Cen_C, Cen_E, Ec, Ee):
    totalC = [*range(0, year, 1)]
    totalE = [*range(0, year, 1)]
    totalC[0] = initialCost_C
    totalE[0] = initialCost_E
    for i in range(1,year,1):
        Cen_C = Cen_C + Cen_C * yearlyRaise_C
        Cen_E = Cen_E + Cen_E * yearlyRaise_E
        combustionCost = (Ec * Cen_C)
        electricCost = (Ee * Cen_E)
        totalC[i] = totalC[i-1] + combustionCost
        totalE[i] = totalE[i-1] + electricCost
    return totalC, totalE, i

def accumulatedCost2(Cen_C, Cen_E, Cm_C, Cm_E, othersC, othersE, otherC, otherE, Ec, Ee):
    totalC = [*range(0, year, 1)]
    totalE = [*range(0, year, 1)]
    totalC[0] = initialCost_C
    totalE[0] = initialCost_E
    bateryCost = 53.6*156 * 4997.9 / USD
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

    ### PARÁMETROS - ECUACIÓN MODELO DE COSTO 
    # Costos en dólares - Tasa de cambio 1USD = 4997.9 COP - 3/11/2022
    # USD = 4997.9
    USD = 1000000
    year = 15
    costGalonFuel = 8932 / USD
    costkWh = 567.34 / USD
    yearlyRaise_C = 0.11
    yearlyRaise_E = 0.0660

    costMaintenance_C = 7227970/ USD
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

    Ec1 = 39000
    Ec2 = 63000
    Ec3 = 105000
    Ec4 = 57000
    
    Ee1 = 45000
    Ee2 = 73000
    Ee3 = 92000
    Ee4 = 62000

    totalC_E11, totalE_E11, i = accumulatedCost1(Cen_C, Cen_E, Ec1, Ee1)
    totalC_E21, totalE_E21, i = accumulatedCost1(Cen_C, Cen_E, Ec2, Ee2)
    totalC_E31, totalE_E31, i = accumulatedCost1(Cen_C, Cen_E, Ec3, Ee3)
    totalC_E41, totalE_E41, i = accumulatedCost1(Cen_C, Cen_E, Ec4, Ee4)

    saveFigure(totalC_E11, totalE_E11, i, Ec1, 'E1')
    saveFigure(totalC_E21, totalE_E21, i, Ec2, 'E2')
    saveFigure(totalC_E31, totalE_E31, i, Ec3, 'E3')
    saveFigure(totalC_E41, totalE_E41, i, Ec4, 'E4')

    totalC_E12, totalE_E12, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, Ec1, Ee1)
    totalC_E22, totalE_E22, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, Ec2, Ee2)
    totalC_E32, totalE_E32, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, Ec3, Ee3)
    totalC_E42, totalE_E42, i = accumulatedCost2(Cen_C, Cen_E, costMaintenance_C, costMaintenance_E, othersC, othersE, otherC, otherE, Ec4, Ee4)

    saveFigure(totalC_E12, totalE_E12, i, Ec1, 'E1_maintenance')
    saveFigure(totalC_E22, totalE_E22, i, Ec2, 'E2_maintenance')
    saveFigure(totalC_E32, totalE_E32, i, Ec3, 'E3_maintenance')
    saveFigure(totalC_E42, totalE_E42, i, Ec4, 'E4_maintenance')