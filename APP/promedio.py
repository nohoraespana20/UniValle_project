import numpy as np
import json

disProm = np.mean([24.5, 31.4, 25.0, 18.1])
print('disProm',disProm)

with open('data_files/TotalResults.json') as file:
                data = json.load(file)

d1 = data["0.35"]["C1Route"]["Diesel"]["CO2"]*1000
d2 = data["0.35"]["C16Route"]["Diesel"]["CO2"]*1000
d3 = data["0.35"]["E1Route"]["Diesel"]["CO2"]*1000
d4 = data["0.35"]["E2Route"]["Diesel"]["CO2"]*1000
d5 = data["0.65"]["C1Route"]["Diesel"]["CO2"]*1000
d6 = data["0.65"]["C16Route"]["Diesel"]["CO2"]*1000
d7 = data["0.65"]["E1Route"]["Diesel"]["CO2"]*1000
d8 = data["0.65"]["E2Route"]["Diesel"]["CO2"]*1000

prom = np.mean([d1,d2,d3,d4,d5,d6,d7,d8])/disProm

print('CO2/km',prom)

d1 = data["0.35"]["C1Route"]["Diesel"]["CO"]
d2 = data["0.35"]["C16Route"]["Diesel"]["CO"]
d3 = data["0.35"]["E1Route"]["Diesel"]["CO"]
d4 = data["0.35"]["E2Route"]["Diesel"]["CO"]
d5 = data["0.65"]["C1Route"]["Diesel"]["CO"]
d6 = data["0.65"]["C16Route"]["Diesel"]["CO"]
d7 = data["0.65"]["E1Route"]["Diesel"]["CO"]
d8 = data["0.65"]["E2Route"]["Diesel"]["CO"]

prom = np.mean([d1,d2,d3,d4,d5,d6,d7,d8])/disProm

print('CO/km',prom)

d1 = data["0.35"]["C1Route"]["Diesel"]["HC"]
d2 = data["0.35"]["C16Route"]["Diesel"]["HC"]
d3 = data["0.35"]["E1Route"]["Diesel"]["HC"]
d4 = data["0.35"]["E2Route"]["Diesel"]["HC"]
d5 = data["0.65"]["C1Route"]["Diesel"]["HC"]
d6 = data["0.65"]["C16Route"]["Diesel"]["HC"]
d7 = data["0.65"]["E1Route"]["Diesel"]["HC"]
d8 = data["0.65"]["E2Route"]["Diesel"]["HC"]

prom = np.mean([d1,d2,d3,d4,d5,d6,d7,d8])/disProm

print('HC/km',prom)

d1 = data["0.35"]["C1Route"]["Diesel"]["PMx"]
d2 = data["0.35"]["C16Route"]["Diesel"]["PMx"]
d3 = data["0.35"]["E1Route"]["Diesel"]["PMx"]
d4 = data["0.35"]["E2Route"]["Diesel"]["PMx"]
d5 = data["0.65"]["C1Route"]["Diesel"]["PMx"]
d6 = data["0.65"]["C16Route"]["Diesel"]["PMx"]
d7 = data["0.65"]["E1Route"]["Diesel"]["PMx"]
d8 = data["0.65"]["E2Route"]["Diesel"]["PMx"]

prom = np.mean([d1,d2,d3,d4,d5,d6,d7,d8])/disProm

print('PMx/km',prom)

d1 = data["0.35"]["C1Route"]["Diesel"]["NOx"]
d2 = data["0.35"]["C16Route"]["Diesel"]["NOx"]
d3 = data["0.35"]["E1Route"]["Diesel"]["NOx"]
d4 = data["0.35"]["E2Route"]["Diesel"]["NOx"]
d5 = data["0.65"]["C1Route"]["Diesel"]["NOx"]
d6 = data["0.65"]["C16Route"]["Diesel"]["NOx"]
d7 = data["0.65"]["E1Route"]["Diesel"]["NOx"]
d8 = data["0.65"]["E2Route"]["Diesel"]["NOx"]

prom = np.mean([d1,d2,d3,d4,d5,d6,d7,d8])/disProm

print('NOx/km',prom)

energyProm = np.mean([4.652937083116812,5.604756459785072,4.657235275631403,3.358411729588637,4.781755856094416,5.73763628064332,4.802046526926851,3.4390207133665034])

print('energyProm',energyProm)

fuelProm1 = np.mean([
            9.040244307958245, 
            8.75446776432504, 
            8.882940686315456, 
            9.765301032415309, 
            9.412104562164004
        ])
 
fuelProm2 = np.mean([
            9.729775961295198, 
            10.421237765029419, 
            10.014606325325525, 
            9.436544190251478, 
            9.737270249872632
        ])

fuelProm3 = np.mean([
            8.543268819941911, 
            8.478979864330473, 
            8.539676933277198, 
            9.10768607647145, 
            8.532360291214486
        ])

fuelProm4 = np.mean([
            7.830838645532862, 
            8.7753188024712, 
            8.984887023258707, 
            7.819360554837972, 
            7.744853995059517
        ])

fuelProm5 = np.mean([
            11.851499333088343, 
            11.994663992310862, 
            12.414603541467763, 
            12.411374913062243, 
            12.376811293807922
        ])

fuelProm6 = np.mean([
            13.617732727108892, 
            13.662865072618333, 
            13.486455630915652, 
            13.43738801820138, 
            13.968749994825338
        ])

fuelProm7 = np.mean([
            12.2009348671167, 
            11.730330495601047, 
            12.017956327587784, 
            12.83292153641041, 
            12.103753240885023
        ])

fuelProm8 = np.mean([
            10.49791776974887, 
            10.329909090700019, 
            10.563191703442312, 
            10.164052729441014, 
            10.693074567158057
        ])

fuelProm = np.mean([fuelProm1,fuelProm2,fuelProm3,fuelProm4,fuelProm5,fuelProm6,fuelProm7,fuelProm8])

print('fuelProm',fuelProm)

EVco2 = energyProm*164.38/disProm

print('EVco2',EVco2)