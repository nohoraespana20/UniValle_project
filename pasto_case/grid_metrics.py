import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import math

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
                Pcarga_annual.append(P_carga.max())

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
                    axs[0].plot(time_index, P_carga, color='green')
                    axs[0].set_ylabel('P_base [kW]')
                    axs[0].legend(['P_base', 'P_base + P_VE', 'P_carga'])
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

def calculate_chargeability(input_folders, S_max_initial, factor_demanda, cargabilidad_min, graph_folder):
    promedio_FP = []
    promedio_Smax = []
    promedio_Sactual = []

    for folder in input_folders:
        case_name = os.path.basename(folder)
        case_aditional = './cargabilidad_S_var'
        csv_output_dir = os.path.join(graph_folder, case_aditional, case_name)
        os.makedirs(csv_output_dir, exist_ok=True)

        chargeability_annual = []
        s_max_annual = []
        s_max_actual = []
        S_max = S_max_initial
        for year in range(30):
            file_path = os.path.join(folder, f"variables_{year}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                S_max = S_max_initial * (1 + 0.08) ** year
                # S_max = S_max_initial
                P_carga = df['P_carga [kW]']
                chargeability = P_carga * factor_demanda / S_max
                s_max_calculated = P_carga * factor_demanda / cargabilidad_min

                chargeability_annual.append(chargeability.max())
                s_max_actual.append(S_max)
                s_max_annual.append(s_max_calculated.max())

                # Crear índice de tiempo
                time_index = pd.date_range(start='2025-01-01 00:00', periods=len(P_carga), freq='5min')
                df_variables = pd.DataFrame({
                    'Hora': time_index,
                    'P_carga [kW]': P_carga,
                    'FC red': chargeability,
                    'S max need': s_max_calculated
                })
                df_variables.to_csv(os.path.join(csv_output_dir, f'cargabilidad_{year}.csv'), index=False)

                # Graficar años seleccionados
                if year in [0, 5, 10, 20, 29]:
                    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
                    date_formatter = mdates.DateFormatter('%H:%M')

                    axs[0].plot(time_index, P_carga, color='black')
                    axs[0].set_ylabel('P_carga [kW]')
                    axs[0].set_title(f'Año {year} - {case_name}')
                    axs[0].grid(True)
                    axs[0].xaxis.set_major_formatter(date_formatter)

                    axs[1].plot(time_index, chargeability, color='blue', label='Factor de cargabilidad')
                    axs[1].axhline(y=1, color='red', linestyle='--', linewidth=2, label='Factor de cargabilidad máximo')
                    axs[1].set_ylabel('Cargabilidad')
                    axs[1].legend()
                    axs[1].grid(True)
                    axs[1].xaxis.set_major_formatter(date_formatter)

                    axs[2].plot(time_index, s_max_calculated, color='green', label='Smax necesario')
                    axs[2].set_ylabel('S max necesario')
                    axs[2].axhline(y=S_max, color='red', linestyle='--', linewidth=2, label='Smax actual')
                    axs[2].legend()
                    axs[2].grid(True)
                    axs[2].xaxis.set_major_formatter(date_formatter)

                    plt.tight_layout()
                    plt.savefig(os.path.join(csv_output_dir, f'Grafica_Cargabilidad_{year}.png'))
                    plt.close()

        promedio_FP.append(chargeability_annual)
        promedio_Smax.append(s_max_annual)
        promedio_Sactual.append(s_max_actual)

    # Gráfico final: promedio anual
    plt.figure(figsize=(10, 6))
    labels = ['Sistema FV sin crecimiento', 'Sistema FV con crecimiento 10%', 'Sistema FV con crecimiento 20%']
    colors = ['#a4165f', '#8f459c', '#0088d1']
    years = np.arange(2025, 2025 + 30)  # Años desde 2025 hasta 2054

    for i, data_case in enumerate(promedio_FP):
        plt.plot(years, data_case, label=labels[i], color=colors[i])
    plt.axhline(y=1, color='red', linestyle='--', linewidth=2, label='Factor de cargabilidad máximo')
    plt.xlabel('Año')
    plt.ylabel('Promedio Cargabilidad')
    plt.title('Promedio anual de Factor de Cargabilidad')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder+case_aditional, 'Promedio_cargabilidad.png'))
    plt.close()

    plt.figure(figsize=(10, 6))
    labels = ['Sistema FV sin crecimiento', 'Sistema FV con crecimiento 10%', 'Sistema FV con crecimiento 20%']
    colors = ['#a4165f', '#8f459c', '#0088d1']
    years = np.arange(2025, 2025 + 30)  # Años desde 2025 hasta 2054
    for i, data_case in enumerate(promedio_Smax):
        plt.plot(years, data_case, label=labels[i], color=colors[i])
    for i, data_case in enumerate(promedio_Sactual):
        plt.plot(years, data_case, linestyle='--', color='black')
    plt.xlabel('Año')
    plt.ylabel('Promedio Smax')
    plt.title('Promedio anual de Smax necesario')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder+case_aditional, 'Promedio_smax.png'))
    plt.close()

