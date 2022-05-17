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
total_CO2 = []
total_CO = []
total_HC = []
total_PMx = []
total_NOx = []
total_Fuel = []
total_Noise = []

while(j<2000):
    traci.simulationStep();
    
    vehicles = traci.vehicle.getIDList();
    
    for i in range(0,len(vehicles)): 

        traci.vehicle.setSpeedMode(vehicles[i],0)
        print('Vehicle ID = ', vehicles[i])
        #get actual speed, emission, edge ID and total distance travelled of vehicles

        speed = traci.vehicle.getSpeed(vehicles[i])
        C02Emission = traci.vehicle.getCO2Emission(vehicles[i])
        C0Emission = traci.vehicle.getCOEmission(vehicles[i])
        HCEmission = traci.vehicle.getHCEmission(vehicles[i])
        PMxEmission = traci.vehicle.getPMxEmission(vehicles[i])
        NOxEmission = traci.vehicle.getNOxEmission(vehicles[i])
        FuelConsumption = traci.vehicle.getFuelConsumption(vehicles[i])
        NoiseEmission = traci.vehicle.getNoiseEmission(vehicles[i])
        EdgeID = traci.vehicle.getRoadID(vehicles[i])
        Distance = traci.vehicle.getDistance(vehicles[i])
        
        total_speed.append(speed)
        total_CO2.append(C02Emission)
        total_CO.append(C0Emission)
        total_HC.append(HCEmission)
        total_PMx.append(PMxEmission)
        total_NOx.append(NOxEmission)
        total_Fuel.append(FuelConsumption)
        total_Noise.append(NoiseEmission)

        # print("Speed ", vehicles[i], ": ",speed, " m/s")
        # print("CO2Emission ", vehicles[i], ": ",  C02Emission, " mg/s")
        # print("EdgeID of veh ", vehicles[i], ": ", EdgeID )
        # print('Distance ', vehicles[i], ": ", Distance, " m")

    # with open('total_speed.txt', 'w') as f:
    #     for data in total_speed:
    #         f.write(data)
    #         f.write('\n')

    print('Time ', len(total_speed), 's')
    print('Mean total speed = ', np.mean(total_speed))
    print('Total CO2 = ', np.sum(total_CO2))

    j = j+1

traci.close()