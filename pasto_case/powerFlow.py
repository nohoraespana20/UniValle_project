from pyomo.environ import Objective, minimize
from doper import DOPER, standard_report
from doper.models.basemodel import base_model, default_output_list
from doper.models.battery import add_battery
from doper.models.network import add_network
from parameter_pasto import parameters, ts_inputs
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
    data4  = ts_inputs(parameter, load='B90', scale_load=demand*0.04, scale_pv=861)
    data5  = ts_inputs(parameter, load='B90', scale_load=demand*0.06, scale_pv=1202)
    data6  = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=137)
    data7  = ts_inputs(parameter, load='B90', scale_load=demand*0.02, scale_pv=440)
    data8  = ts_inputs(parameter, load='B90', scale_load=demand*0.03, scale_pv=560)
    data9  = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=170)
    data10 = ts_inputs(parameter, load='B90', scale_load=demand*0.02, scale_pv=480)
    data11 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=260)
    data12 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=215)
    data13 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=146)
    data14 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=249)
    data15 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=151)
    data16 = ts_inputs(parameter, load='B90', scale_load=demand*0.02, scale_pv=319)
    data17 = ts_inputs(parameter, load='B90', scale_load=demand*0.05, scale_pv=934)
    data18 = ts_inputs(parameter, load='B90', scale_load=demand*0.03, scale_pv=594)
    data19 = ts_inputs(parameter, load='B90', scale_load=demand*0.03, scale_pv=688)
    data20 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=185)
    data21 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=147)
    data22 = ts_inputs(parameter, load='B90', scale_load=demand*0.10, scale_pv=1953)
    data23 = ts_inputs(parameter, load='B90', scale_load=demand*0.02, scale_pv=369)
    data24 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=185)
    data25 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=123)
    data26 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=211)
    data27 = ts_inputs(parameter, load='B90', scale_load=demand*0.02, scale_pv=345)
    data28 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=125)
    data29 = ts_inputs(parameter, load='B90', scale_load=demand*0.01, scale_pv=199)
    data30 = ts_inputs(parameter, load='B90', scale_load=demand*0.14, scale_pv=2772)
    data31 = ts_inputs(parameter, load='B90', scale_load=demand*0.02, scale_pv=506)
    data32 = ts_inputs(parameter, load='B90', scale_load=demand*0.04, scale_pv=866)
    data33 = ts_inputs(parameter, load='B90', scale_load=demand*0.06, scale_pv=1195)
    data34 = ts_inputs(parameter, load='B90', scale_load=demand*0.09, scale_pv=1831)
    data35 = ts_inputs(parameter, load='B90', scale_load=demand*0.02, scale_pv=449)
    data36 = ts_inputs(parameter, load='B90', scale_load=demand*0.08, scale_pv=1594)
    # use data1 as starting point for multinode df
    data = data5.copy()
    # drop load and pv from multinode df
    data = data.drop(labels='load_demand', axis=1)
    data = data.drop(labels='generation_pv', axis=1)
    # demand node
    data['pf_demand_node4']  =  data5['load_demand']
    data['pf_demand_node5']  =  data5['load_demand']
    data['pf_demand_node6']  =  data6['load_demand']
    data['pf_demand_node7']  =  data7['load_demand']
    data['pf_demand_node8']  =  data8['load_demand']
    data['pf_demand_node9']  =  data9['load_demand']
    data['pf_demand_node10'] = data10['load_demand']
    data['pf_demand_node11'] = data11['load_demand']
    data['pf_demand_node12'] = data12['load_demand']
    data['pf_demand_node13'] = data13['load_demand']
    data['pf_demand_node14'] = data14['load_demand']
    data['pf_demand_node15'] = data15['load_demand']
    data['pf_demand_node16'] = data16['load_demand']
    data['pf_demand_node17'] = data17['load_demand']
    data['pf_demand_node18'] = data18['load_demand']
    data['pf_demand_node19'] = data19['load_demand']
    data['pf_demand_node20'] = data20['load_demand']
    data['pf_demand_node21'] = data21['load_demand']
    data['pf_demand_node22'] = data22['load_demand']
    data['pf_demand_node23'] = data23['load_demand']
    data['pf_demand_node24'] = data24['load_demand']
    data['pf_demand_node25'] = data25['load_demand']
    data['pf_demand_node26'] = data26['load_demand']
    data['pf_demand_node27'] = data27['load_demand']
    data['pf_demand_node28'] = data28['load_demand']
    data['pf_demand_node29'] = data29['load_demand']
    data['pf_demand_node30'] = data30['load_demand']
    data['pf_demand_node31'] = data31['load_demand']
    data['pf_demand_node32'] = data32['load_demand']
    data['pf_demand_node33'] = data33['load_demand']
    data['pf_demand_node34'] = data34['load_demand']
    data['pf_demand_node35'] = data35['load_demand']
    data['pf_demand_node36'] = data36['load_demand']
    # generation node
    data['pf_pv_node4']  =  data4['generation_pv']
    data['pf_pv_node5']  =  data5['generation_pv']
    data['pf_pv_node6']  =  data6['generation_pv']
    data['pf_pv_node7']  =  data7['generation_pv']
    data['pf_pv_node8']  =  data8['generation_pv'] 
    data['pf_pv_node9']  =  data9['generation_pv'] 
    data['pf_pv_node10'] = data10['generation_pv'] 
    data['pf_pv_node11'] = data11['generation_pv'] 
    data['pf_pv_node12'] = data12['generation_pv'] 
    data['pf_pv_node13'] = data13['generation_pv'] 
    data['pf_pv_node14'] = data14['generation_pv'] 
    data['pf_pv_node15'] = data15['generation_pv'] 
    data['pf_pv_node16'] = data16['generation_pv'] 
    data['pf_pv_node17'] = data17['generation_pv'] 
    data['pf_pv_node18'] = data18['generation_pv'] 
    data['pf_pv_node19'] = data19['generation_pv'] 
    data['pf_pv_node20'] = data20['generation_pv'] 
    data['pf_pv_node21'] = data21['generation_pv'] 
    data['pf_pv_node22'] = data22['generation_pv'] 
    data['pf_pv_node23'] = data23['generation_pv'] 
    data['pf_pv_node24'] = data24['generation_pv'] 
    data['pf_pv_node25'] = data25['generation_pv'] 
    data['pf_pv_node26'] = data26['generation_pv'] 
    data['pf_pv_node27'] = data27['generation_pv'] 
    data['pf_pv_node28'] = data28['generation_pv'] 
    data['pf_pv_node29'] = data29['generation_pv'] 
    data['pf_pv_node30'] = data30['generation_pv'] 
    data['pf_pv_node31'] = data31['generation_pv'] 
    data['pf_pv_node32'] = data32['generation_pv'] 
    data['pf_pv_node33'] = data33['generation_pv'] 
    data['pf_pv_node34'] = data34['generation_pv'] 
    data['pf_pv_node35'] = data35['generation_pv']
    data['pf_pv_node36'] = data36['generation_pv'] 
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
    print(standard_report(res))
    return df

