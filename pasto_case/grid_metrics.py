import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

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
    labels = ['Sistema FV sin crecimiento','Sistema FV con crecimiento 10%','Sistema FV con crecimiento 20%']
    colors = ['#a4165f', '#8f459c', '#0088d1']
    for i, data in enumerate(data_frames):
        plt.plot(years, data, label=labels[i], color=colors[i])
    plt.xlabel('Año')
    plt.ylabel(f'%')
    plt.title(f'Tasa de utilización de la red')
    plt.grid(True)
    plt.legend()
    plt.savefig(graph_path)
    plt.close()

def generate_figures_indexes(SRG, BUR, GUR, graph_folder, name):
    """
    Genera gráficos de áreas apiladas normalizadas para los datos proporcionados.
    Args:
        SRG (list of lists): Datos para el grupo SRG.
        BUR (list of lists): Datos para el grupo BUR.
        GUR (list of lists): Datos para el grupo GUR.
        graph_folder (str): Carpeta para guardar los gráficos.
        name (str): Nombre adicional para los títulos.
    """
    file_name = ['Sistema FV sin crecimiento','Sistema FV con crecimiento 10%','Sistema FV con crecimiento 20%']
    years = np.arange(len(SRG[0]))
    labels = ['SRG', 'GUR', 'BUR']
    colors = ['#ffc853', '#00aea7', '#a4165f']  # Amarillo, Verde, Fucsia
    data = [SRG, GUR, BUR]
    os.makedirs(graph_folder, exist_ok=True)

    for i in range(len(SRG)):
        graph_path = os.path.join(graph_folder, f"{file_name[i]}.png")      
        plt.figure(figsize=(10, 6))
        SRG_case = np.array(data[0][i])
        GUR_case = np.array(data[1][i])
        BUR_case = np.array(data[2][i])
        total = SRG_case + GUR_case + BUR_case

        SRG_norm = 100 * SRG_case / total
        GUR_norm = 100 * GUR_case / total
        BUR_norm = 100 * BUR_case / total

        plt.stackplot(years, SRG_norm, GUR_norm, BUR_norm, labels=labels, colors=colors, alpha=0.8)
        plt.xlabel('Año')
        plt.ylabel('%')
        plt.title(f'{file_name[i]} {name}')
        plt.grid(True, alpha=0.5)
        plt.legend(loc='lower left')
        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()

