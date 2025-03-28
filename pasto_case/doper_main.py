import gc
import re
import os
from pyomo.environ import Objective, minimize
from doper import DOPER, standard_report
from doper.models.basemodel import base_model, default_output_list
from doper.models.battery import add_battery
from doper.models.network import add_network
from doper_parameter import parameters, ts_inputs
from doper.plotting import plot_dynamic
import pandas as pd
import matplotlib.pyplot as plt

def control_model(inputs, parameter):
    model = base_model(inputs, parameter)
    model = add_battery(model, inputs, parameter)
    model = add_network(model, inputs, parameter)
    
    def objective_function(model):
        return model.sum_energy_cost * parameter['objective']['weight_energy'] \
               + model.sum_demand_cost * parameter['objective']['weight_demand'] \
               + model.sum_export_revenue * parameter['objective']['weight_export'] \
               + model.fuel_cost_total * parameter['objective']['weight_energy'] 
    model.objective = Objective(rule=objective_function, sense=minimize, doc='objective function')
    return model

def pv_value(valor_inicial, incremento, elementos):
    lista_valores = [valor_inicial * (1 + incremento) ** i for i in range(elementos)]
    return lista_valores

def data_multinode(parameter, demand, i):
    # p1 = pv_value(valor_inicial = 6121, incremento = 0.10, elementos = 31)
    # p2 = pv_value(valor_inicial = 4455, incremento = 0.10, elementos = 31)
    # p3 = pv_value(valor_inicial = 9882, incremento = 0.10, elementos = 31)

    p1 = pv_value(valor_inicial = 1048, incremento = 0.01, elementos = 31)
    p2 = pv_value(valor_inicial = 873, incremento = 0.01, elementos = 31)
    p3 = pv_value(valor_inicial = 4833, incremento = 0.01, elementos = 31)

    data4  = ts_inputs(parameter, load='B90', scale_load=demand*0.30, scale_pv=p1[i])
    data5  = ts_inputs(parameter, load='B90', scale_load=demand*0.22, scale_pv=p2[i])
    data6  = ts_inputs(parameter, load='B90', scale_load=demand*0.48, scale_pv=p3[i])
    # use data1 as starting point for multinode df
    data = data5.copy()
    # drop load and pv from multinode df
    data = data.drop(labels='load_demand', axis=1)
    data = data.drop(labels='generation_pv', axis=1)
    # demand node
    data['pf_demand_node4']  =  data4['load_demand']
    data['pf_demand_node18']  =  data5['load_demand']
    data['pf_demand_node27']  =  data6['load_demand']
    # generation node
    data['pf_pv_node4']  =  data4['generation_pv']
    data['pf_pv_node18']  =  data5['generation_pv']
    data['pf_pv_node27']  =  data6['generation_pv']
    return data

def execute_solver(parameter, data):
    output_list = default_output_list(parameter)
    solver_path = "C:\\Nohora\\UniValle_project\\pasto_case\\DOPER\\doper\\solvers\\Windows64\\cbc.exe"
    
    smartDER = DOPER(model=control_model,
                     parameter=parameter,
                     solver_path=solver_path,
                     output_list=output_list)
    res = smartDER.do_optimization(data)
    duration, objective, df, model, result, termination, parameter = res
    return df, res

def save_results_solver(df, i):
  df.to_csv(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper/doperRes{i}.csv', index=False)

def show_results_solver(df, i):
    colors = {'Import Power [kW]': '#00bae1', 'PV Power [kW]': '#ff9800',  'Load Power [kW]': '#000000'}
    plt.plot(df['Import Power [kW]'], color=colors['Import Power [kW]'], label='Import Power [kW]')
    plt.plot(df['PV Power [kW]'], color=colors['PV Power [kW]'], label='PV Power [kW]')
    plt.plot(df['Load Power [kW]'], color=colors['Load Power [kW]'], label='Load Power [kW]')
    plt.title('Power flow at PCC')
    plt.legend(['Import Power [kW]','PV Power [kW]', 'Load Power [kW]'])
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper/Fig1_{i}.jpg')
    plt.close()
    plot_dynamic(df, parameter, plotFile = f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper/Fig2_{i}.jpg', plot_reg=False)

def extract_values(file_path):
    cost_value = None
    objective_value = None
    with open(file_path, 'r') as file:
        for line in file:
            if "Objective [$]" in line:
                match = re.search(r'Objective \[\$\]\s+(\d+\.\d+)', line)
                if match:
                    objective_value = float(match.group(1))
            if "Cost [$]" in line:
                match = re.search(r'Cost \[\$\]\s+(\d+\.\d+)', line)
                if match:
                    cost_value = float(match.group(1))
    return objective_value, cost_value

if __name__ == '__main__':  
    parameter = parameters()
    df_demand = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/fuel_demand.csv')
    scenario = 'Scenario 3'
    scenario_selected = df_demand.loc[df_demand.loc[:, 'Scenario'] == scenario]
    demand = list(scenario_selected["Electricity [kWh]"])
  
    data_frames = []
    for i in range(len(demand)):
        print('Demand = ', demand[i], 'Position = ', i)  
        try:
            data = data_multinode(parameter, demand[i]/24, i)
            df, res = execute_solver(parameter, data)
            data_frames.append(df)
            save_results_solver(df, i)
            show_results_solver(df, i)
            plt.close('all')
            print(standard_report(res))
            with open(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper/terminalRes{i}.txt', 'w') as k:
                k.write(standard_report(res))
            del data, df, res
            gc.collect()
        except:
            print(f'Error in solver {i}')

    folder_path1 = "C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper"
    files1 = sorted([f for f in os.listdir(folder_path1) if f.startswith("terminalRes") and f.endswith(".txt")],
                    key=lambda x: int(re.search(r'\d+', x).group()))

    data1_ob, data1_co, data2_ob, data2_co, data3_ob, data3_co = [], [], [], [], [], []
    for file in files1:
        file_path = os.path.join(folder_path1, file)
        objective_value, cost_value = extract_values(file_path)
        data1_ob.append(objective_value)
        data1_co.append(cost_value)

    years = list(scenario_selected["Year"])
    df_compareCost= pd.DataFrame({'Year': years,
                                  'PV Cost [$]': data1_ob,
                                  'Energy Cost [$]': data1_co})
    df_compareCost.fillna(0, inplace=True)
    df_compareCost.to_csv(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/costEnergyCompare.csv')