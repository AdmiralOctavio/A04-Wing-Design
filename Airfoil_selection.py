import math
import Wing_aerodynamics_design
import WeightParameters
import PlanformParameters as PP
import Drag_calculator as DC
import WeightParameters as WP
import SpeedsAndRange 
import AerodynamicParameters
import FuselageParameters
import PropulsionParameters
import AerodynamicParameters
import HLD

planform = PP.Planform()
Misc = SpeedsAndRange.Miscellaneous()
FUS = FuselageParameters.Fuselage()
PROP = PropulsionParameters.Propulsion()
weightparameters = WeightParameters.Weight()
Aerodynamics = AerodynamicParameters.Aerodynamics()

# Wing planform
b = planform.b
S = planform.wing_area
A = planform.AR
Cr = planform.c_r
Ct = planform.t_r
mach_infty = Misc.VcrM
taper = planform.taper

def MachDD(ka, LEsweep, tcRatio, Clwing):
    MDD = ka/(math.cos(LEsweep)) - tcRatio/((math.cos(LEsweep))**2) - Clwing/(10*(math.cos(LEsweep))**3)
    return MDD

# cruise CL using Design mission weights:
MTOW = weightparameters.MTOW * 9.80665  # [N]
Fuel_Weight = weightparameters.M_fuel *9.80665  # [N]
PL_Weight = weightparameters.M_Payload*9.80665  # [N]
OEW = weightparameters.OEW*9.80665  # [N]

ka_SC = 0.935 #Supercritical ka
ka_l = 0.87 # lower bound standard airfoils
ka_u = 0.9 # upper bound standard airfoils

tcRatio_NACA0012 = 0.12
tcRatio_NACA2416 = 0.16
tcRatio_NACA24012 = 0.12
tcRatio_KC = 0.0796
tcRatio_NASA = 0.1393
tcRatio_Lockheed = 0.1
Cl_NACA0012 = Misc.CL_cruise
Cl_NACA2416 = Misc.CL_cruise
Cl_NACA24012 = Misc.CL_cruise
Cl_NASA = Misc.CL_cruise
Cl_KC = Misc.CL_cruise

print("Drag Divergence Mach Numbers:")
print("KC-135:", MachDD(ka_SC, math.radians(planform.sweep_le), tcRatio_KC, Cl_KC))
print("NACA0012:", MachDD(ka_l, math.radians(planform.sweep_le), tcRatio_NACA0012, Cl_NACA0012), "to", MachDD(ka_u, math.radians(planform.sweep_le), tcRatio_NACA0012, Cl_NACA0012))
print("NACA2416:", MachDD(ka_l, math.radians(planform.sweep_le), tcRatio_NACA2416, Cl_NACA2416), "to", MachDD(ka_u, math.radians(planform.sweep_le), tcRatio_NACA2416, Cl_NACA2416))
print("NACA24012:", MachDD(ka_l, math.radians(planform.sweep_le), tcRatio_NACA24012, Cl_NACA24012), "to", MachDD(ka_u, math.radians(planform.sweep_le), tcRatio_NACA24012, Cl_NACA24012))
print("NASA:", MachDD(ka_SC, math.radians(planform.sweep_le), tcRatio_NASA, Cl_NASA))

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
factor = HighLowAR(C1, math.radians(planform.sweep_le)) # factor = 2.91954 < A so high AR wings

# finding cruise angle of attack and Cd cruise

alpha_Cruise = (Misc.CL_cruise + planform.CL_alpha * alphaZeroLift)/planform.CL_alpha  # radians
alpha_trim = alpha_Cruise/math.pi *180  # deg
Cl_cruise_airfoil = Misc.CL_cruise / (math.cos(math.radians(planform.sweep_le))**2)  # slide 14 ADSEE ppt 2 notes
Cl_cruise_airfoil_zeroM  = Cl_cruise_airfoil*(1-0.77*0.77)**0.5
print('Cl mach 0 and Cl mach 0.77', Cl_cruise_airfoil_zeroM, Cl_cruise_airfoil)
Cd_cruise = 0.00484

# finding CLmax high AR wings 

def CLclGraph(x):
    return -3*10**(-10)*x**5+3*10**(-8)*x**4-2*10**(-6)*x**3+3*10**(-5)*x**2-0.0034*x+0.9

CLClRatio = CLclGraph(planform.sweep_le)  # from graph ADSEE ppt 2 slide 22 with sharpness factor >2.5

Clmax = 1.73/((1-0.2*0.2)**0.5)  # 1.73 at M=0, but for calculations correct for M=0.2
def CLmaxWing(CLClRatio, Clmax):
    CLmax = CLClRatio*Clmax

    return CLmax

CLmax = CLmaxWing(CLClRatio, Clmax)  # at M=0.2
print('CLmax at 0.2 Mach:', CLmax)
CLmax_cruise = CLmax
print(CLmax_cruise)

# finding stall AoA using CLalpha for M=0.2
CLalphaM02 = 2*math.pi*planform.AR/(2+(4+((planform.AR*math.sqrt(0.96)/0.95)**2)*(1+(math.tan(planform.sweep_half)/math.sqrt(0.96))**2))**0.5)
DeltaAlphaCLmax = 2.25  # ADSEE ppt 2 slide 24 graph - (deg)

def alphaStallDeg(CLmax, CLalpha, alphaZeroL, DeltaAlphaCLmax):
    alphaS = CLmax / CLalpha + alphaZeroL/math.pi*180 + DeltaAlphaCLmax

    return alphaS

alphaStall = alphaStallDeg(CLmax, CLalphaM02, alphaZeroLift, DeltaAlphaCLmax)  # deg at M=0.2
print('alpha stall at M=0.2 [deg]:', alphaStall)

# Mcrit
Mcrit_unswept = 0.81333
Mcrit_swept = Mcrit_unswept/math.cos(math.radians(planform.sweep_le))
print('Crit mach', Mcrit_swept)
print('alpha zero lift [deg]:', alphaZeroLift/math.pi*180)
print('Cd cruise', Cd_cruise)
print("Mdd:", MachDD(ka_SC, math.radians(planform.sweep_le), tcRatio_Lockheed, Misc.CL_cruise))
print('alpha cruise/trim is [deg]:', alpha_Cruise/math.pi*180)
print('cruise Cl is:', Cl_cruise_airfoil)
print('CLalpha [1/rad]', planform.CL_alpha)

Aerodynamics.updatealphaStall(alphaStall)
Aerodynamics.updateCL_max_Cruise(CLmax_cruise)
