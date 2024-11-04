import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Y = ['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', ' Emissions', 'Sum']
gas1 = np.array([0.068, 0.021, 0.056, 0.016, 0.004, 0.165])
gas2 = np.array([0.234, 0.039, 0.016, 0.008, 0.004, 0.301])
ev3 = np.array([0.077, 0.028, 0.016, 0.009, 0.01, 0.140])
gas4 = np.array([0.025, 0.021, 0.087, 0.039, 0.015, 0.187])

df = pd.DataFrame({'1 NGV': gas1, '2 NGV': gas2, '3 EV-L3': ev3, '4 NGV': gas4}, index=Y)
df.plot( kind = 'bar', rot=0, color=['#620062', '#d54855', '#ffbc4f', '#00b6d6'], fontsize=6)

# plt.ylabel("Millones COP]")
# plt.title("Costo anual Gasolina, Eléctrico, Hídbrido, Gas")

plt.legend(fontsize=6)
plt.show()