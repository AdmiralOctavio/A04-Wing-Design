import math
import Tail_sizing_WP3
import fuselage_sizing

def Croot(taper, b, A):
    return 2*b/(A*(1+taper))

def Ctip(Cr, taper):
    return Cr*taper


def Sref(A, b):
    return b**2/A

def LESweep(Qcsweep, Cr, b, taper):
    Sweep = math.atan(math.tan(Qcsweep)+0.5*Cr/b*(1-taper))
    return Sweep

def NCandTCLength(D, Ratio):
    return D*Ratio

def SwetNac(d, l):
    return math.pi()*((d**2)/2+d*l)

# flight conditions
M = 0.77  # cruise

# Wing dimensions and HLD
Cr = 4.00444444065026  # m
taper = 0.35286100000000004
Ct = 1.4130122697722916  # m
b = 23.295063854816966  # m
AR = 8.4
S = Sref(AR, b)  # m^2
tcRatio = 0.1
xc_mRatio = 0.35   # wing maximum thickness position
LEsweep = math.radians(16.459155902616462)  # converted to rad
DeltaFlap = 35.0  # deg
FlapAreaRatio = 0.76845689
FlapChordRatio = 0.35

# Fuselage dimensions
D = fuselage_sizing.d_fus_outer  # m (fuselage diameter)
L = fuselage_sizing.l_fus  # m (fuselage length)
ncRatio = fuselage_sizing.nc_ratio  # ratio of nc length/fuselage diameter
tcRatio = fuselage_sizing.tc_ratio  # ratio of tc length/fuselage diameter
L1 = NCandTCLength(D, ncRatio)  # m fuselage nose cone
L2 = fuselage_sizing.l_cabin  # m fuselage cylindrical section length
L3 = NCandTCLength(D, tcRatio)  # m fuselage tail cone length
u = math.radians(10.0)  # rad (fuselage upsweep CHANGE VALUE)
A_base = 0.0  # m^2

# Landing gear
S_A_nose = 0.0  # m^2 (frontal area of nose gear)
S_A_gear = 0.0  # m^2 (frontal area of landing gear)
d = 0.0  # m tire diameter
w = 0.0  # m tire width
a = 0.0  # m nose gear x-position
e = 0.0  # m nose gear strut length
DeltaCD_s = 0.0  # from graph for nose gear

# Tail
A_HT = float(Tail_sizing_WP3.A_h)  # AR
A_VT = Tail_sizing_WP3.A_v  # AR
xc_m_HT = 0.3  # NACA0012
xc_m_VT = 0.3
tc_HT = 0.12
tc_VT = 0.12
taper_HT = Tail_sizing_WP3.taper_h  # m
taper_VT = Tail_sizing_WP3.taper_v  # m
b_HT = 0.0  # m
b_VT = 0.0  # m
S_HT = Sref(A_HT, b_HT)  # m^2 
S_VT = Sref(A_VT, b_VT)  # m^2
Cr_HT = Croot(taper_HT, b_HT, A_HT)  # m
Cr_VT = Croot(taper_VT, b_VT, A_VT)  # m
Ct_HT = Ctip(Cr_HT, taper_HT)  # m
Ct_VT = Ctip(Cr_VT, taper_VT)  # m
cOver4LEsweep_HT = math.radians(Tail_sizing_WP3.sweep_htail_c_over_4)  # rad
cOver4LEsweep_VT = math.radians(Tail_sizing_WP3.sweep_vtail_c_over_4)  # rad
LESweep_HT = LESweep(cOver4LEsweep_HT, Cr_HT, b_HT, taper_HT)  # rad
LESweep_VT = LESweep(cOver4LEsweep_VT, Cr_VT, b_VT, taper_VT)  # rad

# Nacelle
l = 1.9  # m nacelle langth
d_nacelle = 1.08  # m max diameter
Swet_nacelle = SwetNac(d_nacelle, l)  # m^2

# Friction coefficients
Cf_wing = 0.0  
Cf_fuselage = 0.0
Cf_HT = 0.0  
Cf_VT = 0.0
Cf_nacelle = 0.0 

# S_wet of wing, HT, VT:
def ChordAtY(Cr, Ct, b, y):
    return Cr - (Cr-Ct)*2/b*y
ChordAtFuselage = ChordAtY(Cr, Ct, b, D/2)
def S_exp(S, ChordAtIntersection, Cr, yIntersection):
    return S - (ChordAtIntersection + Cr)*yIntersection
S_exp_w = S_exp(S, ChordAtFuselage, Cr, D/2)
S_exp_HT = 0.0  # m^2
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
    return 0.139+0.419*(M-0.161)**2*A_base/S

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
def MiscCD(UpsweepCD, fuselageBaseCD, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap):
    return UpsweepCD + fuselageBaseCD + DeltaCDREF_1 + 2*DeltaCDREF_2 + DeltaCDFlap
CD_misc = MiscCD(UpsweepCD, fuselageBaseCD, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap)

CD_wing = CD0_comp(S, Cf_wing, FF1(xc_mRatio, tcRatio, M, LEsweep, Cr, b, taper), IF_wing, Swet_w)
CD_HT = CD0_comp(S, Cf_HT, FF1(xc_m_HT, tc_HT, M, LESweep_HT, Cr_HT, b_HT, taper_HT), IF_tail, Swet_HT)
CD_VT = CD0_comp(S, Cf_VT, FF1(xc_m_VT, tc_VT, M, LESweep_VT, Cr_VT, b_VT, taper_VT), IF_tail, Swet_VT)
CD_fuselage = CD0_comp(S, Cf_fuselage, FF2(L, D), IF_fuselage, Fuselage_S_wet(L1, L2, L3, D))
CD_nacelle = CD0_comp(S, Cf_nacelle, FF3(l, d_nacelle), IF_nacelle, Swet_nacelle)

def SumOfCD(CD_misc, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac):
    SumCD = CD_misc + CD_wing + CD_HT + CD_VT + CD_fuselage + CD_nacelle
    total = (1+CD_excrescenceFrac)*SumCD
    return total

CD0_total = SumOfCD(CD_misc, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac)
print('CD0 total', CD0_total)



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