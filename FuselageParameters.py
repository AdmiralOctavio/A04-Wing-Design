from math import sqrt,atan,tan,radians,cos

import PlanformParameters
Planform = PlanformParameters.Planform()

class Fuselage:
    def __init__(self):
            self.b_f = 2.9
            self.h_f = 2.9
            self.fineness = 4.5
            self.l_f = 31.93
            self.l_t = (0.9*self.l_f) -(13.5288-0.42*Planform.b/2*tan(radians(Planform.sweep_le))+0.25*Planform.MAC)
            self.S_f_wet = 3.14 * self.b_f * self.l_f * (1 - 2 / self.fineness) ** 0.666667 * (1 + 1 / self.fineness ** 2)

