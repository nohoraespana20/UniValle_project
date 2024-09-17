# Distributed Optimal and Predictive Energy Resources (DOPER) Copyright (c) 2019
# The Regents of the University of California, through Lawrence Berkeley
# National Laboratory (subject to receipt of any required approvals
# from the U.S. Dept. of Energy). All rights reserved.

""""Distributed Optimal and Predictive Energy Resources
Example module.
"""

# pylint: disable=duplicate-code,line-too-long, redefined-outer-name, invalid-name
# pylint: disable=dangerous-default-value, using-constant-test, consider-using-f-string
# pylint: disable=undefined-variable, unused-argument, too-many-lines

import os
import math
import numpy as np
import pandas as pd
from pprint import pprint
import projections as pr
# Example data for running SINGLE-NODE models (development)
def default_parameter():
    """default_parameter"""
    parameter = {}
    parameter['system'] = {
        'pv': True,
        'battery':False,
        'genset':False,
        'load_control': False,
        'external_gen': False,
        'reg_bidding': False,
        'reg_response':False,
        'hvac_control': False,
    }

    parameter['fuels'] = [
        {
            'name': 'ng',
            'unit': 'therms',
            'rate': 3.93, # $/therm
            'conversion': 30.77, # kWh/therm
            'co2': 5.3, # kg/therm
            'reserves': 0 # therm
        },
        {
            'name': 'diesel',
            'unit': 'gallons',
            'rate': 3.4, # $/gal
            'conversion': 35.75, # kWh/gal  
            'co2': 10.18, # kg/gal 
            'reserves': 100 # gal  
        }
    ]
    parameter['tariff'] = {}
    if False:
        parameter['tariff']['energy'] = {0:0.2,1:0.3,2:0.5} # $/kWh for periods 0-offpeak, 1-midpeak, 2-onpeak
        parameter['tariff']['demand'] = {0:1,1:2,2:3} # $/kW for periods 0-offpeak, 1-midpeak, 2-onpeak
        parameter['tariff']['demand_coincident'] = 0.5 # $/kW for coincident
        parameter['tariff']['export'] = {0:0} # $/kWh for periods 0-offpeak, 1-midpeak, 2-onpeak
    else:
        parameter['tariff']['energy'] = {0:0.08671, 1:0.11613, 2:0.16055} # $/kWh for periods 0-offpeak, 1-midpeak, 2-onpeak
        parameter['tariff']['demand'] = {0:0, 1:5.40, 2:19.65} # $/kW for periods 0-offpeak, 1-midpeak, 2-onpeak
        parameter['tariff']['demand_coincident'] = 17.74 # $/kW for coincident
        parameter['tariff']['export'] = {0:0.01} # $/kWh for periods 0-offpeak, 1-midpeak, 2-onpeak

    parameter['site'] = {}
    parameter['site']['customer'] = 'Commercial' # Type of customer [commercial or none]; decides if demand charge
    parameter['site']['regulation'] = False # Enables or disables the regulation bidding
    parameter['site']['regulation_min'] = None # Minial regulation bid
    parameter['site']['regulation_all'] = False # All batteries must participate in regulation
    parameter['site']['regulation_symmetric'] = False # Symmetric bidding into regulation market
    parameter['site']['regulation_xor_building'] = False # For each battery only allow regulaiton or building support
    parameter['site']['regulation_xor'] = False # Only allows bids for regup or regdown per timestep
    parameter['site']['regulation_reserved'] = False # Flag to reserve site capacity for regulation
    parameter['site']['regulation_reserved_battery'] = False # Flag to reserve battery capacity for regulation
    parameter['site']['regulation_reserved_variable_battery'] = False # Flag to reserve battery capacity for regulation (variable ts)
    parameter['site']['import_max'] = 10000 # kW
    parameter['site']['export_max'] = 10000 # kW
    parameter['site']['demand_periods_prev'] = {0:0,1:0,2:0} # kW peak previously set for periods 0-offpeak, 1-midpeak, 2-onpeak
    parameter['site']['demand_coincident_prev'] = 0 # kW peak previously set for coincident
    parameter['site']['input_timezone'] = -8 # Timezone of inputs (in hourly offset from UTC)
    parameter['site']['local_timezone'] = 'America/Los_Angeles' # Local timezone of tariff (as Python timezone string)
    parameter['controller'] = {}
    parameter['controller']['timestep'] = 60*60 # Controller timestep in seconds
    parameter['controller']['horizon'] = 24*60*60 # Controller horizon in seconds
    parameter['controller']['solver_dir'] = 'solvers' # Controller solver directory

    parameter['objective'] = {}
    parameter['objective']['weight_energy'] = 1 # Weight of tariff (energy) cost in objective
    parameter['objective']['weight_fuel'] = 1 # Weight of fuel (energy) cost in objective
    parameter['objective']['weight_demand'] = 1 # Weight of tariff (demand) cost in objective
    parameter['objective']['weight_export'] = 1 # Weight of revenue (export) in objective
    parameter['objective']['weight_regulation'] = 1 # Weight of revenue (regulation) in objective
    parameter['objective']['weight_degradation'] = 1 # Weight of battery degradation cost in objective

    parameter['objective']['weight_co2'] = 0 # Weight of co2 emissions (kg) cost in objective
    parameter['objective']['weight_load_shed'] = 1 # Weight of shed load costs ($/kWh)  in objective

    parameter['network'] = {}
    # Add network settings to define power-flow constaints
    parameter['network']['settings'] = {
        # turn off simepl power exchange to utilize full power-flow equations
        'simplePowerExchange': False,
        'simpleNetworkLosses': 0.05,
        # powerflow parameters
        'slackBusVoltage': 1,
        'sBase': 1,
        'vBase': 1,
        'cableDerating': 1,
        'txDerating': 1,
        # power factors
        'powerFactors': {
            'pv': 1,  
            'genset': 1,
            'batteryDisc': 1,
            'batteryChar': 1,
            'load': 1
        },
        # powerflow model settings
        'enableLosses': True,
        'thetaMin': -0.18,
        'thetaMax': 0.09,
        'voltMin': 0.8,
        'voltMax': 1.1,
        'useConsVoltMin': False,
        'enableConstantPf': 1,
        'enableVoltageAngleConstraint': 1,
        'enableGenPqLimits': False, # not implemented yet
    }

    parameter['network']['nodes'] = [ # list of dict to define inputs for each node in network
        { # node 1
            'node_id': 'N1', # unique str to id node
            'pcc': True, # bool to define if node is pcc
            'slack': True, 
            'load_id': None, # str, list of str, or None to find load profile in ts data (if node is load bus) by column label
            'ders': { # dict of der assets at node, if None or not included, no ders present
                'pv_id': None, # str, list, or None to find pv profile in ts data (if pv at node) by column label
                'pv_maxS': 0,
                'battery': None, # list of str corresponding to battery assets (defined in parameter['system']['battery'])
                'genset': None, # list of str correponsing to genset assets (defined in parameter['system']['genset'])
                'load_control': None # str, list or None correponsing to genset assets (defined in parameter['system']['load_control'])
            },
            'connections': [ # list of connected nodes, and line connecting them
                {
                    'node': 'N2', # str containing unique node_id of connected node
                    'line': 'L1' # str containing unique line_id of line connection nodes, (defined in parameter['network']['lines'])
                },
                {
                    'node': 'N4',
                    'line': 'L2'
                }
            ]
        },
        { # node 2
            'node_id': 'N2',
            'pcc': True,
            'slack': False, 
            'load_id': 'pf_demand_node2',
            'ders': { 
                'pv_id': 'pf_pv_node2',
                'pv_maxS': 300,
                'battery': 'pf_bat_node2', # node can contain multiple battery assets, so should be list
                'genset': None,
                'load_control': None # node likely to only contain single load_control asset, so should be str
            },
            'connections': [
                {
                    'node': 'N1',
                    'line': 'L1'
                },
                {
                    'node': 'N3',
                    'line': 'L1'
                }
            ]
        },
        { # node 3
            'node_id': 'N3',
            'pcc': True,
            'slack': False, 
            'load_id': 'pf_pv_node3',
            'ders': { 
                'pv_id': None,
                'pv_maxS': 1200,
                'battery': 'pf_bat_node3', 
                'genset': 'pf_gen_node3',
                'load_control': None
            },
            'connections': [
                {
                    'node': 'N2',
                    'line': 'L1'
                }
            ]
        },
        { # node 4
            'node_id': 'N4',
            'pcc': True,
            'slack': False, 
            'load_id': 'pf_demand_node4',
            'ders': { 
                'pv_id': 'pf_pv_node4',
                'pv_maxS': 1000,
                'battery': 'pf_bat_node4', 
                'genset': 'pf_gen_node4',
                'load_control': 'testLc4'
            },
            'connections': [
                {
                    'node': 'N1',
                    'line': 'L2'
                },
                {
                    'node': 'N5',
                    'line': 'L3'
                }
            ]
        },
        { # node 5
            'node_id': 'N5',
            'pcc': True,
            'slack': False, 
            'load_id': 'pf_demand_node5',
            'ders': { 
                'pv_id': 'pf_pv_node5',
                'pv_maxS': 1500,
                'battery': 'pf_bat_node5', 
                'genset': 'pf_gen_node5',
                'load_control': None
            },
            'connections': [
                {
                    'node': 'N4',
                    'line': 'L3'
                }
            ]
        }
    ]

    parameter['network']['lines'] = [ # list of dicts define each cable/line properties
        {
            'line_id': 'L1',
            'power_capacity': 3500, # line power capacity only used for simple power=exchange
            
            'length': 1200, # line length in meters
            'resistance': 4.64e-6, # line properties are all in pu, based on SBase/VBase defined above
            'inductance': 8.33e-7,
            'ampacity': 3500,
        },
        {
            'line_id': 'L2',
            'power_capacity': 3500,
            
            'length': 1800,
            'resistance': 4.64e-6,
            'inductance': 8.33e-7,
            'ampacity': 3500,
        },
        {
            'line_id': 'L3',
            'power_capacity': 3500,
            
            'length': 900,
            'resistance': 4.64e-6,
            'inductance': 8.33e-7,
            'ampacity': 3500,
        }
    ]
    parameter['system']['battery'] = True

    # Add batteries options
    parameter['batteries'] = [
        {
          'name':'pf_bat_node2',
          'capacity': 2500,
          'degradation_endoflife': 80,
          'degradation_replacementcost': 6000.0,
          'efficiency_charging': 0.96,
          'efficiency_discharging': 0.96,
          'nominal_V':  400,
          'power_charge': 150,
          'maxS': 150,
          'power_discharge': 150,
          'self_discharging': 0.001,
           'soc_final': 0.5,
          'soc_initial': 0.5,
          'soc_max': 1,
          'soc_min': 0.2,
          # 'temperature_initial': 22.0,
          'thermal_C': 100000.0,
          'thermal_R': 0.01
        },
        {
          'name':'pf_bat_node3',
          'capacity': 2000,
          'degradation_endoflife': 80,
          'degradation_replacementcost': 6000.0,
          'efficiency_charging': 0.96,
          'efficiency_discharging': 0.96,
          'nominal_V':  400,
          'power_charge': 350,
          'maxS': 350,
          'power_discharge': 350,
          'self_discharging': 0.001,
           'soc_final': 0.5,
          'soc_initial': 0.5,
          'soc_max': 1,
          'soc_min': 0.2,
          # 'temperature_initial': 22.0,
          'thermal_C': 100000.0,
          'thermal_R': 0.01
        },
        {
          'name':'pf_bat_node4',
          'capacity': 3500,
          'degradation_endoflife': 80,
          'degradation_replacementcost': 6000.0,
          'efficiency_charging': 0.96,
          'efficiency_discharging': 0.96,
          'nominal_V':  400,
          'power_charge': 350,
          'maxS': 350,
          'power_discharge': 350,
          'self_discharging': 0.001,
           'soc_final': 0.5,
          'soc_initial': 0.5,
          'soc_max': 1,
          'soc_min': 0.2,
          # 'temperature_initial': 22.0,
          'thermal_C': 100000.0,
          'thermal_R': 0.01
        },
        {
          'name':'pf_bat_node5',
          'capacity': 4000,
          'degradation_endoflife': 80,
          'degradation_replacementcost': 6000.0,
          'efficiency_charging': 0.96,
          'efficiency_discharging': 0.96,
          'nominal_V':  400,
          'power_charge': 350,
          'maxS': 350,
          'power_discharge': 350,
          'self_discharging': 0.001,
           'soc_final': 0.5,
          'soc_initial': 0.5,
          'soc_max': 1,
          'soc_min': 0.2,
          # 'temperature_initial': 22.0,
          'thermal_C': 100000.0,
          'thermal_R': 0.01
        },
    ]
    return parameter

