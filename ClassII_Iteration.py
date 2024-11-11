import PlanformParameters
import FuselageParameters
import SpeedsAndRange
from math import sqrt,atan,tan,radians,cos,fabs




OEW_init = 13127
M_fuel_init = 2845
M_Payload = 7255
MTOW_init = OEW_init+M_fuel_init+M_Payload
print("MTOW" ,MTOW_init)
MZFW_init = MTOW_init-M_fuel_init
MaxNumberOfIterations = 100
ft_per_meter = 0.3048
def CalculateWingWeight(Planform,MZFW):
    n_ult = CalculateLoadFactor(Miscellaneous, Planform)
    WingWeight = (MZFW*6.67/1000*Planform.b_s**0.75*(1+sqrt(Planform.b_ref/Planform.b_s))*n_ult**0.55*
                  (Planform.b_s/Planform.t_r*Planform.wing_area/MZFW)**0.3)*0.9


    return WingWeight
def CalculateTailWeight(Miscellaneous,Planform):
    n_ult = CalculateLoadFactor(Miscellaneous, Planform)
    TailWeight = 0.64*(n_ult*Planform.tail_area**2)**0.75
    return TailWeight
def CalculateAirframeStructuralWeight(Miscellaneous,Planform,Fuselage,MTOW):
    n_ult = CalculateLoadFactor(Miscellaneous, Planform)
    StructuralWeight = MTOW*sqrt(1.5*n_ult)*(Fuselage.b_f*Fuselage.h_f*Fuselage.l_f/MTOW)**0.24*0.447
    return StructuralWeight
def CalculateBodyWeight(Miscellaneous,Fuselage):
    BodyWeight = 0.23 * sqrt(Miscellaneous.V_dive_EAS * Fuselage.l_t / (Fuselage.b_f + Fuselage.h_f)) * Fuselage.S_f_wet ** 1.2
    return BodyWeight
def CalculateLandingGearWeight(MTOW):
    A_main = 40
    A_nose = 20
    B_main = 0.16
    B_nose = 0.1
    C_main = 0.019
    C_nose = 0
    D_main = 1.5 * 10 ** (-5)
    D_nose = 2 * 10 ** (-6)
    W_main = 1.08 * (A_main + B_main * (MTOW / 0.453592) ** 0.75 + C_main * (MTOW / 0.453592) + D_main * (
            MTOW / 0.453592) ** 1.5)
    W_nose = 1.08 * (A_nose + B_nose * (MTOW / 0.453592) ** 0.75 + C_nose * MTOW / 0.453592 + D_nose * (
                MTOW / 0.453592) ** 1.5)
    LandingGearWeight = (W_main+W_nose)*0.453592
    return LandingGearWeight

def CalculateSurfaceControlsWeight(MTOW):
    SurfaceControlsWeight = 0.64 * 1.2 * 0.768 * MTOW ** 0.666667
    return SurfaceControlsWeight

def CalculateNacelleWeight(MTOW):
    NacelleWeight = 0.065*0.453592*0.4*MTOW
    return NacelleWeight

def CalculatePropulsionGroup():
    EngineWeight = 1040
    NoEngines = 2
    PropulsionWeight = 1.15*1.18*EngineWeight * NoEngines*0.453592**2
    return PropulsionWeight

def CalculateAirframeServicesAndEquipmentWeight(Miscellaneous,OEW,MTOW,M_fuel):
    W_ba = 0.4 * 85.34
    W_APU = 11.7 * (W_ba ** 0.6)

    # LOW_SUBSONIC
    W_INE_1 = 54.4 + 9.1 * 2 + 0.006 * MTOW

    # HIGH_SUBSONIC
    W_INE_2 = 0.347 * OEW ** (5 / 9) * Miscellaneous.Range ** 0.25

    W_HPE = 0.011 * OEW + 181

    W_EL = 0.02 * MTOW + 181

    W_furnish = 0.196 * (MTOW - M_fuel) ** 0.91

    W_air_conditioning = 14 * (19.44 ** 1.28)

    W_misc = 0.01 * OEW

    W_airframe_services = W_ba + W_APU + W_INE_1 + W_EL + W_furnish + W_air_conditioning + W_misc  # Excludes fuel and passengers

    return W_airframe_services
