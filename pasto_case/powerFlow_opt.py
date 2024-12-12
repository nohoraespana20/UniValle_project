import gc
import pandas as pd
import matplotlib.pyplot as plt
from pyomo.environ import Objective, minimize
from doper import DOPER, standard_report
from doper.models.basemodel import base_model, default_output_list
from doper.models.battery import add_battery
from doper.models.network import add_network
from parameter_pasto import parameters, ts_inputs
from doper.plotting import plot_dynamic

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

def data_multinode_optimized(parameter, demand):
    # Combine all nodes into a single DataFrame step by step
    data_frames = []
    for node_id, load_factor, pv_factor in [
        (4, 0.04, 861), (5, 0.06, 1202), (6, 0.01, 137), (7, 0.02, 440),
        (8, 0.03, 560), (9, 0.01, 170), (10, 0.02, 480), (11, 0.01, 260),
        (12, 0.01, 215), (13, 0.01, 146), (14, 0.01, 249), (15, 0.01, 151),
        (16, 0.02, 319), (17, 0.05, 934), (18, 0.03, 594), (19, 0.03, 688),
        (20, 0.01, 185), (21, 0.01, 147), (22, 0.10, 1953), (23, 0.02, 369),
        (24, 0.01, 185), (25, 0.01, 123), (26, 0.01, 211), (27, 0.02, 345),
        (28, 0.01, 125), (29, 0.01, 199), (30, 0.14, 2772), (31, 0.02, 506),
        (32, 0.04, 866), (33, 0.06, 1195), (34, 0.09, 1831), (35, 0.02, 449),
        (36, 0.08, 1594)
    ]:
        data_node = ts_inputs(parameter, load='B90', scale_load=demand * load_factor, scale_pv=pv_factor)
        data_frames.append(data_node[['load_demand', 'generation_pv']].rename(columns={
            'load_demand': f'pf_demand_node{node_id}',
            'generation_pv': f'pf_pv_node{node_id}'
        }))

    # Merge all data
    final_data = pd.concat(data_frames, axis=1)

    return final_data

def execute_solver_optimized(parameter, data):
    # Debug: Print parameter keys to verify inclusion of tariff_energy_map
    print("Parameter keys:", parameter.keys())
    if 'tariff_energy_map' not in parameter:
        raise ValueError("Missing 'tariff_energy_map' in parameter. Please check 'parameter_pasto.py'.")

    output_list = default_output_list(parameter)
    solver_path = "C:\\Nohora\\UniValle_project\\pasto_case\\DOPER\\doper\\solvers\\Windows64\\cbc.exe"

    smartDER = DOPER(model=control_model,
                     parameter=parameter,
                     solver_path=solver_path,
                     output_list=output_list)

    res = smartDER.do_optimization(data)
    duration, objective, df, model, result, termination, parameter = res
    return df, res

def process_and_save_results(parameter, demands, results_path):
    for i, demand in enumerate(demands):
        print(f'Processing demand {demand} (iteration {i+1}/{len(demands)})')
        try:
            data = data_multinode_optimized(parameter, demand)
            df, res = execute_solver_optimized(parameter, data)

            # Save results to disk to reduce memory usage
            df.to_csv(f'{results_path}/doperRes_{i}.csv', index=False)
            with open(f'{results_path}/terminalRes_{i}.txt', 'w') as f:
                f.write(standard_report(res))

            # Plot results
            plt.figure()
            df[['Import Power [kW]', 'PV Power [kW]', 'Load Power [kW]']].plot()
            plt.title('Power flow at PCC')
            plt.legend(['Import Power [kW]', 'PV Power [kW]', 'Load Power [kW]'])
            plt.savefig(f'{results_path}/Fig1_{i}.jpg')
            plt.close()

            plot_dynamic(df, parameter, plotFile=f'{results_path}/Fig2_{i}.jpg', plot_reg=False)

            # Free memory
            del data, df, res
            gc.collect()

        except Exception as e:
            print(f'Error processing demand {demand}: {e}')

if __name__ == '__main__':
    parameter = parameters()
    print("Loaded parameters:", parameter)  # Debug: Show full parameter dictionary
    results_path = 'C:/Nohora/UniValle_project/pasto_case/results/L1_home'
    demands = [12667.2]
    process_and_save_results(parameter, demands, results_path)
