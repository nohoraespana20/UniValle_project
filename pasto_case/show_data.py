def total_per_trip(data, route, emission_class):
    routee = data[data["route"] == route]
    route_class = routee[routee["emission_class"] == emission_class]

    step_route = route_class.iloc[-1, route_class.columns.get_loc("step")]
    distance_route = route_class.iloc[-1, route_class.columns.get_loc("distance")]/1E3 #Distance in km
    
    total_CO2 = route_class["CO2Emission"].sum()/1E6 #Emission in kg
    total_CO = route_class["COEmission"].sum()/1E6 #Emission in kg
    total_HC = route_class["HCEmission"].sum()/1E6 #Emission in kg
    total_PMx = route_class["PMxEmission"].sum()/1E6 #Emission in kg
    total_NOx = route_class["NOxEmission"].sum()/1E6 #Emission in kg
    total_fuel = route_class["FuelConsumption"].sum()*(0.000264) #Fuel in gallons
    total_noise = route_class["NoiseEmission"].sum()/step_route  # Mean noise in dB
    return [route, emission_class, distance_route, total_CO2, total_CO, total_HC, total_PMx, total_NOx, total_fuel, total_noise]
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pandas as pd

    data_emissions = pd.read_csv("./results/rush/data_emissions_ICE.csv")

    routes = [1, 2, 3, 4, 5, 6]
    category = ['route','emission_class','distance [km]', 'CO2 [kg]', 'CO [kg]', 'HC [kg]', 'PMx [kg]', 'NOx [kg]', 'fuel [gl]', 'noise [dB]']
    emission_classes = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6d']
    total_emission_routes = []
    for route in routes:
        for emission in emission_classes:
            total_route = total_per_trip(data_emissions, route, emission)
            total_emission_routes.append(total_route)
    total_emission_routes = pd.DataFrame(total_emission_routes,columns=category)
    distances = total_emission_routes.iloc[[0,5,10,15,20,25], 2]
    print('HORA PICO')
    print(distances)
    route1 = total_emission_routes.iloc[20:25, [0,1,3,4,5,6,7,8]]
    print(route1)

    data_emissions = pd.read_csv("./results/off_peak/data_emissions_ICE.csv")

    routes = [1, 2, 3, 4, 5, 6]
    category = ['route','emission_class','distance [km]', 'CO2 [kg]', 'CO [kg]', 'HC [kg]', 'PMx [kg]', 'NOx [kg]', 'fuel [gl]', 'noise [dB]']
    emission_classes = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6d']
    total_emission_routes = []
    for route in routes:
        for emission in emission_classes:
            total_route = total_per_trip(data_emissions, route, emission)
            total_emission_routes.append(total_route)
    total_emission_routes = pd.DataFrame(total_emission_routes,columns=category)
    distances = total_emission_routes.iloc[[0,5,10,15,20,25], 2]
    print('HORA VALLE')
    print(distances)
    route1 = total_emission_routes.iloc[20:25, [0,1,3,4,5,6,7,8]]
    print(route1)