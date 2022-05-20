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

total_data = []

steeps = 3

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

while(j < steeps):
    traci.simulationStep();
    
    vehicles = traci.vehicle.getIDList();
    for i in range(0,len(vehicles)): 

        traci.vehicle.setSpeedMode(vehicles[i],0)
        data_vehicle = getData_vehicle(vehicles[i])
        total_data.append(data_vehicle)
    j = j+1

total_data = np.array(total_data)

for k in range(0,len(vehicles)):
    speed = []
    CO2 = []
    CO = []
    HC = []
    PMx = []
    NOx = []
    Fuel = []
    Noise = []
    for i in range(k, np.shape(total_data)[0],len(vehicles)):
        speed.append(total_data[i,0])
        CO2.append(total_data[i,1])
        CO.append(total_data[i,2])
        HC.append(total_data[i,3])
        PMx.append(total_data[i,4])
        NOx.append(total_data[i,5])
        Fuel.append(total_data[i,6])
        Noise.append(total_data[i,7])

    data = {"speed_%d"%k : speed, 
            "CO2Emission_%d"%k : CO2, 
            "COEmission_%d"%k : CO, 
            "HCEmission_%d"%k : HC, 
            "PMxEmission_%d"%k : PMx,
            "NOxEmission_%d"%k : NOx,
            "FuelConsumption_%d"%k : Fuel,
            "NoiseEmission_%d"%k : Noise}

    print(data)

traci.close()