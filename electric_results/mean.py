import json

# file = 'figures\Fuel_mean.json'
# with open(file) as file:
#     fuelConsumption = json.load(file)
# meanFuel = []
# for i in range(2):
#     for j in range(6):
#         meanFuel.append(sum(fuelConsumption[i][j])/len(fuelConsumption[i][j])*3.785) 
# print('Mean fuel = ', meanFuel)

file = 'figures\PMx_mean.json'
with open(file) as file:
    fuelConsumption = json.load(file)
meanFuel = []
for i in range(2):
    for j in range(6):
        meanFuel.append(sum(fuelConsumption[i][j])/len(fuelConsumption[i][j])) 
print('Mean HC = ', meanFuel)