import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Y = ['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', ' Emissions', 'Sum']
gas1 = np.array([0.063, 0.028, 0.059, 0.010, 0.001, 0.161])
gas2 = np.array([0.017, 0.007, 0.219, 0.051, 0.003, 0.297])
ev3 = np.array([0.036, 0.016, 0.008, 0.008, 0.073, 0.141])
gas4 = np.array([0.025, 0.021, 0.087, 0.039, 0.015, 0.187])

df = pd.DataFrame({'Case 1 NGV': gas1, 'Case 2 NGV': gas2, 'Case 3 EV-L3': ev3, 'Case 4 NGV': gas4}, index=Y)
df.plot( kind = 'bar', rot=0, color=['#620062', '#d54855', '#ffbc4f', '#00b6d6'], fontsize=6)

plt.legend(fontsize=6)
plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
plt.show()

Y = ['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', ' Emissions', 'Closeness Coefficient']
gas1 = np.array([0.063, 0.028, 0.059, 0.003, 0.001, 0.810])
gas2 = np.array([0.017, 0.007, 0.220, 0.013, 0.001, 0.843])
phev3 = np.array([0.036, 0.018, 0.004, 0.004, 0.091, 0.779])
gas4 = np.array([0.025, 0.021, 0.088, 0.010, 0.004, 0.652])
df = pd.DataFrame({'Case 1 NGV': gas1, 'Case 2 NGV': gas2, 'Case 3 PHEV': phev3, 'Case 4 NGV': gas4}, index=Y)
df.plot( kind = 'bar', rot=0, color=['#620062', '#d54855', '#ffbc4f', '#00b6d6'], fontsize=6)

plt.legend(fontsize=6)
plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
plt.show()