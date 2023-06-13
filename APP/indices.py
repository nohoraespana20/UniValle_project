import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

################ técnicos

Y = ['Ef', 'E_100km', 'FD']

s1 = [3.333, 135.0, 95.6]
s2 = [8.0, 8.0, 96.8]

fig = Figure(figsize=(11,9))
a1 = fig.add_subplot(121)
df = pd.DataFrame({'Taxi convencional': s1, 'Taxi eléctrico': s2}, index=Y)
df.plot(ax=a1, kind = 'bar')
        
a1.set_title('Comparación de índices - Taxi', fontsize=8)
a1.legend(['Taxi convencional', 'Taxi eléctrico'], fontsize=6)
a1.set_ylabel('Valor', fontsize=8)
a1.set_xlabel('Índice', fontsize=8)


s1 = [40.462, 40.462*10.7*3.785, 95.6] # BUS Convencional
s2 = [20.231, 20.231, 96.8] # BUS Eléctrico

a2 = fig.add_subplot(122)
df = pd.DataFrame({'Bus convencional': s1, 'Bus eléctrico': s2}, index=Y)
df.plot(ax=a2, kind = 'bar')
        
a2.set_title('Comparación de índices - Bus', fontsize=8)
a2.legend(['Bus convencional', 'Bus eléctrico'], fontsize=6)
a2.set_ylabel('Valor', fontsize=8)
a2.set_xlabel('Índice', fontsize=8)

fig.savefig('indiceTec', transparent=True)

################ ambientales 1

Y = ['Pco2 EVco2']

s1 = [297.41]
s2 = [3.2]

fig = Figure(figsize=(11,11))
a1 = fig.add_subplot(121)
df = pd.DataFrame({'Taxi convencional': s1, 'Taxi eléctrico': s2}, index=Y)
df.plot(ax=a1, kind = 'bar')
        
a1.set_title('Comparación de índices - Taxi', fontsize=8)
a1.legend(['Taxi convencional', 'Taxi eléctrico'], fontsize=6)
a1.set_ylabel('Valor', fontsize=8)
a1.set_xlabel('Índice', fontsize=8)


s1 = [1266.79] # BUS Convencional
s2 = [30.745] # BUS Eléctrico

a2 = fig.add_subplot(122)
df = pd.DataFrame({'Bus convencional': s1, 'Bus eléctrico': s2}, index=Y)
df.plot(ax=a2, kind = 'bar')
        
a2.set_title('Comparación de índices - Bus', fontsize=8)
a2.legend(['Bus convencional', 'Bus eléctrico'], fontsize=6)
a2.set_ylabel('Valor', fontsize=8)
a2.set_xlabel('Índice', fontsize=8)

fig.savefig('indiceAmb1', transparent=True)

#################### ambientales 2

Y = ['E_CO', 'E_HC', 'E_PMx', 'E_NOx']

s1 = [9.43, 0.04, 0.02, 13.01]
s2 = [6.14, 0.53, 0.79, 14.81]

fig = Figure(figsize=(11,9))
a1 = fig.add_subplot(111)
df = pd.DataFrame({'Taxi convencional': s1, 'Bus convencional': s2}, index=Y)
df.plot(ax=a1, kind = 'bar')
        
a1.set_title('Comparación de índices', fontsize=8)
a1.legend(['Taxi convencional', 'Bus convencional'], fontsize=6)
a1.set_ylabel('Valor', fontsize=8)
a1.set_xlabel('Índice', fontsize=8)

fig.savefig('indiceAmb2', transparent=True)

################ Económicos

Y = ['ICR', 'Cs']

s1 = [330.533,297.41*995000/1e6]
s2 = [60.48, 13.2*995000/1e6]

fig = Figure(figsize=(11,9))
a1 = fig.add_subplot(121)
df = pd.DataFrame({'Taxi convencional': s1, 'Taxi eléctrico': s2}, index=Y)
df.plot(ax=a1, kind = 'bar')
        
a1.set_title('Comparación de índices - Taxi', fontsize=8)
a1.legend(['Taxi convencional', 'Taxi eléctrico'], fontsize=6)
a1.set_ylabel('Valor', fontsize=8)
a1.set_xlabel('Índice', fontsize=8)


s1 = [3397.225, 1266.79*995000/1e6] # BUS Convencional
s2 = [152.908, 30.745*995000/1e6] # BUS Eléctrico

a2 = fig.add_subplot(122)
df = pd.DataFrame({'Bus convencional': s1, 'Bus eléctrico': s2}, index=Y)
df.plot(ax=a2, kind = 'bar')
        
a2.set_title('Comparación de índices - Bus', fontsize=8)
a2.legend(['Bus convencional', 'Bus eléctrico'], fontsize=6)
a2.set_ylabel('Valor', fontsize=8)
a2.set_xlabel('Índice', fontsize=8)

fig.savefig('indiceEcon', transparent=True)