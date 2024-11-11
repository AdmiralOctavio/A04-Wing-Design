from math import sqrt,atan,tan,radians,cos

import WeightParameters
Weight = WeightParameters.Weight()
class Planform:
    def __init__(self):
            self.MAC =2.915
            self.yMAC = 4.895
            self.xMAC = 1.446
            self.c_r = 4
            self.taper = 0.352
            self.b = 23.3
            self.t_over_c = 0.1
            self.wing_area = 63.1
            self.t_r = self.c_r*self.t_over_c
            self.sweep_le = 16.46
            self.sweep_half = atan(tan(radians(self.sweep_le))-self.c_r/self.b*(1-self.taper))
            self.b_s = self.b/cos(self.sweep_half)
            self.b_ref = 1.905
            self.WingLoading = Weight.MTOW/63.1*9.81
            self.CL_alpha = 5.76
            self.tail_area = 22 #m^2

