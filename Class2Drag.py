import math
import Tail_sizing_WP3
import fuselage_sizing
import matplotlib.pyplot as plt
import numpy as np
import Airfoil_selection
import PlanformParameters as PP
import Drag_calculator as DC
import WeightParameters as WP
import SpeedsAndRange 
import AerodynamicParameters
import FuselageParameters
import HLD

planform = PP.Planform()
Misc = SpeedsAndRange.Miscellaneous()
DRAG = AerodynamicParameters.DragBuildup()
FUS = FuselageParameters.Fuselage()
# change landing gear dimensions
# Change Mach app and to
# HLD ref values


def Croot(taper, b, A):
    return 2*b/(A*(1+taper))

def Ctip(Cr, taper):
    return Cr*taper

def span(A, S):
    return (A*S)**0.5

def AspectR(S, b):
    return b**2/S

def LESweep(Qcsweep, Cr, b, taper):
    Sweep = math.atan(math.tan(Qcsweep)+0.5*Cr*(1-taper) / b)
    return Sweep

def NCandTCLength(D, Ratio):
    return D*Ratio

def SwetNac(d, l):
    return math.pi*((d**2)/2+d*l)

# flight conditions
M = Misc.VcrM  # cruise
M_app = 0.1  # landing
M_to = 0.1  # take-off

# Interference factors IF
IF_tail = DRAG.IFtail
IF_wing = DRAG.IFwing
IF_fuselage = DRAG.IFfuselage
IF_nacelle = DRAG.IFnacelle

# Wing dimensions and HLD
Cr = planform.c_r  # m
taper = planform.taper 
Ct = Ctip(planform.c_r, planform.taper)  # m
b = planform.b  # m
S = planform.wing_area  # m^2
AR = AspectR(planform.wing_area, planform.b)
tcRatio = planform.t_over_c  # airfoil property
xc_mRatio = planform.xc_m   # wing maximum thickness position (airfoil property)
LEsweepwing = math.radians(planform.sweep_le)  # converted to rad
DeltaFlap_app = 35.0  # deg 
DeltaFlap_to = 15  # deg
#FlapAreaRatio = 0.7768427586206897 
FlapAreaRatio = HLD.LiftCoefficient(HLD.Slat[0], HLD.Double_Slotted[0], 8.2, Cr, Ct)[6]
FlapChordRatio = 0.35

# Fuselage dimensions
D = fuselage_sizing.d_fus_outer  # m (fuselage diameter)
L = fuselage_sizing.l_fus  # m (fuselage length)
ncRatio = fuselage_sizing.nc_ratio  # ratio of nc length/fuselage diameter
tailconeRatio = fuselage_sizing.tc_ratio  # ratio of tc length/fuselage diameter
L1 = NCandTCLength(fuselage_sizing.d_fus_outer, fuselage_sizing.nc_ratio)  # m fuselage nose cone
L2 = fuselage_sizing.l_cabin  # m fuselage cylindrical section length
L3 = NCandTCLength(fuselage_sizing.d_fus_outer, fuselage_sizing.tc_ratio)  # m fuselage tail cone length
u = FUS.upsweep  # rad (fuselage upsweep)
A_base = fuselage_sizing.d_fus_outer*math.pi/4  # m^2

# Landing gear
S_A_nose = DRAG.S_Anose  # m^2 (frontal area of nose gear)
S_A_gear = DRAG.S_Agear  # m^2 (frontal area of landing gear)
d_nose = DRAG.D_nose  # m tire diameter
d_main = DRAG.D_main  # m tire diameter
w_nose = DRAG.W_nose  # m tire width
w_main = DRAG.W_main  # m tire width
a = DRAG.Nose_x  # m nose gear x-position
e = DRAG.strut # m nose gear strut length
DeltaCD_s = DRAG.DeltaCDs  # from graph for nose gear

