from math import sqrt,atan,tan,radians,cos, pi, degrees

import WeightParameters
Weight = WeightParameters.Weight()
class Planform:
    def __init__(self):
            self.WingLoading = 3600
            self.wing_area = Weight.MTOW/(self.WingLoading/9.80665)
            self.MAC = 2.915
            self.yMAC = 4.895
            self.xMAC = 1.446
            self.c_r = 4.41
            self.c_t = 1.93
            self.taper = 0.352
            self.b = 23.3
            self.t_over_c = 0.1
            self.t_r = self.c_r * self.t_over_c
            self.sweep_le = 16.46 #deg
            self.sweep_half = degrees(atan(tan(radians(self.sweep_le)) - self.c_r / self.b * (1 - self.taper))) #deg
            self.sweep_quarter_chord=degrees(atan(tan(radians(self.sweep_le))-self.c_r/2/self.b*(1-self.taper))) #deg
            self.b_s = self.b / cos(radians(self.sweep_half))
            self.b_ref = 1.905
            self.tail_area = 22  # m^2
            self.AR = 7.5
            self.dihedral=3-0.1*self.sweep_quarter_chord-2 #deg
            self.xc_m = 0.35
            self.beta = (1 - 0.77**2)**0.5
            self.CL_alpha = 2*pi*self.AR/(2+(4+((self.AR*self.beta/0.95)**2)*(1+(tan(self.sweep_half)/self.beta)**2))**0.5)
            self.xc_mHT = 0.3  # NACA0012
            self.xc_mVT = 0.3
            self.t_c_HT = 0.12
            self.t_c_VT = 0.12

