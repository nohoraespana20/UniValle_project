import os, sys
import time
import numpy as np

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")
    
import traci
import traci.constants

sumoCmd = ["sumo-gui", "-c", "pasto_config.sumocfg", "--start"]
traci.start(sumoCmd)
print("Starting SUMO")
# traci.gui.setSchema("View #0", "real world")
    
j = 0;
total_speed = []
total_C02 = []
total_C0 = []
total_HC = []
total_PMx = []
total_NOx = []
total_Fuel = []
total_Noise = []

def getData_vehicle(vehicle):
    speed = traci.vehicle.getSpeed(vehicle)
    CO2Emission = traci.vehicle.getCO2Emission(vehicle)
    COEmission = traci.vehicle.getCOEmission(vehicle)
    HCEmission = traci.vehicle.getHCEmission(vehicle)
    PMxEmission = traci.vehicle.getPMxEmission(vehicle)
    NOxEmission = traci.vehicle.getNOxEmission(vehicle)
    FuelConsumption = traci.vehicle.getFuelConsumption(vehicle)
    NoiseEmission = traci.vehicle.getNoiseEmission(vehicle)

    dataEmissions = [speed, CO2Emission, COEmission, HCEmission, PMxEmission, NOxEmission, FuelConsumption, NoiseEmission]

    return dataEmissions

while(j<6):
    traci.simulationStep();
    
    vehicles = traci.vehicle.getIDList();
    for i in range(0,len(vehicles)): 

        traci.vehicle.setSpeedMode(vehicles[i],0)
        
        speed = traci.vehicle.getSpeed(vehicles[i])
        
        total_speed.append(speed)


    j = j+1

print(total_speed)
for j in range(0,len(vehicles)):
    s = []
    # print(len(total_speed))
    # print(len(vehicles))
    for i in range(0, len( total_speed), len(vehicles)):
        s.append(total_speed[i])
    data = {"ID_%d"%j+1 : s}
    print(data)

traci.close()