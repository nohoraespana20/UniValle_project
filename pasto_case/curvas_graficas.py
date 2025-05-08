import pandas as pd
import matplotlib.pyplot as plt

scale_pv = 10435
var = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/pv_norm_pasto.csv') * scale_pv
var_single_column = var.iloc[5:282, 0]
time_index = pd.date_range(start='2019-01-01 00:25:00', periods=len(var_single_column), freq='5min')
df_plot = pd.DataFrame({'generation_pv': var_single_column.values}, index=time_index)

plt.figure(figsize=(12, 6))
plt.plot(df_plot.index, df_plot['generation_pv'])
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=2))
plt.xlabel('Hora')
plt.ylabel('kW')
plt.title('Perfil de Generación PV')
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=0)
plt.savefig('C:/Users/noluc/OneDrive/Escritorio/Univalle/Avances2025/documento_final/generacionPV.jpg')

load = [ 0.56, 0.50, 0.49, 0.48, 0.53, 0.67, 0.71, 0.71, 0.76, 0.80, 0.82, 0.84,
         0.80, 0.79, 0.80, 0.79, 0.79, 0.96, 1.00, 0.95, 0.88, 0.78, 0.69, 0.63] 
for i in range(len(load)):
    load[i] = load[i]*100
time_index_load = pd.date_range(start='2019-01-01 00:00:00', periods=24, freq='H')
df_load = pd.DataFrame({'load': load}, index=time_index_load)
plt.figure(figsize=(12, 5))
plt.plot(df_load.index, df_load['load'])
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=2))
plt.title('Demanda eléctrica - Pasto')
plt.xlabel('Hora')
plt.ylabel('MW')
plt.grid(True)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('C:/Users/noluc/OneDrive/Escritorio/Univalle/Avances2025/documento_final/demandaPasto.jpg')
