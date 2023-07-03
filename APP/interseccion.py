import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
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
   
if __name__=="__main__":
  L1 =linea(punto(6,1353.3379065343981),punto(7,1572.132013725358))
  L2 =linea(punto(6,1400.570586133278),punto(6,1418.469405386961)) 
  P = L1.intersecta(L2)
  print ('\nS1_1 = ', P)

  L1 =linea(punto(4,1264.357493524957),punto(5,1554.613318699238))
  L2 =linea(punto(4,1381.8865612981015),punto(5,1401.7636707762465)) 
  P = L1.intersecta(L2)
  print ('S1_2 = ', P)

  L1 =linea(punto(3,1222.636751978921),punto(4,1586.746839272674))
  L2 =linea(punto(3,1373.2411568969442),punto(4,1395.681860547924)) 
  P = L1.intersecta(L2)
  print ('S1_3 = ', P)

  L1 =linea(punto(2,1027.7576836866403),punto(3,1459.6270059139772))
  L2 =linea(punto(2,1358.6582494159813),punto(3,1383.1798933252944)) 
  P = L1.intersecta(L2)
  print ('S1_4 = ', P)

  ###################################
  L1 =linea(punto(6,1353.3379065343981),punto(7,1572.132013725358))
  L2 =linea(punto(6,1468.2811943134404),punto(7,1499.3716945798126)) 
  P = L1.intersecta(L2)
  print ('\nS2_1 = ', P)

  L1 =linea(punto(4,1264.357493524957),punto(5,1554.613318699238))
  L2 =linea(punto(4,1424.935905031275),punto(5,1456.8656323916261)) 
  P = L1.intersecta(L2)
  print ('S2_2 = ', P)

  L1 =linea(punto(3,1222.636751978921),punto(4,1586.746839272674))
  L2 =linea(punto(3,1404.7695919520972),punto(4,1438.7312042810977)) 
  P = L1.intersecta(L2)
  print ('S2_3 = ', P)

  L1 =linea(punto(2,1027.7576836866403),punto(3,1459.6270059139772))
  L2 =linea(punto(2,1379.1737954379312),punto(3,1414.7083283804475)) 
  P = L1.intersecta(L2)
  print ('S2_4 = ', P)
  
  ###################################
  L1 =linea(punto(6,1388.919903541648),punto(7,1621.0245417935514))
  L2 =linea(punto(6,1397.5716797833318),punto(7,1397.5716797833318)) 
  P = L1.intersecta(L2)
  print ('\nS3_1 = ', P)

  L1 =linea(punto(4,1288.2959331938473),punto(5,1591.6103457717522))
  L2 =linea(punto(4,1379.9348100247266),punto(5,1398.6970151433015)) 
  P = L1.intersecta(L2)
  print ('S3_2 = ', P)

  L1 =linea(punto(3,1241.2256370622113),punto(4,1618.6647588311946))
  L2 =linea(punto(3,1371.7501559416044),punto(4,1393.0795255167586))  
  P = L1.intersecta(L2)
  print ('S3_3 = ', P)

  L1 =linea(punto(2,1039.0361066825417),punto(3,1482.86311226809))
  L2 =linea(punto(2,1357.7681571318494),punto(3,1381.3161421311192)) 
  P = L1.intersecta(L2)
  print ('S3_4 = ', P)

  ###################################
  L1 =linea(punto(6,1253.3637356654795),punto(7,1436.5638075160068))
  L2 =linea(punto(6,1397.5716797833318),punto(7,1414.27882982502)) 
  P = L1.intersecta(L2)
  print ('\nS4_1 = ', P)

  L1 =linea(punto(4,1195.3034215457083),punto(5,1449.2837097396587))
  L2 =linea(punto(4,1379.9348100247266),punto(5,1398.6970151433015)) 
  P = L1.intersecta(L2)
  print ('S4_2 = ', P)

  L1 =linea(punto(3,1168.3067269203734),punto(4,1494.6747433003427))
  L2 =linea(punto(3,1371.7501559416044),punto(4,1393.0795255167586)) 
  P = L1.intersecta(L2)
  print ('S4_3 = ', P)

  L1 =linea(punto(2,994.3604117084855),punto(3,1391.7144745907924))
  L2 =linea(punto(2,1357.7681571318494),punto(3,1381.3161421311192)) 
  P = L1.intersecta(L2)
  print ('S4_4 = ', P)

S1_1 =  (6.000000000000026,1353.3379065344034)
S1_2 =  (4.4346831349891795,1390.526805560585)
S1_3 =  (3.440789875031603,1383.1327918548807)
S1_4 =  (2.812329573340543,1378.5779059504425)

S2_1 =  (6.612365897823275,1487.3199564228319)
S2_2 =  (4.621611261367719,1444.7837831308702)
S2_3 =  (3.551669487471116,1423.5051772193292)
S2_4 =  (2.886664812809935,1410.6810154376958)

S3_1 =  (6.037275326795902,1397.571679783332)
S3_2 =  (4.322045917861932,1385.9771015932515)
S3_3 =  (3.3665289087852592,1379.5679864970632)
S3_4 =  (2.758382014892594,1375.6265254422563)

S4_1 =  (6.866150599984222,1412.0425878159656)
S4_2 =  (4.78493705103384,1394.6619599813923)
S4_3 =  (3.6669431272143296,1385.9756323875679)
S4_4 =  (2.972182548452498,1380.6610971993607)

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