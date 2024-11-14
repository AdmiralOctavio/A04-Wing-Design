from math import sqrt,atan,tan,radians,cos


class Fuselage:
    def __init__(self):
            self.b_f = 2.9
            self.h_f = 2.9
            self.fineness = 4.5
            self.l_f = 31.93
            self.S_f_wet = 3.14 * self.b_f * self.l_f * (1 - 2 / self.fineness) ** 0.666667 * (1 + 1 / self.fineness ** 2)
            self.upsweep = radians(5.0)
            self.tc_ratio = 2.5
            self.nc_ratio = 1.8
            self.d_fus_outer = 2.9046338716900144
            self.d_fus_inner = 2.6991711690813536
            self.l_tc = self.tc_ratio*self.d_fus_outer
            self.l_nc = self.nc_ratio*self.d_fus_outer
            self.l_cabin = self.l_f-self.l_nc-self.l_tc
            #the next 2 were chosen just because they looked good on the CAD, so this may be an issue
            # self.X_h = 31.628
            # self.X_v = 30.202
            self.X_h = 33.333
            self.X_v = 30.349
