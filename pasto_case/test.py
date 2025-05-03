import math
import pandas as pd
ev = [2.99832091e+03, 3.02121388e+03, 3.08850598e+03, 3.06590783e+03, 3.08172861e+03, 3.08927837e+03, 3.10807928e+03, 3.14498168e+03, 3.08344271e+03, 3.16490426e+03, 3.09576613e+03, 3.09202088e+03, 3.02642948e+03, 2.92388280e+03, 2.91036992e+03, 2.78604988e+03, 2.63412577e+03, 2.50679974e+03, 2.38711837e+03, 2.21346197e+03, 2.08392897e+03, 1.90280058e+03, 1.72269239e+03, 1.51864277e+03, 1.27440209e+03, 1.14354513e+03, 9.59863737e+02, 7.88124680e+02, 4.81415167e+02, 3.06673172e+02, 1.76169562e+01 ]

phev = [0.00000000e+00, 3.97709763e-01, 6.15583304e+00, 5.03100067e+00, 3.71765862e+01, 3.47595005e+01, 4.72934788e+01, 3.08423068e+01, 1.22354370e+01, 4.33428532e+01, 2.16837742e+01, 2.75079139e+00, 3.24029013e+01, 1.36636732e+00, 1.66806199e+02, 1.25600095e+01, 3.85017798e+01, 1.46953807e+01, 8.38142688e+01, 8.03172595e+00, 2.00982499e+01 , 1.48505466e+02, 2.76977859e+01, 5.42556604e+01, 4.68289512e+00, 1.43444463e+02, 2.40917621e+01, 2.03848623e+01, 7.39347592e+01, 1.01987091e+02, 6.15358721e+00 ]

total = []
for i in range(len(ev)):
    total.append(math.ceil(ev[i])+math.ceil(phev[i]))

print(total)
print(sum(ev))
print(sum(phev))

df_vehicles = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/results_netherlands/ev_projections.csv')
scenario = 'Scenario 1'
scenario_selected_v = df_vehicles.loc[df_vehicles.loc[:, 'Scenario'] == scenario]
ev_min = list(scenario_selected_v["ICEV"])
ev_max = list(scenario_selected_v["Total"])
print('ev_min',  [0] * len(ev_max))
print('ev_max', ev_max)
phev_min = list(scenario_selected_v["PHEV"])
scenario = 'Scenario 3'
scenario_selected_v = df_vehicles.loc[df_vehicles.loc[:, 'Scenario'] == scenario]
phev_max = list(scenario_selected_v["PHEV"])
total_proj = list(scenario_selected_v["Total"])
