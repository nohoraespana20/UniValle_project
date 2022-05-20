def initialize():   
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:   
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumoCmd = ["sumo-gui", "-c", "pasto_config.sumocfg", "--start"]
    traci.start(sumoCmd) # traci.gui.setSchema("View #0", "real world")
    print("Starting SUMO")
    
def getDataPerVehicle(vehicle):
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

def getDataForVehicles(vehicles, data):
    totalDataAllVehicles = []
    for k in range(0,len(vehicles)):
        print('k = ', k)
        speed, CO2, CO, HC, PMx, NOx, Fuel, Noise = [], [], [], [], [], [], [], []

        for i in range(k, np.shape(data)[0],len(vehicles)):
            speed.append(data[i,0])
            CO2.append(data[i,1])
            CO.append(data[i,2])
            HC.append(data[i,3])
            PMx.append(data[i,4])
            NOx.append(data[i,5])
            Fuel.append(data[i,6])
            Noise.append(data[i,7])

        totalData= {"speed_%d"%k : speed, 
                "CO2Emission_%d"%k : CO2, 
                "COEmission_%d"%k : CO, 
                "HCEmission_%d"%k : HC, 
                "PMxEmission_%d"%k : PMx,
                "NOxEmission_%d"%k : NOx,
                "FuelConsumption_%d"%k : Fuel,
                "NoiseEmission_%d"%k : Noise}

        totalDataAllVehicles.append(totalData)
    return totalDataAllVehicles


if __name__ == '__main__':
    import os, sys
    import numpy as np
    import traci
    import traci.constants

    j = 0;
    dataAllVehicle = []
    steeps = 3

    initialize()

    while(j < steeps):
        traci.simulationStep();
        vehicles = traci.vehicle.getIDList();
        for i in range(0,len(vehicles)): 
            traci.vehicle.setSpeedMode(vehicles[i],0)
            dataPerVehicle = getDataPerVehicle(vehicles[i])
            dataAllVehicle.append(dataPerVehicle)
        j = j+1

    dataAllVehicle = np.array(dataAllVehicle)

    totalData = getDataForVehicles(vehicles, dataAllVehicle)
    print(totalData)
    # TODO: include all routes at the simulation
    # TODO: funtion to plot data comparation between the vehicles
    # TODO: repeat the simulations for all EURO types
    traci.close()