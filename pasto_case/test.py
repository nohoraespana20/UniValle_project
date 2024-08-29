import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame(index=pd.date_range(start='2019-01-01 00:00', end='2019-01-01 23:00', freq='5min'))

# data['generation_pv'] = 0
# data['generation_pv'] = data['generation_pv'].astype(float)
var = pd.read_csv('pv_norm_pasto.csv') * 4686
print(var[1])
data.loc[data.index[8:19], 'generation_pv'] = [float(np.sin(i/(10/(np.pi)))) for i in range(11)]



print((var))
plt.plot(var)
plt.show()