def CalculateLoadFactor(Miscellaneous, Planform):
    u_hat = Miscellaneous.GustVelocity * ft_per_meter  # m/s

    mu = 2 * Planform.WingLoading / Miscellaneous.densityFL / 9.81 / Planform.CL_alpha / Planform.MAC

    K = 0.88 * mu / (5.3 + mu)

    u = K * u_hat

    # MAXIMUM LOAD FACTOR
    n_max = 1 + Miscellaneous.densityFL * Miscellaneous.Velocity * Planform.CL_alpha * u / 2 / Planform.WingLoading
    n_ult = 1.5 * n_max

    return n_ult



def IterationClassII (Planform, Fuselage, MTOW, OEW, M_fuel, MZFW, Miscellaneous,iterationNumber):
    AirframeStructuralWeight = CalculateAirframeStructuralWeight(Miscellaneous,Planform,Fuselage,MTOW)
    n_ult = CalculateLoadFactor(Miscellaneous, Planform)
    WingGroupWeight = CalculateWingWeight(Planform,MZFW)
    BodyGroupWeight = CalculateBodyWeight(Miscellaneous,Fuselage)
    TailGroupWeight = CalculateTailWeight(Miscellaneous,Planform)
    LandingGearWeight = CalculateLandingGearWeight(MTOW)
    SurfaceControlsWeight = CalculateSurfaceControlsWeight(MTOW)
    NacelleWeight = CalculateNacelleWeight(MTOW)
    PropulsionWeight = CalculatePropulsionGroup()
    AirframeServicesAndEquipmentWeight = CalculateAirframeServicesAndEquipmentWeight(Miscellaneous,OEW,MTOW,M_fuel)
    OEWnew = (WingGroupWeight + TailGroupWeight + BodyGroupWeight + LandingGearWeight +
              SurfaceControlsWeight + NacelleWeight + PropulsionWeight + AirframeServicesAndEquipmentWeight)
    MTOWnew = OEWnew + M_fuel + M_Payload


    '''print("LoadFactor", n_ult )
    print("WingGroupWeight", WingGroupWeight)
    print("BodyGroupWeight", BodyGroupWeight)
    print("TailGroupWeight", TailGroupWeight)
    print("LandingGearWeight", LandingGearWeight)
    print("SurfaceControlsWeight", SurfaceControlsWeight)
    print("NacelleWeight", NacelleWeight)
    print("PropulsionWeight", PropulsionWeight)
    print("AirframeServices", AirframeServicesAndEquipmentWeight)'''

    print("Iteration Number:", iterationNumber)
    print("RandomTorenbeekEstimate", AirframeStructuralWeight)
    print ("OEWnew = ", OEWnew)
    print ("OEW_init = ", OEW)
    print ("MTOWnew = ", MTOWnew)
    print("MTOW_init = ", MTOW)
    ratio = fabs(OEWnew - OEW)/OEW
    if (iterationNumber <=MaxNumberOfIterations and ratio>0.01):
        iterationNumber = iterationNumber + 1
        MZFW = MTOWnew - M_fuel
        IterationClassII(Planform, Fuselage, MTOWnew, OEWnew, M_fuel_init, MZFW, Miscellaneous, iterationNumber)




Planform = PlanformParameters.Planform()
Fuselage = FuselageParameters.Fuselage()
Miscellaneous = SpeedsAndRange.Miscellaneous()

IterationClassII(Planform, Fuselage, MTOW_init, OEW_init, M_fuel_init, MZFW_init, Miscellaneous, 1)
n_ult_print = CalculateLoadFactor(Miscellaneous, Planform)
print("n_ult", n_ult_print)