# Timeseries Input Example Creation Funcs
def ts_inputs(parameter={}, load='Flexlab', scale_load=4, scale_pv=4):
    """ts_inputs"""
    #scale = 1
    #scale = 30
    if load == 'Flexlab':
        data = pd.read_csv(os.path.join(root_dir, 'ExampleData', 'Flexlab.csv')) # type: ignore
        data.index = pd.to_datetime(data['Date/Time'].apply(lambda x: '2018/'+x[1:6]+' '+'{:2d}'.format(int(x[8:10])-1)+x[10::]))
        del data.index.name
        data = data[['FLEXLAB-X3-ZONEA:Zone Air Heat Balance System Air Transfer Rate [W](Hourly)']]
        data.columns = ['load_demand']
        data['load_demand'] = data['load_demand'].mask(data['load_demand']<0, data['load_demand']*-1/2.) / 1000.
        # Use only 1 day
        data = data.iloc[0:24]
        data['load_demand'] = data['load_demand']/data['load_demand'].max()
    elif load =='B90':
        data = pd.DataFrame(index=pd.date_range(start='2019-01-01 00:00', end='2019-01-01 23:50', freq='h'))
        # data['load_demand'] = [2.8,  2.8,  2.9,  2.9,  3. ,  3.3,  4. ,  4.8,  4.9,  5.1,  5.3,
        #                        5.4,  5.4,  5.4,  5.3,  5.3,  5.2,  4.8,  3.9,  3.1,  2.9,  2.8,
        #                        2.8,  2.8]
        data['load_demand'] = [0.0, 0.0, 0.03, 0.03, 0.06, 0.14, 0.31, 0.54, 0.60, 0.69, 0.74,
                                0.80, 0.80, 0.80, 0.74, 0.74, 0.69, 0.54, 0.31, 0.06, 0.0, 0.0, 0.0, 0.0]
        data['load_demand'] = data['load_demand']/data['load_demand'].max()
    # Scale Load data
    data['load_demand'] = data['load_demand'] * scale_load
    # Mode of OAT
    data['oat'] = np.sin(data.index.view(np.int64)/(1e12*np.pi*4))*3 + 22
    # Makeup Tariff
    data['tariff_energy_map'] = 0
    data['tariff_energy_map'] = data['tariff_energy_map'].mask((data.index.hour>=8) & (data.index.hour<22), 1)
    data['tariff_energy_map'] = data['tariff_energy_map'].mask((data.index.hour>=12) & (data.index.hour<18), 2)
    data['tariff_power_map'] = data['tariff_energy_map'] # Apply same periods to demand charge
    data['tariff_energy_export_map'] = 0
    
    data['tariff_regup'] = data['tariff_power_map'] * 0.05 + 0.01
    data['tariff_regdn'] = data['tariff_power_map'] * 0.01 + 0.01
    data['battery_reg'] = 0
    data['date_time'] = data.index
    # Resample
    if True:
        data = data.resample('5min').asfreq()
        for c in data.columns:
            if c in ['load_demand','oat']:
                data[c] = data[c].interpolate()
            else:
                data[c] = data[c].ffill()
        data = data.loc['2019-01-01 00:00:00':'2019-01-02 00:00:00']
    else:
        data = data.loc['2019-01-01 00:00:00':'2019-01-02 00:00:00']
    
    var = pd.read_csv('pv_norm_pasto.csv') * scale_pv
    var_single_column = var.iloc[5:282, 0]
    
    data['generation_pv'] = var_single_column.values
    
    # input timeseries indicating grid availability
    data['grid_available'] = 1
    data['fuel_available'] = 0

    # input timeseries indicating grid availability
    # data['grid_co2_intensity'] = 0.202 #kg/kWh
    data['grid_co2_intensity'] = 0.16438 #kg/kWh
    return data

