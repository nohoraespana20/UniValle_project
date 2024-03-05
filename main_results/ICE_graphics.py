def mean_calculate(data, route, emission_class):
    route = data[data["route"] == route]
    route_class = route[route["emission_class"] == emission_class]

    step_route = route_class.iloc[-1, route_class.columns.get_loc("step")]
    distance_route = route_class.iloc[-1, route_class.columns.get_loc("distance")]/1E3
    
    total_CO2 = route_class["CO2Emission"].sum()/1E6
    total_CO = route_class["COEmission"].sum()/1E6
    total_HC = route_class["HCEmission"].sum()/1E6
    total_PMx = route_class["PMxEmission"].sum()/1E6
    total_NOx = route_class["NOxEmission"].sum()/1E6
    total_fuel = route_class["FuelConsumption"].sum()*(2.642e-7)
    total_noise = route_class["NoiseEmission"].sum()/step_route
    return [distance_route, total_CO2, total_CO, total_HC, total_PMx, total_NOx, total_fuel, total_noise]
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pandas as pd

    data_emissions = pd.read_csv("data_emissions.csv")

    routes = [1, 2, 3, 4, 5, 6]
    emissions = ['distance', 'CO2', 'CO', 'HC', 'PMx', 'NOx', 'fuel', 'noise']
    emission_classes = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6d']
    total_emission_routes = []
    for route in routes:
        for emission in emission_classes:
            total_route = mean_calculate(data_emissions, route, emission)
            total_emission_routes.append(total_route)
    total_emission_routes = pd.DataFrame(total_emission_routes, columns=emissions)
    route1 = total_emission_routes.iloc[0:5, 1:7]
    route1.index = emission_classes
    route2 = total_emission_routes.iloc[5:10, 1:7]
    route2.index = emission_classes
    route3 = total_emission_routes.iloc[10:15, 1:7]
    route3.index = emission_classes
    route4 = total_emission_routes.iloc[15:20, 1:7]
    route4.index = emission_classes
    route5 = total_emission_routes.iloc[20:25, 1:7]
    route5.index = emission_classes
    route6 = total_emission_routes.iloc[25:30, 1:7]
    route6.index = emission_classes
    print(route1)
    route1.plot( y=emissions[6], kind = "bar")
    plt.show()