import seaborn as sns
import pandas as pd
import numpy as np
from cmap import Color
import matplotlib.pyplot as plt

comparisonMatrix = {}
# #Caso 1
# comparisonMatrix['Availability Factor'] =   [1, 1/4, 1/5, 1/6, 1/7]
# comparisonMatrix['Driving Range'] =         [4, 1,   1/2, 1/3, 1/4]
# comparisonMatrix['Accumulated Cost'] =      [5, 2,   1,   1/2, 1/3]
# comparisonMatrix['Incentives'] =            [6, 3,   2,   1,   1/2]
# comparisonMatrix['Emissions'] =             [7, 4,   3,   2,   1]
# ahp_df = pd.DataFrame(comparisonMatrix, index=['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', 'Emissions'])
# sns.set(rc={"figure.figsize": (6, 3)})
# sns.set(font_scale=0.5) # font size 2
# sns.heatmap(ahp_df, cmap="YlGnBu")
# plt.show()
#Caso 2
# comparisonMatrix = {}
# comparisonMatrix['Availability Factor'] =[5, 2,   1,   1/2, 1/3]
# comparisonMatrix['Driving Range'] =      [6, 3,   2,   1,   1/2]
# comparisonMatrix['Accumulated Cost'] =   [1, 1/4, 1/5, 1/6, 1/7]
# comparisonMatrix['Incentives'] =         [4, 1,   1/2, 1/3, 1/4]
# comparisonMatrix['Emissions'] =          [7, 4,   3,   2,   1]
# ahp_df = pd.DataFrame(comparisonMatrix, index=['Accumulated Cost', 'Incentives', 'Availability Factor', 'Driving Range', 'Emissions'])
# sns.set(rc={"figure.figsize": (6, 3)})
# sns.set(font_scale=0.5) # font size 2
# sns.heatmap(ahp_df, cmap="YlGnBu")
# plt.show()
# # Caso 3
comparisonMatrix = {}
comparisonMatrix['Availability Factor'] =[4, 1,   1/2, 1/3, 1/4]
comparisonMatrix['Driving Range'] =      [5, 2,   1,   1/2, 1/3]
comparisonMatrix['Accumulated Cost'] =   [6, 3,   2,   1,   1/2]
comparisonMatrix['Incentives'] =         [7, 4,   3,   2,   1]
comparisonMatrix['Emissions'] =          [1, 1/4, 1/5, 1/6, 1/7]
ahp_df = pd.DataFrame(comparisonMatrix, index=['Emissions', 'Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives'])
sns.set(rc={"figure.figsize": (6, 3)})
sns.set(font_scale=0.5) # font size 2
sns.heatmap(ahp_df, cmap="YlGnBu")
plt.show()
# # Caso 4
# comparisonMatrix = {}
# comparisonMatrix['Availability Factor'] =   [1, 1, 1, 1, 1]
# comparisonMatrix['Driving Range'] =         [1, 1, 1, 1, 1]
# comparisonMatrix['Accumulated Cost'] =      [1, 1, 1, 1, 1]
# comparisonMatrix['Incentives'] =            [1, 1, 1, 1, 1]
# comparisonMatrix['Emissions'] =             [1, 1, 1, 1, 1]
# ahp_df = pd.DataFrame(comparisonMatrix, index=['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', 'Emissions'])
# sns.set(rc={"figure.figsize": (6, 3)})
# sns.set(font_scale=0.5) # font size 2
# sns.heatmap(ahp_df, cmap="YlGnBu")
# plt.show()

