from math import sqrt,atan,tan,radians,cos,pi

import SpeedsAndRange
import WeightParameters

Miscellaneous = SpeedsAndRange.Miscellaneous()
Weight = WeightParameters.Weight()

class Propulsion:
    def __init__(self):
        self.BypassRatio = 6
        self.ef = 44
        self.TSFC = 22 * self.BypassRatio ** (-.19)
        self.nj = Miscellaneous.Velocity / self.TSFC / self.ef  # Jet efficiency
        self.Thrust_to_Weight = 0.4
        self.Thrust = (self.Thrust_to_Weight*9.80665)*Weight.MTOW
        self.l_nac = 1.9  # m nacelle length
        self.d_nacelle = 1.08  # m max diameter

    def updateTtoW(self,Thrust_to_Weight):
        self.Thrust_to_Weight = Thrust_to_Weight