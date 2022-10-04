import numpy as np
import json

distanceTravel = [7.2, 7.0, 4.0] # distancias por tipo de carrera en km
timeTravel = [20.0, 18.0, 14.0] # tiempo usado por tipo de carrera en minutos
costFuel = 7917 # costo de un galon de gasolina en pesos
costOperative = 26241.4 # costo operativo diario en pesos

totalTravels = 39 # numero de carreras diarias

#Ponderado de la cantidad de carreras dependiendo del tipo
ppTravels = totalTravels * 0.5
pnTravels = totalTravels * 0.3
nnTravels = totalTravels * 0.2

distanceTotal = (ppTravels*distanceTravel[0]) + (pnTravels*distanceTravel[1]) + (nnTravels*distanceTravel[2]) # distancia recorrida diaria

totalFuel = distanceTotal*0.26*costFuel/4.023 # costo gasolina diaria

dailyGain = (ppTravels*6700) + (pnTravels*5800) + (nnTravels*5200) #ganancia bruta diaria de un taxi

gain = dailyGain - totalFuel - costOperative # ganancia nets diarias de un taxi


################ MODELO DE COSTO ################

week = 240
weekend = 120

percentageVehicle = 0.8
num_euro2 = 878*percentageVehicle
num_euro3 = 645*percentageVehicle
num_euro4 = 720*percentageVehicle
num_euro5 = 700*percentageVehicle
num_euro6 = 518*percentageVehicle

Dtraveled = [4.023, 2.412, 6.934, 3.460, 5.981, 7.117]
distanceTotal = (4.023 + 2.412)*nnTravels/2 + (6.934 + 3.460)*pnTravels/2 + (5.981 + 7.117)*ppTravels/2
print('\nDistance = ', distanceTotal)

costVehicle = 51500000 #costo inversión de un taxi

file = 'figures\Fuel_mean.json'
with open(file) as file:
    fuelConsumption = json.load(file)
meanFuel = []
for i in range(2):
    for j in range(6):
        meanFuel.append(sum(fuelConsumption[i][j])/len(fuelConsumption[i][j])) 
meanFuelTotal = sum(meanFuel)/len(meanFuel) # promedio de consumo de combustible en galones

Cdepreciation = (costVehicle*0.8)*0.1
Ctax = 400000   #impuesto vehicular anual
Ctires = 4*200000   #cambio de llantas anual
Crepair = 1000000   #costo reparación anual
Cinspection = (701500 + 570500 + 567600 + 456600)/4     #promedio costo seguro anual
Ccare = (7000*365) + (16*300000) + 300000   #lavado, cambio aceite, cambio aceite caja
Cpark = 6000*365 #parqueo anual
Danual = distanceTotal*365  #distancia anual recorrida por un taxi
Cfuel = 2091.45     #costo del litro de gasolina
fcons = (meanFuelTotal*3.785)/distanceTotal  #promedio consumo combustible en litros por kilometro
Cenergy = fcons * Cfuel     #costo promedio de energía por kilometro

def averageCostperKm(file, route):
    with open(file) as file:
        data = json.load(file)
    #CO[hour][route][norm] 
    hourList = []
    for hour in range(2):
        routeList = ((  data[hour][route][0]*num_euro2 + 
                        data[hour][route][1]*num_euro3 + 
                        data[hour][route][2]*num_euro4 + 
                        data[hour][route][3]*num_euro5 + 
                        data[hour][route][4]*num_euro6))
        hourList.append(routeList)
    average = sum(hourList)/2
    avkm = average/distanceTotal
    cost_avkm = avkm*17660/1e+6
    return cost_avkm

Ctco = []
for i in range(len(Dtraveled)):
    costAV_CO_km = averageCostperKm('figures\CO_mean.json',i)
    costAV_HC_km = averageCostperKm('figures\HC_mean.json',i)
    costAV_NOx_km = averageCostperKm('figures\ENOx_mean.json',i)
    costAV_PMx_km = averageCostperKm('figures\PMx_mean.json',i)

    Cext= (costAV_CO_km + costAV_HC_km + costAV_NOx_km + costAV_PMx_km)
    Ctco.append(Dtraveled[i]*(((Cdepreciation+Ctax+Ctires+Crepair+Cinspection+Ccare+Cpark)/Danual) + Cext + Cenergy))


USD = 0.00024 
costTravels_daily = ((Ctco[0]+Ctco[1])*nnTravels + (Ctco[2]+Ctco[3])*pnTravels + (Ctco[4]+Ctco[5])*ppTravels)*3461*0.8
costTravels_mensual = (costTravels_daily*20) + (costTravels_daily * 10/2) 
costTravels_annual = (costTravels_daily*240) + (costTravels_daily * 120/2)
print('\ndaily cost = ', costTravels_daily*USD, ' , mensual cost = ', costTravels_mensual*USD, ' , annual cost = ', costTravels_annual*USD,'\n')

gainTravels_daily = ((ppTravels*6700) + (pnTravels*5800) + (nnTravels*5200))*3461*0.8
gainTravels_mensual = (gainTravels_daily*20) + (gainTravels_daily * 10) 
gainTravels_annual = (gainTravels_daily*240) + (gainTravels_daily * 120)
print('daily gain = ', gainTravels_daily*USD, ' , mensual gain = ', gainTravels_mensual*USD, ' , annual gain = ', gainTravels_annual*USD)

print('\ndaily diff = ', (gainTravels_daily-costTravels_daily)*USD, ' , mensual diff = ', (gainTravels_mensual-costTravels_mensual)*USD, ' , annual diff = ', (gainTravels_annual-costTravels_annual)*USD,'\n')



print('\nCdepreciation = ', Cdepreciation* USD, '\n Ctax = ',Ctax * USD, '\n Ctires = ',Ctires * USD, '\n Crepair = ',Crepair * USD,'\n Cinspection = ',Cinspection * USD, '\n Ccare = ',Ccare * USD, '\n Cpark = ',Cpark* USD, '\n Dannual = ',Danual* USD, '\n Cfuel = ',Cfuel * USD, '\n fcons = ',fcons * USD, '\n Cenergy = ',Cenergy*USD)

print('\n Cext = ', Cext*USD)