def parameter_add_battery(parameter=None):
    """parameter_add_battery_multinode_test"""
    if parameter is None:
        # if no parameter given, load default
        parameter = parameter_add_network()

    # enable gensets
    parameter['system']['battery'] = True

    # Add genset options
    parameter['batteries'] = [
        {
          'name':'pf_bat_node2',
          'capacity': 1500,
          'degradation_endoflife': 80,
          'degradation_replacementcost': 6000.0,
          'efficiency_charging': 0.96,
          'efficiency_discharging': 0.96,
          'nominal_V':  400,
          'power_charge': 150,
          'maxS': 150,
          'power_discharge': 150,
          'self_discharging': 0.001,
           'soc_final': 0.5,
          'soc_initial': 0.5,
          'soc_max': 1,
          'soc_min': 0.2,
          # 'temperature_initial': 22.0,
          'thermal_C': 100000.0,
          'thermal_R': 0.01
        },
        {
          'name':'pf_bat_node3',
          'capacity': 1000,
          'degradation_endoflife': 80,
          'degradation_replacementcost': 6000.0,
          'efficiency_charging': 0.96,
          'efficiency_discharging': 0.96,
          'nominal_V':  400,
          'power_charge': 350,
          'maxS': 350,
          'power_discharge': 350,
          'self_discharging': 0.001,
           'soc_final': 0.5,
          'soc_initial': 0.5,
          'soc_max': 1,
          'soc_min': 0.2,
          # 'temperature_initial': 22.0,
          'thermal_C': 100000.0,
          'thermal_R': 0.01
        },
        {
          'name':'pf_bat_node4',
          'capacity': 2500,
          'degradation_endoflife': 80,
          'degradation_replacementcost': 6000.0,
          'efficiency_charging': 0.96,
          'efficiency_discharging': 0.96,
          'nominal_V':  400,
          'power_charge': 350,
          'maxS': 350,
          'power_discharge': 350,
          'self_discharging': 0.001,
           'soc_final': 0.5,
          'soc_initial': 0.5,
          'soc_max': 1,
          'soc_min': 0.2,
          # 'temperature_initial': 22.0,
          'thermal_C': 100000.0,
          'thermal_R': 0.01
        },
        {
          'name':'pf_bat_node5',
          'capacity': 2000,
          'degradation_endoflife': 80,
          'degradation_replacementcost': 6000.0,
          'efficiency_charging': 0.96,
          'efficiency_discharging': 0.96,
          'nominal_V':  400,
          'power_charge': 350,
          'maxS': 350,
          'power_discharge': 350,
          'self_discharging': 0.001,
           'soc_final': 0.5,
          'soc_initial': 0.5,
          'soc_max': 1,
          'soc_min': 0.2,
          # 'temperature_initial': 22.0,
          'thermal_C': 100000.0,
          'thermal_R': 0.01
        },
    ]
    return parameter

