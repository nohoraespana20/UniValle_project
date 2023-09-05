import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import numpy as np
from tkinter import *
from matplotlib.figure import Figure
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox as mb
import os
import intersection as IN

class Data():
    '''
        Get data from interface window and save in a .json file
    '''
    def saveConfig(self):
        try:
            currency = self.currency.get()
            modeTransport = self.modeTransport.get()
            time = float(self.time.get())
            annualDistance = float(self.annualDistance.get())
            dailyDistance = float(self.dailyDistance.get())
        
            configuration = {  'Currency' : currency,
                                'Mode of transport' : modeTransport,
                                'Years' : int(time),
                                'Annual distance' : int(annualDistance),
                                'Daily distance' : int(dailyDistance),
                            }
            with open('data_files/data_config.json', 'w') as file:
                json.dump(configuration, file, indent=4)
        except ValueError:
            mb.showerror("Error","Hay casillas vacías en la sección Configuración")
    
    def saveCombustionData(self):
        try: 
            vehicleCost = float(self.combustionCost.get())
            galonCost = float(self.fuelCost.get())
            fuelRaise = float(self.fuelRaise.get())
            maintenanceCost = float(self.combustionMaintenanceCost.get())
            soatCost = float(self.soatCost.get())
            checkCost = float(self.checkCost.get())
            otherInsurance = float(self.otherInsurance.get())
            insuranceRaise = float(self.insuranceRaise.get())
            dailyConsumption = float(self.dailyConsumption.get())
            repairs = float(self.repairs.get())

            dataVCI = { 'Vehicle cost': vehicleCost,
                        'Galon cost': galonCost,
                        'Fuel raise': fuelRaise,
                        'Daily consumption': dailyConsumption,
                        'Maintenance cost': maintenanceCost,
                        'SOAT cost': soatCost,
                        'Other insurances' : otherInsurance,
                        'Annual check': checkCost,
                        'Insurance raise': insuranceRaise,
                        'Repairs per year' : repairs
                        }
            with open('data_files/data_combustion.json', 'w') as file:
                json.dump(dataVCI, file, indent=4)
        except ValueError:
            mb.showerror("Error","Hay casillas vacías en la sección Vehículo Combustión Interna")

    def saveElectricData(self):
        try:
            vehicleCost = float(self.electricCost.get())
            kWhCost = float(self.kWhCost .get())
            kWhRaise = float(self.kWhRaise.get())
            dailykWh = float(self.dailykWh.get())
            bateryCapacity = float(self.bateryCapacity.get())

            dataVE = { 'Vehicle cost': vehicleCost,
                        'kWh cost': kWhCost,
                        'kWh raise': kWhRaise,
                        'Daily consumption': dailykWh,
                        'Batery capacity [kWh]' : bateryCapacity,
                        }
            with open('data_files/data_electric.json', 'w') as file:
                json.dump(dataVE, file, indent=4)  
        except ValueError:
            mb.showerror("Error","Hay casillas vacías en la sección Vehículo Eléctrico")

