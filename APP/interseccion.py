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
  L1 =linea(punto(4,160.577779839420),punto(5,188.4664422256254))
  L2 =linea(punto(4,171.9376925609628),punto(5,180.16336539783057)) 
  P = L1.intersecta(L2)
  print ('\nS1_1 = ', P)

  L1 =linea(punto(3,160.86348230940942),punto(4,197.17138263137875))
  L2 =linea(punto(3,169.98421203259514),punto(4,179.896314236376)) 
  P = L1.intersecta(L2)
  print ('S1_2 = ', P)

  L1 =linea(punto(2,138.6644587552488),punto(3,179.47686905441745))
  L2 =linea(punto(2,163.30909688583282),punto(3,173.99782922296768)) 
  P = L1.intersecta(L2)
  print ('S1_3 = ', P)

  L1 =linea(punto(3,150.227261312262),punto(4,182.53394151459563))
  L2 =linea(punto(3,167.6907164952394),punto(4,176.71286556621095)) 
  P = L1.intersecta(L2)
  print ('S1_4 = ', P)

  ###################################
  L1 =linea(punto(6,218.0392205478918),punto(7,249.4031491693934))
  L2 =linea(punto(6,221.6497823934467),punto(7,237.476472155106)) 
  P = L1.intersecta(L2)
  print ('\nS2_1 = ', P)

  L1 =linea(punto(4,197.17138263137875),punto(5,235.69328748551507))
  L2 =linea(punto(4,200.63198172836385),punto(5,217.09608215820163)) 
  P = L1.intersecta(L2)
  print ('S2_2 = ', P)

  L1 =linea(punto(3,179.47686905441745),punto(4,222.78690458574923))
  L2 =linea(punto(3,189.1598840111358),punto(4,206.20301690115338)) 
  P = L1.intersecta(L2)
  print ('S2_3 = ', P)

  L1 =linea(punto(4,182.53394151459563),punto(5,216.8025493815592))
  L2 =linea(punto(4,197.44853305819836),punto(5,212.95148410460163)) 
  P = L1.intersecta(L2)
  print ('S2_4 = ', P)
  
  ###################################
  L1 =linea(punto(4,163.03016154920076),punto(5,192.3234530338706))
  L2 =linea(punto(4,171.33716916206683),punto(5,179.21980333177123)) 
  P = L1.intersecta(L2)
  print ('\nS3_1 = ', P)

  L1 =linea(punto(3,163.14454012318458),punto(4,201.156502909771))
  L2 =linea(punto(3,169.42510106304513),punto(4,178.92046371317053)) 
  P = L1.intersecta(L2)
  print ('S3_2 = ', P)

  L1 =linea(punto(2,140.04581799438412),punto(3,182.3720578180551))
  L2 =linea(punto(2, 162.97018585335468),punto(3,173.2881883770004)) 
  P = L1.intersecta(L2)
  print ('S3_3 = ', P)

  L1 =linea(punto(3,152.15738715468711),punto(4,185.90596636554292))
  L2 =linea(punto(3,167.21762259792789),punto(4,175.88714589272908)) 
  P = L1.intersecta(L2)
  print ('S3_4 = ', P)

  ###################################
  L1 =linea(punto(3,141.7844296349413),punto(4,174.00794207991407))
  L2 =linea(punto(3,163.90640490025194),punto(4,171.33716916206683)) 
  P = L1.intersecta(L2)
  print ('\nS4_1 = ', P)

  L1 =linea(punto(2,132.332023800244),punto(3,173.0696695143102))
  L2 =linea(punto(2,160.47051256941577),punto(3,169.42510106304513)) 
  P = L1.intersecta(L2)
  print ('S4_2 = ', P)

  L1 =linea(punto(2,145.89121343838664),punto(3,194.96933742986846))
  L2 =linea(punto(2,162.97018585335468),punto(3,173.2881883770004)) 
  P = L1.intersecta(L2)
  print ('S4_3 = ', P)

  L1 =linea(punto(3,160.55557356256264),punto(4,201.0004145952737))
  L2 =linea(punto(3,167.21762259792789),punto(4,175.88714589272908)) 
  P = L1.intersecta(L2)
  print ('S4_4 = ', P)

S1_1 =  (4.577730700259941,176.6899162891156)
S1_2 =  (3.3455371829390144,173.4092119050932)
S1_3 =  (2.8181151770924115,172.05371103472132)
S1_4 =  (3.75000244086752,174.45735032033866)

S2_1 =  (6.232381176483474,225.3276071801)
S2_2 =  (4.156887740521126,203.21499724451397)
S2_3 =  (3.3686393896130102,195.44265411680533)
S2_4 =  (4.794781215825163,209.7699873397367)

S3_1 =  (4.387984707366257,174.3955106736749)
S3_2 =  (3.220242276772338,171.5163813518878)
S3_3 =  (2.7162021339723226,170.35996127912156)
S3_4 =  (3.6005104615441232,172.4237620330565)

S4_1 =  (3.8922760438610227,170.53669783864805)
S4_2 =  (2.8853298338801228,168.39827691294553)
S4_3 =  (2.440632582360211,167.51663395014788)
S4_4 =  (3.2096611303879126,169.03528465184027)

km = [32000, 44000, 52000, 66000]
year1 = [S1_1[0], S1_4[0], S1_2[0], S1_3[0]]
year2 = [S2_1[0], S2_4[0], S2_2[0], S2_3[0]]
year3 = [S3_1[0], S3_4[0], S3_2[0], S3_3[0]]
year4 = [S4_1[0], S4_4[0], S4_2[0], S4_3[0]]

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


km = [32000, 44000, 52000, 66000]
year1 = [S1_1[1], S1_4[1], S1_2[1], S1_3[1]]
year2 = [S2_1[1], S2_4[1], S2_2[1], S2_3[1]]
year3 = [S3_1[1], S3_4[1], S3_2[1], S3_3[1]]
year4 = [S4_1[1], S4_4[1], S4_2[1], S4_3[1]]

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