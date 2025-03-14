import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def process_data_files(input_folder, output_folder, graph_folder):
    """
    Procesa los archivos de datos CSV en la carpeta de entrada, genera nuevas columnas calculadas
    y guarda los resultados en la carpeta de salida.

    Args:
        input_folder (str): Ruta de la carpeta de entrada.
        output_folder (str): Ruta de la carpeta de salida.
        graph_folder (str): Ruta de la carpeta para guardar las gráficas.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        os.makedirs(graph_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            try:
                df = pd.read_csv(input_path)
                if 'Import Power [kW]' not in df.columns or 'PV Power [kW]' not in df.columns or 'Battery Discharging Power [kW]' not in df.columns:
                    print(f"Advertencia: {file_name} no contiene las columnas necesarias. Se omite.")
                    continue

                # Procesamiento de datos
                df = df.drop(['Tariff Energy Period [-]', 'Tariff Power Period [-]', 'Temperature [C]', 
                              'Battery Aggregate SOC [-]', 'Tariff Energy [$/kWh]'], axis=1)
                df['PV/Import Power (%)'] = (df['PV Power [kW]'] / (df['Import Power [kW]'] + 
                                     df['PV Power [kW]'] + df['Battery Discharging Power [kW]'])) * 100
                df['Battery Utilization Rate (%)'] = (df['Battery Discharging Power [kW]'] / 
                                     (df['Import Power [kW]'] + df['PV Power [kW]'] + 
                                      df['Battery Discharging Power [kW]'])) * 100
                df['Profit surplus energy - annual [USD]']  = df['Export Power [kW]'] * 0.12 * 365
                df.to_csv(output_path, index=False)
                print(f"Procesado: {file_name} -> {output_path}")

            except ZeroDivisionError:
                print(f"Error: División por cero en {file_name}. Se omite.")
            except Exception as e:
                print(f"Error inesperado al procesar {file_name}: {e}")

def generate_figures_technical(df, file_name, graph_folder, metric_name):
    """
    Genera figuras a partir de los datos procesados y las guarda en la carpeta de gráficas.

    Args:
        df (pd.DataFrame): DataFrame procesado con los datos calculados.
        file_name (str): Nombre del archivo CSV original.
        graph_folder (str): Ruta de la carpeta para guardar las gráficas.
    """
    graph_path = os.path.join(graph_folder, f"{os.path.splitext(file_name)[0]}.png")

    total_rows = len(df)
    time_intervals = pd.date_range(start='00:00', periods=total_rows, freq='5min').strftime('%H:%M')

    plt.figure(figsize=(10, 6))
    plt.plot(time_intervals, df)
    plt.xlabel('Time')
    plt.ylabel(f'{metric_name}')
    plt.title(f'{file_name}')
    plt.grid(True)
    plt.legend(['Home', 'Workplace', 'Shopping Mall', 'Fast CS'])
    step = max(1, total_rows // 10)
    plt.xticks(ticks=np.arange(0, total_rows, step), labels=time_intervals[::step], rotation=0)
    plt.savefig(graph_path)
    plt.close()

def generate_figures_economic(df, years, file_name, graph_folder, metric_name):
    """
    Genera figuras a partir de los datos procesados y las guarda en la carpeta de gráficas.

    Args:
        df (pd.DataFrame): DataFrame procesado con los datos calculados.
        file_name (str): Nombre del archivo CSV original.
        graph_folder (str): Ruta de la carpeta para guardar las gráficas.
    """
    graph_path = os.path.join(graph_folder, f"{os.path.splitext(file_name)[0]}.png")

    year = list(range(years))
    plt.figure(figsize=(10, 6))
    plt.plot(year, df)
    plt.xlabel('Year')
    plt.ylabel(f'{metric_name}')
    plt.title(f'{file_name}')
    plt.grid(True)
    plt.legend(['Home', 'Workplace', 'Shopping Mall', 'Fast CS'])
    step = max(1, years // 10)
    plt.xticks(ticks=np.arange(0, years, step), labels=year[::step], rotation=0)
    plt.savefig(graph_path)
    plt.close()

def generate_figures_economic2(df, years, file_name, graph_folder, metric_name):
    graph_path = os.path.join(graph_folder, f"bar_{os.path.splitext(file_name)[0]}.png")
    year = list(range(years))
    categories = df.columns  # Asume que las columnas del DataFrame son 'Home', 'Workplace', etc.
    bar_width = 0.2  # Ancho de cada grupo de barras

    # Configurar el tamaño de la figura
    plt.figure(figsize=(12, 6))

    # Graficar cada categoría con un desplazamiento
    for i, category in enumerate(categories):
        plt.bar(
            np.array(year) + i * bar_width,
            df[category],
            width=bar_width,
            label=category
        )

    # Configurar etiquetas y título
    plt.xlabel('Year')
    plt.ylabel(f'{metric_name}')
    plt.title(f'{file_name}')
    plt.xticks(
        ticks=np.arange(years) + bar_width * (len(categories) - 1) / 2,
        labels=year,
        rotation=0
    )
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Guardar la gráfica y cerrar la figura
    plt.savefig(graph_path)
    plt.close()

def calculate_accumulated_cost(I_PV, I_bat, years, profit_energy):
    """
    Calcula el costo acumulado (AC) basado en los costos iniciales, de mantenimiento y retrofit.

    Args:
        I_PV (float): Costo inicial de los paneles solares (equipos e instalación).
        I_bat (float): Costo inicial de las baterías (equipos e instalación).
        years (int): Número total de años para considerar el análisis.

    Returns:
        list: Costo acumulado (accumulated_cost).
        list: Costo anual (annual_cost)
    """
    maintenance_rate = 0.01  # 1% de los costos iniciales anuales
    retrofit_rate = 0.1     # 50% de los costos iniciales cada 10 años
    ipc = 0.0457 # Average value of IPC in Colombia

    initial_cost = (I_PV + I_bat) / 1000
    maintenance_cost = initial_cost * maintenance_rate
    annual_cost = [round(initial_cost)]  # Incluye los costos iniciales en y=0
    accumulated_cost = [round(initial_cost)]
    for year in range(1, years ):
        investment = initial_cost * (1 + ipc)
        maintenance_cost = investment * maintenance_rate
        profit_energy = profit_energy * (1 + ipc)
        if year % 10 == 0:
            retrofit_cost = investment * retrofit_rate
            annual_cost.append(round((retrofit_cost + maintenance_cost - profit_energy)))
            accumulated_cost.append(round((accumulated_cost[-1] + retrofit_cost + maintenance_cost - profit_energy)))
        else: 
            annual_cost.append(round(maintenance_cost - profit_energy))
            accumulated_cost.append(round((accumulated_cost[-1] + maintenance_cost - profit_energy)))

    return annual_cost, accumulated_cost

if __name__ == '__main__':
    input_folder = "C:/Users/noluc/OneDrive/Escritorio/resultados_conbateria_08-08/L2"
    output_folder = "C:/Users/noluc/OneDrive/Escritorio/DERMetrics"
    graph_folder = os.path.join(output_folder, "graficas")

    #####Technical metrics####
    # process_data_files(input_folder, output_folder, graph_folder)

    df1 = pd.read_csv(f"C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L1_home\\doperRes29.csv")
    df2 = pd.read_csv(f"C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L1_work\\doperRes29.csv")
    df3 = pd.read_csv(f"C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L2\\doperRes29.csv")
    df4 = pd.read_csv(f"C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L3\\doperRes30.csv")

    df_SRG = pd.DataFrame({'Home' : []})
    df_SRG['Home'] = df1['PV/Import Power (%)']
    df_SRG['Work'] = df2['PV/Import Power (%)']
    df_SRG['Shopping'] = df3['PV/Import Power (%)']
    df_SRG['Fast'] = df4['PV/Import Power (%)']
    generate_figures_technical(df_SRG,'Shared Renewable Generation 29',graph_folder, 'SGR [%]')
    
    df_BUR = pd.DataFrame({'Home' : []})
    df_BUR['Home'] = df1['Battery Utilization Rate (%)']
    df_BUR['Work'] = df2['Battery Utilization Rate (%)']
    df_BUR['Shopping'] = df3['Battery Utilization Rate (%)']
    df_BUR['Fast'] = df4['Battery Utilization Rate (%)']
    generate_figures_technical(df_BUR,'Battery Utilization Rate 29',graph_folder, 'BUR [%]')


     ####Economis metrics #####
    kW_pv =  20461 # PV total
    kW_bat = 11537 # Bat total
    I_pv = (609 * 1.071) * kW_pv  # USD (compra e instalación)
    I_bat = 67.4 * kW_bat  # USD (compra) 
    years = 30  # Número de años

    df_home = pd.read_csv(f"C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L1_home\\doperRes29.csv")
    profit_energy_home =  round(df_home['Profit surplus energy - annual [USD]'].sum() / 1000)
    max_demand_home = round(df_home['Load Power [kW]'].max()) 
    annual_cost_home, accumulated_cost_home = calculate_accumulated_cost(I_pv, I_bat, years, profit_energy_home)

    df_work = pd.read_csv(f"C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L1_work\\doperRes29.csv")
    profit_energy_work =  round(df_work['Profit surplus energy - annual [USD]'].sum() / 1000)
    max_demand_work = round(df_work['Load Power [kW]'].max()) 
    annual_cost_work, accumulated_cost_work = calculate_accumulated_cost(I_pv, I_bat, years, profit_energy_work)

    df_shop = pd.read_csv(f"C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L2\\doperRes29.csv")
    profit_energy_shop =  round(df_shop['Profit surplus energy - annual [USD]'].sum() / 1000)
    max_demand_shop = round(df_shop['Load Power [kW]'].max()) 
    annual_cost_shop, accumulated_cost_shop = calculate_accumulated_cost(I_pv, I_bat, years, profit_energy_shop)

    df_fast = pd.read_csv(f"C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L3\\doperRes30.csv")
    profit_energy_fast =  round(df_fast['Profit surplus energy - annual [USD]'].sum() / 1000)
    max_demand_fast = round(df_fast['Load Power [kW]'].max()) 
    annual_cost_fast, accumulated_cost_fast = calculate_accumulated_cost(I_pv, I_bat, years, profit_energy_fast)

    df_accum = pd.DataFrame({'Home' : []})
    df_accum['Home'] = accumulated_cost_home
    df_accum['Work'] = accumulated_cost_work
    df_accum['Shopping'] = accumulated_cost_shop
    df_accum['Fast'] = accumulated_cost_fast
    generate_figures_economic(df_accum, years, 'Accumulated Cost 29', graph_folder, 'Thousand of USD')

    df_annual = pd.DataFrame({'Home' : []})
    df_annual['Home'] = annual_cost_home
    df_annual['Work'] = annual_cost_work
    df_annual['Shopping'] = annual_cost_shop
    df_annual['Fast'] = annual_cost_fast
    generate_figures_economic2(df_annual, years, 'Annual Cost 29', graph_folder, 'Thousand of USD')
    
    interestRate = 0.1125
    npc_home = []
    npc_work = []
    npc_shop = []
    npc_fast = []
    for i in range(years-1):
        npc_home.append(annual_cost_home[i] / ((1 + interestRate)**i))
        npc_work.append(annual_cost_work[i] / ((1 + interestRate)**i))
        npc_shop.append(annual_cost_shop[i] / ((1 + interestRate)**i))
        npc_fast.append(annual_cost_fast[i] / ((1 + interestRate)**i))
    npc_home_total = math.ceil(sum(npc_home))
    npc_work_total = math.ceil(sum(npc_work))
    npc_shop_total = math.ceil(sum(npc_shop))
    npc_fast_total = math.ceil(sum(npc_fast))
    
    print('NPC home = ', npc_home_total, '\nNPC workplace = ', npc_work_total, 
          '\nNPC shopping mall = ', npc_shop_total, '\nNPC fast CS = ', npc_fast_total)  