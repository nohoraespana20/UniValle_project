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
   
  
with open('data_files/intersection_EV1_USD.json', "r") as file:
  data_E1 = json.load(file)
with open('data_files/intersection_EV2_USD.json', "r") as file:
  data_E2 = json.load(file)
with open('data_files/intersection_EV3_USD.json', "r") as file:
  data_E3 = json.load(file)
with open('data_files/intersection_EV4_USD.json', "r") as file:
  data_E4 = json.load(file)

if __name__=="__main__":
  L1 =linea(punto(data_E1['40000']['combustion'][0],data_E1['40000']['combustion'][1]),punto(data_E1['40000']['combustion'][2],data_E1['40000']['combustion'][3]))
  L2 =linea(punto(data_E1['40000']['electric'][0],data_E1['40000']['electric'][1]),punto(data_E1['40000']['electric'][2],data_E1['40000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('\nS1_1 = ', P)

  L1 =linea(punto(data_E1['60000']['combustion'][0],data_E1['60000']['combustion'][1]),punto(data_E1['60000']['combustion'][2],data_E1['60000']['combustion'][3]))
  L2 =linea(punto(data_E1['60000']['electric'][0],data_E1['60000']['electric'][1]),punto(data_E1['60000']['electric'][2],data_E1['60000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S1_2 = ', P)

  L1 =linea(punto(data_E1['80000']['combustion'][0],data_E1['80000']['combustion'][1]),punto(data_E1['80000']['combustion'][2],data_E1['80000']['combustion'][3]))
  L2 =linea(punto(data_E1['80000']['electric'][0],data_E1['80000']['electric'][1]),punto(data_E1['80000']['electric'][2],data_E1['80000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S1_3 = ', P)

  L1 =linea(punto(data_E1['100000']['combustion'][0],data_E1['100000']['combustion'][1]),punto(data_E1['100000']['combustion'][2],data_E1['100000']['combustion'][3]))
  L2 =linea(punto(data_E1['100000']['electric'][0],data_E1['100000']['electric'][1]),punto(data_E1['100000']['electric'][2],data_E1['100000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S1_4 = ', P)

  ###################################
  L1 =linea(punto(data_E2['40000']['combustion'][0],data_E2['40000']['combustion'][1]),punto(data_E2['40000']['combustion'][2],data_E2['40000']['combustion'][3]))
  L2 =linea(punto(data_E2['40000']['electric'][0],data_E2['40000']['electric'][1]),punto(data_E2['40000']['electric'][2],data_E2['40000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('\nS2_1 = ', P)

  L1 =linea(punto(data_E2['60000']['combustion'][0],data_E2['60000']['combustion'][1]),punto(data_E2['60000']['combustion'][2],data_E2['60000']['combustion'][3]))
  L2 =linea(punto(data_E2['60000']['electric'][0],data_E2['60000']['electric'][1]),punto(data_E2['60000']['electric'][2],data_E2['60000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S2_2 = ', P)

  L1 =linea(punto(data_E2['80000']['combustion'][0],data_E2['80000']['combustion'][1]),punto(data_E2['80000']['combustion'][2],data_E2['80000']['combustion'][3]))
  L2 =linea(punto(data_E2['80000']['electric'][0],data_E2['80000']['electric'][1]),punto(data_E2['80000']['electric'][2],data_E2['80000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S2_3 = ', P)

  L1 =linea(punto(data_E2['100000']['combustion'][0],data_E2['100000']['combustion'][1]),punto(data_E2['100000']['combustion'][2],data_E2['100000']['combustion'][3]))
  L2 =linea(punto(data_E2['100000']['electric'][0],data_E2['100000']['electric'][1]),punto(data_E2['100000']['electric'][2],data_E2['100000']['electric'][3])) 
  P = L1.intersecta(L2)
  print ('S2_4 = ', P)
  
  ###################################
  L1 =linea(punto(data_E3['40000']['combustion'][0],data_E3['40000']['combustion'][1]),punto(data_E3['40000']['combustion'][2],data_E3['40000']['combustion'][3]))
  L2 =linea(punto(data_E3['40000']['electric'][0],data_E3['40000']['electric'][1]),punto(data_E3['40000']['electric'][2],data_E3['40000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('\nS3_1 = ', P)

  L1 =linea(punto(data_E3['60000']['combustion'][0],data_E3['60000']['combustion'][1]),punto(data_E3['60000']['combustion'][2],data_E3['60000']['combustion'][3]))
  L2 =linea(punto(data_E3['60000']['electric'][0],data_E3['60000']['electric'][1]),punto(data_E3['60000']['electric'][2],data_E3['60000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S3_2 = ', P)

  L1 =linea(punto(data_E3['80000']['combustion'][0],data_E3['80000']['combustion'][1]),punto(data_E3['80000']['combustion'][2],data_E3['80000']['combustion'][3]))
  L2 =linea(punto(data_E3['80000']['electric'][0],data_E3['80000']['electric'][1]),punto(data_E3['80000']['electric'][2],data_E3['80000']['electric'][3])) 
  P = L1.intersecta(L2)
  print ('S3_3 = ', P)

  L1 =linea(punto(data_E3['100000']['combustion'][0],data_E3['100000']['combustion'][1]),punto(data_E3['100000']['combustion'][2],data_E3['100000']['combustion'][3]))
  L2 =linea(punto(data_E3['100000']['electric'][0],data_E3['100000']['electric'][1]),punto(data_E3['100000']['electric'][2],data_E3['100000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S3_4 = ', P)

  ###################################
  L1 =linea(punto(data_E4['40000']['combustion'][0],data_E4['40000']['combustion'][1]),punto(data_E4['40000']['combustion'][2],data_E4['40000']['combustion'][3]))
  L2 =linea(punto(data_E4['40000']['electric'][0],data_E4['40000']['electric'][1]),punto(data_E4['40000']['electric'][2],data_E4['40000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('\nS4_1 = ', P)

  L1 =linea(punto(data_E4['60000']['combustion'][0],data_E4['60000']['combustion'][1]),punto(data_E4['60000']['combustion'][2],data_E4['60000']['combustion'][3]))
  L2 =linea(punto(data_E4['60000']['electric'][0],data_E4['60000']['electric'][1]),punto(data_E4['60000']['electric'][2],data_E4['60000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S4_2 = ', P)

  L1 =linea(punto(data_E4['80000']['combustion'][0],data_E4['80000']['combustion'][1]),punto(data_E4['80000']['combustion'][2],data_E4['80000']['combustion'][3]))
  L2 =linea(punto(data_E4['80000']['electric'][0],data_E4['80000']['electric'][1]),punto(data_E4['80000']['electric'][2],data_E4['80000']['electric'][3]))  
  P = L1.intersecta(L2)
  print ('S4_3 = ', P)

  L1 =linea(punto(data_E4['100000']['combustion'][0],data_E4['100000']['combustion'][1]),punto(data_E4['100000']['combustion'][2],data_E4['100000']['combustion'][3]))
  L2 =linea(punto(data_E4['100000']['electric'][0],data_E4['100000']['electric'][1]),punto(data_E4['100000']['electric'][2],data_E4['100000']['electric'][3]))
  P = L1.intersecta(L2)
  print ('S4_4 = ', P)

S1_1 =  (12.819310344827626,323.7932137931043)
S1_2 =  (9.768599562363232,312.07708971553575)
S1_3 =  (6.7464269248501605,263.1160119870907)
S1_4 =  (5.632788161993772,259.83890576323995)

S2_1 =  (18.754594594594547,516.8692648648633)
S2_2 =  (11.98194444444446,388.7166805555563)
S2_3 =  (9.166754896770778,356.05861831656955)
S2_4 =  (6.354157501099865,290.5900175978882)

S3_1 =  (11.645669291338585,301.35968503936994)
S3_2 =  (9.034622302158283,296.0283183453237)
S3_3 =  (6.38848337388484,254.8540957015411)
S3_4 =  (5.3821166608452655,253.2558959133776)

S4_1 =  (14.957009345794411,341.27284112149556)
S4_2 =  (11.131123919308328,323.5611383285294)
S4_3 =  (8.768189509306254,313.1099323181049)
S4_4 =  (6.0652273771244865,263.4792880110243)

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