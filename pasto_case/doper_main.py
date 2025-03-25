import gc
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
  df.to_csv(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper/doperRes{i}.csv', index=False)

def show_results_solver(df, i):
    plt.plot(df[['Import Power [kW]','PV Power [kW]', 'Load Power [kW]']])
    plt.title('Power flow at PCC')
    plt.legend(['Import Power [kW]','PV Power [kW]', 'Load Power [kW]'])
    plt.savefig(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper/Fig1_{i}.jpg')
    plot_dynamic(df, parameter, plotFile = f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper/Fig2_{i}.jpg', plot_reg=False)

if __name__ == '__main__':  
    parameter = parameters()
    df_demand = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/fuel_demand.csv')
    scenario = 'Scenario 3'
    scenario_selected = df_demand.loc[df_demand.loc[:, 'Scenario'] == scenario]
    demand = list(scenario_selected["Electricity [kWh]"])

    # data_frames = []
    # i=0
    # print('Demand = ', demand[i], 'Position = ', i)
    # data = data_multinode(parameter, demand[i])
    # df, res = execute_solver(parameter, data)
    # data_frames.append(df)
    # save_results_solver(df, i)
    # show_results_solver(df, i)
    # plt.close('all')
    # print(standard_report(res))
    # with open(f'C:/Nohora/UniValle_project/pasto_case/results_netherlands/doper/terminalRes{i}.txt', 'w') as k:
    #     k.write(standard_report(res))

    data_frames = []
    for i in range(len(demand)):
        print('Demand = ', demand[i], 'Position = ', i)
        try:
            data = data_multinode(parameter, demand[i])

            df, res = execute_solver(parameter, data)
            data_frames.append(df)
            save_results_solver(df, i)
            show_results_solver(df, i)
            plt.close('all')
            print(standard_report(res))
            with open(f'C:/Nohora/UniValle_project/pasto_case/results/results_netherlands/doper/terminalRes{i}.txt', 'w') as k:
                k.write(standard_report(res))
            del data, df, res
            gc.collect()
        except:
            print(f'Error in solver {i}')