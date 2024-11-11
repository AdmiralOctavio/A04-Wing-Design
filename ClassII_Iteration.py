import AerodynamicParameters
import PlanformParameters
import FuselageParameters
import SpeedsAndRange
import PropulsionParameters
import AerodynamicParameters
import WeightParameters
from math import sqrt,atan,tan,radians,cos,fabs, e



MaxNumberOfIterations = 10
ft_per_meter = 0.3048
Planform = PlanformParameters.Planform()
Fuselage = FuselageParameters.Fuselage()
Miscellaneous = SpeedsAndRange.Miscellaneous()
Propulsion = PropulsionParameters.Propulsion()
Aerodynamics = AerodynamicParameters.Aerodynamics()
Weight = WeightParameters.Weight()


def ClassIWeightEstimation():
    Req = (Miscellaneous.Rnom + Miscellaneous.Rlost)*(1+Miscellaneous.fcon) + 1.2*Miscellaneous.Rdiv + (Miscellaneous.tE*Miscellaneous.Velocity)/1000 #km, equivalent range
    f_MTOW = 1 - e **(-Req/(1000*Propulsion.nj*Propulsion.ef*Aerodynamics.LD/9.80665)) #Fuel / MTOW ratio
    p_MTOW = 1 - Weight.OE_MTOW - f_MTOW #Payload / MTOW ratio
    MTOW = Weight.M_Payload / p_MTOW
    FuelMass = MTOW * f_MTOW #kg, fuel mass
    OEW = MTOW * Weight.OE_MTOW #kg, structural mass / operating empty
    f_landing = 1 - Miscellaneous.Rnom/Req * f_MTOW #Landing mass fraction
    Weight.updateMTOW(MTOW)
    Weight.updateM_fuel(FuelMass)
    Weight.updateOEW(OEW)
    MZFW = MTOW-FuelMass
    Weight.updateMZFW(MZFW)
def CalculateWingWeight():
    n_ult = CalculateLoadFactor()
    WingWeight = (Weight.MZFW*6.67/1000*Planform.b_s**0.75*(1+sqrt(Planform.b_ref/Planform.b_s))*n_ult**0.55*
                  (Planform.b_s/Planform.t_r*Planform.wing_area/Weight.MZFW)**0.3)*0.9


    return WingWeight
def CalculateTailWeight():
    n_ult = CalculateLoadFactor()
    TailWeight = 0.64*(n_ult*Planform.tail_area**2)**0.75
    return TailWeight
def CalculateAirframeStructuralWeight():
    n_ult = CalculateLoadFactor()
    StructuralWeight = Weight.MTOW*sqrt(1.5*n_ult)*(Fuselage.b_f*Fuselage.h_f*Fuselage.l_f/Weight.MTOW)**0.24*0.447
    return StructuralWeight
def CalculateBodyWeight():
    BodyWeight = 0.23 * sqrt(Miscellaneous.V_dive_EAS * Fuselage.l_t / (Fuselage.b_f + Fuselage.h_f)) * Fuselage.S_f_wet ** 1.2
    return BodyWeight
def CalculateLandingGearWeight():
    A_main = 40
    A_nose = 20
    B_main = 0.16
    B_nose = 0.1
    C_main = 0.019
    C_nose = 0
    D_main = 1.5 * 10 ** (-5)
    D_nose = 2 * 10 ** (-6)
    W_main = 1.08 * (A_main + B_main * (Weight.MTOW / 0.453592) ** 0.75 + C_main * (Weight.MTOW / 0.453592) + D_main * (
            Weight.MTOW / 0.453592) ** 1.5)
    W_nose = 1.08 * (A_nose + B_nose * (Weight.MTOW / 0.453592) ** 0.75 + C_nose * Weight.MTOW / 0.453592 + D_nose * (
                Weight.MTOW / 0.453592) ** 1.5)
    LandingGearWeight = (W_main+W_nose)*0.453592
    return LandingGearWeight

def CalculateSurfaceControlsWeight():
    SurfaceControlsWeight = 0.64 * 1.2 * 0.768 * Weight.MTOW ** 0.666667
    return SurfaceControlsWeight

def CalculateNacelleWeight():
    NacelleWeight = 0.065*0.453592*0.4*Weight.MTOW
    return NacelleWeight

def CalculatePropulsionGroup():
    EngineWeight = 1040
    NoEngines = 2
    PropulsionWeight = 1.15*1.18*EngineWeight * NoEngines*0.453592**2
    return PropulsionWeight

