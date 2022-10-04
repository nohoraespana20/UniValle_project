def initialize(file_config):  
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:   
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumoCmd = ["sumo-gui", "-c", file_config, "--start", "--quit-on-end"]
    traci.start(sumoCmd)
    print("Starting SUMO")
    
if __name__ == '__main__':
    import os, sys
    import traci
    import traci.constants
    import json
    from matplotlib import pyplot as plt
    
    route1_path = 'config1_1.sumocfg'

    min_speed = 10 #km/h
    max_speed = 400 #km/h
    steps = 5 #km/h

    for c in range(min_speed, max_speed, steps):
        speed = c/3.6
        print('Speed [m/s] = ', speed)

        CO2Emission = []
        j = 0
        initialize(route1_path)

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep();
            vehicles = traci.vehicle.getIDList();
            if not vehicles:
                break
            
            traci.vehicle.setSpeedMode(vehicles[0],0)
            traci.vehicle.setSpeed(vehicles[0], speed)
            vehicleData = traci.vehicle.getCO2Emission(vehicles[0])
            CO2Emission.append(vehicleData/1000) #CO2Emission in g units
            distance = traci.vehicle.getDistance(vehicles[0])
            j += 1

        with open('emissions_data/data_%s.json'%c, 'w') as file:
                json.dump(CO2Emission, file, indent=4)
        
        with open('emissions_data/distance.json', 'w') as file:
                json.dump(distance/1000, file, indent=4)

        traci.close()   
        print('Distance travel [km] = ' , distance/1000)
        print('Time travel [s] = ', j)

###########################################

    CO2_speed = []
    for c in range(min_speed, max_speed, steps):
        file = 'emissions_data/data_%s.json'%c
        with open(file) as file:
            data = json.load(file)

        CO2_abs = sum(data)
        CO2_speed.append(CO2_abs)
    
    file = 'emissions_data/distance.json'
    with open(file) as file:
        distance = json.load(file)

    g_km = []   
    for i in range(len(CO2_speed)):
        g_km.append(CO2_speed[i]/distance)

    
    speed_plot = [i for i in range(min_speed, max_speed, steps)]
    plt.plot(speed_plot, CO2_speed )
    
    plt.title("vClass=bus / emissionClass=HBEFA3/PC_G_EU6")
    plt.xlabel("Speed [km/h]")
    plt.ylabel("CO2 Emissions [g]")
    plt.grid()
    plt.savefig('figures/CO2_7.png')
    plt.show()

    plt.plot(speed_plot, g_km )
    
    plt.title("vClass=taxi / emissionClass=HBEFA3/PC_G_EU6")
    plt.xlabel("Speed [km/h]")
    plt.ylabel("g/km")
    plt.grid()
    plt.savefig('figures/g_km_7.png')
    plt.show()











quit()
def getDataEmissions(vehicle):
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

def getDataPerVehicle(vehicles, step):
    global vehicle

    if not vehicles:
        print("Vehicles is empty")
    else:
        data = getDataEmissions(vehicles[0])
        distance = traci.vehicle.getDistance(vehicles[0])
        speed.append(data[0])
        CO2Emission.append(data[1])
        COEmission.append(data[2])
        HCEmission.append(data[3])
        PMxEmission.append(data[4])
        NOxEmission.append(data[5])
        FuelConsumption.append(data[6])
        NoiseEmission.append(data[7])
                
        vehicle = { 'speed': speed,
                    'CO2Emission': CO2Emission,
                    'COEmission': COEmission,
                    'HCEmission': HCEmission,
                    'PMxEmission': PMxEmission,
                    'NOxEmission': NOxEmission,
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

    with open('results1/data_%s.json'%x, 'w') as file:
            json.dump(vehicleData, file, indent=4)
    traci.close()