def parameter_add_network(parameter=None):
    """parameter_add_network"""
    if parameter is None:
        # if no parameter given, load default
        parameter = default_parameter()

    # Add nodes and line options
    parameter['network'] = {}


# Add network settings to define power-flow constaints
    parameter['network']['settings'] = {
    
        # turn off simepl power exchange to utilize full power-flow equations
        'simplePowerExchange': True,
        'simpleNetworkLosses': 0.05,

        # # powerflow parameters
        # 'slackBusVoltage': 1,
        # 'sBase': 1,
        # 'vBase': 1,
        # 'cableDerating': 1,
        # 'txDerating': 1,

        # # power factors
        # 'powerFactors': {
        #     'pv': 1,  
        #     'genset': 1,
        #     'batteryDisc': 1,
        #     'batteryChar': 1,
        #     'load': 1
        # },

        # # powerflow model settings
        # 'enableLosses': True,
        # 'thetaMin': -0.18,
        # 'thetaMax': 0.09,
        # 'voltMin': 0.8,
        # 'voltMax': 1.1,
        # 'useConsVoltMin': False,
        # 'enableConstantPf': 1,
        # 'enableVoltageAngleConstraint': 1,
        # 'enableGenPqLimits': False, # not implemented yet
    }

    parameter['network']['nodes'] = [ # list of dict to define inputs for each node in network
        { # node 1
            'node_id': 'N1', # unique str to id node
            'pcc': True, # bool to define if node is pcc
            'slack': True, 
            'load_id': None, # str, list of str, or None to find load profile in ts data (if node is load bus) by column label
            'ders': { # dict of der assets at node, if None or not included, no ders present
                'pv_id': None, # str, list, or None to find pv profile in ts data (if pv at node) by column label
                'pv_maxS': 0,
                'battery': None, # list of str corresponding to battery assets (defined in parameter['system']['battery'])
                'genset': None, # list of str correponsing to genset assets (defined in parameter['system']['genset'])
                'load_control': None # str, list or None correponsing to genset assets (defined in parameter['system']['load_control'])
            },
            'connections': [ # list of connected nodes, and line connecting them
                {
                    'node': 'N2', # str containing unique node_id of connected node
                    'line': 'L1' # str containing unique line_id of line connection nodes, (defined in parameter['network']['lines'])
                },
                {
                    'node': 'N4',
                    'line': 'L2'
                }
            ]
        },
        { # node 2
            'node_id': 'N2',
            'pcc': True,
            'slack': False, 
            'load_id': 'pf_demand_node2',
            'ders': { 
                'pv_id': 'pf_pv_node2',
                'pv_maxS': 300,
                'battery': 'pf_bat_node2', # node can contain multiple battery assets, so should be list
                'genset': None,
                'load_control': None # node likely to only contain single load_control asset, so should be str
            },
            'connections': [
                {
                    'node': 'N1',
                    'line': 'L1'
                },
                {
                    'node': 'N3',
                    'line': 'L1'
                }
            ]
        },
        { # node 3
            'node_id': 'N3',
            'pcc': True,
            'slack': False, 
            'load_id': 'pf_pv_node3',
            'ders': { 
                'pv_id': None,
                'pv_maxS': 1200,
                'battery': 'pf_bat_node3', 
                'genset': 'pf_gen_node3',
                'load_control': None
            },
            'connections': [
                {
                    'node': 'N2',
                    'line': 'L1'
                }
            ]
        },
        { # node 4
            'node_id': 'N4',
            'pcc': True,
            'slack': False, 
            'load_id': 'pf_demand_node4',
            'ders': { 
                'pv_id': 'pf_pv_node4',
                'pv_maxS': 1000,
                'battery': 'pf_bat_node4', 
                'genset': 'pf_gen_node4',
                'load_control': 'testLc4'
            },
            'connections': [
                {
                    'node': 'N1',
                    'line': 'L2'
                },
                {
                    'node': 'N5',
                    'line': 'L3'
                }
            ]
        },
        { # node 5
            'node_id': 'N5',
            'pcc': True,
            'slack': False, 
            'load_id': 'pf_demand_node5',
            'ders': { 
                'pv_id': 'pf_pv_node5',
                'pv_maxS': 1500,
                'battery': 'pf_bat_node5', 
                'genset': 'pf_gen_node5',
                'load_control': None
            },
            'connections': [
                {
                    'node': 'N4',
                    'line': 'L3'
                }
            ]
        }
    ]

    parameter['network']['lines'] = [ # list of dicts define each cable/line properties
        {
            'line_id': 'L1',
            'power_capacity': 3500, # line power capacity only used for simple power=exchange
            
            'length': 1200, # line length in meters
            'resistance': 4.64e-6, # line properties are all in pu, based on SBase/VBase defined above
            'inductance': 8.33e-7,
            'ampacity': 3500,
        },
        {
            'line_id': 'L2',
            'power_capacity': 3500,
            
            'length': 1800,
            'resistance': 4.64e-6,
            'inductance': 8.33e-7,
            'ampacity': 3500,
        },
        {
            'line_id': 'L3',
            'power_capacity': 3500,
            
            'length': 900,
            'resistance': 4.64e-6,
            'inductance': 8.33e-7,
            'ampacity': 3500,
        }
    ]
    return parameter