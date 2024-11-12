from math import sqrt,atan,tan,radians,cos,pi

import PlanformParameters
Planform = PlanformParameters.Planform()

class Aerodynamics:
    def __init__(self):
            self.CL_alpha = 5.76
            #self.Cd0clean = 0.0192  # zero lift drag coef AT CRUISE
            #self.OswaldEfficiencyclean = 0.8280596821832961  # Oswald
            #self.LD = 1 / 2 * sqrt((pi * Planform.AR * self.OswaldEfficiencyclean) / self.Cd0clean)  # Lift drag ratio

            self.CL_max_Landing = 2.3
            self.CL_max_Takeoff = 1.9
            self.CL_max_Cruise = 1.5

            self.CD0_Landing_DOWN = 0.0822  #Landing = flap cnfiguration, DOWN = gear
            self.CD0_Landing_UP = 0.0647
            self.CD0_Takeoff_DOWN = 0.0562
            self.CD0_Takeoff_UP = 0.0387
            self.CD0_Clean_UP = 0.0192 #Zero lift drag coefficient, clean, at SEA LEVEL
            self.CD0_Cruise = 0.0192 #Zero lift drag coefficient, clean, at CRUISE

            self.e_Takeoff = 0.892    #for different flap configurations
            self.e_Landing = 0.984
            self.e_Clean = 0.8280596821832961

            self.LD = 1 / 2 * sqrt((pi * Planform.AR * self.e_Clean) / self.CD0_Cruise)  # Lift drag ratio

class DragBuildup:
    def __init__(self):
            self.IFtail = 1.04
            self.IFwing = 1.0
            self.IFfuselage = 1.0
            self.IFnacelle = 1.3

            self.S_Anose = 0.26711  # m^2 (frontal area of nose gear)
            self.S_Agear = 0.80149  # m^2 (frontal area of landing gear)
            self.D_nose = 18*0.0254  # m tire diameter
            self.D_main = 33*0.0254  # m tire diameter
            self.W_nose = 4.25*0.0254  # m tire width
            self.W_main = 9.75*0.0254  # m tire width
            self.Nose_x = 8.06  # m nose gear x-position
            self.strut = 1.56  # m nose gear strut length
            self.DeltaCDs = 0.58  # from graph for nose gear

            self.CD_excrFrac = 0.05