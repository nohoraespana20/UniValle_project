#https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/export/?disjunctive.cou_name_en&sort=name&refine.timezone=America&location=4,7.01367,-67.63184&basemap=jawg.light

import pandas as pd


df = pd.read_csv('C:/Nohora/UniValle_project/pasto_case/auxiliary_files/cities_america.csv', delimiter=';', low_memory=False)

columns_to_drop = ['Geoname ID', 'Name', 'Alternate Names', 'Feature Class', 'Feature Code', 'Elevation', 
                   'DIgital Elevation Model', 'Timezone', 'Modification date', 'Coordinates', 'Country Code', 
                   'Country name EN', 'Country Code 2', 'Admin1 Code', 'Admin2 Code', 'Admin3 Code', 'Admin4 Code']
df.drop(columns=columns_to_drop, inplace=True, errors='ignore')  

countries_to_remove = ['Anguilla', 'British Virgin Islands', 'Canada', 'Greenland', 'Montserrat', 
                        'Saint Pierre and Miquelon', 'United States']

df = df[~df['LABEL EN'].isin(countries_to_remove)] 
df = df.sort_values(by='Population', ascending=True) 

df.loc[(df['Population'] <50000), 'Classification'] = 'Small City'
df.loc[(df['Population'] >= 50000) & (df['Population'] <= 1000000), 'Classification'] = 'Medium City'
df.loc[(df['Population'] > 1000000), 'Classification'] = 'Big City'

# df.to_csv('C:/Nohora/UniValle_project/pasto_case/auxiliary_files/cities_LA.csv', index=False, sep=';')
print(df['ASCII Name'] == 'Toluca')
# total_population = df['Population'].sum()
# small_city_population = df[df['Classification'] == 'Small City']['Population'].sum()
# medium_city_population = df[df['Classification'] == 'Medium City']['Population'].sum()
# big_city_population = df[df['Classification'] == 'Big City']['Population'].sum()
# percentage_small = (small_city_population / total_population) * 100
# percentage_medium = (medium_city_population / total_population) * 100
# percentage_big = (big_city_population / total_population) * 100
# print(f"Población total: {total_population}")
# print(f"Población de Medium City: {medium_city_population}")
# print(f"Porcentaje de Small City respecto al total: {percentage_small:.2f}%")
# print(f"Porcentaje de Medium City respecto al total: {percentage_medium:.2f}%")
# print(f"Porcentaje de Big City respecto al total: {percentage_big:.2f}%")

# df_colombia = df[df['LABEL EN'] == 'Colombia'].copy()
# df_colombia.to_csv('C:/Nohora/UniValle_project/pasto_case/auxiliary_files/cities_Colombia.csv', index=False, sep=';')


# total_population = df_colombia['Population'].sum()
# small_city_population = df_colombia[df_colombia['Classification'] == 'Small City']['Population'].sum()
# medium_city_population = df_colombia[df_colombia['Classification'] == 'Medium City']['Population'].sum()
# big_city_population = df_colombia[df_colombia['Classification'] == 'Big City']['Population'].sum()
# percentage_small = (small_city_population / total_population) * 100
# percentage_medium = (medium_city_population / total_population) * 100
# percentage_big = (big_city_population / total_population) * 100
# print('\nCOLOMBIA')
# print(f"Población total: {total_population}")
# print(f"Población de Medium City: {medium_city_population}")
# print(f"Porcentaje de Small City respecto al total: {percentage_small:.2f}%")
# print(f"Porcentaje de Medium City respecto al total: {percentage_medium:.2f}%")
# print(f"Porcentaje de Big City respecto al total: {percentage_big:.2f}%")

# medium_city_count = df_colombia[df_colombia['Classification'] == 'Medium City'].shape[0]
# print(f"Cantidad de ciudades 'Medium City' en Colombia: {medium_city_count}")

# # medium_cities_list = df_colombia[df_colombia['Classification'] == 'Medium City']['ASCII Name'].tolist()
# # print("Ciudades Medium City en Colombia:")
# # for city in medium_cities_list:
# #     print(city)

# cities_population_range = df[(df['Population'] >= 300000) & (df['Population'] <= 500000)]['ASCII Name'].tolist()
# print("Ciudades con población entre 300,000 y 400,000:")
# for city in cities_population_range:
#     print(city)