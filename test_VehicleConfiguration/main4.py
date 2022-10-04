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

    min_speed = 1 #km/h
    max_speed = 100 #km/h
    steps = 1 #km/h

    # for c in range(min_speed, max_speed, steps):
    #     speed = c/3.6
    #     print('Speed [m/s] = ', speed)

    #     CO2Emission = []
    #     j = 0
    #     initialize(route1_path)

    #     while traci.simulation.getMinExpectedNumber() > 0:
    #         traci.simulationStep();
    #         vehicles = traci.vehicle.getIDList();
    #         if not vehicles:
    #             break
            
    #         traci.vehicle.setSpeedMode(vehicles[0],0)
    #         traci.vehicle.setSpeed(vehicles[0], speed)
    #         vehicleData = traci.vehicle.getNoiseEmission(vehicles[0])
    #         CO2Emission.append(vehicleData) #CO2Emission in g units
    #         distance = traci.vehicle.getDistance(vehicles[0])
    #         j += 1

    #     with open('emissions_data/data_%s.json'%c, 'w') as file:
    #             json.dump(CO2Emission, file, indent=4)
        
    #     with open('emissions_data/distance.json', 'w') as file:
    #             json.dump(distance/1000, file, indent=4)

    #     traci.close()   
    #     print('Distance travel [km] = ' , distance/1000)
    #     print('Time travel [s] = ', j)

###########################################

    CO2_speed = []
    for c in range(min_speed, max_speed, steps):
        file = 'emissions_data/data_%s.json'%c
        with open(file) as file:
            data = json.load(file)

        CO2_abs = sum(data)*1000/len(data)
        CO2_speed.append(CO2_abs)
    
    file = 'emissions_data/distance.json'
    with open(file) as file:
        distance = json.load(file)

    g_km = []   
    for i in range(len(CO2_speed)):
        g_km.append(CO2_speed[i]/distance)

    
    speed_plot = [i for i in range(min_speed, max_speed, steps)]
    plt.plot(speed_plot, CO2_speed )
    
    plt.title("vClass=taxi / emissionClass=HBEFA3/PC_G_EU2")
    plt.xlabel("Speed [km/h]")
    plt.ylabel("Noise Emissions [dBA]")
    plt.grid()
    plt.savefig('figures/Noise_9.png')
    plt.show()

 