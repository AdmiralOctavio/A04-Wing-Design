from math import sqrt,atan,tan,radians,cos

import PlanformParameters
import AerodynamicParameters
import WeightParameters
Planform = PlanformParameters.Planform()
Aerodynamics = AerodynamicParameters.Aerodynamics()
Weight = WeightParameters.Weight()

class Miscellaneous:
    def __init__(self):
            self.densitySL = 1.225
            self.densityFL = 0.379597
            self.GustVelocity = 66
            self.VcrM = 0.77  # mach
            self.M_app = 60.61/sqrt(1.4*287*288.15)
            self.Velocity = self.VcrM*296.32
            self.EASVelocity = self.Velocity/sqrt(self.densitySL/self.densityFL)
            self.V_dive_EAS=166.89*1.5
            self.V_stall = sqrt(2*Weight.MTOW*9.80665/(1.225*Planform.wing_area*Aerodynamics.CL_max_Landing))
            self.Range = 2963
            self.fcon = 0.05  # contingency fuel ratio
            self.Rdiv = 250  # km, divergence range
            self.Rnom = 2019  # km, Nominal
            self.tE = 2700  # loiter time
            self.hCR = 10668  # m, cruise height
            self.Mpl = 7200  # kg, design payload mass
            self.Rlost = (1 / 0.7 * Aerodynamics.LD * (self.hCR + self.Velocity ** 2 / (2 * 9.80665))) / 1000  # km, lost range from drag

            self.WingloadStartCr = (Weight.MTOW*9.80665)/Planform.wing_area
            self.WingloadEndCr = (Weight.MTOW*9.80665 - Weight.M_fuel*9.80665)/Planform.wing_area
            self.CL_cruise = 1.1/(0.5*self.densityFL*self.Velocity**2)*0.5*(self.WingloadStartCr + self.WingloadEndCr)

