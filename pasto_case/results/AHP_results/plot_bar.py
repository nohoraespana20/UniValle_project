import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Y = ['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', ' Emissions', 'Sum']
gas1 = np.array([0.063, 0.025, 0.047, 0.006, 0.000, 0.141])
gas2 = np.array([0.017, 0.007, 0.174, 0.021, 0.000, 0.219])
phev3 = np.array([0.036, 0.020, 0.004, 0.005, 0.102, 0.167])
ev4 = np.array([0.027, 0.021, 0.028, 0.033, 0.026, 0.135])

df = pd.DataFrame({'Case 1 NGV': gas1, 'Case 2 NGV': gas2, 'Case 3 PHEV-L3': phev3, 'Case 4 EV-L3': ev4}, index=Y)
df.plot( kind = 'bar', width=0.85, rot=0, color=['#620062', '#d54855', '#ffbc4f', '#00b6d6'], fontsize=7)

plt.legend(fontsize=8)
plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
plt.show()

# Y = ['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', ' Emissions', 'Closeness Coefficient']
# gas1 = np.array([0.063, 0.028, 0.059, 0.003, 0.001, 0.810])
# gas2 = np.array([0.017, 0.007, 0.220, 0.013, 0.001, 0.843])
# phev3 = np.array([0.036, 0.018, 0.004, 0.004, 0.091, 0.779])
# gas4 = np.array([0.025, 0.021, 0.088, 0.010, 0.004, 0.652])
# df = pd.DataFrame({'Case 1 NGV': gas1, 'Case 2 NGV': gas2, 'Case 3 PHEV': phev3, 'Case 4 NGV': gas4}, index=Y)
# df.plot( kind = 'bar', rot=0, color=['#620062', '#d54855', '#ffbc4f', '#00b6d6'], fontsize=6)

# plt.legend(fontsize=6)
# plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
# plt.show()