class IndexCalculation():
    '''
    Import data and process to calculate the technical, economic, ambiental, and social indexes. 
    '''
    def readJson(file):
        with open(file) as file:
            data = json.load(file)
        return data

    def importData():
        dataConfig = IndexCalculation.readJson('data_files/data_config.json')
        dataCombustion = IndexCalculation.readJson('data_files/data_combustion.json')
        dataElectric = IndexCalculation.readJson('data_files/data_electric.json')

        currency = dataConfig['Currency']
        vehicle = dataConfig['Mode of transport']
        year = dataConfig['Years']
        annualDistance = dataConfig['Annual distance']
        dailyDistance = dataConfig['Daily distance']

        vciCost = dataCombustion['Vehicle cost']
        galonCost = dataCombustion['Galon cost']
        fuelRaise = dataCombustion['Fuel raise']
        dailyFuel = dataCombustion['Daily consumption']
        maintenanceCombustionCost = dataCombustion['Maintenance cost']
        soatCost = dataCombustion['SOAT cost']
        otherInsurance = dataCombustion['Other insurances']
        checkCost = dataCombustion['Annual check']
        insuranceRaise = dataCombustion['Insurance raise']
        repairs = dataCombustion['Repairs per year']

        evCost = dataElectric['Vehicle cost']
        kWhCost =  dataElectric['kWh cost']
        kWhRaise =  dataElectric['kWh raise']
        dailykWh =  dataElectric['Daily consumption']
        bateryCapacity =  dataElectric['Batery capacity [kWh]']

        configuration = [currency, vehicle, year, annualDistance, dailyDistance]
        combustion = [vciCost, galonCost, fuelRaise, dailyFuel, maintenanceCombustionCost, soatCost, otherInsurance, checkCost, insuranceRaise, repairs]
        electric = [evCost, kWhCost, kWhRaise, dailykWh, bateryCapacity]

        return configuration, combustion, electric
        
    def averageData(data):
        configuration, _, _ = IndexCalculation.importData()
        if configuration[1] == 'Taxi':
            distances = [3.2, 5.3, 6.6] #Average distance from results of emissions simulation
            average = []
            for i in range(2):
                average.append([np.mean(data[i][0:2])/distances[0], np.mean(data[i][2:4])/distances[1], np.mean(data[i][4:])/distances[2]])
        elif configuration[1] == 'Bus':
            distances = [24.5*6, 31.4*6, 25.0*6, 18.1*6] # C1, C16, E1, E2
            average = []
            for i in range(2):
                average.append([np.mean(data[i][0])/distances[0], np.mean(data[i][1])/distances[1], np.mean(data[i][2])/distances[2], np.mean(data[i][3])/distances[3]])
        else:
            print('currency parameter is not defined')
        
        averagePerKm = round(np.mean(average),2)
        # print(averagePerKm)
        return averagePerKm

    def consumptionIndex(dailyConsumption, distance, typeVehicle, modeTransport):
        '''
        typeVehicle parameter has two options: VCI or EV in string format
        modeTransport parameter has two options: Taxi or Bus in string format
        '''
        if modeTransport == 'Taxi':
            conversionFactor = 36.7
        elif modeTransport == 'Bus':
            conversionFactor = 40.5
        else:
            print('modeTransport parameter is not defined')
        
        if typeVehicle == 'VCI':
            E100km = round(dailyConsumption * conversionFactor * 100 / distance, 2)
        elif typeVehicle == 'EV':
            E100km = round(dailyConsumption * 100 / distance, 2)
        else:
            print('typeVehicle parameter is not defined')
        return E100km

    def availabilityFactor(typeVehicle):
        '''
        typeVehicle parameter has two options: VCI or EV in string format
        '''
        _ , combustion, _ = IndexCalculation.importData()
        if typeVehicle == 'VCI':
            days2repair =  5
            days2maintenance = 6
        elif typeVehicle == 'EV':
            days2repair =  5
            days2maintenance = 2.5
        else:
            print('typeVehicle parameter is not defined')
        avaliabilityFactor = round((365 - (combustion[9] * days2repair) - days2maintenance) * 100 / 365, 2)
        return avaliabilityFactor
    
    def icrIndex(costConsumption, consumption, distance):
        icr = round(costConsumption * consumption / (distance), 2)
        return icr

    def accumulatedCost(configuration, combustion, electric, typeVehicle):
        if configuration[0] == "USD":
            currency = 1000
        elif configuration[0] == "COP":
            currency = 1000000
        else:
            print("currency parameter is not defined")

        ipc = 0.0457 # Average value of IPC in Colombia
        otherInsurance = combustion[6]
        insuranceCostRaise = combustion[8] / 100 
        totalCost = []
        totalCost = [*range(0, configuration[2], 1)]

        if typeVehicle == 'VCI':
            configuration, _, _ = IndexCalculation.importData()
            if configuration[1] == 'Taxi':
                powerConsumption = IndexCalculation.averageData(IndexCalculation.readJson('data_files/taxi/Fuel_mean.json'))*configuration[3]
            elif configuration[1] == 'Bus':
                powerConsumption = IndexCalculation.averageData(IndexCalculation.readJson('data_files/bus/Fuel_mean.json'))*configuration[3]
            else:
                print('currency parameter is not defined')
            
            totalCost[0] = combustion[0] 
            taxCost = combustion[0] * 0.01 # Based on "Ley 1964 de 2019, Congreso de Colombia"
            annualPowerCost = powerConsumption * combustion[1]
            annualPowerCostRaise  = combustion[2] / 100
            maintenanceCost = combustion[4]
            soatCost = combustion[5]
            otherInsurance = combustion[6] # Contractual insuarence and all damages insurance
            checkCost = combustion[7]
        elif typeVehicle == 'EV':
            configuration, _, _ = IndexCalculation.importData()
            if configuration[1] == 'Taxi':
                powerConsumption = IndexCalculation.averageData(IndexCalculation.readJson('data_files/taxi/kWh_mean.json'))*configuration[3]
            elif configuration[1] == 'Bus':
                powerConsumption = IndexCalculation.averageData(IndexCalculation.readJson('data_files/bus/kWh_mean.json'))*configuration[3]
            else:
                print('currency parameter is not defined')

            # totalCost[0] = electric[0]
            # taxCost = combustion[0] * 0.01 * 0.4 # Based on "Ley 1964 de 2019, Congreso de Colombia"
            # annualPowerCost = powerConsumption * electric[1]
            # annualPowerCostRaise  = electric[2] / 100
            # maintenanceCost = combustion[4] * 0.4
            # soatCost = combustion[5] * 0.9
            # checkCost = combustion[7] * 0.7 
            # # bateryCost = electric[4] * 156 * 4000 # Batery cost in COP
            # bateryCost = electric[4] * 156 # Batery cost in USD
            # batteryYearlyRaise = -0.0967 # According to technology reduction cost trend

            totalCost[0] = electric[0]
            taxCost = combustion[0] * 0.01 * 0.9
            annualPowerCost = powerConsumption * electric[1]
            annualPowerCostRaise  = electric[2] / 100
            maintenanceCost = combustion[4]
            soatCost = combustion[5] * 0.9
            checkCost = combustion[7] 
            bateryCost = electric[4] * 156 / 5000 * 0# Batery cost in COP
            batteryYearlyRaise = -0.0967 # According to technology reduction cost trend
        else:
            print('typeVehicle parameter is not defined ')

        for i in range(1,configuration[2],1):
            totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + taxCost
            if i >= 2:
                #Annual variance of parameters costs
                taxCost = taxCost * (1 + insuranceCostRaise)
                annualPowerCost = annualPowerCost * (1 + annualPowerCostRaise)
                maintenanceCost = maintenanceCost * (1 + ipc)
                soatCost = soatCost * (1 + insuranceCostRaise)
                otherInsurance = otherInsurance * (1 + insuranceCostRaise)
                checkCost = checkCost * (1 + insuranceCostRaise)
                # totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + \
                #     taxCost + checkCost
                totalCost[i] = totalCost[i] + checkCost
                if typeVehicle == 'EV':
                    bateryCost = bateryCost * (1 + batteryYearlyRaise)
                    if i==8 or i==16 or i==24:
                        # totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance \
                        #     + checkCost + taxCost + bateryCost
                        totalCost[i] = totalCost[i] + bateryCost
            # else:
            #     totalCost[i] = totalCost[i-1] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + taxCost

        for i in range(len(totalCost)):
            totalCost[i] = round(totalCost[i] / currency , 2)
        
        return totalCost

    def annualCost(configuration, combustion, electric, typeVehicle):
        if configuration[0] == "USD":
            currency = 1000
        elif configuration[0] == "COP":
            currency = 1000000
        else:
            print("currency parameter is not defined")

        ipc = 0.0457 # Average value of IPC in Colombia
        otherInsurance = combustion[6]
        insuranceCostRaise = combustion[8] / 100 
        totalCost = []
        totalCost = [*range(0, configuration[2], 1)]

        if typeVehicle == 'VCI':
            configuration, _, _ = IndexCalculation.importData()
            if configuration[1] == 'Taxi':
                powerConsumption = IndexCalculation.averageData(IndexCalculation.readJson('data_files/taxi/Fuel_mean.json'))*configuration[3]
            elif configuration[1] == 'Bus':
                powerConsumption = IndexCalculation.averageData(IndexCalculation.readJson('data_files/bus/Fuel_mean.json'))*configuration[3]
            else:
                print('currency parameter is not defined')

            totalCost[0] = combustion[0] 
            taxCost = combustion[0] * 0.01 # Based on "Ley 1964 de 2019, Congreso de Colombia"
            annualPowerCost = powerConsumption * combustion[1]
            annualPowerCostRaise  = combustion[2] / 100
            maintenanceCost = combustion[4]
            soatCost = combustion[5]
            otherInsurance = combustion[6] # Contractual insuarence and all damages insurance
            checkCost = combustion[7]
        elif typeVehicle == 'EV':
            configuration, _, _ = IndexCalculation.importData()
            if configuration[1] == 'Taxi':
                powerConsumption = IndexCalculation.averageData(IndexCalculation.readJson('data_files/taxi/kWh_mean.json'))*configuration[3]
            elif configuration[1] == 'Bus':
                powerConsumption = IndexCalculation.averageData(IndexCalculation.readJson('data_files/bus/kWh_mean.json'))*configuration[3]
            else:
                print('currency parameter is not defined')
                
            # totalCost[0] = electric[0]
            # taxCost = combustion[0] * 0.01 * 0.4 # Based on "Ley 1964 de 2019, Congreso de Colombia"
            # annualPowerCost = powerConsumption * electric[1]
            # annualPowerCostRaise  = electric[2] / 100
            # maintenanceCost = combustion[4] * 0.4
            # soatCost = combustion[5] * 0.9
            # checkCost = combustion[7] * 0.7 
            # # bateryCost = electric[4] * 156 * 4000 # Batery cost in COP
            # bateryCost = electric[4] * 156 # Batery cost in USD
            # batteryYearlyRaise = -0.0967 # According to technology reduction cost trend

            totalCost[0] = electric[0]
            taxCost = combustion[0] * 0.01 * 0.9
            annualPowerCost = powerConsumption * electric[1]
            annualPowerCostRaise  = electric[2] / 100
            maintenanceCost = combustion[4]
            soatCost = combustion[5] * 0.9
            checkCost = combustion[7] 
            bateryCost = electric[4] * 156 / 5000 * 0# Batery cost in COP
            batteryYearlyRaise = -0.0967 # According to technology reduction cost trend
        else:
            print('typeVehicle parameter is not defined ')

        for i in range(1,configuration[2],1):
            totalCost[i] = totalCost[i] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + taxCost
            if i >= 2:
                #Annual variance of parameters costs
                taxCost = taxCost * (1 + insuranceCostRaise)
                annualPowerCost = annualPowerCost * (1 + annualPowerCostRaise)
                maintenanceCost = maintenanceCost * (1 + ipc)
                soatCost = soatCost * (1 + insuranceCostRaise)
                otherInsurance = otherInsurance * (1 + insuranceCostRaise)
                checkCost = checkCost * (1 + insuranceCostRaise)
                # totalCost[i] = totalCost[i] + annualPowerCost + maintenanceCost + soatCost + otherInsurance + \
                #     taxCost + checkCost
                totalCost[i] = totalCost[i] + checkCost
                if typeVehicle == 'EV':
                    bateryCost = bateryCost * (1 + batteryYearlyRaise)
                    # print('BateryCost: ', bateryCost)
                    if i==8 or i==16 or i==24:
                        # totalCost[i] = totalCost[i] + annualPowerCost + maintenanceCost + soatCost + otherInsurance \
                        #     + checkCost + taxCost + bateryCost
                        totalCost[i] = totalCost[i] + bateryCost
        
        for i in range(len(totalCost)):
            totalCost[i] = totalCost[i] / currency
        
        return totalCost

    def emissionsPerKm():
        configuration, _, _ = IndexCalculation.importData()
        if configuration[1] == 'Taxi':
            co2PerKm = IndexCalculation.averageData(IndexCalculation.readJson('data_files/taxi/co2_mean.json'))
        elif configuration[1] == 'Bus':
            co2PerKm = IndexCalculation.averageData(IndexCalculation.readJson('data_files/bus/co2_mean.json'))
        else:
            print('currency parameter is not defined')
        
        return round(co2PerKm, 2)

    def indexesCalculation():
        configuration, combustion, electric = IndexCalculation.importData()

        if configuration[0] == 'USD':
            socialFactor = 220
        elif configuration[0] == 'COP':
            socialFactor = 995000
        else:
            print('currency parameter is not defined')

        combustionConsumption = IndexCalculation.consumptionIndex(combustion[3], configuration[4], 'VCI', configuration[1])
        electricConsumption = IndexCalculation.consumptionIndex(electric[3], configuration[4], 'EV', configuration[1])
        
        avaliabilityCombustion = IndexCalculation.availabilityFactor('VCI')
        avaliabilityElectric = IndexCalculation.availabilityFactor('EV')

        icrCombustion = IndexCalculation.icrIndex(combustion[1], combustion[3], configuration[4])
        icrElectric = IndexCalculation.icrIndex(electric[1], electric[3], configuration[4])

        emissionsCombustion = IndexCalculation.emissionsPerKm() 
        emissionsElectric = round(164.38 * electricConsumption / 100 , 2)

        combustionAccumulatedCost = IndexCalculation.accumulatedCost(configuration, combustion, electric, 
                                                                        'VCI')
        electricAccumulatedCost = IndexCalculation.accumulatedCost(configuration, combustion, electric, 
                                                                        'EV')
        
        socialEmissionsCostCombustion = round(emissionsCombustion * socialFactor / 1000000 , 3)
        socialEmissionsCostElectric = round(emissionsElectric * socialFactor / 1000000 , 3)

        return combustionConsumption, electricConsumption, avaliabilityCombustion, avaliabilityElectric, \
                    icrCombustion, icrElectric, emissionsCombustion , emissionsElectric, \
                    combustionAccumulatedCost, electricAccumulatedCost, \
                    socialEmissionsCostCombustion, socialEmissionsCostElectric
    
    def createGraphics():
        configuration, combustion, electric = IndexCalculation.importData()
        icrCombustion = IndexCalculation.icrIndex(combustion[1], combustion[3], configuration[4])
        icrElectric = IndexCalculation.icrIndex(electric[1], electric[3], configuration[4])
        combustionAccumulatedCost = IndexCalculation.accumulatedCost(configuration, combustion, electric, 
                                                                        'VCI')
        electricAccumulatedCost = IndexCalculation.accumulatedCost(configuration, combustion, electric, 
                                                                        'EV')
        combustionAnnualCost = IndexCalculation.annualCost(configuration, combustion, electric, 
                                                                        'VCI')
        electricAnnualCost = IndexCalculation.annualCost(configuration, combustion, electric, 
                                                                        'EV')
        
        if configuration[0] == "USD":
            text = "miles de dólares [USD]"
        elif configuration[0] == "COP":
            text = "millones de pesos [COP]"
        else:
            print("currency parameter is not defined")

        years = [*range(0, configuration[2], 1)]
        fig = Figure(figsize=(7,8))
        a1 = fig.add_subplot(211)
        a1.plot(years, combustionAccumulatedCost, label = "VCI", color='#A0A0A0')
        # a1.plot(years, electricAccumulatedCost, label = "VE", color='#33FF33')
        a1.plot(years, electricAccumulatedCost, label = "Gas", color='#00ADFF')
        a1.grid()
        a1.set_title ('Costo acumulado para %d km/año' %configuration[3], fontsize=8)
        # a1.legend(['VCI', 'VE'], fontsize=8)
        a1.legend(['VCI', 'Gas'], fontsize=8)
        a1.set_ylabel('Costo en %s' %text, fontsize=8)
        a1.set_xlabel('Año', fontsize=8)
        IN.getVectors(configuration[3], combustionAccumulatedCost, electricAccumulatedCost)
        
        Y = [str(x) for x in years]
        conventional = combustionAnnualCost
        electric = electricAnnualCost
        
        a2 = fig.add_subplot(212)
        df = pd.DataFrame({'VCI': conventional, 'EV': electric}, index=Y)
        # df.plot(ax=a2, kind = 'bar', rot=0, color=['#A0A0A0', '#33FF33'])
        df.plot(ax=a2, kind = 'bar', rot=0, color=['#A0A0A0', '#00ADFF'])
        
        a2.set_title('Costo anual para %d km/año' %configuration[3], fontsize=8)
        # a2.legend(['VCI', 'VE'], fontsize=8)
        a2.legend(['VCI', 'Gas'], fontsize=8)
        a2.grid()
        a2.set_ylabel('Costo en %s' %text, fontsize=8)
        a2.set_xlabel('Año', fontsize=8)
        fig.savefig("images/figura_600dpi.png", dpi=600, transparent=True)
        return fig

