def initialize(file_config):  
    print(file_config)
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:   
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumoCmd = ["sumo-gui", "-c", file_config, "--start", "--quit-on-end"]
    traci.start(sumoCmd)
    print("Starting SUMO")
    
def getDataEmissions(vehicle):
    speed = traci.vehicle.getSpeed(vehicle)
    # CO2Emission = traci.vehicle.getCO2Emission(vehicle)
    # COEmission = traci.vehicle.getCOEmission(vehicle)
    # HCEmission = traci.vehicle.getHCEmission(vehicle)
    # PMxEmission = traci.vehicle.getPMxEmission(vehicle)
    # NOxEmission = traci.vehicle.getNOxEmission(vehicle)
    # FuelConsumption = traci.vehicle.getFuelConsumption(vehicle)
    FuelConsumption = traci.vehicle.getElectricityConsumption(vehicle)
    NoiseEmission = traci.vehicle.getNoiseEmission(vehicle)

    dataEmissions = [speed, CO2Emission, COEmission, HCEmission, PMxEmission, NOxEmission, FuelConsumption, NoiseEmission]

    return dataEmissions

def getDataPerVehicle(vehicles,step):
    global vehicle

    if not vehicles:
        print("Vehicles is empty")
    else:
        data = getDataEmissions(vehicles[0])
        distance = traci.vehicle.getDistance(vehicles[0])
        speed.append(data[0])
        # CO2Emission.append(data[1])
        # COEmission.append(data[2])
        # HCEmission.append(data[3])
        # PMxEmission.append(data[4])
        # NOxEmission.append(data[5])
        FuelConsumption.append(data[6])
        NoiseEmission.append(data[7])
                
        vehicle = { 'speed': speed,
                    # 'CO2Emission': CO2Emission,
                    # 'COEmission': COEmission,
                    # 'HCEmission': HCEmission,
                    # 'PMxEmission': PMxEmission,
                    # 'NOxEmission': NOxEmission,
                    'FuelConsumption': FuelConsumption,
                    'NoiseEmission': NoiseEmission,
                    'Step' : step,
                    'Distance' : distance
                }
            
    if not vehicle:
        print("Data vehicle is empty")
    else:
        return vehicle

def saveDataVehicle(file_config):
    j = 0;
    global speed, CO2Emission, COEmission, HCEmission, PMxEmission, NOxEmission, FuelConsumption, NoiseEmission 
    speed, CO2Emission, COEmission, HCEmission, PMxEmission, NOxEmission, FuelConsumption, NoiseEmission = [], [], [], [], [], [], [], []
    initialize(file_config)
    x = file_config.split("/", 3)[2].split(".",2)[0]
    print(x)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep();
        vehicles = traci.vehicle.getIDList();
        for i in range(len(vehicles)):
            traci.vehicle.setSpeedMode(vehicles[i],0)
        vehicleData = getDataPerVehicle(vehicles,j)
        j = j+1

    with open('results2/data_%s.json'%x, 'w') as file:
            json.dump(vehicleData, file, indent=4)
    traci.close()

if __name__ == '__main__':
    import os, sys
    import traci
    import traci.constants
    import json
    
    route1_paths = ['config_files2/route1/config1_1.sumocfg']

    route2_paths = ['config_files2/route2/config2_1.sumocfg']
    
    route3_paths = ['config_files2/route3/config3_1.sumocfg']
    
    route4_paths = ['config_files2/route4/config4_1.sumocfg']

    route5_paths = ['config_files2/route5/config5_1.sumocfg']

    route6_paths = ['config_files2/route6/config6_1.sumocfg']

    routesPaths = [route1_paths, route2_paths, route3_paths, route4_paths, route5_paths, route6_paths]

    for k in routesPaths:
        for i in k:
            saveDataVehicle(i)