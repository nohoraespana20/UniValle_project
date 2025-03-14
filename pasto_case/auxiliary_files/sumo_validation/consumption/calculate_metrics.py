import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Conversión correcta de litros a galones
LITERS_TO_GALLONS = 3.785

def total_per_trip(data, route, emission_class):
    """
    Suma los datos de consumo y emisiones para cada clase de vehículo en una ruta específica.
    """
    route_class = data[(data["route"] == route) & (data["emission_class"] == emission_class)]
    
    if route_class.empty:
        return None  

    step_route = route_class.iloc[-1]["step"]
    distance_route = route_class.iloc[-1]["distance"] / 1E3  # Convertir m a km
    fuel_gallons = (route_class["FuelConsumption"].sum() / 1E3) / LITERS_TO_GALLONS  # Litros a galones
    
    return {
        "route": route,
        "emission_class": emission_class,
        "distance [km]": distance_route,
        "CO2 [kg]": route_class["CO2Emission"].sum() / 1E3,  
        "CO [kg]": route_class["COEmission"].sum() / 1E3,  
        "HC [kg]": route_class["HCEmission"].sum() / 1E3,  
        "PMx [kg]": route_class["PMxEmission"].sum() / 1E3,  
        "NOx [kg]": route_class["NOxEmission"].sum() / 1E3,  
        "fuel [gl]": fuel_gallons,  
        "energy [kWh]": route_class["ElectricityConsumption"].sum() / 1E3,  
        "noise [dB]": route_class["NoiseEmission"].sum() / step_route,  
        # "E100km": ((route_class["FuelConsumption"].sum() / 1E3) * 10.70 * 100) / distance_route  # Cálculo del E100km
        "E100km": ((route_class["ElectricityConsumption"].sum() / 1E3)  * 100) / distance_route  # Cálculo del E100km
    }

def generate_data_frame(emission_classes, file, vehicle_name):
    """
    Carga los datos desde CSV y estructura la información en un DataFrame.
    """
    data = pd.read_csv(file)
    total_data = [total_per_trip(data, 6, emission) for emission in emission_classes]
    df = pd.DataFrame([d for d in total_data if d])  
    df["vehicle"] = vehicle_name  # Agregar nombre del vehículo
    return df