def calculate_and_plot_P_carga(output_folders, data, graph_folder, scale_load, incremento_pico=0.10):
    os.makedirs(graph_folder, exist_ok=True)
    promedio_anual_Pcarga = []

    for folder in output_folders:
        case_name = os.path.basename(folder)
        csv_output_dir = os.path.join(graph_folder, 'csv_por_caso', case_name)
        os.makedirs(csv_output_dir, exist_ok=True)

        Pcarga_annual = []
        for year in range(30):
            file_path = f"{folder}/doperRes{year}.csv"
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)

                pico_pasto = scale_load * (1 + incremento_pico) ** year 
                P_base = data['load_demand'].values * pico_pasto 
                P_VE = df['Load Power [kW]']
                P_DER = df['PV Power [kW]']#.values * 0
                P_carga = P_base + P_VE - P_DER
                Pcarga_annual.append(np.mean(P_carga))

                # Crear índice de tiempo
                time_index = pd.date_range(start='2025-01-01 00:00', periods=len(P_base), freq='5min')
                df_variables = pd.DataFrame({
                    'Hora': time_index,
                    'P_base [kW]': P_base,
                    'P_VE [kW]': P_VE,
                    'P_DER [kW]': P_DER,
                    'P_carga [kW]': P_carga
                })
                df_variables.to_csv(os.path.join(csv_output_dir, f'variables_{year}.csv'), index=False)

                # Graficar años seleccionados
                if year in [5, 10, 20, 29]:
                    fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
                    date_formatter = mdates.DateFormatter('%H:%M')

                    axs[0].plot(time_index, P_base, color='black')
                    axs[0].plot(time_index, P_base + P_VE, color='red')
                    axs[0].set_ylabel('P_base [kW]')
                    axs[0].legend(['P_base', 'P_base + P_VE'])
                    axs[0].set_title(f'Año {year} - {case_name}')
                    axs[0].grid(True)
                    axs[0].xaxis.set_major_formatter(date_formatter)

                    axs[1].plot(time_index, P_VE, color='blue')
                    axs[1].set_ylabel('P_VE [kW]')
                    axs[1].grid(True)
                    axs[1].xaxis.set_major_formatter(date_formatter)

                    axs[2].plot(time_index, P_DER, color='green')
                    axs[2].set_ylabel('P_DER [kW]')
                    axs[2].grid(True)
                    axs[2].xaxis.set_major_formatter(date_formatter)

                    axs[3].plot(time_index, P_carga, color='red')
                    axs[3].set_ylabel('P_carga [kW]')
                    axs[3].set_xlabel('Hora')
                    axs[3].grid(True)
                    axs[3].xaxis.set_major_formatter(date_formatter)

                    plt.tight_layout()
                    plt.savefig(os.path.join(graph_folder, f'Subplots_Variables_{year}_{case_name}.png'))
                    plt.close()

        promedio_anual_Pcarga.append(Pcarga_annual)

    # Gráfico final: promedio anual
    plt.figure(figsize=(10, 6))
    labels = ['Sistema FV sin crecimiento', 'Sistema FV con crecimiento 10%', 'Sistema FV con crecimiento 20%']
    colors = ['#a4165f', '#8f459c', '#0088d1']
    years = np.arange(2025, 2025 + 30)  # Años desde 2025 hasta 2054

    for i, data_case in enumerate(promedio_anual_Pcarga):
        plt.plot(years, data_case, label=labels[i], color=colors[i])

    plt.xlabel('Año')
    plt.ylabel('Promedio P_carga [kW]')
    plt.title('Promedio anual de P_carga')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder, 'Promedio_Pcarga_anual.png'))
    plt.close()

if __name__ == '__main__':
    
    output_folders = [
        "C:/Nohora/UniValle_project/pasto_case/results_grid/results_DER_case1",
        "C:/Nohora/UniValle_project/pasto_case/results_grid/results_DER_case2",
        "C:/Nohora/UniValle_project/pasto_case/results_grid/results_DER_case3"
    ]
    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_grid/1_conDER"

    df_SRG_list = []
    df_BUR_list = []
    df_GUR_list = []
    for folder in output_folders:
        SRG_values = []
        BUR_values = []
        GUR_values = []
        for year in range(30):
            file_path = f"{folder}/doperRes{year}.csv"
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                SRG_values.append(df['PV/Import Power (%)'][0])
                BUR_values.append(df['Battery Utilization Rate (%)'][0])
                GUR_values.append(df['Grid Utilization rate (%)'][0])
        df_SRG_list.append(SRG_values)
        df_BUR_list.append(BUR_values)
        df_GUR_list.append(GUR_values)

    # Graficar comparaciones
    # generate_figures_comparison(df_GUR_list, f'Grid Utilization rate', graph_folder,'line', 'GUR [%]')
    # generate_figures_indexes(df_SRG_list, df_BUR_list, df_GUR_list, graph_folder, f' ')

    # data = {}
    # data = pd.DataFrame(index=pd.date_range(start='2019-01-01 00:00', end='2019-01-01 23:00', freq='h'))
    # data['load_demand'] = [
    #     0.56, 0.50, 0.49, 0.48, 0.53, 0.67, 0.71, 0.71, 0.76, 0.80, 0.82, 0.84, 
    #     0.80, 0.79, 0.80, 0.79, 0.79, 0.96, 1.00, 0.95, 0.88, 0.78, 0.69, 0.63
    # ]
    # data = data.resample('5min').asfreq()
    # data['load_demand'] = data['load_demand'].interpolate()
    # scale_load = 100000 

    # calculate_and_plot_P_carga(output_folders, data, graph_folder, scale_load, incremento_pico=0.10)