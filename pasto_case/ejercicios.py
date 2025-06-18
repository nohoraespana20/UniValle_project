##6.4
# Vs = 24; D = 0.65; L = 250e-6; C =  75e-6; R = 10; f = 25e3
##6.5
# Vs = 15; D = 0.60; L =  50e-6; C = 150e-6; R =  5; f = 50e3

# Vo = Vs * D
# print('Vo = ', Vo)
# Il = Vo / R
# deltaIl = Vo * (1 - D) / (L * f)
# print('Imax = ', Il + (deltaIl / 2))
# print('Imax = ', Il - (deltaIl / 2))
# deltaVo = (1 - D) * 100 / (8 * L * C * (f**2))
# print('Rizado = ', deltaVo)

##6.6
# Vs = 50; Vo = 25; f = 10e3; Po = 125; Imax = 6.25; deltaVo = 0.05

# D = Vo / Vs
# R = (Vo**2) / Po
# Il = Vo / R
# deltaIl = 2 * (Imax - Il)
# L = ((Vs - Vo) * D) / (deltaIl * f)
# C = (1 - D) / (8 * L * deltaVo * (f**2))
# print('D = ', D)
# print('L = ', L)
# print('C = ', C)

Vo = 12; Vs = 18; R = ((Vo**2) / 10); deltaVo = 0.1/12; f = 50e3
print('R = ', R)
D = Vo / Vs
Lmin = (1 - D) * R / (2 * f)
print('Lmin ', Lmin)
L = 1.25 * Lmin
C = (1 - D) / (8 * L * deltaVo * (f**2))

print('D = ', D)
print('L = ', L)
print('C = ', C)