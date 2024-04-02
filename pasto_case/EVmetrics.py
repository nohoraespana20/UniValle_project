def total_per_trip(data, route, emission_class):
    '''
    Sum all data for each category data and express in km for distance, kg for emissions, gallon for fuel, kWh for electricity and mean dB for noise.
    '''
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
    total_energy = route_class["ElectricityConsumption"].sum()/1E3 #Energy in kWh
    total_noise = route_class["NoiseEmission"].sum()/step_route  # Mean noise in dB
    return [route, emission_class, distance_route, total_CO2, total_CO, total_HC, total_PMx, total_NOx, total_fuel, total_energy, total_noise]

def generate_data_frame(emission_classes, file):
    '''
    Organize data in a data frame
    '''
    data = pd.read_csv(file)
    routes = [1, 2, 3, 4, 5, 6]
    category = ['route','emission_class','distance [km]', 'CO2 [kg]', 'CO [kg]', 'HC [kg]', 'PMx [kg]', 'NOx [kg]', 'fuel [gl]', 'energy [kWh]', 'noise [dB]']
    total_data = []
    for route in routes:
        for emission in emission_classes:
            total_route = total_per_trip(data, route, emission)
            total_data.append(total_route)
    total_data_frame = pd.DataFrame(total_data,columns=category)
    data_frame = total_data_frame.iloc[:, [0,1,3,4,5,6,7,8,9,10]]
    return data_frame

def consumption_metric(vehType, distance, consumption):
    if vehType == "ICE":
        E_100km = (consumption*3.785*10.7*100)/distance
    elif vehType == "EV":
        E_100km = (consumption*100)/distance
    else:
        print('Vehicle type is not defined')
    return E_100km

def autonomy_metric(vehType, E_100km, capacity):
    if vehType == "ICE":
        consumption = (E_100km/(100*3.785*10.7))
        autonomy = capacity / consumption
    elif vehType == "EV":
        autonomy = capacity / (E_100km/100)
    else:
        print('Vehicle type is not defined')
    return autonomy

def ICR_metric(powerCost, consumption, distance):
    icr = powerCost * consumption / distance
    return icr

def CA_metric(years, maintenance, insurance, tax, tm_inspection, consumption):
#TODO: include the values to annual increase. Write the equation.
    CA = []
    for i in range(years):
        CA    
    return CA

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pandas as pd

    #Generate data frame for EV
    emission_classes_EV = ['Energy/unknown']
    rush_df_EV = generate_data_frame(emission_classes_EV,"./results/rush/data_emissions_EV.csv")
    offPeak_df_EV = generate_data_frame(emission_classes_EV,"./results/off_peak/data_emissions_EV.csv")

    #Import SUMO data for ICE
    emission_classes_ICE = ['HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
                        'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
                        'HBEFA4/PC_petrol_Euro-6d']
    rush_df_ICE = generate_data_frame(emission_classes_ICE,"./results/rush/data_emissions_ICE.csv")
    offPeak_df_ICE = generate_data_frame(emission_classes_ICE,"./results/off_peak/data_emissions_ICE.csv")
