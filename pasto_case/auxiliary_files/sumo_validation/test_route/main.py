def initialize(file_config):  
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:   
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumoCmd = ["sumo", "-c", file_config]
    traci.start(sumoCmd)
    print("Starting SUMO")

def get_data_emissions(min_speed, max_speed, steps, norm):
    for c in range(min_speed, max_speed, steps):
        speed = c/3.6
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
            traci.vehicle.setEmissionClass(vehicles[0], norm)

            vehicleData = traci.vehicle.getCO2Emission(vehicles[0])
            CO2Emission.append(vehicleData/1000) #CO2Emission in g units
            distance = traci.vehicle.getDistance(vehicles[0])
            j += 1
        file_name = norm.split('_')[-1]
        print('file name : ', file_name)
        with open(f'C:/Nohora/UniValle_project/test_VehicleConfiguration/emissions_data/data_{c}_{file_name}2.json', 'w') as file:
                json.dump(CO2Emission, file, indent=4)
        
        with open(f'C:/Nohora/UniValle_project/test_VehicleConfiguration/emissions_data/distance_{c}_{file_name}2.json', 'w') as file:
                json.dump(distance/1000, file, indent=4)

        traci.close()   

def get_figures_all(min_speed, max_speed, steps, emission_classes):
    plt.figure(figsize=(10, 5))
    
    for norm in emission_classes:
        CO2_speed = []
        file_name = norm.split('_')[-1]
        
        for c in range(min_speed, max_speed, steps):
            file = f'C:/Nohora/UniValle_project/test_VehicleConfiguration/emissions_data/data_{c}_{file_name}2.json'
            with open(file) as file:
                data = json.load(file)
            
            CO2_abs = sum(data)
            CO2_speed.append(CO2_abs)
        
        file = f'C:/Nohora/UniValle_project/test_VehicleConfiguration/emissions_data/distance_{c}_{file_name}2.json'
        with open(file) as file:
            distance = json.load(file)
        
        g_km = [CO2_speed[i] / distance for i in range(len(CO2_speed))]
        speed_plot = [i for i in range(min_speed, max_speed, steps)]
        
        plt.plot(speed_plot, g_km, label=norm)
    

    plt.title("CO2 Emissions per km vs Speed")
    plt.xlabel("Speed [km/h]")
    plt.ylabel("g/km")
    plt.legend()
    plt.grid()
    
    plt.tight_layout()
    plt.savefig('C:/Nohora/UniValle_project/test_VehicleConfiguration/figures/CO2_all.png')
    plt.show()

if __name__ == '__main__':
    import os, sys
    import traci
    import traci.constants
    import json
    from matplotlib import pyplot as plt
    
    route1_path = 'C:/Nohora/UniValle_project/test_VehicleConfiguration/config1_1.sumocfg'

    min_speed = 1 #km/h
    max_speed = 200 #km/h
    steps = 5 #km/h

    emission_classes = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6ab','HBEFA4/PC_CNG_petrol_Euro-5_(CNG)']
    
    for norm in emission_classes:
        print(norm)
        get_data_emissions(min_speed, max_speed, steps, norm)
    
    get_figures_all(min_speed, max_speed, steps, emission_classes)
