import math
import matplotlib.pyplot as plt
import numpy as np
# import Planform
import PlanformParameters as PP
# import Drag_calculator as Aerodynamics
import WeightParameters as WP
import SpeedsAndRange
import AerodynamicParameters
import FuselageParameters
import PropulsionParameters
# import HLD

Planform = PP.Planform()
Miscellaneous = SpeedsAndRange.Miscellaneous()
Aerodynamics = AerodynamicParameters.Aerodynamics()
Fuselage = FuselageParameters.Fuselage()
Propulsion = PropulsionParameters.Propulsion()
Weight = WP.Weight()
# change landing gear dimensions
# Change Mach app and to
# HLD ref values

def GearSA(D, W, L, W_s):
    return 2*D*W+W_s*(L-D/2)

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

def SwetNac(d, l):
    return math.pi*((d**2)/2+d*l)

# S_wet of wing, HT, VT:
def ChordAtY(Cr, Ct, b, y):
    return Cr - (Cr-Ct)*2/b*y

def S_exp(S, ChordAtIntersection, Cr, yIntersection):
    return S - (ChordAtIntersection + Cr)*yIntersection

def S_wet_w(S_exp_w):
    return 1.07*2*S_exp_w

def Swet_tail(S_exp_tail):
    return 1.05*2*S_exp_tail

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

def MiscellaneousCD(UpsweepCD, fuselageBaseCD, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap):
    return UpsweepCD + fuselageBaseCD + DeltaCDREF_1 + 2*DeltaCDREF_2 + DeltaCDFlap

def MiscellaneousCAerodynamicsruise(UpsweepCD, fuselageBaseCD):
    return UpsweepCD + fuselageBaseCD

def SumOfCD(CD_misc, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac):
    SumCD = CD_misc + CD_wing + CD_HT + CD_VT + CD_fuselage + CD_nacelle
    total = (1+CD_excrescenceFrac)*SumCD
    return total

def TimeGroundEffect(b, V_stall, gamma):
    t = b/(2*V_stall*math.sin(gamma))
    return t

# Define the function
def f(gamma):
    return 23.295063854816966/(2*50.6*np.sin(gamma))

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
def OswaldTot(E, deltaE):
    return E + deltaE


#MAIN FUNCTION
#This will be called from the main iteration program.
# The arguments are the parameter classes, so they do not need to be imported.

