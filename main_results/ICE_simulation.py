def initialize(file_config):  
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:   
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumoCmd = ["sumo", "-c", file_config]
    traci.start(sumoCmd)
    print("Starting SUMO")
    
def getDataEmissions(vehicle):
    speed = traci.vehicle.getSpeed(vehicle)
    CO2Emission = traci.vehicle.getCO2Emission(vehicle)
    COEmission = traci.vehicle.getCOEmission(vehicle)
    HCEmission = traci.vehicle.getHCEmission(vehicle)
    PMxEmission = traci.vehicle.getPMxEmission(vehicle)
    NOxEmission = traci.vehicle.getNOxEmission(vehicle)
    FuelConsumption = traci.vehicle.getFuelConsumption(vehicle)
    NoiseEmission = traci.vehicle.getNoiseEmission(vehicle)
    distance = traci.vehicle.getDistance(vehicle)

    dataEmissions = [speed, CO2Emission, COEmission, HCEmission, PMxEmission, 
                     NOxEmission, FuelConsumption, NoiseEmission, distance]

    return dataEmissions

def saveDataVehicle(file_config, route):
    emission_classes = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6d']
    
    for emission_class in emission_classes:
        step = 0;
        initialize(file_config)
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep();
            vehicles = traci.vehicle.getIDList();
            
            for i in range(len(vehicles)):
                traci.vehicle.setSpeedMode(vehicles[i],0) 
                traci.vehicle.setEmissionClass(vehicles[0], emission_class)
            
            if not vehicles:
                print("Vehicles is empty")
            else:
                if vehicles[0]!='1':
                    break
                data = getDataEmissions(vehicles[0])
                with open('data_emissions.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([route, emission_class, step, data[0], 
                                     data[1], data[2], data[3], data[4], 
                                     data[5], data[6], data[7], data[8]])
            step = step + 1
        traci.close()

if __name__ == '__main__':
    import os, sys
    import traci
    import traci.constants
    import csv

    routesPaths = ['config_files/config1.sumocfg','config_files/config2.sumocfg',
                   'config_files/config3.sumocfg','config_files/config4.sumocfg',
                   'config_files/config5.sumocfg','config_files/config6.sumocfg']
    
    field = ["route", "emission_class", "step", "speed", "CO2Emission", "COEmission", 
             "HCEmission", "PMxEmission", "NOxEmission", "FuelConsumption", 
             "NoiseEmission", "distance"]
    with open('data_emissions.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(field)
    
    for file_config in routesPaths:
        route = file_config.split("/", 3)[1].split(".",2)[0][6]
        print('Route: ', route)
        saveDataVehicle(file_config, route)