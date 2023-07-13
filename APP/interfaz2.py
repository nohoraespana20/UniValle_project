import tkinter as tk
from tkinter import ttk
from tkinter import *
import functions_cost as FC
import intersection as IN
import os
from os import path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from os import remove
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class ConventionalV(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = ('Vehicle cost', 'Galon fuel cost', 'Fuel yearly raise [%]',
                       'Maintenance annual cost', 'Soat annual cost',
                       'Other insurances', 'Insurances yearly raise [%]',
                       'Daily consumption [gl]', 'Daily distance [km]', 'Repairs per year'
                       )
        self.entries = {}
        for field in self.fields:
            row = ttk.Notebook(self)
            lab = Label(row, width=22, text=field+": ", anchor='w')
            ent = Entry(row)
            ent.insert(0,"0")
            row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
            lab.pack(side = LEFT)
            ent.pack(side = RIGHT, expand = YES, fill = X)
            self.entries[field] = ent
        self.greet_button = ttk.Button(self, text="Ok", command=self.show_index)
        self.greet_button.pack()
        self.greet_label = ttk.Label(self)
        self.greet_label.pack()

    def save_data(self):
        vehicle_cost = float(self.entries['Vehicle cost'].get())
        galon_cost = float(self.entries['Galon fuel cost'].get())
        fuel_raise = float(self.entries['Fuel yearly raise [%]'].get())
        maintenance_cost = float(self.entries['Maintenance annual cost'].get())
        soat_cost = float(self.entries['Soat annual cost'].get())
        other_cost = float(self.entries['Other insurances'].get())
        insurance_raise = float(self.entries['Insurances yearly raise [%]'].get())
        daily_consumption = float(self.entries['Daily consumption [gl]'].get())
        daily_distance = float(self.entries['Daily distance [km]'].get())
        repairs = int(self.entries['Repairs per year'].get())
        # data_combustion = { 'Vehicle cost': vehicle_cost,
        #                     'Galon cost': galon_cost,
        #                     'Fuel raise': fuel_raise,
        #                     'Maintenance cost': maintenance_cost,
        #                     'SOAT cost': soat_cost,
        #                     'Other insurances': other_cost,
        #                     'Insurance raise': insurance_raise,
        #                     'Daily consumption': daily_consumption,
        #                     'Daily distance' : daily_distance,
        #                     'Repairs per year' : repairs
        #                 }
        data_combustion = { 'Vehicle cost': 195400000, # Bus FRR --> https://casaeditorialeltiempo.pressreader.com/precios 195400000
                            'Galon cost': 8396,
                            'Fuel raise': 4,
                            'Maintenance cost': 14700000,
                            'SOAT cost': 1200000,
                            'Other insurances': 360000,
                            'Insurance raise': 10,
                            'Daily consumption': 20.83,
                            'Daily distance' : 148,
                            'Repairs per year' : 2
                        }
        with open('data_files/data_combustion.json', 'w') as file:
            json.dump(data_combustion, file, indent=4)

    def show_index(self):
        self.save_data()
        file = 'data_files/data_combustion.json'
        with open(file) as file:
                data = json.load(file)
        file = 'data_files/data_config.json'
        with open(file) as file:
                config = json.load(file)

        gl_100km = 100 * (data['Daily consumption'] / data['Daily distance'])
        icr = (gl_100km/100) * data['Galon cost']
        co2, co, nox, hc, pmx = self.emissions()
        tco = self.cost_equation()
        availability = (365 - (data['Repairs per year'] * 5) - 6) * 100 / 365

        self.greet_label["text"] = "\ngl/100km = {} ".format(round(gl_100km,3)) + \
                                   "\n\nICR = {} $/km".format(round(icr,3)) + \
                                   "\n\ngr CO2/km = {}".format(co2) + \
                                   "\n\ngr CO/km = {}".format(co) + \
                                   "\n\ngr NOx/km = {}".format(nox) + \
                                   "\n\ngr HCkm = {}".format(hc) + \
                                   "\n\ngr PMx/km = {}".format(pmx) + \
                                   "\n\nTCO = {} $/km".format(round(tco,2)) + \
                                   "\n\n Availability factor = {} %".format(round(availability,1))
        
        results = {
        'gl/100km': round(gl_100km,3),
        'ICR': round(icr,3), 
        'TCO': round(tco,2)
        }

        with open('data_files/combustionTemp.json', 'w') as outfile:
            json.dump(results, outfile)

    def mean_emission(self, file):
        distances = [(4022.095899057417+2415.0392316822504)/2000,
                     (6938.748453744248+3465.652911930644)/2000,
                     (5978.676979676662+7116.311075331374)/2000]
        with open(file) as file:
                data = json.load(file)
        emission = [np.mean(data[0][0:2]), np.mean(data[0][2:4]), np.mean(data[0][4:])]
        emission_km = round(np.mean([emission[0]/distances[0], emission[1]/distances[1], emission[2]/distances[2]]),2)
        return emission_km

    def emissions(self):
        co2 = self.mean_emission('data_files/co2_mean.json')        
        co = self.mean_emission('data_files/co_mean.json')        
        nox = self.mean_emission('data_files/ENOx_mean.json')        
        hc = self.mean_emission('data_files/HC_mean.json')        
        pmx = self.mean_emission('data_files/PMx_mean.json')        
        return co2, co, nox, hc, pmx

    def accumulated_conventional_cost(self, initialCost_C, yearlyRaise_C, Cen_C, Cm_C, othersC, 
                                      otherC, yearlyRaise_others, currency, year, IPC, Ec):
        initialCost_C =  initialCost_C / currency
        Cm_C = Cm_C / currency 
        Cen_C = Cen_C / currency
        othersC = othersC / currency
        otherC = otherC / currency

        totalC = []
        totalC = [*range(0, year, 1)]
        totalC[0] = initialCost_C

        for i in range(1,year,1):
            Cen_C = Cen_C + (Cen_C * yearlyRaise_C)
            Cm_C = Cm_C + (Cm_C * IPC)
            if i > 2:
                combustionCost = (Ec * Cen_C)
                combustionMaintenance = Cm_C
                totalC[i] = totalC[i-1] + combustionCost + combustionMaintenance + othersC + otherC
                othersC = othersC + (othersC * yearlyRaise_others)
                otherC = otherC + (otherC * yearlyRaise_others)
            else:
                combustionCost = (Ec * Cen_C)
                combustionMaintenance = Cm_C
                totalC[i] = totalC[i-1] + combustionCost + combustionMaintenance + othersC
                othersC = othersC + (othersC * yearlyRaise_others)
                otherC = otherC + (otherC * yearlyRaise_others)
        return totalC[-1]

    def cost_equation(self):
        currency, year, annual_distance, ipc = Comparison.get_data_config(self)
        initialCost, yearlyRaise, yearlyRaise_others, Cen, costMaintenance, others, other = Comparison.get_data_combustion(self)
        total_combustion = self.accumulated_conventional_cost(initialCost, yearlyRaise, Cen, costMaintenance, others, other, yearlyRaise_others,
                     currency, year, ipc, annual_distance )
        return total_combustion * currency / (annual_distance*year)

class ElectricV(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = ('Vehicle cost', 'kWh cost', 'kWh yearly raise [%]',
                       'Daily consumption [kWh]',
                       'Batery capacity [kWh]'
                       )
        self.entries = {}
        for field in self.fields:
            row = ttk.Notebook(self)
            lab = Label(row, width=22, text=field+": ", anchor='w')
            ent = Entry(row)
            ent.insert(0,"0")
            row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
            lab.pack(side = LEFT)
            ent.pack(side = RIGHT, expand = YES, fill = X)
            self.entries[field] = ent
        self.greet_button = ttk.Button(self, text="Ok", command=self.show_index)
        self.greet_button.pack()
        self.greet_label = ttk.Label(self)
        self.greet_label.pack()

    def save_data(self):
        file = 'data_files/data_combustion.json'
        with open(file) as file:
                data = json.load(file)
        maintenance_cost = data['Maintenance cost']#*0.35
        soat_cost =   data['SOAT cost']#*0.9
        other_cost = data['Other insurances']#*0.9
        insurance_raise = data['Insurance raise']
        daily_distance = data['Daily distance']
        repairs = data['Repairs per year']#*0.9

        vehicle_cost = float(self.entries['Vehicle cost'].get())
        kWh_cost = float(self.entries['kWh cost'].get())
        kWh_raise = float(self.entries['kWh yearly raise [%]'].get())
        daily_consumption = float(self.entries['Daily consumption [kWh]'].get())
        batery_capacity = float(self.entries['Batery capacity [kWh]'].get())


        # data_electric = { 'Vehicle cost': vehicle_cost,
        #                     'kWh cost': kWh_cost,
        #                     'kWh raise': kWh_raise,
        #                     'Maintenance cost': maintenance_cost,
        #                     'SOAT cost': soat_cost,
        #                     'Other insurances': other_cost,
        #                     'Insurance raise': insurance_raise,
        #                     'Daily consumption': daily_consumption,
        #                     'Daily distance' : daily_distance,
        #                     'Batery capacity [kWh]' : batery_capacity,
        #                     'Repairs per year' : repairs  
        #                 }

        # data_electric = { 'Vehicle cost': 185000*5118*1.35, # cost of Sunwin 8 m - 30 pasajeros with USD=5118 (historical maximum) and 35% of importation costs
        #                     'kWh cost': 755.8,
        #                     'kWh raise': 6,
        #                     'Maintenance cost': 14700000*0.35,
        #                     'SOAT cost': 1200000*0.9,
        #                     'Other insurances': 360000*0.9,
        #                     'Insurance raise': 10,
        #                     'Daily consumption': 71.37,
        #                     'Daily distance' : 148,
        #                     'Batery capacity [kWh]' : 324,
        #                     'Repairs per year' : 2*0.9
        #                 } # this data is for EV
        data_electric = { 'Vehicle cost': 195400000*1.1, # with a surcharge of 10%
                            'kWh cost': 2086, # GNV cost at 2023 --> https://www.grupovanti.com/gas-natural-vehicular-gnv/precio-historico-del-gas-natural-vehicular/
                            'kWh raise': 3.4,
                            'Maintenance cost': 14700000,
                            'SOAT cost': 1200000*0.9,
                            'Other insurances': 360000*0.9,
                            'Insurance raise': 10,
                            'Daily consumption': 82.69,
                            'Daily distance' : 148,
                            'Batery capacity [kWh]' : 0,
                            'Repairs per year' : 2*0.9
                        } # this data is for GNV
        with open('data_files/data_electric.json', 'w') as file:
            json.dump(data_electric, file, indent=4)

    def show_index(self):
        self.save_data()
        file = 'data_files/data_electric.json'
        with open(file) as file:
                data = json.load(file)
        file = 'data_files/data_config.json'
        with open(file) as file:
                config = json.load(file)

        kWh_100km = 100 * (data['Daily consumption'] / data['Daily distance'])
        icr = (kWh_100km/100) * data['kWh cost']
        co2_km = 0
        tco = self.cost_equation()
        availability = (365 - (data['Repairs per year'] * 5) - 2.5) * 100 / 365

        self.greet_label["text"] = "\nkWh/100km = {} ".format(round(kWh_100km,3)) + \
                                   "\n\nICR = {} $/km".format(round(icr,3)) + \
                                   "\n\nTon CO2/km = {}".format(round(co2_km,4)) + \
                                   "\n\nTCO = $ {}".format(round(tco,2)) + \
                                   "\n\n Availability factor = {} %".format(round(availability,1))
        
        results = {
        'gl/100km': round(kWh_100km,3),
        'ICR': round(icr,3), 
        'TCO': round(tco,2)
        }

        with open('data_files/electricTemp.json', 'w') as outfile:
            json.dump(results, outfile)

    def accumulated_electric_cost(self, yearlyRaise_others, initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, 
                         Cm_E, othersE, otherE, batery_capacity, currency, year, IPC, Ec):
    
        initialCost_E = initialCost_E / currency
        Cen_E = Cen_E / currency
        Cm_E = Cm_E / currency
        othersE = otherE / currency
        otherE = otherE / currency

        Ee = Ec * 1.16
        totalE = []
        totalE = [*range(0, year, 1)]
        totalE[0] = initialCost_E
        #capacidad bateria: 53.6 kWh # USD 156/kWh # tasa de cambio dolar USD=5118 (historical maximum) cambio a millones de pesos
        bateryCost = batery_capacity * 156 * 5118 / currency 
        for i in range(1,year,1):
            Cen_E = Cen_E + (Cen_E * yearlyRaise_E)
            Cm_E = Cm_E + (Cm_E * IPC)
            bateryCost = bateryCost + (bateryCost * yearlyRaise_batery)
            if i > 2:
                electricCost = (Ee * Cen_E)
                electricMaintenance = Cm_E
                if i==8 or i==16 or i==24:
                    totalE[i] = totalE[i-1] + electricCost + electricMaintenance + othersE + otherE + bateryCost
                else:
                    totalE[i] = totalE[i-1] + electricCost + electricMaintenance + othersE + otherE
                othersE = othersE + (othersE * yearlyRaise_others)
                otherE = otherE + (otherE * yearlyRaise_others)
            else:
                electricCost = (Ee * Cen_E)
                electricMaintenance = Cm_E
                totalE[i] = totalE[i-1] + electricCost + electricMaintenance + othersE
                othersE = othersE + (othersE * yearlyRaise_others)
                otherE = otherE + (otherE * yearlyRaise_others)
        return totalE[-1]
    
    def cost_equation(self):
        currency, year, annual_distance, ipc = Comparison.get_data_config(self)
        initialCost, yearlyRaise, yearlyRaise_others, Cen, costMaintenance, others, other = Comparison.get_data_combustion(self)
        initialCost, yearlyRaise,yearlyRaise_batery, Cen, costMaintenance, others, other, batery_capacity = Comparison.get_data_electric(self)
        total = self.accumulated_electric_cost(yearlyRaise_others, initialCost, yearlyRaise, yearlyRaise_batery, Cen, costMaintenance, others, other, batery_capacity, 
                     currency, year, ipc, annual_distance )
        return total * currency / (annual_distance * year)


class Comparison(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.greet_button = ttk.Button(self, text= "Graph", command=self.show_figures)
        self.greet_button.pack()
        self.greet_label = ttk.Label(self)
        self.greet_label.pack()

    def show_figures(self):
        # self.create_figure_accumulated()
        # self.create_figure_annual()
        # self.create_figure_emissions()
        self.create_figures()

    def get_data_combustion(self):
        file = 'data_files/data_combustion.json'
        with open(file) as file:
                data_combustion = json.load(file)
        file_C = 'data_files/Fuel_mean.json'
        ### Combustion data###
        initialCost =  data_combustion['Vehicle cost']
        costGalonFuel = data_combustion['Galon cost']
        yearlyRaise = data_combustion['Fuel raise'] / 100
        costMaintenance = data_combustion['Maintenance cost']
        yearlyRaise_others = 0.1
        soat = data_combustion['SOAT cost']
        tax = initialCost * 0.01
        other = data_combustion['Other insurances']
        others = soat + tax

        #Costo energético promedio por kilómetro - combustion
        CenPeak_C,  CenPeakOff_C =  FC.meanFuelPerKM_C(file_C)
        CenPeak_C = CenPeak_C * costGalonFuel
        CenPeakOff_C =  CenPeakOff_C * costGalonFuel
        Cen = (CenPeak_C + CenPeakOff_C)/2
        return initialCost, yearlyRaise, yearlyRaise_others, Cen, costMaintenance, others, other

    def get_data_electric(self):
        file = 'data_files/data_electric.json'
        with open(file) as file:
                data_electric = json.load(file)
        file_E = 'data_files/kWh_mean.json'

        ### Electric data###
        initialCost = data_electric['Vehicle cost']
        costkWh = data_electric['kWh cost']
        yearlyRaise = data_electric['kWh raise'] /100
        costMaintenance = data_electric['Maintenance cost']
        yearlyRaise_batery = -0.0967
        soat = data_electric['SOAT cost']
        tax = initialCost * 0.01 * 0.4
        other = data_electric['Other insurances']
        others = soat + tax
        batery_capacity = data_electric['Batery capacity [kWh]']

        #Costo energético promedio por kilómetro - electrico
        CenPeak_E,  CenPeakOff_E =  FC.meanFuelPerKM_E(file_E)
        CenPeak_E = CenPeak_E * costkWh
        CenPeakOff_E =  CenPeakOff_E * costkWh
        Cen = (CenPeak_E + CenPeakOff_E)/2
        return initialCost, yearlyRaise,yearlyRaise_batery, Cen, costMaintenance, others, other, batery_capacity

    def get_data_config(self):
        file = 'data_files/data_config.json'
        with open(file) as file:
                data_config = json.load(file)
        ###GENERAL DATA###
        currency = data_config['Currency']
        year = data_config['Years']
        annual_distance = data_config['Annual distance']
        ipc = 0.0457
        return currency, year, annual_distance, ipc

    def mean_emission(self, file):
        distances = [(4022.095899057417+2415.0392316822504)/2000,
                     (6938.748453744248+3465.652911930644)/2000,
                     (5978.676979676662+7116.311075331374)/2000]
        with open(file) as file:
                data = json.load(file)
        emission = [np.mean(data[0][0:2]), np.mean(data[0][2:4]), np.mean(data[0][4:])]
        emission_km = round(np.mean([emission[0]/distances[0], emission[1]/distances[1], emission[2]/distances[2]]),2)
        return emission_km

    def emissions(self):
        co2 = self.mean_emission('data_files/co2_mean.json')        
        co = self.mean_emission('data_files/co_mean.json')        
        nox = self.mean_emission('data_files/ENOx_mean.json')        
        hc = self.mean_emission('data_files/HC_mean.json')        
        pmx = self.mean_emission('data_files/PMx_mean.json')        
        noise_c = self.mean_emission('data_files/Noise_c.json') 
        noise_e = self.mean_emission('data_files/Noise_e.json') 
        return co2, co, nox, hc, pmx, noise_c, noise_e
    
    def create_figures(self):
        currency, year, annual_distance, ipc = self.get_data_config()
        initialCost_C, yearlyRaise_C, yearlyRaise_others, Cen_C, costMaintenance_C, others_C, other_C = self.get_data_combustion()
        initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, costMaintenance_E, others_E, other_E, batery_capacity = self.get_data_electric()
        total_combustion, total_electric, j = FC.accumulatedCost2(initialCost_C, yearlyRaise_C, Cen_C, costMaintenance_C, others_C, other_C, yearlyRaise_others,
                     initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, costMaintenance_E, others_E, other_E, batery_capacity,
                     currency, year, ipc, annual_distance )

        years = [*range(0, j+1, 1)]
        fig = Figure(figsize=(15,5))
        a1 = fig.add_subplot(131)
        # a1.plot(years, total_combustion, label = "conventional")
        # a1.plot(years, total_electric, label = "electric")
        a1.plot(years, total_combustion, label = "Conventional", color="#A3AF9E")
        a1.plot(years, total_electric, label = "electric", color="#00ADFF")
        a1.grid()
        a1.set_title ('%d km/año' %annual_distance, fontsize=8)
        a1.legend(['Diesel', 'Gas'], fontsize=8)
        # a1.set_ylabel('Costo acumulado [millones COP]', fontsize=8)
        a1.set_ylabel('Cumulative Cost [USD]', fontsize=8)
        a1.set_xlabel('Año', fontsize=8)

        # print(total_combustion)
        # print(total_electric)
        IN.getVectors(annual_distance, total_combustion, total_electric)
        # print([total_combustion[año], total_electric[año]])

        currency, year, annual_distance, ipc = self.get_data_config()
        initialCost_C, yearlyRaise_C, yearlyRaise_others, Cen_C, costMaintenance_C, others_C, other_C = self.get_data_combustion()
        initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, costMaintenance_E, others_E, other_E, batery_capacity = self.get_data_electric()

        total_combustion, total_electric, j = FC.accumulatedPerYear(initialCost_C, yearlyRaise_C, Cen_C, costMaintenance_C, others_C, other_C, yearlyRaise_others,
                     initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, costMaintenance_E, others_E, other_E, batery_capacity,
                     currency, year, ipc, annual_distance )

        years = [*range(0, j+1, 1)]
        Y = [str(x) for x in years]
        # conventional = total_combustion
        conventional = []
        # electric = total_electric
        electric = []

        for dataCom in total_combustion:
             conventional.append(dataCom/1000)

        for dataElec in total_electric:
             electric.append(dataElec/1000)
        
        a2 = fig.add_subplot(132)
        df = pd.DataFrame({'Conventional': conventional, 'Electric': electric}, index=Y)
        df.plot(ax=a2, kind = 'bar', color={"Conventional": "#A3AF9E", "Electric": "#00ADFF"})
        
        # a2.set_title('Costo anual', fontsize=8)
        a2.set_title('Annual Cost', fontsize=8)
        a2.legend(['Diesel', 'Gas'], fontsize=8)
        # a2.set_ylabel('Costo [Millones de COP]', fontsize=8)
        a2.set_ylabel('Cost [thousands of USD]', fontsize=8)
        a2.set_xlabel('Año', fontsize=8)

        currency, year, annual_distance, ipc = self.get_data_config()
        co2, co, nox, hc, pmx, noise_c, noise_e = self.emissions()
        emissions_c = [co2, co, nox]
        emissions_e = [0, 0, 0]
        for i in range(len(emissions_c)):
            emissions_c[i] = emissions_c[i] * annual_distance / 1000000
        index=['CO2','CO','NOx']
        # emissions_c.append(noise_c)

        a3 = fig.add_subplot(133)
        df = pd.DataFrame({'Conventional': emissions_c, 'Electric': emissions_e}, index=index)
        df.plot(ax=a3, kind = 'bar', fontsize=8)
        a3.set_title('Annual emissions', fontsize=8)
        a3.legend(['conventional', 'electric'], fontsize=8)
        a3.set_ylabel('Tons of emissions', fontsize=8)
        canvas3 = FigureCanvasTkAgg(fig, self)
        canvas3.get_tk_widget().pack()
        fig.savefig('images/APPGraphics', transparent=True)



    def create_figure_accumulated(self):
        currency, year, annual_distance, ipc = self.get_data_config()
        initialCost_C, yearlyRaise_C, yearlyRaise_others, Cen_C, costMaintenance_C, others_C, other_C = self.get_data_combustion()
        initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, costMaintenance_E, others_E, other_E, batery_capacity = self.get_data_electric()
        total_combustion, total_electric, j = FC.accumulatedCost2(initialCost_C, yearlyRaise_C, Cen_C, costMaintenance_C, others_C, other_C, yearlyRaise_others,
                     initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, costMaintenance_E, others_E, other_E, batery_capacity,
                     currency, year, ipc, annual_distance )

        years = [*range(0, j+1, 1)]
        fig = Figure(figsize=(5,5),dpi=100)
        a = fig.add_subplot(221)
        a.plot(years, total_combustion, label = "conventional", color="#A3AF9E")
        a.plot(years, total_electric, label = "electric", color="#00ADFF")
        a.grid()
        a.set_title ('%d km/año' %annual_distance, fontsize=10)
        a.set_ylabel('Accumulated cost [millions COP]')
        a.set_xlabel('Year')
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        canvas.draw()
    
    def create_figure_annual(self):
        currency, year, annual_distance, ipc = self.get_data_config()
        initialCost_C, yearlyRaise_C, yearlyRaise_others, Cen_C, costMaintenance_C, others_C, other_C = self.get_data_combustion()
        initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, costMaintenance_E, others_E, other_E, batery_capacity = self.get_data_electric()

        total_combustion, total_electric, j = FC.accumulatedPerYear(initialCost_C, yearlyRaise_C, Cen_C, costMaintenance_C, others_C, other_C, yearlyRaise_others,
                     initialCost_E, yearlyRaise_E, yearlyRaise_batery, Cen_E, costMaintenance_E, others_E, other_E, batery_capacity,
                     currency, year, ipc, annual_distance )

        years = [*range(0, j+1, 1)]
        Y = [str(x) for x in years]
        conventional = total_combustion
        electric = total_electric
        fig = Figure(figsize=(5,5),dpi=100)
        a = fig.add_subplot(222)
        df = pd.DataFrame({'Conventional': conventional, 'Electric': electric}, index=Y)
        df.plot(ax=a, kind = 'bar')
        
        a.set_title('Costo anual')
        a.legend(['Convencional', 'Eléctrico'])
        a.set_ylabel('Costo [millones COP]')
        a.set_xlabel('Año')
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        canvas.draw()
    
    def create_figure_emissions(self):
        currency, year, annual_distance, ipc = self.get_data_config()
        co2, co, nox, hc, pmx = self.emissions()
        emissions = [co2, co, nox]
        for i in range(len(emissions)):
            emissions[i] = emissions[i] * annual_distance / 1000
        index=['CO2','CO','NOx']
        fig = Figure(figsize=(5,5),dpi=100)
        a = fig.add_subplot(223)
        plt.bar(index, emissions, color ='r', width=0.2)
        a.set_title('Annual emissions')
        a.set_ylabel('Total emissions [Kg]')
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack()
        canvas.draw()

class Application(ttk.Frame):


    def __init__(self, main_window):
        super().__init__(main_window)

        main_folder = os.path.dirname(__file__)
        images_folder = os.path.join(main_folder, 'images')

        main_window.title("Vehicles APP")
        main_window.iconbitmap(os.path.join(images_folder, "logo.ico"))
        self.notebook = ttk.Notebook(self)

        self.main_panel()

        self.greeting_frame = ConventionalV(self.notebook)
        self.notebook.add(self.greeting_frame, text="Conventional Vehicle", padding=10)

        self.about_frame = ElectricV(self.notebook)
        self.notebook.add(self.about_frame, text="Electric Vehicle", padding=10)

        self.about_frame = Comparison(self.notebook)
        self.notebook.add(self.about_frame, text="Comparison", padding=10)

        self.notebook.pack(padx=10, pady=10)
        self.pack()

    def main_panel(self):
        option = IntVar()
        Label(self, text="Choose a currency").pack()
        Radiobutton(self, text="USD", value=1, variable=option,
                    command=lambda:self.set_config(option)).pack()
        Radiobutton(self, text="COP", value=2, variable=option,
                    command=lambda:self.set_config(option)).pack()

        self.fields = ('Annual distance [km]', 'Years')
        self.entries = {}
        for field in self.fields:
            row = ttk.Notebook(self)
            lab = Label(row, width=22, text=field+": ", anchor='w') ####CAMBIAR CONFIG DE TAMAÑO
            ent = Entry(row)
            ent.insert(0,"0")
            row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
            lab.pack(side = LEFT)
            ent.pack(side = RIGHT, expand = YES, fill = X)
            self.entries[field] = ent
        self.greet_button = ttk.Button(self, text="Ok", command=lambda:self.set_config(option))
        self.greet_button.pack()
        self.greet_label = ttk.Label(self)
        self.greet_label.pack()

    def set_config(self,option):
        annual_distance = float(self.entries['Annual distance [km]'].get())
        years = float(self.entries['Years'].get())
        options  = option.get()
        if options == 1:
            currency_name = "USD"
            currency = 5118 # USD=5118 (historical maximum)
        elif options == 2:
            currency_name = "COP"
            currency =  1000000
        config = {'Annual distance' : annual_distance,
                  'Years' : int(years),
                  'Currency' : currency,
                  'Currency name' : currency_name
                  }
        # config = {'Annual distance' : 50000,
        #           'Years' : 10,
        #           'Currency' : 1000000,
        #           'Currency name' : "COP"
        #           }
        with open('data_files/data_config.json', 'w') as file:
            json.dump(config, file, indent=4)

def end_action():
    if path.exists('data_files/data_config.json'):
        remove('data_files/data_config.json')
    if path.exists('data_files/data_combustion.json'):
        remove('data_files/data_combustion.json')
    if path.exists('data_files/data_electric.json'):
        remove('data_files/data_electric.json')
    if path.exists('data_files/electricTemp.json'):
        remove('data_files/electricTemp.json')
    if path.exists('data_files/combustionTemp.json'):
        remove('data_files/combustionTemp.json')
    main_window.destroy()

if __name__ == '__main__':
    main_window = tk.Tk()
    main_window.geometry("1600x900")
    main_window.option_add('*Font', 'Calibri-Light 12')
    app = Application(main_window)
    button = ttk.Button(app, text="Quite", command=end_action)
    button.pack()

    app.mainloop()