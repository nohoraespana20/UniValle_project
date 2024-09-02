import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# data = pd.DataFrame(index=pd.date_range(start='2019-01-01 00:00', end='2019-01-01 23:00', freq='5min'))
# var = pd.read_csv('pv_norm_pasto.csv') * 4686
# data.loc[data.index[8:19], 'generation_pv'] = var

data = pd.DataFrame(index=pd.date_range(start='2019-01-01 00:00', end='2019-01-01 23:50', freq='5min'))

var = pd.read_csv('pv_norm_pasto.csv') * 4686
var_single_column = var.iloc[:, 0]

data['generation_pv'] = var_single_column.values

# print(f"Length of data index: {len(data.index)}")
# print(f"Length of var_single_column: {len(var_single_column)}")

# # Ajustar el índice de var_single_column para que coincida con el índice de data
# if len(data.index) == len(var_single_column):
#     data['generation_pv'] = var_single_column.values
# else:
#     print("Lengths do not match. Please verify the data.")

# # Imprimir los datos para verificar
# print(data.head())
# print(data['generation_pv'].head())

print(var_single_column)
print(data['generation_pv'])
plt.plot(data['generation_pv'] )
plt.show()