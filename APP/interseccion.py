import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import json

class punto:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def __str__(self):
    return "("+str(self.x)+","+str(self.y)+")"

class linea:
  def __init__(self, p0, p1):
    self.p0 = p0
    self.p1 = p1
    self.A = p1.x - p0.x
    self.B = p1.y - p0.y
    self.C = p1.x*p0.y - p0.x*p1.y
  def intersecta(self, otro):
    det = self.A*otro.B - otro.A*self.B
    x = otro.A*self.C-self.A*otro.C
    y = otro.B*self.C-self.B*otro.C
    return punto(x/det,y/det)
   
  def __str__(self):
    return str(self.p0) + "," + str(self.p1)
   
  
with open('data_files/intersection_E1EV.json', "r") as file:
  data_E1 = json.load(file)
with open('data_files/intersection_E2EV.json', "r") as file:
  data_E2 = json.load(file)
with open('data_files/intersection_E3EV.json', "r") as file:
  data_E3 = json.load(file)
with open('data_files/intersection_E4EV.json', "r") as file:
  data_E4 = json.load(file)

if __name__=="__main__":
  L1 =linea(punto(data_E1['40000.0']['combustion'][0],data_E1['40000.0']['combustion'][1]),punto(data_E1['40000.0']['combustion'][2],data_E1['40000.0']['combustion'][3]))
  L2 =linea(punto(data_E1['40000.0']['electric'][0],data_E1['40000.0']['electric'][1]),punto(data_E1['40000.0']['electric'][2],data_E1['40000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('\nS1_1 = ', P)

  L1 =linea(punto(data_E1['60000.0']['combustion'][0],data_E1['60000.0']['combustion'][1]),punto(data_E1['60000.0']['combustion'][2],data_E1['60000.0']['combustion'][3]))
  L2 =linea(punto(data_E1['60000.0']['electric'][0],data_E1['60000.0']['electric'][1]),punto(data_E1['60000.0']['electric'][2],data_E1['60000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S1_2 = ', P)

  L1 =linea(punto(data_E1['80000.0']['combustion'][0],data_E1['80000.0']['combustion'][1]),punto(data_E1['80000.0']['combustion'][2],data_E1['80000.0']['combustion'][3]))
  L2 =linea(punto(data_E1['80000.0']['electric'][0],data_E1['80000.0']['electric'][1]),punto(data_E1['80000.0']['electric'][2],data_E1['80000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S1_3 = ', P)

  L1 =linea(punto(data_E1['100000.0']['combustion'][0],data_E1['100000.0']['combustion'][1]),punto(data_E1['100000.0']['combustion'][2],data_E1['100000.0']['combustion'][3]))
  L2 =linea(punto(data_E1['100000.0']['electric'][0],data_E1['100000.0']['electric'][1]),punto(data_E1['100000.0']['electric'][2],data_E1['100000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S1_4 = ', P)

  ###################################
  L1 =linea(punto(data_E2['40000.0']['combustion'][0],data_E2['40000.0']['combustion'][1]),punto(data_E2['40000.0']['combustion'][2],data_E2['40000.0']['combustion'][3]))
  L2 =linea(punto(data_E2['40000.0']['electric'][0],data_E2['40000.0']['electric'][1]),punto(data_E2['40000.0']['electric'][2],data_E2['40000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('\nS2_1 = ', P)

  L1 =linea(punto(data_E2['60000.0']['combustion'][0],data_E2['60000.0']['combustion'][1]),punto(data_E2['60000.0']['combustion'][2],data_E2['60000.0']['combustion'][3]))
  L2 =linea(punto(data_E2['60000.0']['electric'][0],data_E2['60000.0']['electric'][1]),punto(data_E2['60000.0']['electric'][2],data_E2['60000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S2_2 = ', P)

  L1 =linea(punto(data_E2['80000.0']['combustion'][0],data_E2['80000.0']['combustion'][1]),punto(data_E2['80000.0']['combustion'][2],data_E2['80000.0']['combustion'][3]))
  L2 =linea(punto(data_E2['80000.0']['electric'][0],data_E2['80000.0']['electric'][1]),punto(data_E2['80000.0']['electric'][2],data_E2['80000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S2_3 = ', P)

  L1 =linea(punto(data_E2['100000.0']['combustion'][0],data_E2['100000.0']['combustion'][1]),punto(data_E2['100000.0']['combustion'][2],data_E2['100000.0']['combustion'][3]))
  L2 =linea(punto(data_E2['100000.0']['electric'][0],data_E2['100000.0']['electric'][1]),punto(data_E2['100000.0']['electric'][2],data_E2['100000.0']['electric'][3])) 
  P = L1.intersecta(L2)
  print ('S2_4 = ', P)
  
  ###################################
  L1 =linea(punto(data_E3['40000.0']['combustion'][0],data_E3['40000.0']['combustion'][1]),punto(data_E3['40000.0']['combustion'][2],data_E3['40000.0']['combustion'][3]))
  L2 =linea(punto(data_E3['40000.0']['electric'][0],data_E3['40000.0']['electric'][1]),punto(data_E3['40000.0']['electric'][2],data_E3['40000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('\nS3_1 = ', P)

  L1 =linea(punto(data_E3['60000.0']['combustion'][0],data_E3['60000.0']['combustion'][1]),punto(data_E3['60000.0']['combustion'][2],data_E3['60000.0']['combustion'][3]))
  L2 =linea(punto(data_E3['60000.0']['electric'][0],data_E3['60000.0']['electric'][1]),punto(data_E3['60000.0']['electric'][2],data_E3['60000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S3_2 = ', P)

  L1 =linea(punto(data_E3['80000.0']['combustion'][0],data_E3['80000.0']['combustion'][1]),punto(data_E3['80000.0']['combustion'][2],data_E3['80000.0']['combustion'][3]))
  L2 =linea(punto(data_E3['80000.0']['electric'][0],data_E3['80000.0']['electric'][1]),punto(data_E3['80000.0']['electric'][2],data_E3['80000.0']['electric'][3])) 
  P = L1.intersecta(L2)
  print ('S3_3 = ', P)

  L1 =linea(punto(data_E3['100000.0']['combustion'][0],data_E3['100000.0']['combustion'][1]),punto(data_E3['100000.0']['combustion'][2],data_E3['100000.0']['combustion'][3]))
  L2 =linea(punto(data_E3['100000.0']['electric'][0],data_E3['100000.0']['electric'][1]),punto(data_E3['100000.0']['electric'][2],data_E3['100000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S3_4 = ', P)

  ###################################
  L1 =linea(punto(data_E4['40000.0']['combustion'][0],data_E4['40000.0']['combustion'][1]),punto(data_E4['40000.0']['combustion'][2],data_E4['40000.0']['combustion'][3]))
  L2 =linea(punto(data_E4['40000.0']['electric'][0],data_E4['40000.0']['electric'][1]),punto(data_E4['40000.0']['electric'][2],data_E4['40000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('\nS4_1 = ', P)

  L1 =linea(punto(data_E4['60000.0']['combustion'][0],data_E4['60000.0']['combustion'][1]),punto(data_E4['60000.0']['combustion'][2],data_E4['60000.0']['combustion'][3]))
  L2 =linea(punto(data_E4['60000.0']['electric'][0],data_E4['60000.0']['electric'][1]),punto(data_E4['60000.0']['electric'][2],data_E4['60000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S4_2 = ', P)

  L1 =linea(punto(data_E4['80000.0']['combustion'][0],data_E4['80000.0']['combustion'][1]),punto(data_E4['80000.0']['combustion'][2],data_E4['80000.0']['combustion'][3]))
  L2 =linea(punto(data_E4['80000.0']['electric'][0],data_E4['80000.0']['electric'][1]),punto(data_E4['80000.0']['electric'][2],data_E4['80000.0']['electric'][3]))  
  P = L1.intersecta(L2)
  print ('S4_3 = ', P)

  L1 =linea(punto(data_E4['100000.0']['combustion'][0],data_E4['100000.0']['combustion'][1]),punto(data_E4['100000.0']['combustion'][2],data_E4['100000.0']['combustion'][3]))
  L2 =linea(punto(data_E4['100000.0']['electric'][0],data_E4['100000.0']['electric'][1]),punto(data_E4['100000.0']['electric'][2],data_E4['100000.0']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S4_4 = ', P)

S1_1 =  (1.9136053629810619,816.5143365817303)
S1_2 =  (1.468032154489715,891.755643905392)
S1_3 =  (1.2100560398956597,948.7167273349469)
S1_4 =  (1.0418057385364339,996.9345625566502)

S2_1 =  (1.9199528802383405,818.6177612343305)
S2_2 =  (1.4715459314321249,893.4678879758137)
S2_3 =  (1.2123092455205489,950.1660148767421)
S2_4 =  (1.0433867166827233,998.1979669797946)

S3_1 =  (0,0)
S3_2 =  (0,0)
S3_3 =  (0,0)
S3_4 =  (0,0)

S4_1 =  (0,0)
S4_2 =  (0,0)
S4_3 =  (0,0)
S4_4 =  (0,0)

km = [40000, 60000, 80000, 100000]
year1 = [S1_1[0], S1_2[0], S1_3[0], S1_4[0]]
year2 = [S2_1[0], S2_2[0], S2_3[0], S2_4[0]]
year3 = [S3_1[0], S3_2[0], S3_3[0], S3_4[0]]
year4 = [S4_1[0], S4_2[0], S4_3[0], S4_4[0]]

Y = [str(x) for x in km]
s1 = year1
s2 = year2
s3 = year3
s4 = year4

fig = Figure(figsize=(10,7))
a1 = fig.add_subplot(121)
df = pd.DataFrame({'Escenario 1': s1, 'Escenario 2': s2, 'Escenario 3': s3, 'Escenario 4': s4}, index=Y)
df.plot(ax=a1, kind = 'bar')
        
a1.set_title('Análisis sensibilidad - Año de cruce', fontsize=8)
a1.legend(['Escenario 1', 'Escenario 2', 'Escenario 3', 'Escenario 4'], fontsize=6)
a1.set_ylabel('Año de cruce', fontsize=8)
a1.set_xlabel('km/año', fontsize=8)


km = [40000, 60000, 80000, 100000]
year1 = [S1_1[1], S1_2[1], S1_3[1], S1_4[1]]
year2 = [S2_1[1], S2_2[1], S2_3[1], S2_4[1]]
year3 = [S3_1[1], S3_2[1], S3_3[1], S3_4[1]]
year4 = [S4_1[1], S4_2[1], S4_3[1], S4_4[1]]

s1 = year1
s2 = year2
s3 = year3
s4 = year4

a2 = fig.add_subplot(122)
df = pd.DataFrame({'Escenario 1': s1, 'Escenario 2': s2, 'Escenario 3': s3, 'Escenario 4': s4}, index=Y)
df.plot(ax=a2, kind = 'bar')
        
a2.set_title('Análisis sensibilidad - Costo de cruce', fontsize=8)
a2.legend(['Escenario 1', 'Escenario 2', 'Escenario 3', 'Escenario 4'], fontsize=6)
a2.set_ylabel('Costo de cruce', fontsize=8)
a2.set_xlabel('km/año', fontsize=8)

fig.savefig('images/cruce', transparent=True)