from pyomo.environ import Objective, minimize
from doper import DOPER, standard_report
from doper.models.basemodel import base_model, default_output_list
from doper.models.battery import add_battery
from doper.models.network import add_network
from test_parameter import default_parameter, ts_inputs, parameter_add_battery, parameter_add_network
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
               + model.fuel_cost_total * parameter['objective']['weight_energy'] \
               + model.load_shed_cost_total
    model.objective = Objective(rule=objective_function, sense=minimize, doc='objective function')
    return model

if __name__ == '__main__':  
    parameter = default_parameter()
    # parameter = parameter_add_network(parameter)
    # parameter = parameter_add_battery()
    
    data2 = ts_inputs(parameter, load='B90', scale_load=3000, scale_pv=4686)
    data3 = ts_inputs(parameter, load='B90', scale_load=1500, scale_pv=2162)
    data4 = ts_inputs(parameter, load='B90', scale_load=1000, scale_pv=1708)
    data5 = ts_inputs(parameter, load='B90', scale_load=700, scale_pv=1147)
    # use data1 as starting point for multinode df
    data = data2.copy()
    # drop load and pv from multinode df
    data = data.drop(labels='load_demand', axis=1)
    data = data.drop(labels='generation_pv', axis=1)
    # add node specifc load and pv (where applicable)
    data['pf_demand_node2'] = data2['load_demand']
    data['pf_demand_node3'] = data3['load_demand']
    data['pf_demand_node4'] = data4['load_demand']
    data['pf_demand_node5'] = data5['load_demand']

    data['pf_pv_node2'] = data2['generation_pv']
    data['pf_pv_node3'] = data3['generation_pv']
    data['pf_pv_node4'] = data4['generation_pv']
    data['pf_pv_node5'] = data5['generation_pv'] 

    demand = data2['load_demand'] + data3['load_demand'] + data4['load_demand'] + data5['load_demand']
    # data.to_excel('./results/demand_generation.xlsx', index=False)
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
    plt.plot(df['Import Power [kW]'] + df['PV Power [kW]'])
    plt.plot(demand)
    plt.title('Power flow at PCC')
    plt.legend(['Import Power [kW]','PV Power [kW]', 'Load Power [kW]', 'Total [kW]', 'Demand [kW]'])
    plt.show()

    plotData = plot_dynamic(df, parameter, plotFile = None, plot_reg=False)