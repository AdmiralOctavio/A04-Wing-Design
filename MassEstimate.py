import math
VcrM = 0.77 #mach
Vcr = VcrM * 296.32
fcon = 0.05 #contingency fuel ratio
Rdiv = 45894 #km, divergence range
Rnom = 2574 #km, Nominal 
tE = 4985 #loiter time
hCR = 10668 #m, cruise height


AR = 7.5
SwSratio = 6 #wet to total area ratio or whatever
Cd0 = 0.0192 #zero lift drag coef
e = 0.8280596821832961 #Oswald
LD = 1/2 * math.sqrt( (math.pi * AR * e) / (Cd0) )#Lift drag ratio

Rlost = (1/0.7 * LD * (hCR + Vcr**2 /(2*9.80665))) / 1000  #km, lost range from drag

Req = (Rnom + Rlost)*(1+fcon) + 1.2*Rdiv + tE*Vcr #km, equivalent range
