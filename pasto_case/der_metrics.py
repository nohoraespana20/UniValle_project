import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

                # Llamada a la función para generar figuras
                generate_figures(df, file_name, graph_folder)

            except ZeroDivisionError:
                print(f"Error: División por cero en {file_name}. Se omite.")
            except Exception as e:
                print(f"Error inesperado al procesar {file_name}: {e}")

def generate_figures(df, file_name, graph_folder):
    """
    Genera figuras a partir de los datos procesados y las guarda en la carpeta de gráficas.

    Args:
        df (pd.DataFrame): DataFrame procesado con los datos calculados.
        file_name (str): Nombre del archivo CSV original.
        graph_folder (str): Ruta de la carpeta para guardar las gráficas.
    """
    graph_path_pv = os.path.join(graph_folder, f"pv_{os.path.splitext(file_name)[0]}.png")
    graph_path_bat = os.path.join(graph_folder, f"bat_{os.path.splitext(file_name)[0]}.png")

    total_rows = len(df)
    time_intervals = pd.date_range(start='00:00', periods=total_rows, freq='5min').strftime('%H:%M')

    # Figura de PV/Import Power
    plt.figure(figsize=(10, 6))
    plt.plot(time_intervals, df['PV/Import Power (%)'], label='PV/Import Power (%)')
    plt.xlabel('Time')
    plt.ylabel('SRG [%]')
    plt.title(f'Share of Renewable Generation L1 - Home chargers')
    plt.grid(True)
    plt.legend()
    step = max(1, total_rows // 10)
    plt.xticks(ticks=np.arange(0, total_rows, step), labels=time_intervals[::step], rotation=0)
    plt.savefig(graph_path_pv)
    plt.close()

    # Figura de Battery Utilization Rate
    plt.figure(figsize=(10, 6))
    plt.plot(time_intervals, df['Battery Utilization Rate (%)'], label='Battery Utilization Rate (%)')
    plt.xlabel('Time')
    plt.ylabel('BUR [%]')
    plt.title(f'Battery Utilization Rate L1 - Home chargers')
    plt.grid(True)
    plt.legend()
    plt.xticks(ticks=np.arange(0, total_rows, step), labels=time_intervals[::step], rotation=0)
    plt.savefig(graph_path_bat)
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
    input_folder = "C:\\Users\\noluc\\OneDrive\\Escritorio\\Univalle\\AvanceTesis_2024B\\simulador\\results_DOPER_oct2024\\L1_home"
    output_folder = "C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L1_home"
    graph_folder = os.path.join(output_folder, "graficas")

    # #Technical metrics
    # process_data_files(input_folder, output_folder, graph_folder)

    # # Economis metrics
    kW_pv =  20461 # PV total
    kW_bat = 11537 # Bat total

    I_pv = (609 * 1.071) * kW_pv  # USD (compra e instalación)
    I_bat = 67.4 * kW_bat  # USD (compra) 
    df = pd.read_csv("C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\L2\\doperRes8.csv")
    profit_energy = round(df['Profit surplus energy - annual [USD]'].sum() / 1000)
    years = 30  # Número de años

    annual_cost, accumulated_cost = calculate_accumulated_cost(I_pv, I_bat, years, profit_energy)
    print(f"El costo acumulado (AC) es: {accumulated_cost[-1]} thousand USD", accumulated_cost[-1]*5000/1000000, 'million COP')
    year = list(range(years))
    plt.plot(year, accumulated_cost)
    plt.xlabel("Year")
    plt.ylabel("Thousands of USD")
    plt.title(f"Accumulated cost - PV system {kW_pv} kW")
    plt.grid(axis = 'y')
    plt.savefig('C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\accumPV_Shopping8.png')
    plt.close()

    plt.plot(year, annual_cost)
    plt.xlabel("Year")
    plt.ylabel("Thousands of USD")
    plt.title(f"Annual cost - PV system {kW_pv} kW")
    plt.grid(axis = 'y')
    plt.savefig('C:\\Users\\noluc\\OneDrive\\Escritorio\\DERMetrics\\annualPV_Shopping8.png')