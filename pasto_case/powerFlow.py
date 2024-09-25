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

def data_multinode(parameter):
    L2_demand = [8.9, 38.7, 582.5, 1155.6, 2989.8, 6340.0, 9108.8, 23724.3, 11865.5,
             4629.7, 19548.7, 25972.5, 35441.8, 41558.6, 536.5, 2301.6, 139.3,
             86847.3, 123598.7, 155795.6, 109602.5, 108342.6, 99047.5, 67926.1,
             14709.8, 236133.7, 19783.1, 226017.5, 20115.6, 35732.1]

    data5  = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.03, scale_pv=345)
    data6  = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.01, scale_pv=125)
    data7  = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.02, scale_pv=199)
    data8  = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.24, scale_pv=2772)
    data9  = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.05, scale_pv=594)
    data10 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.04, scale_pv=506)
    data11 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.08, scale_pv=866)
    data12 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.07, scale_pv=856)
    data13 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.10, scale_pv=1202)
    data14 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.01, scale_pv=137)
    data15 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.04, scale_pv=440)
    data16 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.06, scale_pv=688)
    data17 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.05, scale_pv=560)
    data18 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.01, scale_pv=170)
    data19 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.04, scale_pv=480)
    data20 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.02, scale_pv=260)
    data21 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.02, scale_pv=215)
    data22 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.01, scale_pv=144)
    data23 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.02, scale_pv=249)
    data24 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.01, scale_pv=149)
    data25 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.02, scale_pv=185)
    data26 = ts_inputs(parameter, load='B90', scale_load=L2_demand[-1]*0.03, scale_pv=319)

    # use data1 as starting point for multinode df
    data = data5.copy()
    # drop load and pv from multinode df
    data = data.drop(labels='load_demand', axis=1)
    data = data.drop(labels='generation_pv', axis=1)

    # add node specifc load and pv (where applicable)
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
    return data

if __name__ == '__main__':  
    parameter = parameters()
    data = data_multinode(parameter)
    output_list = default_output_list(parameter)
    solver_path = "C:\\Nohora\\UniValle_project\\pasto_case\\DOPER\\doper\\solvers\\Windows64\\cbc.exe"
    smartDER = DOPER(model=control_model,
                     parameter=parameter,
                     solver_path=solver_path,
                     output_list=output_list)
    res = smartDER.do_optimization(data)
    duration, objective, df, model, result, termination, parameter = res
    df.to_excel('./results/doperRes.xlsx', index=False)
    df.to_csv('./results/doperRes.csv', index=False)
    print(standard_report(res))

    plt.plot(df[['Import Power [kW]','PV Power [kW]', 'Load Power [kW]']])
    plt.title('Power flow at PCC')
    plt.legend(['Import Power [kW]','PV Power [kW]', 'Load Power [kW]'])
    plt.show()

    plotData = plot_dynamic(df, parameter, plotFile = None, plot_reg=False)