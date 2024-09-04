import math
Vcr = 0.77 #mach
fcon = 0.05 #contingency fuel ratio
Rdiv = 45894 #km, divergence range
Rnom = 2574 #km, Nominal 
Rlost = 435 #km, lost range from drag
tE = 4985 #loiter time

Req = (Rnom + Rlost)*(1+fcon) + 1.2*Rdiv + tE*Vcr #km, equivalent range

AR = 8
φ = 0.97
Ψ = 0.0075
e = 1/(math.pi * AR * 1/φ * Ψ) #oswald efficiency factor
