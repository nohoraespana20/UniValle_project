import gc
from pyomo.environ import Objective, minimize
from doper import DOPER, standard_report
from doper.models.basemodel import base_model, default_output_list
from doper.models.battery import add_battery
from doper.models.network import add_network
from parameter_pasto_reduce import parameters, ts_inputs
from doper.plotting import plot_dynamic
import pandas as pd
import matplotlib.pyplot as plt

DEBUG_MODE = False

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

def data_multinode(parameter, demand):
    data4  = ts_inputs(parameter, load='B90', scale_load=demand*0.30, scale_pv=6124)
    data5  = ts_inputs(parameter, load='B90', scale_load=demand*0.22, scale_pv=4455)
    data6  = ts_inputs(parameter, load='B90', scale_load=demand*0.48, scale_pv=9882)
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
    # print(type(res))
    # print(standard_report(res))
    return df, res

def save_results_solver(df, i):
    df.to_csv(f'C:/Nohora/UniValle_project/pasto_case/results/L1_home/doperRes{i}.csv', index=False)

def show_results_solver(df, i):
    plt.plot(df[['Import Power [kW]','PV Power [kW]', 'Load Power [kW]']])
    plt.title('Power flow at PCC')
    plt.legend(['Import Power [kW]','PV Power [kW]', 'Load Power [kW]'])
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results/L1_home/Fig1_{i}.jpg')
    plot_dynamic(df, parameter, plotFile = f'C:/Nohora/UniValle_project/pasto_case/results/L1_home/Fig2_{i}.jpg', plot_reg=False)

if __name__ == '__main__':  
    parameter = parameters()
    # DEMAND L1 HOME-WORKPLACE
    demand = [11.2, 105.6, 304.5, 709.0, 1353.9, 909.9, 2684.1, 139.3, 21.6,5031.2,
              848.3, 5882.9, 6526.3, 243.5, 19847.1, 23634.2, 29872.8, 1163.5, 2629.1, 1135.7, 
              39.4, 4308.3, 33677.1, 6931.9, 66063.3, 12667.2, 71894.8, 335.3, 27659.8, 45793.6]
    # #DEMAND L2 SHOPPING MALL
    # # demand = [8.9, 38.7, 582.5, 1155.6, 2989.8, 6340.0, 9108.8, 23724.3, 11865.5, 
    # #          4629.7, 19548.7, 25972.5, 35441.8, 41558.6, 536.5, 2301.6, 139.3,
    # #          86847.3, 123598.7, 155795.6, 109602.5, 108342.6, 99047.5, 67926.1,
    # #          14709.8, 236133.7, 19783.1, 226017.5, 20115.6, 35732.1]
    # #DEMAND L3 FAST
    # # demand = [0.0, 4.7, 226.5, 134.2, 522.4, 87.2, 1514.9, 124.9, 497.5, 14610.3, 4553.6, 
    # #           13179.0, 983.2, 1183.4, 32933.0, 492.7, 112.1, 52.1, 76430.1, 41323.4, 53832.9,
    # #           150721.6, 102287.8, 10489.3, 208568.5, 111.6, 16747.6, 3055.4, 227745.7, 164255.1, 62742.2]
    # demand = [1000, 2000, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000]
    data_frames = []
    # demand = [12667.2]
    for i in range(len(demand)):
    # for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 17, 18, 20, 21, 25, 27]:
        print('Demand = ', demand[i], 'Position = ', i)
        try:
            data = data_multinode(parameter, demand[i])

            df, res = execute_solver(parameter, data)
            data_frames.append(df)
            save_results_solver(df, i)
            show_results_solver(df, i)
            del data, df, res
            gc.collect()
            print(standard_report(res))
            with open(f'C:/Nohora/UniValle_project/pasto_case/results/L1_home/terminalRes{i}.txt', 'w') as k:
                k.write(standard_report(res))
        except:
            print(f'Error in solver {i}')