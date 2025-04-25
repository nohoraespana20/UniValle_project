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
                df['Profit surplus energy - [USD]']  = df['Export Power [kW]'] * 0.12
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
    step = max(1, years // 10)
    plt.xticks(ticks=np.arange(0, years, step), labels=year[::step], rotation=0)
    plt.savefig(graph_path)
    plt.close()

def generate_figures_economic2(data_list, years, file_name, graph_folder, metric_name):
    graph_path = os.path.join(graph_folder, f"bar_{os.path.splitext(file_name)[0]}.png")
    year = list(range(years))

    plt.figure(figsize=(12, 6))
    plt.bar(year, data_list, color='skyblue')
    plt.xlabel('Year')
    plt.ylabel(f'{metric_name}')
    plt.title(f'{file_name}')
    plt.xticks(ticks=np.arange(years), labels=year, rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(graph_path)
    plt.close()

def calculate_accumulated_cost(I_PV_base, I_bat_base, years, rate_new, energy_import_cost_list):
    """
    Calcula costos anuales y acumulados considerando inversión, mantenimiento, retrofit y costo de energía.

    Args:
        I_PV_base (float): Inversión base del 100% inicial de paneles solares.
        I_bat_base (float): Inversión base del 100% inicial de baterías.
        years (int): Número de años del análisis.
        energy_import_cost_list (list): Lista con costo de energía importada por año (en miles de USD).

    Returns:
        list: Costos anuales (sin descuento).
        list: Costos acumulados.
        float: NPC total.
    """
    maintenance_rate = 0.1
    retrofit_rate = 0.5
    annual_cost = []
    accumulated_cost = []
    npc = []

    # Variables acumuladas para mantenimiento
    cumulative_pv = I_PV_base
    cumulative_bat = I_bat_base

    for year in range(years):
        if year == 0:
            investment = (I_PV_base + I_bat_base) / 1000
            maintenance = investment * maintenance_rate
            retrofit = 0
        else:
            # Nueva inversión del 10% de la base
            new_pv = I_PV_base * rate_new
            new_bat = I_bat_base * rate_new
            new_investment = (new_pv + new_bat) / 1000

            # Actualizar acumulado
            cumulative_pv += new_pv
            cumulative_bat += new_bat

            # Mantenimiento sobre la capacidad total acumulada
            maintenance = ((cumulative_pv + cumulative_bat) / 1000) * maintenance_rate

            # Retrofit si aplica
            total_investment_to_date = (cumulative_pv + cumulative_bat) / 1000
            retrofit = total_investment_to_date * retrofit_rate if year % 10 == 0 else 0

            investment = new_investment

        # Costo de energía importada (ya en miles de USD)
        energy_cost = energy_import_cost_list[year]

        total_cost = investment + maintenance + retrofit + energy_cost

        # Tasa de descuento variable
        discount_rate = 0.09

        discounted = total_cost / ((1 + discount_rate) ** year)

        annual_cost.append(round(discounted))
        accumulated_cost.append(round(sum(annual_cost)))
        npc.append(discounted)

    return annual_cost, accumulated_cost, round(sum(npc))

def calculate_discounted_profits(profit_energy_list):
    discounted_profits = []
    for year, profit in enumerate(profit_energy_list):
        discount_rate = 0.09
        discounted = profit / ((1 + discount_rate) ** year)
        discounted_profits.append(round(discounted))
    return discounted_profits

def generate_income_vs_cost_bar_chart(profits, costs, years, graph_folder, file_name='Income_vs_Cost'):
    graph_path = os.path.join(graph_folder, f"{file_name}.png")
    x = np.arange(years)
    width = 0.6

    plt.figure(figsize=(14, 7))
    plt.bar(x, profits, width, label='Profit from the sale of surplus energy', color='green')
    plt.bar(x, [-c for c in costs], width, label='New infrastructure, maintenance, retrofit costs', color='red')  # Costos como negativos

    plt.axhline(0, color='black', linewidth=0.8)
    plt.xlabel('Year')
    plt.ylabel('Thousand of USD')
    plt.legend()
    plt.xticks(ticks=x, labels=x)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.savefig(graph_path)
    plt.close()

def generate_technical_comparison(input_folder1, input_folder2, input_folder3, graph_folder, metric_col, graph_name):
    """
    Genera una gráfica comparativa del promedio anual de una métrica técnica específica.

    Args:
        input_folder (str): Carpeta donde están los archivos doperRes*.csv.
        graph_folder (str): Carpeta donde guardar la gráfica.
        metric_col (str): Nombre de la columna a analizar (e.g., 'PV/Import Power (%)').
        graph_name (str): Nombre para el archivo de salida.
    """
    years = []
    averages1 = []
    averages2 = []
    averages3 = []

    for year in range(1, 31):
        file_path1 = os.path.join(input_folder1, f"doperRes{year}.csv")
        file_path2 = os.path.join(input_folder2, f"doperRes{year}.csv")
        file_path3 = os.path.join(input_folder3, f"doperRes{year}.csv")
        try:
            df1 = pd.read_csv(file_path1)
            df2 = pd.read_csv(file_path2)
            df3 = pd.read_csv(file_path3)
            if metric_col in df1.columns:
                mean_val1 = df1[metric_col].mean()
                years.append(year)
                averages1.append(mean_val1)
            else:
                print(f"Columna {metric_col} no encontrada en {file_path}.")
            if metric_col in df2.columns:
                mean_val2 = df2[metric_col].mean()
                averages2.append(mean_val2)
            else:
                print(f"Columna {metric_col} no encontrada en {file_path}.")
            if metric_col in df3.columns:
                mean_val3 = df3[metric_col].mean()
                averages3.append(mean_val3)
            else:
                print(f"Columna {metric_col} no encontrada en {file_path}.")
        except Exception as e:
            print(f"Error al leer {file_path}: {e}")

    # Graficar
    graph_path = os.path.join(graph_folder, f"{graph_name}.png")
    plt.figure(figsize=(10, 6))
    plt.plot(years, averages1, marker='o', linestyle='-', color='blue')
    plt.plot(years, averages2, marker='o', linestyle='-', color='red')
    plt.plot(years, averages3, marker='o', linestyle='-', color='green')
    plt.legend(['PV system without growth','PV system with growth 10\%','PV system with growth 50\%'])
    plt.xlabel("Año")
    plt.ylabel(f"{metric_col}")
    plt.title(f"Evolución Anual de {metric_col}")
    plt.grid(True)
    plt.savefig(graph_path)
    plt.close()

if __name__ == '__main__':
    input_folder = "C:/Nohora/UniValle_project/pasto_case/results_DOPER_case3"
    output_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case3"
    # graph_folder = os.path.join(output_folder, "graficas")
    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case3"

    #####Technical metrics####
    # process_data_files(input_folder, output_folder, graph_folder)
    
    years = 30  # Número de años
    profit_energy_list = []
    for year in range(1, years + 1):
        file_path = output_folder+f"/doperRes{year}.csv"
        df_year = pd.read_csv(file_path)
        profit = df_year['Profit surplus energy - [USD]'].sum() * 365 / 1000
        profit_energy_list.append(profit)
    
    energy_import_cost_list = []
    for year in range(1, years + 1):
        file_path = output_folder+f"/doperRes{year}.csv"
        df = pd.read_csv(file_path)
        import_energy_cost = df["Import Power [kW]"].sum() * 0.22 * 365 / 1000  # En miles de USD
        energy_import_cost_list.append(import_energy_cost)

    # Recalcular inversiones base
    kW_pv = 4833
    kW_bat = 5754
    I_pv_base = (609 * 1.071) * kW_pv
    I_bat_base = 67.4 * kW_bat
    rate_new = 0.1 #0.1
    
    # #  Calcular métricas económicas
    annual_cost, accumulated_cost, npc_total = calculate_accumulated_cost(I_pv_base, I_bat_base, years, rate_new, energy_import_cost_list)
    # Ingresos con descuento
    discounted_profits = calculate_discounted_profits(profit_energy_list)

    # # Gráficas
    generate_figures_economic(accumulated_cost, years, 'Accumulated Cost', graph_folder, 'Thousand of USD')
    generate_figures_economic2(annual_cost, years, 'Annual Cost', graph_folder, 'Thousand of USD')
    generate_income_vs_cost_bar_chart(discounted_profits, annual_cost, years, graph_folder)

    print('NPC =', npc_total)
    print('Valor presente neto de ingresos:', sum(discounted_profits))

    generate_technical_comparison(
        input_folder1="C:/Nohora/UniValle_project/pasto_case/results_DER_case1",
        input_folder2="C:/Nohora/UniValle_project/pasto_case/results_DER_case2",
        input_folder3="C:/Nohora/UniValle_project/pasto_case/results_DER_case3",
        graph_folder=graph_folder,
        metric_col='PV/Import Power (%)',
        graph_name='PV_Import_Power_Evolution'
    )

    generate_technical_comparison(
        input_folder1="C:/Nohora/UniValle_project/pasto_case/results_DER_case1",
        input_folder2="C:/Nohora/UniValle_project/pasto_case/results_DER_case2",
        input_folder3="C:/Nohora/UniValle_project/pasto_case/results_DER_case3",
        graph_folder=graph_folder,
        metric_col='Battery Utilization Rate (%)',
        graph_name='Battery_Utilization_Evolution'
    )