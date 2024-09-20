import math
import yaml
#Go to bottom of program if you want to check different configurations

#Taken from ADSEE II Slides
#Delta Cl (For airfoil!):
Plain = (0.9, "Plain")
Slotted = (1.3,"Slotted")
Fowler = (1.3, "Fowler") #c' / c
Double_Slotted = (1.6, "Double_Slotted") #c' / c
Triple_Slotted = (1.9, "Triple_Slotted")# c' / c

Fixed_Slot = (0.2, "Fixed_Slot")
Leading_edge = (0.3,"Leading_edge")
Kruger = (0.3, "Kruger")
Slat = (0.4, "Slat") #c' / c

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

'''
    Flap dCl is localised to the region where its acting, S'/S fraction has to be included (Sf).
    Official eq: dCL = 0.9 * dCl * Swf/Sw * cos(HingeAngle)
    Interpreted: CL = [ 1 + ClTot/(AR * math.pi * e) ] * ClTot * Swf/Sw * cos(HingeAngle)
    0.9 coefficient is probably from 1 + ClTot/(AR * math.pi * e)
'''
def LiftCoefficient(Slat, Flap, Cl):
    f = open("HLD_Data_" + str(Slat[1]) + str(Flap[1]) + ".txt", "w")
    f.write("CL:         Wing Fraction:       Wetted Area Ratio: \n")

    for Wf in range(50, 100, 5):
        ClTot = Slat[0] + (Flap[0] * Wf/100) + Cl #Maths 
        CLValues = [] 
        Swf = []

        for i in range (10):
            Swf.append((i / 100) + 1)
            CLValues.append( ( ClTot / ( 1 + ClTot/( AR * math.pi * e ) ) ) * Swf[i] * math.cos(math.radians(16.9))) #Also maths

        #This is just for a nice output
        for j in range(10):

            if round(CLValues[j], 3) >= 2.3:
                full = ("%.3f" % round(CLValues[j], 3)) + "*            " + str(Wf) + "%                  " + str(Swf[j]) + "\n"

            else: full = ("%.3f" % round(CLValues[j], 3)) + "             " + str(Wf) + "%                  " + str(Swf[j]) + "\n"

            f.writelines(full) 

        f.write("\n" * 2)

LiftCoefficient(Kruger, Double_Slotted, 1.323)
#Just input configuration here! ^^^^
#Check HLD_Data.txt for results 