# Tail
A_HT = float(Tail_sizing_WP3.A_h)  # AR
A_VT = Tail_sizing_WP3.A_v  # AR
xc_m_HT = planform.xc_mHT  # NACA0012
xc_m_VT = planform.xc_mVT
tc_HT = planform.t_c_HT
tc_VT = planform.t_c_VT
taper_HT = Tail_sizing_WP3.taper_h  # m
taper_VT = Tail_sizing_WP3.taper_v  # m
S_HT = Tail_sizing_WP3.S_h  # m^2 
S_VT = Tail_sizing_WP3.S_v  # m^2
b_HT = span(float(Tail_sizing_WP3.A_h), Tail_sizing_WP3.S_h)  # m
b_VT = span(Tail_sizing_WP3.A_v, Tail_sizing_WP3.S_v)  # m
Cr_HT = Croot(Tail_sizing_WP3.taper_h, span(float(Tail_sizing_WP3.A_h), Tail_sizing_WP3.S_h), float(Tail_sizing_WP3.A_h))  # m
Cr_VT = Croot(Tail_sizing_WP3.taper_v, span(Tail_sizing_WP3.A_v, Tail_sizing_WP3.S_v), Tail_sizing_WP3.A_v)  # m
Ct_HT = Ctip(Cr_HT, Tail_sizing_WP3.taper_h)  # m
Ct_VT = Ctip(Cr_VT, Tail_sizing_WP3.taper_v)  # m
QCsweep_HT = math.radians(Tail_sizing_WP3.sweep_htail_c_over_4)  # rad
QCsweep_VT = math.radians(Tail_sizing_WP3.sweep_vtail_c_over_4)  # rad
LESweep_HT = LESweep(QCsweep_HT, Cr_HT, b_HT, taper_HT)  # rad
LESweep_VT = LESweep(QCsweep_VT, Cr_VT, b_VT, taper_VT)  # rad

# Nacelle
l = 1.9  # m nacelle langth
d_nac = 1.08  # m max diameter
Swet_nacelle = SwetNac(d_nac, l)  # m^2

# Friction coefficients cruise
Cf_wing = DC.Cf_W_cr
Cf_fuselage = DC.Cf_fus_cr
Cf_HT = DC.Cf_HT_cr
Cf_VT = DC.Cf_VT_cr
Cf_nacelle = DC.Cf_eng_cr

# Friction coefficients Takeoff/landing
Cf_wing_app = DC.Cf_W_app
Cf_fuselage_app = DC.Cf_fus_app
Cf_HT_app = DC.Cf_HT_app
Cf_VT_app = DC.Cf_VT_app
Cf_nacelle_app = DC.Cf_eng_app

# S_wet of wing, HT, VT:
def ChordAtY(Cr, Ct, b, y):
    return Cr - (Cr-Ct)*2/b*y
ChordAtFuselage = ChordAtY(Cr, Ct, b, D/2)
def S_exp(S, ChordAtIntersection, Cr, yIntersection):
    return S - (ChordAtIntersection + Cr)*yIntersection
S_exp_w = S_exp(S, ChordAtFuselage, Cr, D/2)
S_exp_HT = S_HT  # m^2
S_exp_VT = S_exp(S_VT, ChordAtY(Cr_VT, Ct_VT, b_VT, D/2), Cr_VT, D/4)  # m^2
def S_wet_w(S_exp_w):
    return 1.07*2*S_exp_w
def Swet_tail(S_exp_tail):
    return 1.05*2*S_exp_tail
Swet_w = S_wet_w(S_exp_w)
Swet_HT = Swet_tail(S_exp_HT)
Swet_VT = Swet_tail(S_exp_VT)

def Fuselage_S_wet(L1, L2, L3, D):
    Swet = math.pi*D/4*(1/(3*L1**2)*((4*L1**2+D**2/4)**1.5-D**3/8)-D+4*L2+2*math.sqrt(L3**2+D**2/4))
    return Swet 

# Form Factors FF
# f = length/diameter = l/sqrt(4/pi*Amax) where Amax is maxium frontal area
    # Wing, tail, strut, pylon: (position max thickness, sweep at maximum thickness)
def FF1(xc_mRatio, tcRatio, M, LEsweep, Cr, b, taper):
    SweepM = math.atan(math.tan(LEsweep)-xc_mRatio*2*Cr/b*(1-taper))
    FF = (1+0.6/xc_mRatio*tcRatio+100*tcRatio**4)*(1.34*M**0.18*(math.cos(SweepM))**0.28)
    return FF

    # Fuselage and smooth canopy 
def FF2(l, d):
    f = l/d
    FF = 1+60/(f**3)+f/400
    return FF

    # Nacelle and smooth external store
def FF3(l, d):
    f = l/d
    FF = 1+0.35/f
    return FF

def CD0_comp(S_ref, Cf, FF, IF, S_wet):
    return 1/S_ref*Cf*FF*IF*S_wet


# Miscellaneous drag coefficients
    # Fuselage upsweep 
def CD_upsweep(u, D, S):
    return 3.83 * u**2.5*D**2/4*math.pi/S  # u in radians

    # Fuselage base drag
def CD_fuselageBase(M, A_base, S):
    return (0.139+0.419*(M-0.161)**2)*A_base/S

    # Nose gear
