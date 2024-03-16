def initialize(file_config):  
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:   
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumoCmd = ["sumo", "-c", file_config]
    traci.start(sumoCmd)
    print("Starting SUMO")

#TODO: Include EV data - kWh
def getDataEmissions(vehicle):
    speed = traci.vehicle.getSpeed(vehicle)
    CO2Emission = traci.vehicle.getCO2Emission(vehicle)
    COEmission = traci.vehicle.getCOEmission(vehicle)
    HCEmission = traci.vehicle.getHCEmission(vehicle)
    PMxEmission = traci.vehicle.getPMxEmission(vehicle)
    NOxEmission = traci.vehicle.getNOxEmission(vehicle)
    FuelConsumption = traci.vehicle.getFuelConsumption(vehicle)
    ElectricityConsumption = traci.vehicle.getElectricityConsumption(vehicle)
    NoiseEmission = traci.vehicle.getNoiseEmission(vehicle)
    distance = traci.vehicle.getDistance(vehicle)

    dataEmissions = [speed, CO2Emission, COEmission, HCEmission, PMxEmission, NOxEmission, 
                     FuelConsumption, ElectricityConsumption, NoiseEmission, distance]

    return dataEmissions

def saveDataVehicle(file_config, route, hour):
    emission_classes = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6d','Energy/unknown']
    
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
                if emission_class == 'Energy/unknown':
                    if hour == 'rush':
                        with open('results/rush/data_emissions_EV.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([route, emission_class, step, data[0], 
                                            data[1], data[2], data[3], data[4], 
                                            data[5], data[6], data[7], data[8], data[9]])
                    else:
                        with open('results/off_peak/data_emissions_EV.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([route, emission_class, step, data[0], 
                                            data[1], data[2], data[3], data[4], 
                                            data[5], data[6], data[7], data[8], data[9]])
                else: 
                    if hour == 'rush':
                        with open('results/rush/data_emissions_ICE.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([route, emission_class, step, data[0], 
                                            data[1], data[2], data[3], data[4], 
                                            data[5], data[6], data[7], data[8], data[9]])
                    else:
                        with open('results/off_peak/data_emissions_ICE.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([route, emission_class, step, data[0], 
                                            data[1], data[2], data[3], data[4], 
                                            data[5], data[6], data[7], data[8], data[9]])
            step = step + 1
        traci.close()

if __name__ == '__main__':
    import os, sys
    import traci
    import traci.constants
    import csv

    routesPaths_rush = ['config_files/rush/config1.sumocfg','config_files/rush/config2.sumocfg',
                        'config_files/rush/config3.sumocfg','config_files/rush/config4.sumocfg',
                        'config_files/rush/config5.sumocfg','config_files/rush/config6.sumocfg']
    
    routesPaths_offPeak = ['config_files/off_peak/config1.sumocfg','config_files/off_peak/config2.sumocfg',
                            'config_files/off_peak/config3.sumocfg','config_files/off_peak/config4.sumocfg',
                            'config_files/off_peak/config5.sumocfg','config_files/off_peak/config6.sumocfg']
    
    field = ["route", "emission_class", "step", "speed", "CO2Emission", "COEmission", 
             "HCEmission", "PMxEmission", "NOxEmission", "FuelConsumption","ElectricityConsumption", 
             "NoiseEmission", "distance"]
    
    with open('results/rush/data_emissions_EV.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(field)
    with open('results/rush/data_emissions_ICE.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(field)
    with open('results/off_peak/data_emissions_EV.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(field)
    with open('results/off_peak/data_emissions_ICE.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(field)
    
    for file_config in routesPaths_rush:
        route = file_config.split("/", 3)[2].split(".",2)[0][6]
        print('Route: ', route)
        saveDataVehicle(file_config, route, 'rush')
    for file_config in routesPaths_offPeak:
        route = file_config.split("/", 3)[2].split(".",2)[0][6]
        print('Route: ', route)
        saveDataVehicle(file_config, route, 'off_peak')