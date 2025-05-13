import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Y = ['M1', 'M2', 'M3', 'M4', 'M5', 'Sum']
# gas1 = np.array([0.064, 0.029, 0.051, 0.006, 0.001, 0.151])
# gas2 = np.array([0.017, 0.007, 0.192, 0.023, 0.001, 0.240])
# evl33 = np.array([0.036, 0.016, 0.009, 0.006, 0.098, 0.165])
# evl24 = np.array([0.027, 0.024, 0.028, 0.035, 0.039, 0.153])

# df = pd.DataFrame({'Caso 1 VGN': gas1, 'Caso 2 VGN': gas2, 'Caso 3 VE-L3': evl33, 'Caso 4 VE-L2': evl24}, index=Y)
# df.plot( kind = 'bar', width=0.7, rot=0, color=['#006cbe', '#00a0dc', '#00d0db', '#73fac9'], fontsize=7)

# plt.legend(fontsize=8)
# plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
# plt.show()

Y = ['M1', 'M2', 'M3', 'M4', 'M5','DPI','DNI','CC']
gas1 = np.array([0.06354770162368663,0.02850868589969544,0.05141466748286392,0.005921180415902573,0.0010135753981822897,0.012463956274442816,0.05904472542510241,0.8257000971320929])
gas2 = np.array([0.016979575737150344,0.007425125564513936,0.1924243572902395,0.022734305455943463,0.0010135753981822897,0.023220261506311977,0.1751216628563845,0.8829281223275296])
evl23 = np.array([0.034842582585852655,0.016358156444418098,0.009366410885919529,0.006032497491785243,0.0982891104325448,0.01673064872725892,0.09420951067758827,0.8491921336961057])
gas4 = np.array([0.025276546418037817,0.021910242443791677,0.07653814496408005,0.017472364250091882,0.005821664841475563,0.03786341686915735,0.07257974898297229,0.6571683129778081])

df = pd.DataFrame({'Caso 1 VGN': gas1, 'Caso 2 VGN': gas2, 'Caso 3 VE-L2': evl23, 'Caso 4 VGN': gas4}, index=Y)
df.plot( kind = 'bar', width=0.7, rot=0, color=['#006cbe', '#00a0dc', '#00d0db', '#73fac9'], fontsize=7)

plt.legend(fontsize=8)
plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
plt.show()