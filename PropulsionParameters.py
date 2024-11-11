from math import sqrt,atan,tan,radians,cos,pi
import SpeedsAndRange

Misc = SpeedsAndRange.Miscellaneous()
class Propulsion:
    def __init__(self):
        self.BypassRatio = 6
        self.ef = 44
        self.TSFC = 22 * self.BypassRatio ** (-.19)
        self.nj = Misc.Velocity / self.TSFC / self.ef  # Jet efficiency