def DeltaCD_ref1(DeltaCD_s, w, d, S):
    return DeltaCD_s*w*d/S

    # Retractable gear
def DeltaCD_ref2(S_A_gear, d, w, S):
    DeltaCD_sClosed = 0.04955*math.exp(5.615*S_A_gear/d/w)
    Delta_CD_ref = DeltaCD_sClosed*d*w/S
    return Delta_CD_ref

    # Flap
def DeltaCD_flap(FlapChordRatio, FlappedAreaRatio, DeltaFlap):  # delta flap in degrees
    return 0.0074*FlapChordRatio*FlappedAreaRatio*(DeltaFlap - 10)



# Calculating totals: 

# Cruise
CD_excrescenceFrac = 0.05
UpsweepCD = CD_upsweep(u, D, S)
fuselageBaseCD = CD_fuselageBase(M, A_base, S)

def MiscCD(UpsweepCD, fuselageBaseCD, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap):
    return UpsweepCD + fuselageBaseCD + DeltaCDREF_1 + 2*DeltaCDREF_2 + DeltaCDFlap
def MiscCDCruise(UpsweepCD, fuselageBaseCD):
    return UpsweepCD + fuselageBaseCD
CD_miscCruise = MiscCDCruise(UpsweepCD, fuselageBaseCD)

CD_wing = CD0_comp(S, Cf_wing, FF1(xc_mRatio, tcRatio, M, LEsweepwing, Cr, b, taper), IF_wing, Swet_w)
CD_HT = CD0_comp(S, Cf_HT, FF1(xc_m_HT, tc_HT, M, LESweep_HT, Cr_HT, b_HT, taper_HT), IF_tail, Swet_HT)
CD_VT = CD0_comp(S, Cf_VT, FF1(xc_m_VT, tc_VT, M, LESweep_VT, Cr_VT, b_VT, taper_VT), IF_tail, Swet_VT)
CD_fuselage = CD0_comp(S, Cf_fuselage, FF2(L, D), IF_fuselage, Fuselage_S_wet(L1, L2, L3, D))
CD_nacelle = CD0_comp(S, Cf_nacelle, FF3(l, d_nac), IF_nacelle, Swet_nacelle)

def SumOfCD(CD_misc, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac):
    SumCD = CD_misc + CD_wing + CD_HT + CD_VT + CD_fuselage + CD_nacelle
    total = (1+CD_excrescenceFrac)*SumCD
    return total

CD0_total_Cruise = SumOfCD(CD_miscCruise, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac)
print('CD0 total Cruise', CD0_total_Cruise)

# Approach with Flaps and Gear
fuselageBaseCD_app = CD_fuselageBase(M_app, A_base, S)
DeltaCDREF_1 = DeltaCD_ref1(DeltaCD_s, w_nose, d_nose, S)
DeltaCDREF_2 = DeltaCD_ref2(S_A_gear, e, 3*w_main, S)
DeltaCDFlap_app = DeltaCD_flap(FlapChordRatio, FlapAreaRatio, DeltaFlap_app)

CD_misc_app = MiscCD(UpsweepCD, fuselageBaseCD_app, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap_app)

CD_wing_app = CD0_comp(S, Cf_wing_app, FF1(xc_mRatio, tcRatio, M_app, LEsweepwing, Cr, b, taper), IF_wing, Swet_w)
CD_HT_app = CD0_comp(S, Cf_HT_app, FF1(xc_m_HT, tc_HT, M_app, LESweep_HT, Cr_HT, b_HT, taper_HT), IF_tail, Swet_HT)
CD_VT_app = CD0_comp(S, Cf_VT_app, FF1(xc_m_VT, tc_VT, M_app, LESweep_VT, Cr_VT, b_VT, taper_VT), IF_tail, Swet_VT)
CD_fuselage_app = CD0_comp(S, Cf_fuselage_app, FF2(L, D), IF_fuselage, Fuselage_S_wet(L1, L2, L3, D))
CD_nacelle_app = CD0_comp(S, Cf_nacelle_app, FF3(l, d_nac), IF_nacelle, Swet_nacelle)

print(UpsweepCD, fuselageBaseCD_app, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap_app)
print(CD_misc_app, CD_wing_app, CD_HT_app, CD_VT_app, CD_fuselage_app, CD_nacelle_app)

CD0_total_app = SumOfCD(CD_misc_app, CD_wing_app, CD_HT_app, CD_VT_app, CD_fuselage_app, CD_nacelle_app, CD_excrescenceFrac)
print('CD0 total approach with flaps and gear', CD0_total_app)

