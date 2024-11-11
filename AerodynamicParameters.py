from math import sqrt,atan,tan,radians,cos,pi
import PlanformParameters
Planform = PlanformParameters.Planform()
class Aerodynamics:
    def __init__(self):
            self.CL_alpha = 5.76
            self.Cd0clean = 0.0192  # zero lift drag coef
            self.OswaldEfficiencyclean = 0.8280596821832961  # Oswald
            self.LD = 1 / 2 * sqrt((pi * Planform.AR * self.OswaldEfficiencyclean) / self.Cd0clean)  # Lift drag ratio
