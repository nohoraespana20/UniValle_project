from cProfile import label


def getMeanData(serie, route, dataType):
    data_out = []
    for k in range(1,numberNorms+1):
        file = 'results%d\data_config%d_%d.json'%(serie,route, k)
        with open(file) as file:
            
                data = json.load(file)
        if dataType == 'FuelConsumption':
            data_out.append(sum(data[dataType])*0.264172/1E3)
        else:
            data_out.append(sum(data[dataType])/1E3)
    return data_out
        
def listDataperType(dataType):
    list1 = [getMeanData(1,1, dataType), getMeanData(1,2, dataType),
            getMeanData(1,3, dataType), getMeanData(1,4, dataType),
            getMeanData(1,5, dataType), getMeanData(1,6, dataType)]
    list2 = [getMeanData(2,1, dataType), getMeanData(2,2, dataType),
            getMeanData(2,3, dataType), getMeanData(2,4, dataType),
            getMeanData(2,5, dataType), getMeanData(2,6, dataType)]
    return [list1, list2]

def plotData(data1, data2, name_file):
    index1 = ['Euro2','Euro3','Euro4','Euro5','Euro6']
    list_df = []
    for i in range(numberRoutes):
        # df = pd.DataFrame({'Rush hour': data2[i], 'Peak off hour': data1[i]}, index=index1)  
        df = pd.DataFrame({'Hora pico': data2[i], 'Hora valle': data1[i]}, index=index1)  
        list_df.append(df)

    fig, axes = plt.subplots(1, numberRoutes)
    for k in range(numberRoutes):

        if name_file=='CO2':
                y = 3000
        elif name_file=='CO':
                y = 150
        elif name_file=='HC':
                y = 0.6
        elif name_file=='PMx':
                y = 0.6
        elif name_file=='NOx':
                y = 5.5
        elif name_file=='combustible':
                y = 0.5
        ax = list_df[k].plot(kind = 'bar', ax=axes[k], ylim=(0,y), fontsize=6, legend=False)
        ax.set_xlabel("Ruta %d"%k, fontsize=8)
        
        if name_file=='Combustible':
            plt.suptitle('Consumo de %s [gl]'%name_file)
            plt.legend(['Hora pico', 'Hora valle'])
            plt.savefig('figures/%s Consumption.png'%name_file, dpi=fig.dpi)
        else:
            plt.suptitle('Emisiones de %s [g]'%name_file)
            plt.legend(['Hora pico', 'Hora valle'])
            plt.savefig('figures/%s Emissions.png'%name_file, dpi=fig.dpi)


if __name__ == '__main__':
    import json
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    numberNorms = 5
    numberRoutes = 6
    
    dataType = ['CO2Emission', 'COEmission', 'HCEmission', 'PMxEmission', 'NOxEmission', 'FuelConsumption']
    
    CO2_mean = listDataperType(dataType[0])
    CO_mean = listDataperType(dataType[1])
    HC_mean = listDataperType(dataType[2])
    PMx_mean = listDataperType(dataType[3])
    NOx_mean = listDataperType(dataType[4])
    Fuel_mean = listDataperType(dataType[5])

    plotData(CO2_mean[0],  CO2_mean[1],  'CO2')
    plotData(CO_mean[0],   CO_mean[1],   'CO')
    plotData(HC_mean[0],   HC_mean[1],   'HC')
    plotData(PMx_mean[0],  PMx_mean[1],  'PMx')
    plotData(NOx_mean[0],  NOx_mean[1],  'NOx')
    plotData(Fuel_mean[0], Fuel_mean[1], 'combustible')