import math
import Wing_aerodynamics_design

A = Wing_aerodynamics_design.AR

def MachDD(ka, LEsweep, tcRatio, Clwing):
    MDD = ka/(math.cos(LEsweep)) - tcRatio/((math.cos(LEsweep))**2) - Clwing/(10*(math.cos(LEsweep))**3)
    return MDD

# cruise CL using Design mission weights:
S = 63.1  # [m^2]
MTOW = 23173*9.80665  # [N]
OEW = 13127*9.80665  # [N]
Fuel_Weight = 2845*9.80665  # [N]
PL_Weight = 7200*9.80665  # [N]
hcr = 35000*0.3048 #m
T_cr = 288.15-0.0065*hcr
rho_cr = 1.225*((T_cr/288.15)**((9.80665/0.0065/287)-1))
print('rho', rho_cr)
Vcr = 0.77*(1.4*287*T_cr)**0.5 #m/s
WingloadStartCr = (MTOW)/S
WingloadEndCr = (MTOW - Fuel_Weight)/S
CL_cruise = 1.1/(0.5*rho_cr*Vcr**2)*0.5*(WingloadStartCr + WingloadEndCr)
print('CL cruise', CL_cruise)

ka_SC = 0.935 #Supercritical ka
ka_l = 0.87 # lower bound standard airfoils
ka_u = 0.9 # upper bound standard airfoils

LEsweep = math.radians(27.2)
tcRatio_NACA0012 = 0.12
tcRatio_NACA2416 = 0.16
tcRatio_NACA24012 = 0.12
tcRatio_KC = 0.0796
tcRatio_NASA = 0.1393
tcRatio_Lockheed = 0.1
Cl_NACA0012 = CL_cruise
Cl_NACA2416 = CL_cruise
Cl_NACA24012 = CL_cruise
Cl_NASA = CL_cruise
Cl_KC = CL_cruise

print("Drag Divergence Mach Numbers:")
print("KC-135:", MachDD(ka_SC, LEsweep, tcRatio_KC, Cl_KC))
print("NACA0012:", MachDD(ka_l, LEsweep, tcRatio_NACA0012, Cl_NACA0012), "to", MachDD(ka_u, LEsweep, tcRatio_NACA0012, Cl_NACA0012))
print("NACA2416:", MachDD(ka_l, LEsweep, tcRatio_NACA2416, Cl_NACA2416), "to", MachDD(ka_u, LEsweep, tcRatio_NACA2416, Cl_NACA2416))
print("NACA24012:", MachDD(ka_l, LEsweep, tcRatio_NACA24012, Cl_NACA24012), "to", MachDD(ka_u, LEsweep, tcRatio_NACA24012, Cl_NACA24012))
print("NASA:", MachDD(ka_SC, LEsweep, tcRatio_NASA, Cl_NASA))

# Finding dCL/dalpha for wing
def dCLdalpha(A, mach_infty, LEsweep, Cr, Ct, b, Cl_alpha):
    sweep_halfChord = math.atan(math.tan(LEsweep) - Cr/b*(1-Ct/Cr))
    beta = (1 - mach_infty**2)**0.5
    CLalpha = 2*math.pi*A/(2+(4+((A*beta/0.95)**2)*(1+(math.tan(sweep_halfChord)/beta)**2))**0.5)
    
    return CLalpha

Cr = Wing_aerodynamics_design.Root_chord
Ct = Wing_aerodynamics_design.Tip_chord
mach_infty = 0.77
LEsweep = Wing_aerodynamics_design.Sweep
b = Wing_aerodynamics_design.Span
Clalpha_airfoil = 0.11511*180/math.pi  # 1/rad
print('Clalpha airfoil [1/rad]', Clalpha_airfoil)

CLalpha = dCLdalpha(A, mach_infty, LEsweep, Cr, Ct, b, Clalpha_airfoil)  # 1/rad
alphaZeroLift = math.radians(-1.0)  # degrees to radians

# Sharpness factor (Delta Y from 0.0015c->0.06c)
def linearInterpolation(xUpper, xLower, x, yUpper, yLower):
    c = xLower + (x - xLower)/(xUpper - xLower)
    y = yLower + c*(yUpper - yLower)

    return y

DeltaY = linearInterpolation(0.06767, 0.05206, 0.06, 0.04668, 0.04164) - linearInterpolation(0.00433, 0.00106, 0.0015, 0.01115, 0.00529)
print('Delta Y as %:', DeltaY*100)  # 3.8381256714894203

# DeltaY = linearInterpolation(0.95, 0.925, 0.94, 0.00884, 0.01236) - linearInterpolation(1.0, 0.975, 0.9985, 0.0015, 0.00521)
# print('Delta Y as %:', DeltaY*100)

# Calculation showing high AR DATCOM method required for CLmax
def HighLowAR(C1, LEsweep):
    factor = 4/((C1 + 1)*math.cos(LEsweep))

    return factor

C1 = 0.5  # from graph AC ADSEE ppt 2 slide 20 bc taper = 0.316
factor = HighLowAR(C1, LEsweep) # factor = 2.91954 < A so high AR wings

# finding cruise angle of attack and Cd cruise

alpha_Cruise = (CL_cruise + CLalpha * alphaZeroLift)/CLalpha  # radians
alpha_trim = alpha_Cruise/math.pi *180  # deg
Cl_cruise_airfoil = CL_cruise / (math.cos(LEsweep)**2)  # slide 14 ADSEE ppt 2 notes
Cd_cruise = 0.005149

# finding CLmax high AR wings 
CLClRatio = 0.8  # from graph ADSEE ppt 2 slide 22 with sharpness factor >2.5
Clmax = 1.6
def CLmaxWing(CLClRatio, Clmax):
    CLmax = CLClRatio*Clmax

    return CLmax

CLmax = CLmaxWing(CLClRatio, Clmax)  # at M=0.2
print('CLmax at 0.2 Mach:', CLmax)

# finding stall AoA using CLalpha for M=0.2
Mach = 0.2
CLalphaM02 = dCLdalpha(A, Mach, LEsweep, Cr, Ct, b, Clalpha_airfoil) /180 *math.pi  # 1/deg
DeltaAlphaCLmax = 2.25  # ADSEE ppt 2 slide 24 graph - (deg)

def alphaStallDeg(CLmax, CLalpha, alphaZeroL, DeltaAlphaCLmax):
    alphaS = CLmax / CLalpha + alphaZeroL/math.pi*180 + DeltaAlphaCLmax

    return alphaS

alphaStall = alphaStallDeg(CLmax, CLalphaM02, alphaZeroLift, DeltaAlphaCLmax)  # deg at M=0.2
print('alpha stall at M=0.2 [deg]:', alphaStall)

# span efficiency factor
e = 4.61*(1-0.045*A**0.68)*(math.cos(LEsweep))**0.15 -3.1

# Mcrit
Mcrit_unswept = 1
Mcrit_swept = Mcrit_unswept*math.cos(LEsweep)
print('span efficiency factor:', e)
print('alpha zero lift [deg]:', alphaZeroLift/math.pi*180)
print('Cd cruise', Cd_cruise)
print("Mdd:", MachDD(ka_SC, LEsweep, tcRatio_Lockheed, CL_cruise))
print('alpha cruise/trim is [deg]:', alpha_Cruise/math.pi*180)
print('cruise Cl is:', Cl_cruise_airfoil)
print('CLalpha [1/rad]', CLalpha)