class Interface():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Evaluación de vehículos")
        self.window.geometry("800x550")
        self.createWidgets()
        self.generalMenu()
        self.configurationFrame()
        self.combustionFrame()
        self.electricFrame()
        self.resultsFrame()
           
    def generalMenu(self):
        menubar = tk.Menu(self.window)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Acerca de ", command=lambda:self.aboutFunction())
        filemenu.add_command(label="Documentación", command=lambda:self.docFunction())
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.window.quit)
        menubar.add_cascade(label="Ayuda", menu=filemenu)

        self.window.config(menu=menubar)

        quitButton = ttk.Button(self.window, text="Cerrar", command=self.window.destroy)
        quitButton.grid(row=1, column=3)
    
    def aboutFunction(self):
        text = "Este trabajo ha sido financiado por el Fondo de Ciencia, Tecnología e Innovación \nSistema General de Regalías de Colombia \nProyecto SIGP 66777, BPIN2020020020000100041. \n\nDESARROLLO DE UN MODELO ALTERNATIVO DE ENERGÍA Y MOVILIDAD CON FUENTES NO CONVENCIONALES EN LA UNIVERSIDAD DE NARIÑO."
        mb.showinfo("Acerca de ", text)

    def docFunction(self):
        file = "documentation.pdf"
        os.startfile(file)
        
    def createWidgets(self):
        # Create some room around all the internal frames
        self.window['padx'] = 5
        self.window['pady'] = 5

    def createBox(self, frame, text, variable, values, row):
        textLabel = ttk.Label(frame, text=text)
        textLabel.grid(row=row, column=1, sticky=tk.W, pady=3)
        box = ttk.Combobox(frame, height=4, textvariable=variable)
        box.grid(row=row, column=2)
        box['values'] = values
        box.current(0)
        return box
    
    def createEntry(self, frame, text, variable, initialValue, row):
        textLabel = ttk.Label(frame, text=text)
        textLabel.grid(row=row, column=1, sticky=tk.W + tk.N)
        entry = ttk.Entry(frame, textvariable=variable, width=20)
        entry.grid(row=row, column=2, sticky=tk.W, pady=3)
        entry.insert(tk.END, initialValue)
        return entry

    def configurationFrame(self):
        cfgFrame = ttk.LabelFrame(self.window, text="Configuración", relief=tk.SUNKEN, padding=10)
        cfgFrame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        self.currency = tk.StringVar()
        self.modeTransport = tk.StringVar()
        self.time = tk.StringVar()
        self.annualDistance = tk.StringVar()
        self.dailyDistance = tk.StringVar()

        self.createBox(cfgFrame, "Divisa", self.currency, ('', 'USD', 'COP'), 1)
        self.createBox(cfgFrame, "Modo de transporte", self.modeTransport, (" ", "Taxi", "Bus"), 2)
        self.createEntry(cfgFrame, "Años", self.time, "", 3)
        self.createEntry(cfgFrame, "Distancia anual [km]", self.annualDistance, "", 4)
        self.createEntry(cfgFrame, "Distancia diaria [km]", self.dailyDistance, "", 5)

        buttonSave = tk.Button(cfgFrame, text="Guardar", command=lambda:Data.saveConfig(self))
        buttonSave.grid(row=6, column=1)

    def combustionFrame(self):
        cFrame = ttk.LabelFrame(self.window, text="Vehículo combustión interna",
                                     relief=tk.RIDGE, padding=10)
        cFrame.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        self.combustionCost = tk.StringVar()
        self.fuelCost = tk.StringVar()
        self.fuelRaise = tk.StringVar()
        self.dailyConsumption = tk.StringVar()
        self.combustionMaintenanceCost = tk.StringVar()
        self.soatCost = tk.StringVar()
        self.checkCost = tk.StringVar()
        self.otherInsurance = tk.StringVar()
        self.insuranceRaise = tk.StringVar()
        self.repairs = tk.StringVar()

        self.createEntry(cFrame, "Costo de compra", self.combustionCost, "", 1)
        self.createEntry(cFrame, "Costo galón de combustible", self.fuelCost, "", 2)
        self.createEntry(cFrame, "% Incremento anual combustible", self.fuelRaise, "", 3)
        self.createEntry(cFrame, "Consumo diario [gl]", self.dailyConsumption, "", 4)
        self.createEntry(cFrame, "Costo anual mantenimiento", self.combustionMaintenanceCost, "", 5)
        self.createEntry(cFrame, "Costo anual SOAT", self.soatCost, "", 6)
        self.createEntry(cFrame, "Costo anual otros seguros", self.otherInsurance, "", 7)
        self.createEntry(cFrame, "Costo revisión tecnomecánica", self.checkCost, "", 8)
        self.createEntry(cFrame, "% Incremento anual seguros", self.insuranceRaise, "", 9)
        self.createEntry(cFrame, "Reparaciones por año", self.repairs, "", 10)

        buttonSave = tk.Button(cFrame, text="Guardar", command=lambda:Data.saveCombustionData(self))
        buttonSave.grid(row=12, column=1)

    def electricFrame(self):
        eFrame = ttk.LabelFrame(self.window, text="Vehículo eléctrico",
                                        relief=tk.RIDGE, padding=10)
        eFrame.grid(row=1, column=2, sticky=tk.E + tk.W + tk.N + tk.S, padx=6)

        self.electricCost = tk.StringVar()
        self.kWhCost = tk.StringVar()
        self.kWhRaise = tk.StringVar()
        self.dailykWh = tk.StringVar()
        self.bateryCapacity = tk.StringVar()

        self.createEntry(eFrame, "Costo de compra", self.electricCost, "", 1)
        self.createEntry(eFrame, "Costo kWh", self.kWhCost, "", 2)
        self.createEntry(eFrame, "% Incremento anual kWh", self.kWhRaise, "", 3)
        self.createEntry(eFrame, "Consumo diario [kWh]", self.dailykWh, "", 4)
        self.createEntry(eFrame, "Capacidad de batería [kWh]", self.bateryCapacity, "", 5)

        buttonSave = tk.Button(eFrame, text="Guardar", command=lambda:Data.saveElectricData(self))
        buttonSave.grid(row=6, column=1)

    def resultsFrame(self):
        rFrame = ttk.LabelFrame(self.window, text="Comparar", relief=tk.RIDGE, padding=10)
        rFrame.grid(row=2, column=2, padx=6, sticky=tk.E + tk.W + tk.N + tk.S)

        buttonIndex = tk.Button(rFrame, text="Mostrar índices", command=lambda:self.showIndexes())
        buttonIndex.grid(row=2, column=2)

        buttonGraphics = tk.Button(rFrame, text="Mostrar gráficas", command=lambda:self.showGraphics())
        buttonGraphics.grid(row=4, column=2)   
    
    def showIndexes(self):
        indexWindow = Toplevel()
        indexWindow.geometry("600x400")
        indexWindow.title("Índices")
        configuration, _, _ = IndexCalculation.importData()
        combustionConsumption, electricConsumption, avaliabilityCombustion, avaliabilityElectric, \
            icrCombustion, icrElectric, emissionsCombustion , emissionsElectric, \
            combustionAccumulatedCost, electricAccumulatedCost, \
            socialEmissionsCostCombustion, socialEmissionsCostElectric = IndexCalculation.indexesCalculation()

        text1 = ttk.Label(indexWindow, text="Índices técnicos")
        text1.grid(row=1, column=1, sticky=tk.W, pady=3)

        text1 = ttk.Label(indexWindow, text="VCI")
        text1.grid(row=2, column=2, sticky=tk.W, pady=3)
        text1 = ttk.Label(indexWindow, text="VE")
        text1.grid(row=2, column=4, sticky=tk.W, pady=3)

        text1 = ttk.Label(indexWindow, text="Consumo")
        text1.grid(row=3, column=1, sticky=tk.W, pady=3)
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=3, column=2, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(combustionConsumption)+" kWh/100km")
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=3, column=4, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(electricConsumption)+" kWh/100km")

        text1 = ttk.Label(indexWindow, text="Factor de disponibilidad")
        text1.grid(row=4, column=1, sticky=tk.W, pady=3)
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=4, column=2, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(avaliabilityCombustion)+" %")
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=4, column=4, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(avaliabilityElectric)+" %")

        text1 = ttk.Label(indexWindow, text="Índices económicos")
        text1.grid(row=6, column=1, sticky=tk.W, pady=3)

        text1 = ttk.Label(indexWindow, text="Costo/recorrido")
        text1.grid(row=8, column=1, sticky=tk.W, pady=3)
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=8, column=2, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(icrCombustion)+" %s/km" %configuration[0])
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=8, column=4, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(icrElectric)+" %s/km" %configuration[0])

        text1 = ttk.Label(indexWindow, text="Costo acumulado")
        text1.grid(row=9, column=1, sticky=tk.W, pady=3)
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=9, column=2, sticky=tk.W, pady=3)
        if configuration[0]=="USD":
            text = " miles de "
        if configuration[0]=="COP":
            text = " millones de "
        box3.insert(tk.END, str(combustionAccumulatedCost[-1])+text+"%s" %configuration[0])
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=9, column=4, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(electricAccumulatedCost[-1])+text+"%s" %configuration[0])

        text1 = ttk.Label(indexWindow, text="Índices ambientales")
        text1.grid(row=11, column=1, sticky=tk.W, pady=3)

        text1 = ttk.Label(indexWindow, text="Emisiones por kilómetro")
        text1.grid(row=13, column=1, sticky=tk.W, pady=3)
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=13, column=2, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(emissionsCombustion)+" gr CO2/km")
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=13, column=4, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(emissionsElectric)+" gr CO2/km")

        text1 = ttk.Label(indexWindow, text="Costo social por emisiones")
        text1.grid(row=14, column=1, sticky=tk.W, pady=3)
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=14, column=2, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(socialEmissionsCostCombustion)+" %s/tonCO2" %configuration[0])
        box3 = ttk.Entry(indexWindow, width=30)
        box3.grid(row=14, column=4, sticky=tk.W, pady=3)
        box3.insert(tk.END, str(socialEmissionsCostElectric)+" %s/tonCO2" %configuration[0])

        quitButton = ttk.Button(indexWindow, text="Cerrar", command=indexWindow.destroy)
        quitButton.grid(row=17, column=4)

    def showGraphics(self):
        graphicsWindow = Toplevel()
        graphicsWindow.geometry("800x800")
        graphicsWindow.title("Gráficas comparativas")
        fig = IndexCalculation.createGraphics()
        canvas3 = FigureCanvasTkAgg(fig, graphicsWindow)
        canvas3.get_tk_widget().pack()

    
if __name__ == '__main__':
    # Create the entire GUI program
    program = Interface()

    # Start the GUI event loop
    program.window.mainloop()