import math
import Tail_sizing_WP3
import fuselage_sizing
import matplotlib.pyplot as plt
import numpy as np
import Airfoil_selection

# change landing gear dimensions and fuselage upsweep angle and fuselage base area
# calculate separately for landing by changing mach and Cf values


def Croot(taper, b, A):
    return 2*b/(A*(1+taper))

def Ctip(Cr, taper):
    return Cr*taper

def span(A, S):
    return (A*S)**0.5

def Sref(A, b):
    return b**2/A

def LESweep(Qcsweep, Cr, b, taper):
    Sweep = math.atan(math.tan(Qcsweep)+0.5*Cr*(1-taper) / b)
    return Sweep

def NCandTCLength(D, Ratio):
    return D*Ratio

def SwetNac(d, l):
    return math.pi*((d**2)/2+d*l)

# flight conditions
M = 0.77  # cruise
M_ld = 0.1  # landing

# Wing dimensions and HLD
Cr = 4.00444444065026  # m
taper = 0.35286100000000004
Ct = 1.4130122697722916  # m
b = 23.295063854816966  # m
AR = 8.4
S = Sref(AR, b)  # m^2
tcRatio = 0.1
xc_mRatio = 0.35   # wing maximum thickness position
LEsweepwing = math.radians(16.459155902616462)  # converted to rad
DeltaFlap = 35.0  # deg 15 for TO
FlapAreaRatio = 0.76845689
FlapChordRatio = 0.35

# Fuselage dimensions
D = fuselage_sizing.d_fus_outer  # m (fuselage diameter)
L = fuselage_sizing.l_fus  # m (fuselage length)
ncRatio = fuselage_sizing.nc_ratio  # ratio of nc length/fuselage diameter
tailconeRatio = fuselage_sizing.tc_ratio  # ratio of tc length/fuselage diameter
L1 = NCandTCLength(D, ncRatio)  # m fuselage nose cone
L2 = fuselage_sizing.l_cabin  # m fuselage cylindrical section length
L3 = NCandTCLength(D, tailconeRatio)  # m fuselage tail cone length
u = math.radians(10.0)  # rad (fuselage upsweep CHANGE VALUE)
A_base = 0.0225*math.pi  # m^2

# Landing gear
S_A_nose = 1.0  # m^2 (frontal area of nose gear)
S_A_gear = 1.0  # m^2 (frontal area of landing gear)
d = 0.8382  # m tire diameter
w = 1.0  # m tire width
a = 1.0  # m nose gear x-position
e = 1.0  # m nose gear strut length
DeltaCD_s = 0.58  # from graph for nose gear

# Tail
A_HT = float(Tail_sizing_WP3.A_h)  # AR
A_VT = Tail_sizing_WP3.A_v  # AR
xc_m_HT = 0.3  # NACA0012
xc_m_VT = 0.3
tc_HT = 0.12
tc_VT = 0.12
taper_HT = Tail_sizing_WP3.taper_h  # m
taper_VT = Tail_sizing_WP3.taper_v  # m
S_HT = Tail_sizing_WP3.S_v  # m^2 
S_VT = Tail_sizing_WP3.S_h  # m^2
b_HT = span(A_HT, S_HT)  # m
b_VT = span(A_VT, S_VT)  # m
Cr_HT = Croot(taper_HT, b_HT, A_HT)  # m
Cr_VT = Croot(taper_VT, b_VT, A_VT)  # m
Ct_HT = Ctip(Cr_HT, taper_HT)  # m
Ct_VT = Ctip(Cr_VT, taper_VT)  # m
QCsweep_HT = math.radians(Tail_sizing_WP3.sweep_htail_c_over_4)  # rad
QCsweep_VT = math.radians(Tail_sizing_WP3.sweep_vtail_c_over_4)  # rad
LESweep_HT = LESweep(QCsweep_HT, Cr_HT, b_HT, taper_HT)  # rad
LESweep_VT = LESweep(QCsweep_VT, Cr_VT, b_VT, taper_VT)  # rad

# Nacelle
l = 1.9  # m nacelle langth
d_nac = 1.08  # m max diameter
Swet_nacelle = SwetNac(d_nac, l)  # m^2