def calculate_reinforcement(input_folders, graph_folder, S_max):
    os.makedirs(graph_folder, exist_ok=True)
    promedio_anual_Stotal = []
    promedio_anual_Srefor = []
    costo_anual_refor = []

    FP_VE = 0.9
    FP_DER = 0.95
    costo_por_unidad_S = 60  # USD/kVA

    for folder in input_folders:
        case_name = os.path.basename(folder)
        csv_output_dir = os.path.join(graph_folder, case_name)
        os.makedirs(csv_output_dir, exist_ok=True)

        Stotal_annual = []
        Srefor_annual = []
        costo_annual = []

        for year in range(30):
            file_path = os.path.join(folder, f"variables_{year}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)

                P_VE = df['P_VE [kW]'].values
                P_DER = df['P_DER [kW]'].values
                delta_P = P_VE - P_DER
                delta_Q = (P_VE * math.tan(math.acos(FP_VE))) - (P_DER * math.tan(math.acos(FP_DER)))
                S_total = np.sqrt(delta_P**2 + delta_Q**2)
                S_refor = np.maximum(S_total, 0)  
                S_refor_avg = np.mean(S_refor)
                costo_refor = S_refor_avg * costo_por_unidad_S / 1000

                Stotal_annual.append(np.mean(S_total))
                Srefor_annual.append(S_refor_avg)
                costo_annual.append(costo_refor)

        promedio_anual_Stotal.append(Stotal_annual)
        promedio_anual_Srefor.append(Srefor_annual)
        costo_anual_refor.append(costo_annual)

    plt.figure(figsize=(10, 6))
    labels = ['Escenario 1', 'Escenario 2', 'Escenario 3']
    colors = ['#a4165f', '#8f459c', '#0088d1']
    years = np.arange(2025, 2025 + 30)

    for i, data_case in enumerate(promedio_anual_Srefor):
        label = labels[i] if i < len(labels) else f'Escenario {i+1}'
        color = colors[i] if i < len(colors) else None
        plt.plot(years, data_case, label=label, color=color)

    plt.xlabel('Año')
    plt.ylabel('Promedio S de reforzamiento [kVA]')
    plt.title('Promedio anual de potencia de reforzamiento')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder, 'Promedio_reforzamiento.png'))
    plt.close()

    # Gráfica de costos
    plt.figure(figsize=(10, 6))
    for i, costo_case in enumerate(costo_anual_refor):
        label = labels[i] if i < len(labels) else f'Escenario {i+1}'
        color = colors[i] if i < len(colors) else None
        plt.plot(years, costo_case, label=label, color=color)

    plt.xlabel('Año')
    plt.ylabel('Miles de dólares')
    plt.title('Costo anual estimado por reforzamiento de red')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder, 'Costo_reforzamiento.png'))
    plt.close()

def calculate_reinforcement2(input_folders, graph_folder, S_max):
    os.makedirs(graph_folder, exist_ok=True)
    labels = ['Escenario 1', 'Escenario 2', 'Escenario 3']
    colors = ['#a4165f', '#8f459c', '#0088d1']

    FP_VE = 0.9
    FP_DER = 0.95
    costo_por_unidad_S = 60  # USD/kVA
    tasa_descuento = 0.09
    year_final = 29  # Último año del horizonte (0 a 29)

    refuerzo_final = []
    costo_valor_presente = []

    for folder in input_folders:
        print(folder)
        case_name = os.path.basename(folder)
        csv_output_dir = os.path.join(graph_folder, case_name)
        os.makedirs(csv_output_dir, exist_ok=True)

        file_path = os.path.join(folder, f"variables_{year_final}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            P_VE = df['P_VE [kW]'].values
            P_DER = df['P_DER [kW]'].values
            delta_P = P_VE - P_DER
            delta_Q = (P_VE * math.tan(math.acos(FP_VE))) - (P_DER * math.tan(math.acos(FP_DER)))
            S_total = np.sqrt(delta_P**2 + delta_Q**2)
            S_refor = np.maximum(S_total, 0)
            S_refor_avg = np.mean(S_refor)

            # Costo de reforzamiento en el año final
            costo_final = S_refor_avg * costo_por_unidad_S / 1000  # en miles de USD

            # Traer a valor presente
            vp_costo = costo_final / ((1 + tasa_descuento) ** year_final)

            refuerzo_final.append(S_refor_avg)
            costo_valor_presente.append(vp_costo)
        else:
            refuerzo_final.append(0)
            costo_valor_presente.append(0)

    # Imprimir o guardar resultados
    for i in range(len(input_folders)):
        label = labels[i] if i < len(labels) else f'Escenario {i+1}'
        print(f"{label}:")
        print(f"  Refuerzo promedio en año final [kVA]: {refuerzo_final[i]:.2f}")
        print(f"  Costo en valor presente [mil USD]: {costo_valor_presente[i]:.2f}")

    # Graficar resultados
    x_labels = labels[:len(input_folders)]

    plt.figure(figsize=(8, 5))
    plt.bar(x_labels, costo_valor_presente, color=colors[:len(input_folders)])
    plt.ylabel('Costo en valor presente [mil USD]')
    plt.title('Costo único de reforzamiento (VP) en el año inicial')
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder, 'Costo_valor_presente_reforzamiento.png'))
    plt.close()

