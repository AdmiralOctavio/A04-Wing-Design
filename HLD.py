import math
import yaml

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

def LiftCoefficient(Slat, Flap, Cl): 
    #Slat, Flap, Cl
    ClTot = Slat + Flap + Cl
    CL = ClTot / (1 + ClTot/(AR * math.pi * e) )
    return CL
print(LiftCoefficient(0.4, 0.9, 1))