# Friction coefficients cruise
Cf_wing = 0.00237006342792386
Cf_fuselage = 0.0015165019899108692
Cf_HT = 0.002521515845393527
Cf_VT = 0.0011986993682703805
Cf_nacelle = 0.005643410494315579

# Friction coefficients Takeoff/landing
# Cf_wing = 0.002667669112660721 
# Cf_fuselage = 0.001651629724690628  
# Cf_HT = 0.0028431069019490066
# Cf_VT = 0.0013496122438869278 
# Cf_nacelle = 0.00614626593506182

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

# Interference factors IF
IF_tail = 1.04
IF_wing = 1.0
IF_fuselage = 1.0
IF_nacelle = 1.3

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
    S_s = d*w
    Delta_CD_ref = DeltaCD_sClosed*S_s/S
    return Delta_CD_ref

    # Flap
def DeltaCD_flap(FlapChordRatio, FlappedAreaRatio, DeltaFlap):  # delta flap in degrees
    return 0.0074*FlapChordRatio*FlappedAreaRatio*(DeltaFlap - 10)

# Calculating totals:
CD_excrescenceFrac = 0.05
UpsweepCD = CD_upsweep(u, D, S)
fuselageBaseCD = CD_fuselageBase(M, A_base, S)
DeltaCDREF_1 = DeltaCD_ref1(DeltaCD_s, w, d, S)
DeltaCDREF_2 = DeltaCD_ref2(S_A_gear, d, w, S)
DeltaCDFlap = DeltaCD_flap(FlapChordRatio, FlapAreaRatio, DeltaFlap)
print('UpsweepCd', UpsweepCD)
print(fuselageBaseCD, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap)
def MiscCD(UpsweepCD, fuselageBaseCD, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap):
    return UpsweepCD + fuselageBaseCD + DeltaCDREF_1 + 2*DeltaCDREF_2 + DeltaCDFlap
CD_misc = MiscCD(UpsweepCD, fuselageBaseCD, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap)
def MiscCDCruise(UpsweepCD, fuselageBaseCD):
    return UpsweepCD + fuselageBaseCD
CD_miscCruise = MiscCDCruise(UpsweepCD, fuselageBaseCD)

CD_wing = CD0_comp(S, Cf_wing, FF1(xc_mRatio, tcRatio, M, LEsweepwing, Cr, b, taper), IF_wing, Swet_w)
CD_HT = CD0_comp(S, Cf_HT, FF1(xc_m_HT, tc_HT, M, LESweep_HT, Cr_HT, b_HT, taper_HT), IF_tail, Swet_HT)
CD_VT = CD0_comp(S, Cf_VT, FF1(xc_m_VT, tc_VT, M, LESweep_VT, Cr_VT, b_VT, taper_VT), IF_tail, Swet_VT)
CD_fuselage = CD0_comp(S, Cf_fuselage, FF2(L, D), IF_fuselage, Fuselage_S_wet(L1, L2, L3, D))
CD_nacelle = CD0_comp(S, Cf_nacelle, FF3(l, d_nac), IF_nacelle, Swet_nacelle)

#print(xc_mRatio, tcRatio, M, LEsweepwing, Cr, b, taper)
#print(S, Cf_wing, FF1(xc_mRatio, tcRatio, M, LEsweepwing, Cr, b, taper), IF_wing, Swet_w)
#print(CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_misc, CD_miscCruise, CD_excrescenceFrac)

def SumOfCD(CD_misc, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac):
    SumCD = CD_misc + CD_wing + CD_HT + CD_VT + CD_fuselage + CD_nacelle
    total = (1+CD_excrescenceFrac)*SumCD
    return total

CD0_total = SumOfCD(CD_misc, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac)
CD0_total_Cruise = SumOfCD(CD_miscCruise, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac)
print('CD0 total landing', CD0_total)
print('CD0 total Cruise', CD0_total_Cruise)



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
deltaOswald = changeOswaldFlapDeflection(math.radians(DeltaFlap))
CL_cruise = Airfoil_selection.CL_cruise

CDi_cruise = CD_i(CL_cruise, AR, Oswald, Delta_e=0.0)
CD_cruise = CD(CD0_total_Cruise, CDi_cruise)
CLCD_max = CLCDmax(AR, Oswald, CD0_total_Cruise)
print('max L/D cruise', CLCD_max)

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
