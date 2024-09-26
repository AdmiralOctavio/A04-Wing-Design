import math
import os

import yaml
import Wing_aerodynamics_design as W
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

'''
    dc / cf = 0.5 for Double slotted and 0.7 for Fowler
    Calculate cf??
    Surface area of wings = 63.1m^2
    Extra area required by flaps = 63.1 * (1-Sf)
    Af = dc/cf * Wf (maybe?? probably not???)
'''

def LiftCoefficient(Slat, Flap, Cl):
    f = open("HLD_Data_" + str(Slat[1]) + str(Flap[1]) + ".txt", "w")

def LiftCoefficient(Slat, Flap, Cl, dccf):
    os.makedirs("output/hld", exist_ok=True)
    f = open("output/hld/HLD_Data_" + str(Slat[1]) + str(Flap[1]) + ".txt", "w")
    f.write(" CL:          Wf:       W. Area Ratio:       Delta Chord:        Flap Root Chord:      Flap Tip Chord: \n")

    for Wf in range(50, 100, 5):
        #ClTot = Slat[0] + (Flap[0] * Wf/100) + Cl #Maths
        dCl =  Slat[0] + (Flap[0] * Wf/100)
        CLValues = [] 
        Swf = []
        for i in range (10):
            Swf.append((i / 100) + 1)
            CLValues.append( ( dCl / ( 1 + dCl/( AR * math.pi * e ) ) ) * Swf[i] * math.cos(math.radians(16.9)) + (Cl/(1+Cl/( AR * math.pi * e ))) )  #Also maths 
        #This is just for a nice output
        for j in range(10):

            CL = ("%.3f" % round(CLValues[j], 3))
            WF = ("%.0f" % round(Wf,3))
            SWF = ("%.2f" % round(Swf[j],3))
            FCHORD =("%.3f" % (W.MAC_flap(Wf/100)[0]*0.35) )
            FCHORD_2 = ("%.3f" % (W.MAC_flap(Wf/100)[1]*0.35) )
            DC = ("%.3f" % (float(FCHORD) * 0.5))

            if round(CLValues[j], 3) >= 2.3:
                full = CL + "*        " + WF + "%           " + SWF +"               "+ DC + "m                " + FCHORD + "m                " + FCHORD_2 + "m \n"

            else: full = CL + "         " + WF + "%           " + SWF +"               "+ DC + "m                " + FCHORD +  "m                " + FCHORD_2 + "m \n"

            f.writelines(full) 

        f.write("\n" * 2)

LiftCoefficient(Slat, Double_Slotted, 1.323)
#Just input configuration here! ^^^^
#Check HLD_Data.txt for results 