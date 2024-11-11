import math
import os

import yaml
import Wing_aerodynamics_design as W
#Go to bottom of program if you want to check different configurations

Cr = 4.41 #m
Ct = 1.39 #m

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

def LiftCoefficient(Slat, Flap, alpha, Cr, Ct):
    os.makedirs("output/hld", exist_ok=True)
    #f = open("output/hld/HLD_Data_" + str(Slat[1]) + str(Flap[1]) + ".txt", "w")
    #f.write(" CL:          Wf:       Alpha Stall:       Alpha:        Flap Root Chord:      Flap Tip Chord: \n")
    CLValues = [] 
    Cl = alpha * (1.0918 - 0.1143)/8.5 + 0.1143
    for Wf in range(50,100,1):
        #ClTot = Slat[0] + (Flap[0] * Wf/100) + Cl #Maths
        SwfS_TE = (2*Cr - (Wf/100)*(Cr-Ct))/(Cr+Ct) * (Wf/100)
        SwfS_LE = 0.97

        dCL_TE = 0.9 * SwfS_TE * Flap[0] * math.cos(math.radians(16.9))
        dCL_LE = 0.9 * SwfS_LE * Slat[0] * math.cos(math.radians(24))

        dCL = dCL_LE + dCL_TE
        CL_wing = Cl / (1 + (Cl)/(math.pi * AR * e))
        CL_max = CL_wing + dCL
        CLValues.append(CL_max)
        
        dAlpha_L = -15 * SwfS_TE * math.cos(math.radians(16.9))
        Alpha_stall = 19.32 + dAlpha_L

        #This is just for a nice output
        ind = Wf-50
        CL = ("%.4f" % round(CLValues[ind],3))
        WF = ("%.0f" % round(Wf,3))
        FCHORD =("%.3f" % (W.MAC_flap(Wf/100)[0]*0.35) )
        FCHORD_2 = ("%.3f" % (W.MAC_flap(Wf/100 + 0.5)[1]*0.35) )
        DC = ("%.3f" % (float(FCHORD) * 0.5)) #I forgot what this does but dont delete it
        A = ("%.3f" % (float(Alpha_stall)))

        '''Legacy code, dont remove probably idk
        if round(CLValues[ind], 3) >= 2.3:
            full = CL + "*       " + WF + "%           " + A +  "             "+ str(alpha) + "deg              " + FCHORD + "m                " + FCHORD_2 + "m \n"

        else: full = CL + "        " + WF + "%           " + A + "             "+ str(alpha) + "deg              " + FCHORD +  "m                " + FCHORD_2 + "m \n"

        f.writelines(full) 
        '''
        if round(CLValues[ind], 3) >= 2.375 and Alpha_stall < alpha:
            print("Max CL = " + CL + ",  Wing Fraction = " + WF + "%,  Stalling AOA = " + A +  "deg,  AOA = "+ str(alpha) + "deg,  Flap Cr = " + FCHORD + "m,  Flap Ct = " + FCHORD_2 + "m \n")
            break

LiftCoefficient(Slat, Double_Slotted, 8.2, Cr, Ct)
#Just input configuration here! ^^^^
'''For iteration, change values of Cr and Ct. You can also iterate through alpha (8.2 value)'''