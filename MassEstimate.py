import math
VcrM = 0.77 #mach
Vcr = VcrM * 296.32 #Cruise speed in m/s
fcon = 0.05 #contingency fuel ratio
Rdiv = 250 #km, divergence range
Rnom = 2574 #km, Nominal 
tE = 2700 #loiter time
hCR = 10668 #m, cruise height

B = 9 #Bypass Ratio

TSFC = 22*B**(-.19)

AR = 7.5
SwSratio = 6 #wet to total area ratio or whatever
Cd0 = 0.0192 #zero lift drag coef
e = 0.8280596821832961 #Oswald
LD = 1/2 * math.sqrt( (math.pi * AR * e) / (Cd0) )#Lift drag ratio

Rlost = (1/0.7 * LD * (hCR + Vcr**2 /(2*9.80665))) / 1000  #km, lost range from drag

Req = (Rnom + Rlost)*(1+fcon) + 1.2*Rdiv + (tE*Vcr)/1000 #km, equivalent range
ef = 44 #MJ/kg

nj = Vcr/TSFC/ef #Jet efficiency

f_MTOW = 1 - math.e **(-Req/(1000*nj*ef*LD/9.80665)) #Fuel / MTOW ratio
OE_MTOW = 0.566492308 #OE / MTOW ratio
p_MTOW = 1 - OE_MTOW - f_MTOW #Payload / MTOW ratio
MTOW = 6355 / p_MTOW
fuel = MTOW * f_MTOW #kg, fuel mass 
structure = MTOW * OE_MTOW #kg, structural mass / operating empty
print(fuel, structure, MTOW)

f_landing = 1 - Rnom/Req * f_MTOW
print(f_landing)
print(Req-Rnom)
print(nj)