def save_results_solver(df, i):
    df.to_excel(f'./results/L2_3/doperRes{i}.xlsx', index=False)
    df.to_csv(f'./results/L2_3/doperRes{i}.csv', index=False)

def show_results_solver(df, i):
    plt.plot(df[['Import Power [kW]','PV Power [kW]', 'Load Power [kW]']])
    plt.title('Power flow at PCC')
    plt.legend(['Import Power [kW]','PV Power [kW]', 'Load Power [kW]'])
    plt.save(f'./results/L2_3/Fig1_{i}.jpg')
    plot_dynamic(df, parameter, plotFile = f'./results/L2_3/Fig2_{i}.jpg', plot_reg=False)

if __name__ == '__main__':  
    parameter = parameters()
    demand = [8.9, 38.7, 582.5, 1155.6, 2989.8, 6340.0, 9108.8, 23724.3, 11865.5,
             4629.7, 19548.7, 25972.5, 35441.8, 41558.6, 536.5, 2301.6, 139.3,
             86847.3, 123598.7, 155795.6, 109602.5, 108342.6, 99047.5, 67926.1,
             14709.8, 236133.7, 19783.1, 226017.5, 20115.6, 35732.1]
    data_frames = []

    print('Demand = ', demand[6], 'Año = ', 6)
    data = data_multinode(parameter, demand[6])
    df = execute_solver(parameter, data)
    data_frames.append(df)
    save_results_solver(df, 6)
    show_results_solver(df, 6)
    

    # for i in range(len(demand)):
    #     print('Demand = ', demand[i], 'Año = ', i)
    #     data = data_multinode(parameter, demand[i])
    #     df = execute_solver(parameter, data)
    #     data_frames.append(df)
    #     save_results_solver(df, i)
    #     show_results_solver(df, i)
    # #TODO: Correr para L1, L2y3, L4