def calcular_y_graficar_iip(income_files, potencia_dirs, graph_folder, nombres_casos=None):
    plt.figure(figsize=(10, 6))

    for i, (income_path, potencia_dir) in enumerate(zip(income_files, potencia_dirs)):
        # Leer ingresos por excedentes
        ingresos_df = pd.read_csv(income_path)
        ingresos = ingresos_df['Utilidades (miles de dólares)'] * 1000
        anios = ingresos_df['Año'] if 'Año' in ingresos_df.columns else range(1, len(ingresos) + 1)

        energia_total_anual = []

        for year in range(len(anios)):
            file_path = os.path.join(potencia_dir, f"variables_{year}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                potencia = df['P_DER [kW]']
                energia_diaria = potencia.mean()  # energía diaria promedio (kWh)
                dias_del_ano = 365
                energia_anual = energia_diaria * dias_del_ano  # kWh/año
                energia_total_anual.append(energia_anual)
            else:
                print(f"Archivo no encontrado: {file_path}")
                energia_total_anual.append(float('nan'))

        # Calcular IIP
        energia_total_anual = pd.Series(energia_total_anual)
        iip = ingresos / energia_total_anual
        nombre = nombres_casos[i] if nombres_casos else f'Caso {i+1}'
        plt.plot(anios, iip, label=nombre)

    plt.title("Índice de Ingresos por Potencia Autogenerada")
    plt.xlabel("Año")
    plt.ylabel("IIP [USD/kWh]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graph_folder, 'iip.jpg'))


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

    data = {}
    data = pd.DataFrame(index=pd.date_range(start='2019-01-01 00:00', end='2019-01-01 23:00', freq='h'))
    data['load_demand'] = [
        0.56, 0.50, 0.49, 0.48, 0.53, 0.67, 0.71, 0.71, 0.76, 0.80, 0.82, 0.84, 
        0.80, 0.79, 0.80, 0.79, 0.79, 0.96, 1.00, 0.95, 0.88, 0.78, 0.69, 0.63
    ]
    data = data.resample('5min').asfreq()
    data['load_demand'] = data['load_demand'].interpolate()
    scale_load = 100000 

    # calculate_and_plot_P_carga(output_folders, data, graph_folder, scale_load, incremento_pico=0.10)

    S_max = 104000
    factor_demanda = 0.8
    cargabilidad_min = 0.9
    input_folders = [
        "C:/Nohora/UniValle_project/pasto_case/results_grid/1_conDER/results_DER_case1",
        "C:/Nohora/UniValle_project/pasto_case/results_grid/1_conDER/results_DER_case2",
        "C:/Nohora/UniValle_project/pasto_case/results_grid/1_conDER/results_DER_case3"
    ]
    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_grid/1_conDER"

    # calculate_chargeability(input_folders, S_max, factor_demanda, cargabilidad_min, graph_folder)

    calculate_reinforcement(input_folders, graph_folder, S_max)
    calculate_reinforcement2(input_folders, graph_folder, S_max)

    income_folders = [
        "C:/Nohora/UniValle_project/pasto_case/results_DER_case1/Income_vs_Cost_datos.csv",
        "C:/Nohora/UniValle_project/pasto_case/results_DER_case2/Income_vs_Cost_datos.csv",
        "C:/Nohora/UniValle_project/pasto_case/results_DER_case3/Income_vs_Cost_datos.csv"
    ]

    power_folders = [
        "C:/Nohora/UniValle_project/pasto_case/results_grid/1_conDER/results_DER_case1",
        "C:/Nohora/UniValle_project/pasto_case/results_grid/1_conDER/results_DER_case2",
        "C:/Nohora/UniValle_project/pasto_case/results_grid/1_conDER/results_DER_case3"
    ]
    # IIP = (Ahorro en factura + Beneficios fiscales + Ingresos por excedentes) / Potencia autogenerada
    nombres_casos = ['Sistema FV sin crecimiento','Sistema FV con crecimiento 10%','Sistema FV con crecimiento 20%']
    calcular_y_graficar_iip(income_folders, power_folders, "C:/Nohora/UniValle_project/pasto_case/results_DER_case3/",nombres_casos)

