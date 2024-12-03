import seaborn as sns
import pandas as pd
import numpy as np
from cmap import Color
import matplotlib.pyplot as plt

#Caso 1
comparisonMatrix = {}
comparisonMatrix['Availability Factor'] =   [1, 1/3, 1/5, 1/7, 1/9]
comparisonMatrix['Driving Range'] =         [3, 1,   1/3, 1/5, 1/7]
comparisonMatrix['Accumulated Cost'] =      [5, 3,   1,   1/3, 1/5]
comparisonMatrix['Incentives'] =            [7, 5,   3,   1,   1/3]
comparisonMatrix['Emissions'] =             [9, 7,   5,   3,   1]
ahp_df = pd.DataFrame(comparisonMatrix, index=['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', 'Emissions'])
sns.set(rc={"figure.figsize": (6, 5)})
sns.set(font_scale=0.5) # font size 2
sns.heatmap(ahp_df, cmap="YlGnBu")
plt.show()

#Caso 2
comparisonMatrix = {}
comparisonMatrix['Availability Factor'] =[1, 1/3, 5, 3, 1/5]
comparisonMatrix['Driving Range'] =      [3, 1, 7, 5, 1/3]
comparisonMatrix['Accumulated Cost'] =   [1/5, 1/7, 1, 1/3, 1/9] 
comparisonMatrix['Incentives'] =         [1/3, 1/5, 3, 1, 1/7]
comparisonMatrix['Emissions'] =          [5, 3, 9, 7, 1]
ahp_df = pd.DataFrame(comparisonMatrix, index=['Accumulated Cost', 'Incentives', 'Availability Factor', 'Driving Range', 'Emissions'])
sns.set(rc={"figure.figsize": (6, 5)})
sns.set(font_scale=0.5) # font size 2
sns.heatmap(ahp_df, cmap="YlGnBu")
plt.show()

# Caso 3
comparisonMatrix = {}
comparisonMatrix['Availability Factor'] =[1, 1/3, 1/5, 1/7, 3]
comparisonMatrix['Driving Range'] =      [3, 1, 1/3, 1/5, 5]
comparisonMatrix['Accumulated Cost'] =   [5, 3, 1, 1/3, 7]
comparisonMatrix['Incentives'] =         [7, 5, 3, 1, 9]
comparisonMatrix['Emissions'] =          [1/3, 1/5, 1/7, 1/9, 1]
ahp_df = pd.DataFrame(comparisonMatrix, index=['Emissions', 'Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives'])
sns.set(rc={"figure.figsize": (6, 5)})
sns.set(font_scale=0.5) # font size 2
sns.heatmap(ahp_df, cmap="YlGnBu")
plt.show()

# Caso 4
comparisonMatrix = {}
comparisonMatrix['Availability Factor'] =   [1, 1, 1, 1, 1]
comparisonMatrix['Driving Range'] =         [1, 1, 1, 1, 1]
comparisonMatrix['Accumulated Cost'] =      [1, 1, 1, 1, 1]
comparisonMatrix['Incentives'] =            [1, 1, 1, 1, 1]
comparisonMatrix['Emissions'] =             [1, 1, 1, 1, 1]
ahp_df = pd.DataFrame(comparisonMatrix, index=['Availability Factor', 'Driving Range', 'Accumulated Cost', 'Incentives', 'Emissions'])
sns.set(rc={"figure.figsize": (6, 5)})
sns.set(font_scale=0.5) # font size 2
sns.heatmap(ahp_df, cmap="YlGnBu")
plt.show()