# Take-off with Flaps and Gear
fuselageBaseCD_to = CD_fuselageBase(M_to, A_base, S)
DeltaCDFlap_to = DeltaCD_flap(FlapChordRatio, FlapAreaRatio, DeltaFlap_to)

CD_misc_to = MiscCD(UpsweepCD, fuselageBaseCD_to, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap_to)

CD_wing_to = CD0_comp(S, Cf_wing_app, FF1(xc_mRatio, tcRatio, M_to, LEsweepwing, Cr, b, taper), IF_wing, Swet_w)
CD_HT_to = CD0_comp(S, Cf_HT_app, FF1(xc_m_HT, tc_HT, M_to, LESweep_HT, Cr_HT, b_HT, taper_HT), IF_tail, Swet_HT)
CD_VT_to = CD0_comp(S, Cf_VT_app, FF1(xc_m_VT, tc_VT, M_to, LESweep_VT, Cr_VT, b_VT, taper_VT), IF_tail, Swet_VT)
CD_fuselage_to = CD0_comp(S, Cf_fuselage_app, FF2(L, D), IF_fuselage, Fuselage_S_wet(L1, L2, L3, D))
CD_nacelle_to = CD0_comp(S, Cf_nacelle_app, FF3(l, d_nac), IF_nacelle, Swet_nacelle)

print(UpsweepCD, fuselageBaseCD_to, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap_to)
print(CD_misc_to, CD_wing_to, CD_HT_to, CD_VT_to, CD_fuselage_to, CD_nacelle_to)

CD0_total_to = SumOfCD(CD_misc_to, CD_wing_to, CD_HT_to, CD_VT_to, CD_fuselage_to, CD_nacelle_to, CD_excrescenceFrac)
print('CD0 total take-off with flaps and gear', CD0_total_to)
# Lift induced drag
    # Normal CD_i
def oswaldEfficiency(AR, LEsweep):
    return 4.61*(1-0.045*AR**0.68)*(math.cos(LEsweep))**0.15-3.1

def changeOswaldFlapDeflection(Flap_def):  # wing mounted engines
    return 0.0046*Flap_def*math.pi/180

def CD_i(CL, AR, e, Delta_e):
    return CL**2/(math.pi*AR*(e+Delta_e))

    # Ground effect
def CD_iGroundEffect(h, b, AR, Delta_e, e, CL):
    Phi = 33*(h/b)**1.5/(1+33*(h/b)**1.5)
    CD_i = CL**2/(math.pi*AR*Phi*(e + Delta_e))
    return CD_i

def CLCDmax(A, e, CD0):
    return (math.pi*A*e/4/CD0)**0.5

def CD(CD0, CDi):
    return CD0+CDi
def CLopt(A, e, CD0):
    return (math.pi*A*e*CD0)**0.5
Oswald = oswaldEfficiency(AR, LEsweepwing)
deltaOswald = changeOswaldFlapDeflection(math.radians(DeltaFlap_app))
CL_cruise = Airfoil_selection.CL_cruise

CDi_cruise = CD_i(CL_cruise, AR, Oswald, Delta_e=0.0)
CD_cruise = CD(CD0_total_Cruise, CDi_cruise)
CLCD_max_cruise = CLCDmax(AR, Oswald, CD0_total_Cruise)
print('max L/D cruise', CLCD_max_cruise)

V_stall = 50.6  # m/s
def TimeGroundEffect(b, V_stall, gamma):
    t = b/(2*V_stall*math.sin(gamma))
    return t
gamma1 = math.radians(1)
gamma3 = math.radians(3)
gamma5 = math.radians(5)
print('time ground effect at gamma=1deg', TimeGroundEffect(b, V_stall, gamma1))
print('time ground effect at gamma=3deg', TimeGroundEffect(b, V_stall, gamma3))
print('time ground effect at gamma=5deg', TimeGroundEffect(b, V_stall, gamma5))
# Define the function
def f(gamma):
    return 23.295063854816966/(2*50.6*np.sin(gamma))

# Generate x values
gamma = np.linspace(-0.35, 0.35, 400)

# Compute y values
t = f(gamma)

# Create the plot
plt.plot(gamma, t, label='f(gamma) = b/(2*V_stall*sin(gamma))')

# Add title and labels
plt.title('Plot of f(gamma) = b/(2*V_stall*sin(gamma))')
plt.xlabel('gamma')
plt.ylabel('time for ground effect')

# Add a legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
