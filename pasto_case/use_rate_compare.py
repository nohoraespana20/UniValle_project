import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def process_data_files(input_folder, output_folder):
    """
    Procesa los archivos de datos CSV en la carpeta de entrada, calcula los promedios diarios,
    y guarda los resultados en la carpeta de salida.

    Args:
        input_folder (str): Ruta de la carpeta de entrada.
        output_folder (str): Ruta de la carpeta de salida.
        graph_folder (str): Ruta de la carpeta para guardar las gráficas.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            try:
                df = pd.read_csv(input_path)
                if 'Import Power [kW]' not in df.columns or 'PV Power [kW]' not in df.columns or 'Battery Discharging Power [kW]' not in df.columns:
                    print(f"Advertencia: {file_name} no contiene las columnas necesarias. Se omite.")
                    continue

                # Calcular promedios diarios multiplicados por 365
                daily_avg_import = df['Import Power [kW]'].mean() * 365
                daily_avg_pv = df['PV Power [kW]'].mean() * 365
                daily_avg_battery = df['Battery Discharging Power [kW]'].mean() * 365

                df['PV/Import Power (%)'] = round((daily_avg_pv / (daily_avg_import + daily_avg_pv + daily_avg_battery)) * 100 )
                df['Battery Utilization Rate (%)'] = round((daily_avg_battery / (daily_avg_import + daily_avg_pv + daily_avg_battery)) * 100)
                df['Grid Utilization rate (%)'] = round((daily_avg_import / (daily_avg_import + daily_avg_pv + daily_avg_battery)) * 100)

                df.to_csv(output_path, index=True)
                print(f"Procesado: {file_name} -> {output_path}")

            except ZeroDivisionError:
                print(f"Error: División por cero en {file_name}. Se omite.")
            except Exception as e:
                print(f"Error inesperado al procesar {file_name}: {e}")

def generate_figures_comparison(data_frames, file_name, graph_folder, name, metric_name):
    """
    Genera figuras comparando datos de múltiples carpetas y las guarda en la carpeta de gráficas.

    Args:
        data_frames (list of list of float): Lista de listas con valores anuales para cada carpeta.
        file_name (str): Nombre del archivo para la gráfica.
        graph_folder (str): Ruta de la carpeta para guardar las gráficas.
        metric_name (str): Nombre del métrica para la gráfica.
    """
    graph_path = os.path.join(graph_folder, f"{file_name}_{name}.png")

    years = np.arange(len(data_frames[0]))
    plt.figure(figsize=(10, 6))
    labels = ['Caso 1', 'Caso 2', 'Caso 3', 'Caso 4', 'Caso 5']
    colors = ['#a4165f', '#8f459c', '#0088d1', '#009ec3', '#00aea7']
    for i, data in enumerate(data_frames):
        plt.plot(years, data, label=labels[i], color=colors[i])
    plt.xlabel('Year')
    plt.ylabel(f'{metric_name}')
    plt.title(f'{file_name}')
    plt.grid(True)
    plt.legend()
    plt.savefig(graph_path)
    plt.close()

def generate_subplots_comparison(data_frames, file_name, graph_folder, name, metric_name):
   """
    Genera figuras comparando datos de múltiples carpetas como subplots (2x2) 
    y las guarda en la carpeta de gráficas.

    Args:
        data_frames (list of list of float): Lista de listas con valores anuales para cada carpeta.
        file_name (str): Nombre del archivo para la gráfica.
        graph_folder (str): Ruta de la carpeta para guardar las gráficas.
        metric_name (str): Nombre de la métrica para la gráfica.
    """
   graph_path = os.path.join(graph_folder, f"{file_name}_{name}.png")
   years = np.arange(len(data_frames[0]))
   labels = ['Caso 1', 'Caso 2', 'Caso 3', 'Caso 4', 'Caso 5']
   colors = ['#a4165f', '#8f459c', '#0088d1', '#009ec3', '#00aea7']
   fig, axes = plt.subplots(5, 1, figsize=(12, 10))
   axes = axes.flatten()  # Convierte la matriz de ejes en una lista para iterar fácilmente

   for i, ax in enumerate(axes):
       ax.plot(years, data_frames[i], label=labels[i], color=colors[i])
       ax.set_xlabel('Year')
       ax.set_ylabel(metric_name)
       ax.set_title(f'{labels[i]}')
       ax.grid(True)

   fig.suptitle(file_name, fontsize=16)
   plt.tight_layout(rect=[0, 0, 1, 0.96])
   
    # Guardar la figura
   plt.savefig(graph_path)
   plt.close()

def generate_figures_indexes(SRG, BUR, GUR, graph_folder, name):
    """
    Genera gráficos de áreas individuales (no apiladas) para los datos proporcionados.

    Args:
        SRG (list of lists): Datos para el grupo SRG.
        BUR (list of lists): Datos para el grupo BUR.
        GUR (list of lists): Datos para el grupo GUR.
        graph_folder (str): Carpeta para guardar los gráficos.
    """
    file_name = ['Caso 1', 'Caso 2', 'Caso 3', 'Caso 4', 'Caso 5']
    years = np.arange(len(SRG[0]))
    labels = ['SRG', 'GUR', 'BUR']
    colors = ['#ffc853','#00aea7', '#a4165f']
    data = [SRG, GUR, BUR]

    # Asegúrate de que la carpeta para gráficos exista
    os.makedirs(graph_folder, exist_ok=True)

    for i in range(len(SRG)):
        graph_path = os.path.join(graph_folder, f"{file_name[i]}.png")
        
        plt.figure(figsize=(10, 6))
        
        # Dibujar áreas individuales con transparencia
        for j, label in enumerate(labels):
            plt.fill_between(years, data[j][i], alpha=0.5, label=label, color=colors[j])

        plt.xlabel('Year')
        plt.ylabel('%')
        plt.title(f'{file_name[i]} {name} ')
        plt.grid(True, alpha=0.5)
        plt.legend()
        plt.tight_layout()
        
        # Guardar el gráfico
        plt.savefig(graph_path)
        plt.close()

def generate_figures_areas(data_frames, file_name, graph_folder, name, metric_name):
    """
    Genera un gráfico de áreas apiladas comparando datos de múltiples carpetas y lo guarda en la carpeta de gráficas.

    Args:
        data_frames (list of list of float): Lista de listas con valores anuales para cada carpeta.
        file_name (str): Nombre del archivo para la gráfica.
        graph_folder (str): Ruta de la carpeta para guardar las gráficas.
        metric_name (str): Nombre de la métrica para la gráfica.
    """
    import os
    import numpy as np
    import matplotlib.pyplot as plt

    graph_path = os.path.join(graph_folder, f"{file_name}_{name}.png")

    years = np.arange(len(data_frames[0]))
    labels = ['Caso 1', 'Caso 2', 'Caso 3', 'Caso 4', 'Caso 5']
    colors = ['#a4165f', '#8f459c', '#0088d1', '#009ec3', '#00aea7']  # Paleta de colores

    # Convertir data_frames a un array de NumPy para facilitar el apilado
    data_array = np.array(data_frames)

    plt.figure(figsize=(10, 6))
    plt.stackplot(years, data_array, labels=labels, colors=colors, alpha=0.8)
    plt.xlabel('Year')
    plt.ylabel(metric_name)
    plt.title(file_name)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.savefig(graph_path)
    plt.close()

if __name__ == '__main__':
    input_folders = [
        "C:/Nohora/UniValle_project/pasto_case/results_DOPER_case1",
        "C:/Nohora/UniValle_project/pasto_case/results_DOPER_case2",
        "C:/Nohora/UniValle_project/pasto_case/results_DOPER_case3"
    ]
    output_folders = [
        "C:/Nohora/UniValle_project/pasto_case/results_grid/results_DER_case1",
        "C:/Nohora/UniValle_project/pasto_case/results_grid/results_DER_case2",
        "C:/Nohora/UniValle_project/pasto_case/results_grid/results_DER_case3"
    ]
    graph_folder = "C:/Users/noluc/OneDrive/Escritorio/resultados_configuracionesPV/Processed/"

    # # Procesar archivos CSV
    for i in range(len(input_folders)):
        process_data_files(input_folders[i], output_folders[i])

    # # Generar datos para gráficas comparativas
    # df_SRG_list = []
    # df_BUR_list = []
    # df_GUR_list = []

    # for folder in output_folders:
    #     SRG_values = []
    #     BUR_values = []
    #     GUR_values = []
    #     for year in range(30):
    #         file_path = f"{folder}/doperRes{year}.csv"
    #         if os.path.exists(file_path):
    #             df = pd.read_csv(file_path)
    #             SRG_values.append(df['PV/Import Power (%)'][0])
    #             BUR_values.append(df['Battery Utilization Rate (%)'][0])
    #             GUR_values.append(df['Grid Utilization rate (%)'][0])
    #     df_SRG_list.append(SRG_values)
    #     df_BUR_list.append(BUR_values)
    #     df_GUR_list.append(GUR_values)

    # # Graficar comparaciones

    # generate_figures_comparison(df_SRG_list, f'Shared Renewable Generation ', graph_folder,'line', 'SGR [%]')
    # generate_figures_comparison(df_BUR_list, f'Battery Utilization Rate ', graph_folder,'line', 'BUR [%]')
    # generate_figures_comparison(df_GUR_list, f'Grid Utilization rate ', graph_folder,'line', 'GUR [%]')

    # generate_subplots_comparison(df_SRG_list, f'Shared Renewable Generation ', graph_folder,'subplot', 'SGR [%]')
    # generate_subplots_comparison(df_BUR_list, f'Battery Utilization Rate ', graph_folder,'subplot', 'BUR [%]')
    # generate_subplots_comparison(df_GUR_list, f'Grid Utilization rate  ', graph_folder,'subplot', 'GUR [%]')

    # generate_figures_indexes(df_SRG_list, df_BUR_list, df_GUR_list, graph_folder, f' ')

    # generate_figures_areas(df_SRG_list, f'Shared Renewable Generation  ', graph_folder,'areas', 'SGR [%]')
    # generate_figures_areas(df_BUR_list, f'Battery Utilization Rate ', graph_folder,'areas', 'BUR [%]')
    # generate_figures_areas(df_GUR_list, f'Grid Utilization rate  ', graph_folder,'areas{', 'GUR [%]')