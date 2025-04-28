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
    plt.xlabel('Hora')
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

    start_year = 2025
    year = list(range(start_year, start_year + years))
    plt.figure(figsize=(10, 6))
    plt.plot(year, df)
    plt.xlabel('Año')
    plt.ylabel(f'{metric_name}')
    plt.title(f'{file_name}')
    plt.grid(True)
    step = max(1, years // 10)
    plt.xticks(ticks=year[::step], labels=year[::step], rotation=90) 
    plt.savefig(graph_path)
    plt.close()

def generate_comparison_economic(df1, df2, df3, years, file_name, graph_folder, metric_name):
    graph_path = os.path.join(graph_folder, f"{os.path.splitext(file_name)[0]}_comparison.png")

    start_year = 2025
    year = list(range(start_year, start_year + years))

    plt.figure(figsize=(10, 6))
    plt.plot(year, df1, label='Sistema FV sin crecimiento')
    plt.plot(year, df2, label='Sistema FV con crecimiento 10%')
    plt.plot(year, df3, label='Sistema FV con crecimiento 20%')
    
    plt.xlabel('Año')
    plt.ylabel(f'{metric_name}')
    plt.title(f'{file_name}')
    plt.legend()
    plt.grid(True)

    step = max(1, years // 10)
    plt.xticks(ticks=year[::step], labels=year[::step], rotation=90) 
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()

def generate_figures_economic2(data_list, years, file_name, graph_folder, metric_name):
    graph_path = os.path.join(graph_folder, f"bar_{os.path.splitext(file_name)[0]}.png")
    
    start_year = 2025
    year = list(range(start_year, start_year + years))

    plt.figure(figsize=(12, 6))
    plt.bar(year, data_list, color='skyblue')
    plt.xlabel('Año')
    plt.ylabel(f'{metric_name}')
    plt.title(f'{file_name}')
    plt.xticks(ticks=year, labels=year, rotation=90)  
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()  
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
    # x = np.arange(years)
    start_year = 2025
    x = list(range(start_year, start_year + years))
    width = 0.6

    plt.figure(figsize=(14, 7))
    plt.bar(x, profits, width, label='Utilidades de la venta de excedentes de energía', color='green')
    plt.bar(x, [-c for c in costs], width, label='Costos de nueva infraestructura, mantenimiento, actualización, electricidad', color='red')  # Costos como negativos

    plt.axhline(0, color='black', linewidth=0.8)
    plt.xlabel('Año')
    plt.ylabel('Miles de dólares')
    plt.legend()
    plt.xticks(ticks=x, labels=x, rotation=90)
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

    start_year = 2025
    year = list(range(start_year, start_year + 30))
    plt.figure(figsize=(10, 6))
    plt.plot(year, averages1, color='red')
    plt.plot(year, averages2, color='blue')
    plt.plot(year, averages3, color='green')
    plt.legend(['Sistema FV sin crecimiento','Sistema FV con crecimiento 10%','Sistema FV con crecimiento 20%'])
    plt.xlabel("Año")
    plt.ylabel(f"{graph_name} (%")
    plt.title(f"Evolución anual de {graph_name}")
    plt.grid(True)
    plt.savefig(graph_path)
    plt.close()

def calcular_area(kW_pv_inicial, graph_folder, graph_name):
    graph_path = os.path.join(graph_folder, f"{graph_name}.png")
    
    factores_incremento = {
        'Sistema FV sin crecimiento': 0, 
        'Sistema FV con crecimiento 10%': 0.10, 
        'Sistema FV con crecimiento 20%': 0.20
    }
    start_year = 2025
    n_years = 30
    year = np.arange(start_year, start_year + n_years)  

    plt.figure(figsize=(10,6))
    
    for nombre_caso, incremento in factores_incremento.items():
        kW_pv = kW_pv_inicial * (1 + incremento) ** (year - start_year)
        num_paneles = kW_pv * 1000 / (0.9 * 550 * 3.5)  
        area_PV = num_paneles * 3  # m²

        area_inicio = area_PV[0]
        area_final = area_PV[-1]
        print(f"{nombre_caso}:")
        print(f" - Área en {start_year}: {area_inicio:.2f} m²")
        print(f" - Área en {start_year + n_years - 1}: {area_final:.2f} m²\n")
        plt.plot(year, area_PV, label=nombre_caso)

    plt.xlabel('Año')
    plt.ylabel('Área necesaria (m²)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()

def calcular_trabajos(kW_pv_inicial, graph_folder, graph_name):
    graph_path = os.path.join(graph_folder, f"{graph_name}.png")
    factores_incremento = {'Sistema FV sin crecimiento': 0, 'Sistema FV con crecimiento 10%': 0.10, 'Sistema FV con crecimiento 20%': 0.20}
    factores_incremento = {
        'Sistema FV sin crecimiento': 0, 
        'Sistema FV con crecimiento 10%': 0.10, 
        'Sistema FV con crecimiento 20%': 0.20
    }
    start_year = 2025
    n_years = 30
    year = np.arange(start_year, start_year + n_years)

    plt.figure(figsize=(10,6))

    for nombre_caso, incremento in factores_incremento.items():
        kW_pv = kW_pv_inicial * (1 + incremento) ** (year - start_year)

        energia_anual_kWh = kW_pv * 24 * 365  # kWh/año
        energia_anual_GWh = energia_anual_kWh / 1e6  # GWh/año

        trabajos = 0.87 * energia_anual_GWh  # jobs por año
        trabajos_inicio = trabajos[0]
        trabajos_final = trabajos[-1]
        print(f"{nombre_caso}:")
        print(f" - Trabajos en {start_year}: {trabajos_inicio:.2f} ")
        print(f" - Trabajos en {start_year + n_years - 1}: {trabajos_final:.2f}")
        plt.plot(year, trabajos, label=nombre_caso)

    plt.xlabel('Año')
    plt.ylabel('Trabajos generados')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()

def calcular_emisiones_CO2(kW_pv_inicial, base_folder, graph_folder, graph_name):
    factores_incremento = {
        'Sistema FV sin crecimiento': 0, 
        'Sistema FV con crecimiento 10%': 0.10, 
        'Sistema FV con crecimiento 20%': 0.20
    }
    carpetas_casos = {
        'Sistema FV sin crecimiento': 'results_DER_case1',
        'Sistema FV con crecimiento 10%': 'results_DER_case2',
        'Sistema FV con crecimiento 20%': 'results_DER_case3'
    }

    start_year = 2025
    n_years = 30
    years = np.arange(start_year, start_year + n_years)
    
    plt.figure(figsize=(10,6))
    
    for nombre_caso, incremento in factores_incremento.items():
        co2_total = []  # Lista para almacenar las emisiones de cada año
        carpeta = os.path.join(base_folder, carpetas_casos[nombre_caso])
        
        for i in range(1, n_years + 1):
            # Cargar datos de Import Power
            file_path = os.path.join(carpeta, f'doperRes{i}.csv')
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
            else:
                print(f"Archivo no encontrado: {file_path}")
                co2_total.append(np.nan)
                continue

            # Cálculo de kW_pv para ese año
            kW_pv = kW_pv_inicial * (1 + incremento) ** (i - 1)

            # Emisiones CO2 por paneles solares
            CO2paneles = (kW_pv * 24 * 365) * 40  # g CO2 eq por año

            # Emisiones CO2 por electricidad importada
            if 'Import Power [kW]' in df.columns:
                CO2electricidad = df['Import Power [kW]'].sum() * 164.38  # g CO2 eq anual
            else:
                print(f"Columna 'Import Power [kW]' no encontrada en {file_path}")
                CO2electricidad = 0

            # Emisiones totales
            CO2total_anual = CO2paneles + CO2electricidad
            co2_total.append(CO2total_anual / 1e6)  # Convertir a toneladas de CO2 eq (t CO2 eq)

        plt.plot(years, co2_total, label=nombre_caso)

    plt.xlabel('Año')
    plt.ylabel('Toneladas de CO₂ eq./kWh')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    graph_path = os.path.join(graph_folder, f"{graph_name}.png")
    plt.savefig(graph_path)
    plt.close()

if __name__ == '__main__':
    #####Technical metrics####
    # input_folder = "C:/Nohora/UniValle_project/pasto_case/results_DOPER_case3"
    # process_data_files(input_folder, output_folder, graph_folder)
    
    output_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case3"
    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case3"

    kW_pv = 6754
    kW_bat = 5754
    I_pv_base = (609 * 1.071) * kW_pv
    I_bat_base = 67.4 * kW_bat

    ### COMPARISON ACCUMULATED COST 3 CASES
    output_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case1"
    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case1"   
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
    rate_new = 0.0 # 0% de crecimiento en PV
    annual_cost1, accumulated_cost1, npc_total1 = calculate_accumulated_cost(I_pv_base, I_bat_base, years, rate_new, energy_import_cost_list)
    generate_figures_economic(accumulated_cost1, years, 'Costo acumulado descontado', graph_folder, 'Miles de dólares')
    generate_figures_economic2(annual_cost1, years, 'Costo anual', graph_folder, 'Miles de dólares')
    discounted_profits = calculate_discounted_profits(profit_energy_list)
    generate_income_vs_cost_bar_chart(discounted_profits, annual_cost1, years, graph_folder)
    print('NPC =', npc_total1)
    print('Valor presente neto de ingresos:', sum(discounted_profits))


    output_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case2"
    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case2"   
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
    rate_new = 0.1 # 10% de crecimiento en PV
    annual_cost2, accumulated_cost2, npc_total2 = calculate_accumulated_cost(I_pv_base, I_bat_base, years, rate_new, energy_import_cost_list)
    generate_figures_economic(accumulated_cost2, years, 'Costo acumulado descontado', graph_folder, 'Miles de dólares')
    generate_figures_economic2(annual_cost2, years, 'Costo anual', graph_folder, 'Miles de dólares')
    discounted_profits = calculate_discounted_profits(profit_energy_list)
    generate_income_vs_cost_bar_chart(discounted_profits, annual_cost2, years, graph_folder)
    print('NPC =', npc_total2)
    print('Valor presente neto de ingresos:', sum(discounted_profits))


    output_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case3"
    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case3"   
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
    rate_new = 0.2 # 20% de crecimiento en PV
    annual_cost3, accumulated_cost3, npc_total3 = calculate_accumulated_cost(I_pv_base, I_bat_base, years, rate_new, energy_import_cost_list)
    generate_figures_economic(accumulated_cost3, years, 'Costo acumulado descontado', graph_folder, 'Miles de dólares')
    generate_figures_economic2(annual_cost3, years, 'Costo anual', graph_folder, 'Miles de dólares')
    discounted_profits = calculate_discounted_profits(profit_energy_list)
    generate_income_vs_cost_bar_chart(discounted_profits, annual_cost3, years, graph_folder)
    print('NPC =', npc_total3)
    print('Valor presente neto de ingresos:', sum(discounted_profits))

    generate_comparison_economic(accumulated_cost1, accumulated_cost2, accumulated_cost3, years, 'Costo acumulado descontado', graph_folder, 'Miles de dólares')
    
    generate_technical_comparison(
        input_folder1="C:/Nohora/UniValle_project/pasto_case/results_DER_case1",
        input_folder2="C:/Nohora/UniValle_project/pasto_case/results_DER_case2",
        input_folder3="C:/Nohora/UniValle_project/pasto_case/results_DER_case3",
        graph_folder=graph_folder,
        metric_col='PV/Import Power (%)',
        graph_name='Comparación cuota de generación renovable'
    )
    generate_technical_comparison(
        input_folder1="C:/Nohora/UniValle_project/pasto_case/results_DER_case1",
        input_folder2="C:/Nohora/UniValle_project/pasto_case/results_DER_case2",
        input_folder3="C:/Nohora/UniValle_project/pasto_case/results_DER_case3",
        graph_folder=graph_folder,
        metric_col='Battery Utilization Rate (%)',
        graph_name='Comparación tasa de utilización de baterías'
    )

    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case1"  
    df = pd.read_csv("C:/Nohora/UniValle_project/pasto_case/results_DER_case1/doperRes30.csv")
    generate_figures_technical(df['PV/Import Power (%)'],'Cuota de generación renovable',graph_folder, '%')
    generate_figures_technical(df['Battery Utilization Rate (%)'],'Tasa de utilización de baterías',graph_folder, '%')

    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case2"  
    df = pd.read_csv("C:/Nohora/UniValle_project/pasto_case/results_DER_case2/doperRes30.csv")
    generate_figures_technical(df['PV/Import Power (%)'],'Cuota de generación renovable',graph_folder, '%')
    generate_figures_technical(df['Battery Utilization Rate (%)'],'Tasa de utilización de baterías',graph_folder, '%')

    graph_folder = "C:/Nohora/UniValle_project/pasto_case/results_DER_case3"  
    df = pd.read_csv("C:/Nohora/UniValle_project/pasto_case/results_DER_case3/doperRes30.csv")
    generate_figures_technical(df['PV/Import Power (%)'],'Cuota de generación renovable',graph_folder, '%')
    generate_figures_technical(df['Battery Utilization Rate (%)'],'Tasa de utilización de baterías',graph_folder, '%')

    calcular_area(kW_pv, graph_folder, 'area')
    calcular_trabajos(kW_pv, graph_folder, 'jobs')

    calcular_emisiones_CO2(kW_pv, "C:/Nohora/UniValle_project/pasto_case", graph_folder, 'emisiones')