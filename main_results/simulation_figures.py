def getMeanData(serie, route, dataType):
    data_out = []
    for k in range(1,numberNorms+1):
        file = 'results%d\data_config%d_%d.json'%(serie,route, k)
        with open(file) as file:
                data = json.load(file)
        if dataType == 'FuelConsumption':
            data_out.append((sum(data[dataType]))/(3785))
        elif dataType == 'NoiseEmission':
            data_out.append((sum(data[dataType]))/data['Step'])
        else:
        #     data_out.append((sum(data[dataType])*data['Step'])/1E3/(data['Distance']/1000))
                data_out.append((sum(data[dataType]))/1E3)
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
        df = pd.DataFrame({'Rush hour': data2[i], 'Peak off hour': data1[i]}, index=index1)  
        # df = pd.DataFrame({'Hora pico': data2[i], 'Hora valle': data1[i]}, index=index1)  
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
        elif name_file=='Fuel':
                y = 0.5
        ax = list_df[k].plot(kind = 'bar', ax=axes[k],  fontsize=6, legend=False)
        ax.set_xlabel("Road %d"%(k+1), fontsize=8)
        
        if name_file=='Fuel':
            plt.suptitle('%s Consumption [gl]'%name_file)
            plt.legend(['Rush hour', 'Peak off hour'])
            plt.savefig('figures/%s Consumption.png'%name_file, dpi=fig.dpi, transparent=True)
        elif name_file=='Noise':
            plt.suptitle('%s Emissions [dBA]'%name_file)
            plt.legend(['Rush hour', 'Peak off hour'])
            plt.savefig('figures/%s Emissions.png'%name_file, dpi=fig.dpi, transparent=True)
        else:
            plt.suptitle('%s Emissions [g]'%name_file)
            plt.legend(['Rush hour', 'Peak off hour'])
            plt.savefig('figures/%s Emissions.png'%name_file, dpi=fig.dpi, transparent=True)


if __name__ == '__main__':
    import json
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    numberNorms = 5
    numberRoutes = 6
    
    dataType = ['CO2Emission', 'COEmission', 'HCEmission', 'PMxEmission', 'NOxEmission', 'NoiseEmission', 'FuelConsumption']
    
    CO2_mean = listDataperType(dataType[0])
    with open('figures/CO2_mean.json', 'w') as file:
            json.dump(CO2_mean, file, indent=4)
    CO_mean = listDataperType(dataType[1])
    with open('figures/CO_mean.json', 'w') as file:
            json.dump(CO_mean, file, indent=4)
    HC_mean = listDataperType(dataType[2])
    with open('figures/HC_mean.json', 'w') as file:
            json.dump(HC_mean, file, indent=4)
    PMx_mean = listDataperType(dataType[3])
    with open('figures/PMx_mean.json', 'w') as file:
            json.dump(PMx_mean, file, indent=4)
    NOx_mean = listDataperType(dataType[4])
    with open('figures/ENOx_mean.json', 'w') as file:
            json.dump(NOx_mean, file, indent=4)
    Noise_mean = listDataperType(dataType[5])
    with open('figures/Noise_mean.json', 'w') as file:
            json.dump(Noise_mean, file, indent=5)
    Fuel_mean = listDataperType(dataType[6])
    with open('figures/Fuel_mean.json', 'w') as file:
            json.dump(Fuel_mean, file, indent=6)

    plotData(CO2_mean[0],  CO2_mean[1],  'CO2')
    plotData(CO_mean[0],   CO_mean[1],   'CO')
    plotData(HC_mean[0],   HC_mean[1],   'HC')
    plotData(PMx_mean[0],  PMx_mean[1],  'PMx')
    plotData(NOx_mean[0],  NOx_mean[1],  'NOx')
    plotData(Noise_mean[0],  Noise_mean[1],  'Noise')
    plotData(Fuel_mean[0], Fuel_mean[1], 'Fuel')