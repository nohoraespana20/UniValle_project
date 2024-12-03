import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Y = ['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', ' Emissions', 'Sum']
gas1 = np.array([0.064, 0.027, 0.061, 0.010, 0.002, 0.164])
gas2 = np.array([0.0170, 0.007, 0.219, 0.051, 0.003, 0.297])
ev3 = np.array([0.036, 0.016, 0.008, 0.008, 0.073, 0.141])
gas4 = np.array([0.025, 0.021, 0.087, 0.039, 0.015, 0.187])

df = pd.DataFrame({'Case 1 NGV': gas1, 'Case 2 NGV': gas2, 'Case 3 EV-L3': ev3, 'Case 4 NGV': gas4}, index=Y)
df.plot( kind = 'bar', rot=0, color=['#620062', '#d54855', '#ffbc4f', '#00b6d6'], fontsize=6)

# plt.ylabel("Millones COP]")
# plt.title("Costo anual Gasolina, Eléctrico, Hídbrido, Gas")

plt.legend(fontsize=6)
plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
plt.show()