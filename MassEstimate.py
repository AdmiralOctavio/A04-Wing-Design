import math
global VcrM
global Vcr
VcrM = 0.77 #mach
Vcr = VcrM * 296.32 #Cruise speed in m/s
fcon = 0.05 #contingency fuel ratio
Rdiv = 250 #km, divergence range
Rnom = 2019 #km, Nominal 
tE = 2700 #loiter time
hCR = 10668 #m, cruise height
Mpl = 7200 #kg, design payload mass

B = 9 #Bypass Ratio

TSFC = 22*B**(-.19) #Thrust specific fuel consumption

AR = 7.5 #Aspect ratio duh
SwSratio = 6 #wet to total area ratio or whatever
Cd0 = 0.0192 #zero lift drag coef
e = 0.8280596821832961 #Oswald
global LD
LD = 1/2 * math.sqrt( (math.pi * AR * e) / (Cd0) )#Lift drag ratio
global Rlost
Rlost = (1/0.7 * LD * (hCR + Vcr**2 /(2*9.80665))) / 1000  #km, lost range from drag

global ef
ef = 44 #MJ/kg
global nj
nj = Vcr/TSFC/ef #Jet efficiency

def main(Rnom, Mpl):
    Req = (Rnom + Rlost)*(1+fcon) + 1.2*Rdiv + (tE*Vcr)/1000 #km, equivalent range
    f_MTOW = 1 - math.e **(-Req/(1000*nj*ef*LD/9.80665)) #Fuel / MTOW ratio
    OE_MTOW = 0.566492308 #OE / MTOW ratio
    p_MTOW = 1 - OE_MTOW - f_MTOW #Payload / MTOW ratio
    MTOW = Mpl / p_MTOW
    fuel = MTOW * f_MTOW #kg, fuel mass 
    structure = MTOW * OE_MTOW #kg, structural mass / operating empty
    f_landing = 1 - Rnom/Req * f_MTOW #Landing mass fraction
    return structure, fuel

def ferry():
    Rnom = 2963 #km
    Req = (Rnom + Rlost)*(1+fcon) + 1.2*Rdiv + (tE*Vcr)/1000
    f_MTOW = 1 - math.e **(-Req/(1000*nj*ef*LD/9.80665))
    OE_MTOW = 1 - f_MTOW
    OE = main(2574, 6355)[0]
    MTOW = OE/OE_MTOW
    Fuel = MTOW - OE
    return OE_MTOW, MTOW, Fuel