def Class2_Drag(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight):
    ChordAtFuselage = ChordAtY(Planform.c_r, Planform.t_r, Planform.b, Fuselage.d_fus_outer/2)
    
    # Fuselage dimensions
    D = Fuselage.d_fus_outer  # m (fuselage diameter)
    L = Fuselage.l_f  # m (fuselage length)
    ncRatio = Fuselage.nc_ratio  # ratio of nc length/fuselage diameter
    tailconeRatio = Fuselage.tc_ratio  # ratio of tc length/fuselage diameter
    L1 = Fuselage.l_nc  # m fuselage nose cone
    L2 = Fuselage.l_cabin  # m fuselage cylindrical section length
    L3 = Fuselage.l_tc  # m fuselage tail cone length
    u = Fuselage.upsweep  # rad (fuselage upsweep)
    A_base = 0.0 # m^2
    
    S_exp_w = S_exp(Planform.wing_area, ChordAtY(Planform.c_r, Planform.t_r, Planform.b, Fuselage.d_fus_outer/2), Planform.c_r, Fuselage.d_fus_outer/2)
    S_exp_HT = Planform.HT_area  # m^2
    S_exp_VT = Planform.VT_area  # m^2
    
    Swet_w = S_wet_w(S_exp_w)
    Swet_HT = Swet_tail(S_exp_HT)
    Swet_VT = Swet_tail(S_exp_VT)
    print('S', Planform.wing_area, Planform.HT_area, Planform.VT_area)
    print('S', S_exp_w, S_exp_HT, S_exp_VT)
    print('S', Swet_w, Swet_HT, Swet_VT)

    # flight conditions
    M = Miscellaneous.VcrM  # cruise

    # Interference factors IF
    IF_tail = Aerodynamics.IFtail
    IF_wing = Aerodynamics.IFwing
    IF_fuselage = Aerodynamics.IFfuselage
    IF_nacelle = Aerodynamics.IFnacelle

    # Wing dimensions and HLD
    Cr = Planform.c_r  # m
    taper = Planform.taper
    Ct = Ctip(Planform.c_r, Planform.taper)  # m
    b = Planform.b  # m
    S = Planform.wing_area  # m^2
    AR = AspectR(Planform.wing_area, Planform.b)
    tcRatio = Planform.t_over_c  # airfoil property
    xc_mRatio = Planform.xc_m  # wing maximum thickness position (airfoil property)
    LEsweepwing = math.radians(Planform.sweep_le)  # converted to rad
    DeltaFlap_app = Planform.FlapDeflectionL  # deg
    DeltaFlap_to = Planform.FlapDeflectionTO  # deg
    FlapAreaRatio = Planform.FlapAreaRatio
    # FlapAreaRatio = HLD.LiftCoefficient(HLD.Slat[0], HLD.Double_Slotted[0], 8.2, Cr, Ct)[6]
    FlapChordRatio = Planform.FlapChordRatio

    # Landing gear
    d_nose = Aerodynamics.D_nose  # m tire diameter
    d_main = Aerodynamics.D_main  # m tire diameter
    w_nose = Aerodynamics.W_nose  # m tire width
    w_main = Aerodynamics.W_main  # m tire width
    a = Aerodynamics.Nose_x  # m nose gear x-position
    e = Aerodynamics.strut  # m nose gear strut length
    DeltaCD_s = Aerodynamics.DeltaCDs  # from graph for nose gear
    S_A_nose = GearSA(d_nose, w_nose, Aerodynamics.strut, W_s=0.05)  # m^2 (frontal area of nose gear)
    S_A_gear = GearSA(d_main, w_main, Aerodynamics.strut, W_s=0.05)  # m^2 (frontal area of landing gear)

    # Tail
    A_HT = float(Planform.HT_AR)  # AR
    A_VT = Planform.VT_AR  # AR
    xc_m_HT = Planform.xc_mHT  # NACA0012
    xc_m_VT = Planform.xc_mVT
    tc_HT = Planform.t_c_HT
    tc_VT = Planform.t_c_VT
    taper_HT = Planform.HT_taper  # m
    taper_VT = Planform.VT_taper  # m
    S_HT = Planform.HT_area  # m^2
    S_VT = Planform.VT_area  # m^2
    b_HT = span(A_HT, S_HT)  # m
    b_VT = span(A_VT, S_VT)  # m
    Cr_HT = Croot(taper_HT, b_HT, A_HT)  # m
    Cr_VT = Croot(taper_VT, b_VT, A_VT)  # m
    Ct_HT = Ctip(Cr_HT, taper_HT)  # m
    Ct_VT = Ctip(Cr_VT, taper_VT)  # m
    QCsweep_HT = math.radians(Planform.HT_quarter_sweep)  # rad
    QCsweep_VT = math.radians(Planform.VT_quarter_sweep)  # rad
    LESweep_HT = LESweep(QCsweep_HT, Cr_HT, b_HT, taper_HT)  # rad
    LESweep_VT = LESweep(QCsweep_VT, Cr_VT, b_VT, taper_VT)  # rad

    # Nacelle
    Swet_nacelle = SwetNac(Propulsion.d_nacelle, Propulsion.l_nac)  # m^2

    # Friction coefficients cruise
    Cf_wing = Aerodynamics.Cf_W_cr
    Cf_fuselage = Aerodynamics.Cf_fus_cr
    Cf_HT = Aerodynamics.Cf_HT_cr
    Cf_VT = Aerodynamics.Cf_VT_cr
    Cf_nacelle = Aerodynamics.Cf_eng_cr

    # Friction coefficients Takeoff/landing
    Cf_wing_app = Aerodynamics.Cf_W_app
    Cf_fuselage_app = Aerodynamics.Cf_fus_app
    Cf_HT_app = Aerodynamics.Cf_HT_app
    Cf_VT_app = Aerodynamics.Cf_VT_app
    Cf_nacelle_app = Aerodynamics.Cf_eng_app


    # Calculating totals: 
    
    # Cruise
    CD_excrescenceFrac = Aerodynamics.CD_excrFrac
    UpsweepCD = CD_upsweep(Fuselage.upsweep, Fuselage.d_fus_outer, Planform.wing_area)
    fuselageBaseCD = CD_fuselageBase(Miscellaneous.VcrM, A_base, Planform.wing_area)
    
    CD_miscCruise = MiscellaneousCAerodynamicsruise(CD_upsweep(Fuselage.upsweep, Fuselage.d_fus_outer, Planform.wing_area), fuselageBaseCD)
    
    CD_wing = CD0_comp(Planform.wing_area, Cf_wing, FF1(Planform.xc_m, Planform.t_over_c, Miscellaneous.VcrM, math.radians(Planform.sweep_le), Cr, Planform.b, taper), Aerodynamics.IFwing, Swet_w)
    CD_HT = CD0_comp(Planform.wing_area, Cf_HT, FF1(Planform.xc_mHT, Planform.t_c_HT, Miscellaneous.VcrM, LESweep_HT, Cr_HT, b_HT, taper_HT), Aerodynamics.IFtail, Swet_HT)
    CD_VT = CD0_comp(Planform.wing_area, Cf_VT, FF1(Planform.xc_mVT, Planform.t_c_VT, Miscellaneous.VcrM, LESweep_VT, Cr_VT, b_VT, taper_VT), Aerodynamics.IFtail, Swet_VT)
    CD_fuselage = CD0_comp(Planform.wing_area, Cf_fuselage, FF2(L, Fuselage.d_fus_outer), Aerodynamics.IFfuselage, Fuselage_S_wet(Fuselage.l_nc, Fuselage.l_cabin, Fuselage.l_tc, Fuselage.d_fus_outer))
    CD_nacelle = CD0_comp(Planform.wing_area, Cf_nacelle, FF3(Propulsion.l_nac, Propulsion.d_nacelle), Aerodynamics.IFnacelle, SwetNac(Propulsion.d_nacelle, Propulsion.l_nac))
    
    CD0_total_Cruise = SumOfCD(CD_miscCruise, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac)
    print(CD_miscCruise, CD_wing, CD_HT, CD_VT, CD_fuselage, CD_nacelle, CD_excrescenceFrac)
    print(CD_upsweep(Fuselage.upsweep, Fuselage.d_fus_outer, Planform.wing_area), fuselageBaseCD)
    print('CD0 total Cruise', CD0_total_Cruise)
    
    # Approach with Flaps and Gear
    fuselageBaseCD_app = CD_fuselageBase(Miscellaneous.M_app, A_base, Planform.wing_area)
    DeltaCDREF_1 = DeltaCD_ref1(Aerodynamics.DeltaCDs, Aerodynamics.W_nose, Aerodynamics.D_nose, Planform.wing_area)
    DeltaCDREF_2 = DeltaCD_ref2(S_A_gear, Aerodynamics.strut, 3*Aerodynamics.W_main, Planform.wing_area)
    DeltaCDFlap_app = DeltaCD_flap(FlapChordRatio, FlapAreaRatio, DeltaFlap_app)
    
    CD_misc_app = MiscellaneousCD(UpsweepCD, fuselageBaseCD_app, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap_app)
    
    CD_wing_app = CD0_comp(Planform.wing_area, Cf_wing_app, FF1(Planform.xc_m, Planform.t_over_c, Miscellaneous.M_app, math.radians(Planform.sweep_le), Cr, b, taper), Aerodynamics.IFwing, Swet_w)
    CD_HT_app = CD0_comp(Planform.wing_area, Cf_HT_app, FF1(Planform.xc_mHT, Planform.t_c_HT, Miscellaneous.M_app, LESweep_HT, Cr_HT, b_HT, taper_HT), Aerodynamics.IFtail, Swet_HT)
    CD_VT_app = CD0_comp(Planform.wing_area, Cf_VT_app, FF1(Planform.xc_mVT, Planform.t_c_VT, Miscellaneous.M_app, LESweep_VT, Cr_VT, b_VT, taper_VT), Aerodynamics.IFtail, Swet_VT)
    CD_fuselage_app = CD0_comp(Planform.wing_area, Cf_fuselage_app, FF2(L, Fuselage.d_fus_outer), Aerodynamics.IFfuselage, Fuselage_S_wet(Fuselage.l_nc, Fuselage.l_cabin, Fuselage.l_tc, Fuselage.d_fus_outer))
    CD_nacelle_app = CD0_comp(Planform.wing_area, Cf_nacelle_app, FF3(Propulsion.l_nac, Propulsion.d_nacelle), Aerodynamics.IFnacelle, SwetNac(Propulsion.d_nacelle, Propulsion.l_nac))
    
    print(UpsweepCD, fuselageBaseCD_app, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap_app)
    print(CD_misc_app, CD_wing_app, CD_HT_app, CD_VT_app, CD_fuselage_app, CD_nacelle_app)
    
    CD0_Landing_DOWN = SumOfCD(CD_misc_app, CD_wing_app, CD_HT_app, CD_VT_app, CD_fuselage_app, CD_nacelle_app, CD_excrescenceFrac)
    print('CD0 total approach with flaps and gear', CD0_Landing_DOWN)

    # Approach with Flaps no Gear
    DeltaCDREF_1_up = 0.0
    DeltaCDREF_2_up = 0.0
    CD_misc_app_up = MiscellaneousCD(UpsweepCD, fuselageBaseCD_app, DeltaCDREF_1_up, DeltaCDREF_2_up, DeltaCD_flap(FlapChordRatio, FlapAreaRatio, DeltaFlap_app))
    CD0_Landing_UP = SumOfCD(CD_misc_app_up, CD_wing_app, CD_HT_app, CD_VT_app, CD_fuselage_app, CD_nacelle_app, CD_excrescenceFrac)
    print('CD0 app no gear', CD0_Landing_UP)

    # Approach at sea-level clean
    CD_misc_SL_clean = MiscellaneousCAerodynamicsruise(CD_upsweep(Fuselage.upsweep, Fuselage.d_fus_outer, Planform.wing_area), fuselageBaseCD_app)
    CD0_SL_clean = SumOfCD(CD_misc_SL_clean, CD_wing_app, CD_HT_app, CD_VT_app, CD_fuselage_app, CD_nacelle_app, CD_excrescenceFrac)
    print('Sea level approach, clean config', CD0_SL_clean)
    
    # Take-off with Flaps and Gear
    fuselageBaseCD_to = CD_fuselageBase(Miscellaneous.M_app, A_base, Planform.wing_area)
    DeltaCDFlap_to = DeltaCD_flap(FlapChordRatio, FlapAreaRatio, DeltaFlap_to)
    
    CD_misc_to = MiscellaneousCD(UpsweepCD, fuselageBaseCD_to, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap_to)
    
    CD_wing_to = CD0_comp(Planform.wing_area, Cf_wing_app, FF1(xc_mRatio, Planform.t_over_c, Miscellaneous.M_app, math.radians(Planform.sweep_le), Cr, b, taper), Aerodynamics.IFwing, Swet_w)
    CD_HT_to = CD0_comp(Planform.wing_area, Cf_HT_app, FF1(xc_m_HT, Planform.t_c_HT, Miscellaneous.M_app, LESweep_HT, Cr_HT, b_HT, taper_HT), Aerodynamics.IFtail, Swet_HT)
    CD_VT_to = CD0_comp(Planform.wing_area, Cf_VT_app, FF1(xc_m_VT, Planform.t_c_VT, Miscellaneous.M_app, LESweep_VT, Cr_VT, b_VT, taper_VT), Aerodynamics.IFtail, Swet_VT)
    CD_fuselage_to = CD0_comp(Planform.wing_area, Cf_fuselage_app, FF2(L, Fuselage.d_fus_outer), Aerodynamics.IFfuselage, Fuselage_S_wet(Fuselage.l_nc, Fuselage.l_cabin, Fuselage.l_tc, Fuselage.d_fus_outer))
    CD_nacelle_to = CD0_comp(Planform.wing_area, Cf_nacelle_app, FF3(Propulsion.l_nac, Propulsion.d_nacelle), Aerodynamics.IFnacelle, SwetNac(Propulsion.d_nacelle, Propulsion.l_nac))
    
    print(UpsweepCD, fuselageBaseCD_to, DeltaCDREF_1, DeltaCDREF_2, DeltaCDFlap_to)
    print(CD_misc_to, CD_wing_to, CD_HT_to, CD_VT_to, CD_fuselage_to, CD_nacelle_to)
    
    CD0_Takeoff_DOWN = SumOfCD(CD_misc_to, CD_wing_to, CD_HT_to, CD_VT_to, CD_fuselage_to, CD_nacelle_to, CD_excrescenceFrac)
    print('CD0 total take-off with flaps and gear', CD0_Takeoff_DOWN)

    # Take-off Flaps no gear
    CD_misc_to_up = MiscellaneousCD(UpsweepCD, fuselageBaseCD_to, DeltaCDREF_1_up, DeltaCDREF_2_up, DeltaCD_flap(FlapChordRatio, FlapAreaRatio, DeltaFlap_to))
    CD0_Takeoff_UP = SumOfCD(CD_misc_to_up, CD_wing_to, CD_HT_to, CD_VT_to, CD_fuselage_to, CD_nacelle_to, CD_excrescenceFrac)
    print('CD0 to no gear', CD0_Takeoff_UP)

    # Lift induced drag
    
    Oswald = oswaldEfficiency(Planform.AR, math.radians(Planform.sweep_le))
    Oswald_app = OswaldTot(Oswald, changeOswaldFlapDeflection(DeltaFlap_app))
    Oswald_to = OswaldTot(Oswald, changeOswaldFlapDeflection(DeltaFlap_to))
    CL_cruise = Miscellaneous.CL_cruise
    print(CL_cruise, Oswald, Oswald_app, Oswald_to)
    
    # Cruise CD total
    CDi_cruise = CD_i(CL_cruise, Planform.AR, Oswald, Delta_e=0.0)
    CD_cruise = CD(CD0_total_Cruise, CDi_cruise)
    CLCD_max_cruise = CLCDmax(Planform.AR, Oswald, CD0_total_Cruise)
    print('CD cruise', CD_cruise)
    print('max L/D cruise', CLCD_max_cruise)

    # V_stall = Miscellaneous.V_stall  # m/s
    
    # gamma1 = math.radians(1)
    # gamma3 = math.radians(3)
    # gamma5 = math.radians(5)
    # # print('time ground effect at gamma=1deg', TimeGroundEffect(b, V_stall, gamma1))
    # # print('time ground effect at gamma=3deg', TimeGroundEffect(b, V_stall, gamma3))
    # # print('time ground effect at gamma=5deg', TimeGroundEffect(b, V_stall, gamma5))
    
    # # Generate x values
    # gamma = np.linspace(-0.35, 0.35, 400)
    
    # # Compute y values
    # t = f(gamma)
    
    # # Create the plot
    # plt.plot(gamma, t, label='f(gamma) = b/(2*V_stall*sin(gamma))')
    
    # # Add title and labels
    # plt.title('Plot of f(gamma) = b/(2*V_stall*sin(gamma))')
    # plt.xlabel('gamma')
    # plt.ylabel('time for ground effect')
    
    # # Add a legend
    # plt.legend()
    
    # # Show the plot
    # plt.grid(True)
    # #plt.show()


    # These are the 6 needed parameters, only 3 were calculated
    # Gear UP and DOWN were approximated as the same
    # CD0_Cruise and CD0_Clean_UP were approximated as the same
    # To change if there is enough time left
    Aerodynamics.updateCD0_Landing_UP(CD0_Landing_UP)
    Aerodynamics.updateCD0_Landing_DOWN(CD0_Landing_DOWN)
    Aerodynamics.updateCD0_Takeoff_UP(CD0_Takeoff_UP)
    Aerodynamics.updateCD0_Takeoff_DOWN(CD0_Takeoff_DOWN)
    Aerodynamics.updateCD0_Cruise(CD0_total_Cruise)
    Aerodynamics.updateCD0_Clean_UP(CD0_SL_clean)
    Aerodynamics.updateCD_cruise(CD_cruise)
    Aerodynamics.updatee_Clean(Oswald)
    Aerodynamics.updatee_Takeoff(Oswald_to)
    Aerodynamics.updatee_Landing(Oswald_app)
    Aerodynamics.updateLD(CLCD_max_cruise)


Class2_Drag(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)

