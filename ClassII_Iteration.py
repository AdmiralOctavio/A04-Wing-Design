
from math import sqrt,atan,tan,radians,cos,fabs, e



MaxNumberOfIterations = 10
ft_per_meter = 0.3048



def ClassIWeightEstimation(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
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
def CalculateWingWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    n_ult = CalculateLoadFactor(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
    WingWeight = (Weight.MZFW*6.67/1000*Planform.b_s**0.75*(1+sqrt(Planform.b_ref/Planform.b_s))*n_ult**0.55*
                  (Planform.b_s/Planform.t_r*Planform.wing_area/Weight.MZFW)**0.3)*0.9
    Weight.updateWingGroupWeight(WingWeight)
def CalculateTailWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    n_ult = CalculateLoadFactor(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
    TailWeight = 0.64*(n_ult*(Planform.HT_area+Planform.VT_area)**2)**0.75
    Weight.updateTailGroupWeight(TailWeight)

def CalculateAirframeStructuralWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    n_ult = CalculateLoadFactor(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
    StructuralWeight = Weight.MTOW*sqrt(1.5*n_ult)*(Fuselage.b_f*Fuselage.h_f*Fuselage.l_f/Weight.MTOW)**0.24*0.447
    Weight.updateAirframeStructuralWeight(StructuralWeight)
def CalculateBodyWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    BodyWeight = 0.23 * sqrt(Miscellaneous.V_dive_EAS * Fuselage.l_t / (Fuselage.b_f + Fuselage.h_f)) * Fuselage.S_f_wet ** 1.2
    Weight.updateBodyGroupWeight(BodyWeight)
def CalculateLandingGearWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
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
    Weight.updateLandingGearWeight(LandingGearWeight)
    Weight.updateW_nose(W_nose)

def CalculateSurfaceControlsWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    SurfaceControlsWeight = 0.64 * 1.2 * 0.768 * Weight.MTOW ** 0.666667
    Weight.updateSurfaceControlsWeight(SurfaceControlsWeight)

def CalculateNacelleWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    NacelleWeight = 0.065*0.453592*0.4*Weight.MTOW
    Weight.updateNacelleWeight(NacelleWeight)

def CalculatePropulsionGroup(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    EngineWeight = 1040
    NoEngines = 2
    PropulsionWeight = 1.15*1.18*EngineWeight * NoEngines*0.453592**2
    Weight.updatePropulsionWeight(PropulsionWeight)

def CalculateAirframeServicesAndEquipmentWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
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

    Weight.updateAirframeServicesAndEquipmentWeight(W_airframe_services)
def CalculateLoadFactor(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    u_hat = Miscellaneous.GustVelocity * ft_per_meter  # m/s

    mu = 2 * Planform.WingLoading / Miscellaneous.densityFL / 9.81 / Aerodynamics.CL_alpha / Planform.MAC

    K = 0.88 * mu / (5.3 + mu)

    u = K * u_hat

    # MAXIMUM LOAD FACTOR
    n_max = 1 + Miscellaneous.densityFL * Miscellaneous.Velocity * Aerodynamics.CL_alpha * u / 2 / Planform.WingLoading
    n_ult = 1.5 * n_max

    return n_ult

def ClassIIWeightEstimation (Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):

    CalculateAirframeStructuralWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculateLoadFactor(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculateWingWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculateBodyWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculateTailWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculateLandingGearWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculateSurfaceControlsWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculateNacelleWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculatePropulsionGroup(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    CalculateAirframeServicesAndEquipmentWeight(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    OEWnew = (Weight.WingGroupWeight + Weight.TailGroupWeight + Weight.BodyGroupWeight + Weight.LandingGearWeight +
              Weight.SurfaceControlsWeight + Weight.NacelleWeight + Weight.PropulsionWeight + Weight.AirframeServicesAndEquipmentWeight)

    MTOWnew = OEWnew + Weight.M_fuel + Weight.M_Payload



    print("WingGroupWeight", Weight.WingGroupWeight)
    print("BodyGroupWeight", Weight.BodyGroupWeight)
    print("TailGroupWeight", Weight.TailGroupWeight)
    print("LandingGearWeight", Weight.LandingGearWeight)
    print("SurfaceControlsWeight", Weight.SurfaceControlsWeight)
    print("NacelleWeight", Weight.NacelleWeight)
    print("PropulsionWeight", Weight.PropulsionWeight)
    print("AirframeServices", Weight.AirframeServicesAndEquipmentWeight)

    print("RandomTorenbeekEstimate", Weight.AirframeStructuralWeight)
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


def CGPositions (Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    x_f = 0.435 * Fuselage.l_f
    x_tail = 0.9 * Fuselage.l_f # Subject to change
    x_nose = 0.5 * Planform.MAC
    x_airframe_services = x_f

    x_wing = 0.07 * Planform.b / 2 * tan(radians(Planform.sweep_le)) + (0.2 + 0.7 * 0.4) * (Planform.c_r - Planform.c_r * (1 - Planform.taper) * 0.35)
    x_nacelle = -0.1 * Propulsion.l_nac  # w.r.t. the xLEMAC
    x_prop = -0.4 * Propulsion.l_nac

    W_fuselage_group = Weight.BodyGroupWeight + Weight.W_nose + Weight.TailGroupWeight + Weight.AirframeServicesAndEquipmentWeight  # Excludes main LG
    X_fuselage_group = ( Weight.BodyGroupWeight * x_f + x_tail * Weight.TailGroupWeight + x_nose * Weight.W_nose + x_airframe_services * Weight.AirframeServicesAndEquipmentWeight ) / W_fuselage_group
    W_wing_group = Weight.WingGroupWeight + Weight.NacelleWeight + Weight.PropulsionWeight
    X_wing_group = (Weight.WingGroupWeight * x_wing + Weight.NacelleWeight * x_nacelle + Weight.PropulsionWeight * x_prop) / W_wing_group

    X_OE = 0.225 * Planform.MAC
    X_LEMAC = X_fuselage_group - X_OE + W_wing_group / W_fuselage_group * ((X_wing_group - X_OE))
    x_wg = (0.2 + 0.7 * (0.6 - 0.2)) * Planform.MAC + tan(Planform.sweep_le * 3.14 / 180) * 0.35 * Planform.b / 2 - Planform.b / 6 * (
                (1 + 2 * Planform.taper) / 1 + Planform.taper) * tan(Planform.sweep_le * 3.14 / 180) + X_LEMAC




'''def WeightIteration(iterationNumber):
    ClassIWeightEstimation()
    print(" ")
    print("iterationNumber", iterationNumber)
    ClassIIWeightEstimation()
    if (iterationNumber <= MaxNumberOfIterations):
        iterationNumber = iterationNumber + 1
        WeightIteration(iterationNumber)'''







#WeightIteration(1)






