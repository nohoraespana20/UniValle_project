import numpy as np

N = 10
np.random.seed(0)
b = np.random.random((1,N))
Pref = []
for i in range(N):
    Pref_r = np.random.random((1,3))
    suma = sum(Pref_r[0])
    Pref_norm = [Pref_r[0][0]/ suma, Pref_r[0][1]/ suma, Pref_r[0][2]/ suma]
    Pref.append(Pref_norm)
print('b = ', b, '\nPref = ', Pref[-1][:])