def CalculateAirframeServicesAndEquipmentWeight():
    W_ba = 0.4 * 85.34
    W_APU = 11.7 * (W_ba ** 0.6)

    # LOW_SUBSONIC
    W_INE_1 = 54.4 + 9.1 * 2 + 0.006 * Weight.MTOW

    # HIGH_SUBSONIC
    W_INE_2 = 0.347 * Weight.OEW ** (5 / 9) * Miscellaneous.Range ** 0.25

    W_HPE = 0.011 * Weight.OEW + 181

    W_EL = 0.02 * Weight.MTOW + 181

    W_furnish = 0.196 * Weight.MZFW ** 0.91

    W_air_conditioning = 14 * (19.44 ** 1.28)

    W_misc = 0.01 * Weight.OEW

    W_airframe_services = W_ba + W_APU + W_INE_1 + W_EL + W_furnish + W_air_conditioning + W_misc  # Excludes fuel and passengers

    return W_airframe_services
def CalculateLoadFactor():
    u_hat = Miscellaneous.GustVelocity * ft_per_meter  # m/s

    mu = 2 * Planform.WingLoading / Miscellaneous.densityFL / 9.81 / Aerodynamics.CL_alpha / Planform.MAC

    K = 0.88 * mu / (5.3 + mu)

    u = K * u_hat

    # MAXIMUM LOAD FACTOR
    n_max = 1 + Miscellaneous.densityFL * Miscellaneous.Velocity * Aerodynamics.CL_alpha * u / 2 / Planform.WingLoading
    n_ult = 1.5 * n_max

    return n_ult

def ClassIIWeightEstimation ():

    AirframeStructuralWeight = CalculateAirframeStructuralWeight()
    n_ult = CalculateLoadFactor()
    WingGroupWeight = CalculateWingWeight()
    BodyGroupWeight = CalculateBodyWeight()
    TailGroupWeight = CalculateTailWeight()
    LandingGearWeight = CalculateLandingGearWeight()
    SurfaceControlsWeight = CalculateSurfaceControlsWeight()
    NacelleWeight = CalculateNacelleWeight()
    PropulsionWeight = CalculatePropulsionGroup()
    AirframeServicesAndEquipmentWeight = CalculateAirframeServicesAndEquipmentWeight()
    OEWnew = (WingGroupWeight + TailGroupWeight + BodyGroupWeight + LandingGearWeight +
              SurfaceControlsWeight + NacelleWeight + PropulsionWeight + AirframeServicesAndEquipmentWeight)
    MTOWnew = OEWnew + Weight.M_fuel + Weight.M_Payload


    print("LoadFactor", n_ult )
    print("WingGroupWeight", WingGroupWeight)
    print("BodyGroupWeight", BodyGroupWeight)
    print("TailGroupWeight", TailGroupWeight)
    print("LandingGearWeight", LandingGearWeight)
    print("SurfaceControlsWeight", SurfaceControlsWeight)
    print("NacelleWeight", NacelleWeight)
    print("PropulsionWeight", PropulsionWeight)
    print("AirframeServices", AirframeServicesAndEquipmentWeight)

    print("RandomTorenbeekEstimate", AirframeStructuralWeight)
    print ("OEWnew = ", OEWnew)
    print ("OEW_init = ", Weight.OEW)
    print ("MTOWnew = ", MTOWnew)
    print("MTOW_init = ", Weight.MTOW)
    '''ratio = fabs(OEWnew - OEW)/OEW
    if (iterationNumber <=MaxNumberOfIterations and ratio>0.0001):
        iterationNumber = iterationNumber + 1
        MZFW = MTOWnew - M_fuel
        ClassIIWeightEstimation(Planform, Fuselage, MTOWnew, OEWnew, M_fuel_init, MZFW, Miscellaneous, iterationNumber)'''
    Weight.updateMTOW(MTOWnew)
    Weight.updateOEW(OEWnew)
    Weight.updateMZFW(MTOWnew-Weight.M_fuel)
    Weight.updateOE_MTOW(OEWnew/MTOWnew)
    return OEWnew, MTOWnew,


def WeightIteration(iterationNumber):
    ClassIWeightEstimation()
    print(" ")
    print("iterationNumber", iterationNumber)
    ClassIIWeightEstimation()
    if (iterationNumber <= MaxNumberOfIterations):
        iterationNumber = iterationNumber + 1
        WeightIteration(iterationNumber)







#ClassIIWeightEstimation(Planform, Fuselage, MTOW_init, OEW_init, M_fuel_init, MZFW_init, Miscellaneous)
n_ult_print = CalculateLoadFactor()

WeightIteration(1)
print("n_ult", n_ult_print)





