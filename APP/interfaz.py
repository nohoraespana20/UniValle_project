import tkinter as tk
from tkinter import ttk
from tkinter import *
import functions_cost as FC
import os
from os import path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from os import remove

class ConventionalV(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = ('Vehicle cost', 'Galon fuel cost', 'Fuel yearly raise [%]',  
                       'Maintenance annual cost', 'Soat annual cost', 
                       'Other annual cost', 'Insurances yearly raise [%]', 
                       'Daily consumption [gl]', 'Daily distance [km]' 
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
        other_cost = float(self.entries['Other annual cost'].get())
        insurance_raise = float(self.entries['Insurances yearly raise [%]'].get())
        daily_consumption = float(self.entries['Daily consumption [gl]'].get())
        daily_distance = float(self.entries['Daily distance [km]'].get())
        data_combustion = { 'Vehicle cost': vehicle_cost,
                            'Galon cost': galon_cost,
                            'Fuel raise': fuel_raise,
                            'Maintenance cost': maintenance_cost,
                            'SOAT cost': soat_cost,
                            'Other cost': other_cost,
                            'Insurance raise': insurance_raise,
                            'Daily consumption': daily_consumption,
                            'Daily distance' : daily_distance
                        }
        with open('data_files/data_combustion.json', 'w') as file:
            json.dump(data_combustion, file, indent=4)
        
    def show_index(self):
        self.save_data()
        file = 'data_files/data_combustion.json'
        with open(file) as file:
                data = json.load(file)
        gl_100km = 100 * (data['Daily consumption'] / data['Daily distance'])

        self.greet_label["text"] = "gl/100km = {} ".format(gl_100km)
       
class ElectricV(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = ('Vehicle cost', 'kWh cost', 'kWh yearly raise [%]',  
                       'Daily consumption [kWh]', 'Daily distance [km]',
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
        maintenance_cost = data['Maintenance cost']*0.35
        soat_cost =   data['SOAT cost']*0.9  
        other_cost = data['Other cost']*0.7
        insurance_raise = data['Insurance raise']

        vehicle_cost = float(self.entries['Vehicle cost'].get())
        kWh_cost = float(self.entries['kWh cost'].get())
        kWh_raise = float(self.entries['kWh yearly raise [%]'].get())
        daily_consumption = float(self.entries['Daily consumption [kWh]'].get())
        daily_distance = float(self.entries['Daily distance [km]'].get())
        batery_capacity = float(self.entries['Batery capacity [kWh]'].get())
        
        data_electric = { 'Vehicle cost': vehicle_cost,
                            'kWh cost': kWh_cost,
                            'kWh raise': kWh_raise,
                            'Maintenance cost': maintenance_cost,
                            'SOAT cost': soat_cost,
                            'Other cost': other_cost,
                            'Insurance raise': insurance_raise,
                            'Daily consumption': daily_consumption,
                            'Daily distance' : daily_distance,
                            'Batery capacity [kWh]' : batery_capacity
                        }
        with open('data_files/data_electric.json', 'w') as file:
            json.dump(data_electric, file, indent=4)
        
    def show_index(self):
        self.save_data()
        file = 'data_files/data_electric.json'
        with open(file) as file:
                data = json.load(file)
        kWh_100km = 100 * (data['Daily consumption'] / data['Daily distance'])
        self.greet_label["text"] = "kWH/100km = {} ".format(kWh_100km)

class Comparison(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.greet_button = ttk.Button(self, text= "Graph", command=self.create_figure)
        self.greet_button.pack()
        self.greet_label = ttk.Label(self)
        self.greet_label.pack()

    def create_figure(self):
        file = 'data_files/data_config.json'
        with open(file) as file:
                data_config = json.load(file)
        file = 'data_files/data_combustion.json'
        with open(file) as file:
                data_combustion = json.load(file)
        file = 'data_files/data_electric.json'
        with open(file) as file:
                data_electric = json.load(file)

        ###GENERAL DATA###
        currency = data_config['Currency']
        year = data_config['Years']
        annual_distance = data_config['Annual distance']
        IPC = 0.0457 
        file_C = 'data_files/Fuel_mean.json' 
        file_E = 'data_files/kWh_mean.json' 

        ### Combustion data###
        initialCost_C =  data_combustion['Vehicle cost'] / currency
        costGalonFuel = data_combustion['Galon cost']  / currency 
        yearlyRaise_C = data_combustion['Fuel raise'] / 100 
        costMaintenance_C = data_combustion['Maintenance cost'] / currency 
        yearlyRaise_others = 0.1 
        SOAT_C = data_combustion['SOAT cost'] / currency 
        tax_C = initialCost_C * 0.01 
        otherC = data_combustion['Other cost'] / currency 
        othersC = SOAT_C + tax_C  

        ### Electric data###
        initialCost_E = data_electric['Vehicle cost'] / currency 
        costkWh = data_electric['kWh cost'] / currency 
        yearlyRaise_E = data_electric['kWh raise'] /100
        costMaintenance_E = data_electric['Maintenance cost'] / currency
        yearlyRaise_batery = -0.0967 
        SOAT_E = data_electric['SOAT cost'] / currency
        tax_E = initialCost_E * 0.01 * 0.4 
        otherE = data_electric['Other cost'] / currency
        othersE = SOAT_E + tax_E
        batery_capacity = data_electric['Batery capacity [kWh]']

        #Costo energético promedio por kilómetro - combustion
        CenPeak_C,  CenPeakOff_C =  FC.meanFuelPerKM_C(file_C)
        CenPeak_C = CenPeak_C * costGalonFuel
        CenPeakOff_C =  CenPeakOff_C * costGalonFuel
        Cen_C = (CenPeak_C + CenPeakOff_C)/2

        #Costo energético promedio por kilómetro - electrico
        CenPeak_E,  CenPeakOff_E =  FC.meanFuelPerKM_E(file_E)
        CenPeak_E = CenPeak_E * costkWh
        CenPeakOff_E =  CenPeakOff_E * costkWh
        Cen_E = (CenPeak_E + CenPeakOff_E)/2

        total_combustion, total_electric, j = FC.accumulatedCost2(initialCost_C, initialCost_E,
                                                                  currency, year,
                                                                  yearlyRaise_C, yearlyRaise_E,
                                                                  IPC, yearlyRaise_batery, yearlyRaise_others,
                                                                  Cen_C, Cen_E, 
                                                                  costMaintenance_C, costMaintenance_E, 
                                                                  othersC, othersE, 
                                                                  otherC, otherE, 
                                                                  annual_distance, annual_distance*1.16,
                                                                  batery_capacity) 

        years = [*range(0, j+1, 1)]
        fig = Figure(figsize=(5,5))
        a = fig.add_subplot(111)
        a.plot(years, total_combustion, label = "convencional")
        a.plot(years, total_electric, label = "eléctrico")
        a.grid()
        a.set_title ('%d km/año' %annual_distance, fontsize=10)
        a.set_ylabel('Costo acumulado [millones COP]')
        a.set_xlabel('Año')
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
            lab = Label(row, width=22, text=field+": ", anchor='w')
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
            currency = 4999
        elif options == 2:
            currency_name = "COP"
            currency =  1000000
        config = {'Annual distance' : annual_distance,
                  'Years' : int(years),
                  'Currency' : currency,
                  'Currency name' : currency_name
                  }
        with open('data_files/data_config.json', 'w') as file:
            json.dump(config, file, indent=4)
        
def end_action():
    if path.exists('data_files/data_config.json'):
        remove('data_files/data_config.json')
    if path.exists('data_files/data_combustion.json'):
        remove('data_files/data_combustion.json')
    if path.exists('data_files/data_config.json'):
        remove('data_files/data_config.json')
    main_window.destroy()

if __name__ == '__main__':
    main_window = tk.Tk()
    app = Application(main_window)
    greet_button = ttk.Button(app, text="Quite", command=end_action)
    greet_button.pack()
    app.mainloop()