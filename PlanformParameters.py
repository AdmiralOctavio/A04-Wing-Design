from math import sqrt,atan,tan,radians,cos,pi

import WeightParameters
Weight = WeightParameters.Weight()
class Planform:
    def __init__(self):
            self.MAC =2.915
            self.yMAC = 4.895
            self.xMAC = 1.446
            self.c_r = 4.41 
            self.c_t = 1.93 
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
            self.tail_area = 22 #m^2
            self.AR = 7.5
    
    def updateC_r(self, c_r): self.c_r = c_r
    def updateC_t(self, c_t): self.c_t = c_t
    def updateMAC(self, MAC): self.MAC = MAC
    def updateyMAC(self, yMAC): self.yMAC = yMAC
    def updatexMAC(self, xMAC): self.xmAC = xMAC
    def updateTaper(self, Taper): self.Taper = Taper
    def updateb(self, b): self.b = b
    def updatet_over_c(self, t_over_c): self.t_over_c = t_over_c
    def updatewing_area(self, wing_area): self.wing_area = wing_area
    def updatesweep_le(self, sweep_le): self.sweep_le = sweep_le
    def updateb_s(self, b_s): self.b_s = b_s
    def updatetail_area(self, tail_area): self.tail_area = tail_area
    def updateAR(self, AR): self.AR = AR