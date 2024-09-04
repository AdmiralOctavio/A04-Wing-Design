import math
Vcr = 0.77 #mach
fcon = 0.05 #contingency fuel ratio
Rdiv = 45894 #km, divergence range
Rnom = 2574 #km, Nominal 
Rlost = 435 #km, lost range from drag
tE = 4985 #loiter time

Req = (Rnom + Rlost)*(1+fcon) + 1.2*Rdiv + tE*Vcr #km, equivalent range


SwSratio = 6 #wet to total area ratio or whatever
Cd0 = 0.0192 #zero lift drag coef
e = 0.8232410800988017 #Oswald
LD = 1/2 * math.sqrt( () / () )