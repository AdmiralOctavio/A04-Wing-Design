import math
import yaml

#Taken from ADSEE II Slides
#Delta Cl (For airfoil!):
Plain = 0.9
Slotted = 1.3
Fowler = 1.3 #c' / c
Double_Slotted = 1.6 #c' / c
Triple_Slotted = 1.9# c' / c

Fixed_Slot = 0.2
Leading_edge = 0.3
Kruger = 0.3
Slat = 0.4 #c' / c

#For full wing
CL_takeoff = 1.9
CL_landing = 2.3

deplLanding = 35 #Degrees
deplTakeoff = 15 #Degrees

#Global parameters used in other files
with open("aircraft_parameters.yaml") as file:
   aircraft_parameters = yaml.safe_load(file)
AR = aircraft_parameters['aspect_ratio']
ZL = aircraft_parameters['zero_lift_drag_coefficient_estimation']
e = ZL['euler_efficiency']

def LiftCoefficient(Slat, Flap, Cl, Sf): 
    #Slat, Flap, Cl
    #Flap dCl is localised to the region where its acting, S'/S fraction has to be included (Sf).
    ClTot = Slat + (Flap * Sf) + Cl
    #Official eq: dCL = 0.9 * dCl * Swf/Sw * cos(HingeAngle)
    #Interpreted: CL = [ 1 + ClTot/(AR * math.pi * e) ] * ClTot * Swf/Sw * cos(HingeAngle)
    #0.9 coefficient is probably from 1 + ClTot/(AR * math.pi * e)
    #What is Swf/Sw and Hinge Angle ??
    return ClTot / (1 + ClTot/(AR * math.pi * e) )

ClVal1 = []
ClVal2 = []
for i in range(50, 100, 5):
    #ClVal1.append(LiftCoefficient(Slat, Plain, 1.598, i/100))
    ClVal2.append(LiftCoefficient(Slat, Double_Slotted, 1.323, i/100))

    #print(str(ClVal1[int((i-50)/5)]) + " " + str(i) + "%  | 1")
    print(str(  round(ClVal2[int((i-50)/5)], 3)  ) + " " + str(i) + "%")
    #print("\n")