if __name__ == '__main__':
    # Clases de emisión evaluadas
    # emission_classes_ICEV = [
    #     'HBEFA4/PC_petrol_Euro-2', 'HBEFA4/PC_petrol_Euro-3', 
    #     'HBEFA4/PC_petrol_Euro-4', 'HBEFA4/PC_petrol_Euro-5', 
    #     'HBEFA4/PC_petrol_Euro-6d'
    # ]
    emission_classes_ICEV = [
        'Energy/unknown'
    ]

    
    
    # Diccionario de archivos CSV por modelo de vehículo
    # files = {
    #     "Hyunday Accent": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/data_emissions_ICE_accent.csv",
    #     "Chevrolet Beat": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/data_emissions_ICE_chevrolet_beat.csv",
    #     "Grand Eko": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/data_emissions_ICE_grand_eko.csv",
    #     "Grand Metro": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/data_emissions_ICE_grand_metro.csv",
    #     "Kia Sephia": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/data_emissions_ICE_sephia.csv",
    #     "Chevrolet Spark GT": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/data_emissions_ICE_sparkGT.csv"
    # }

    # files = {
    #     "Hyunday Accent": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/CNG/data_emissions_CNG_accent.csv",
    #     "Chevrolet Beat": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/CNG/data_emissions_CNG_chevrolet_beat.csv",
    #     "Grand Eko": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/CNG/data_emissions_CNG_grand_eko.csv",
    #     "Grand Metro": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/CNG/data_emissions_CNG_grand_metro.csv",
    #     "Kia Sephia": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/CNG/data_emissions_CNG_sephia.csv",
    #     "Chevrolet Spark GT": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/CNG/data_emissions_CNG_sparkGT.csv"
    # }

    files = {
        "BYD": "C:/Nohora/UniValle_project/test_VehicleConfiguration/consumption/results/data_emissions_EV_byd.csv"
    }
    
    # Generar DataFrame combinado
    vehicle_data_frames = [generate_data_frame(emission_classes_ICEV, path, name) for name, path in files.items()]
    final_df = pd.concat(vehicle_data_frames, ignore_index=True)

    # Imprimir el DataFrame con todos los datos
    # print(final_df)

   # Crear figura con dos subplots (1 fila, 2 columnas)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # Aumentar tamaño para mejor visualización
    # ---- Primera gráfica: Comparación de E100km ----
    sns.barplot(ax=axes[0], data=final_df, x="vehicle", y="E100km", hue="emission_class", palette="viridis")
    axes[0].set_title("Comparison kWh/km")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("kWh/100km")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)
    axes[0].legend(loc='lower left')
    axes[0].grid(axis="y", linestyle="--", alpha=0.7)
    # ---- Segunda gráfica: Comparación CO₂/km ----
    final_df["CO2 per km"] = final_df["CO2 [kg]"] / final_df["distance [km]"]
    sns.barplot(ax=axes[1], data=final_df, x="vehicle", y="CO2 per km", hue="emission_class", palette="magma")
    axes[1].set_title("Comparison kg CO₂/km")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("CO₂ [kg/km]")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
    axes[1].legend(loc='lower left')
    axes[1].grid(axis="y", linestyle="--", alpha=0.7)
    # Ajustar espaciado
    plt.tight_layout()
    plt.savefig("comparison_all_CNG.jpg")

    print(final_df)
    # # Filtrar solo los datos de 'HBEFA4/PC_petrol_Euro-4'
    # df_euro4 = final_df[final_df["emission_class"] == "HBEFA4/PC_petrol_Euro-4"]
    # print(df_euro4)
    # # Definir colores personalizados
    # color_e100km = "#2A7B8EFF"  # Azul específico
    # third_magma_color = sns.color_palette("magma", n_colors=5)[2]  # Tercer color de la paleta 'magma'
    # # Crear figura con dos subplots (1 fila, 2 columnas)
    # fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    # # ---- Primera gráfica: kWh/100km ----
    # sns.barplot(ax=axes[0], data=df_euro4, x="vehicle", y="E100km", color=color_e100km)
    # axes[0].set_title("kWh/100km - HBEFA4/PC_petrol_Euro-4")
    # axes[0].set_xlabel("")
    # axes[0].set_ylabel("kWh/100km")
    # axes[0].set_xticks(range(len(df_euro4["vehicle"])))  # Asegurar que los ticks están fijos
    # axes[0].set_xticklabels(df_euro4["vehicle"], rotation=0)
    # axes[0].grid(axis="y", linestyle="--", alpha=0.7)
    # # ---- Segunda gráfica: CO₂ por km ----
    # sns.barplot(ax=axes[1], data=df_euro4, x="vehicle", y="CO2 per km", color=third_magma_color)
    # axes[1].set_title("kg CO₂/km - HBEFA4/PC_petrol_Euro-4")
    # axes[1].set_xlabel("")
    # axes[1].set_ylabel("CO₂ [kg/km]")
    # axes[1].set_xticks(range(len(df_euro4["vehicle"])))  # Asegurar que los ticks están fijos
    # axes[1].set_xticklabels(df_euro4["vehicle"], rotation=0)
    # axes[1].grid(axis="y", linestyle="--", alpha=0.7)
    # # Ajustar espaciado
    # plt.tight_layout()
    # plt.savefig("comparison_euro4.jpg")


    # # ---- Filtrar solo la clase de emisión 'HBEFA4/PC_petrol_Euro-4' ----
    # df_euro4 = final_df[final_df["emission_class"] == "HBEFA4/PC_petrol_Euro-4"]
    # E100km_max = df_euro4["E100km"].max()
    # E100km_min = df_euro4["E100km"].min()
    # E100km_diff = ((E100km_max - E100km_min) / E100km_max) * 100
    # CO2_max = df_euro4["CO2 per km"].max()
    # CO2_min = df_euro4["CO2 per km"].min()
    # CO2_diff = ((CO2_max - CO2_min) / CO2_max) * 100
    # print(f"Diferencia porcentual en E100km: {E100km_diff:.2f}%")
    # print(f"Diferencia porcentual en CO₂ por km: {CO2_diff:.2f}%")