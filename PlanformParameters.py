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
            self.c_r = 4.004
            self.c_t = 1.413
            self.taper = 0.352
            self.b = 23.3
            self.t_over_c = 0.1
            self.t_r = self.c_r * self.t_over_c
            self.sweep_le = 16.46 #deg
            self.sweep_half = degrees(atan(tan(radians(self.sweep_le)) - self.c_r / self.b * (1 - self.taper))) #deg
            self.sweep_quarter_chord=degrees(atan(tan(radians(self.sweep_le))-self.c_r/2/self.b*(1-self.taper))) #deg
            self.sweep_te = degrees(atan(tan(radians(self.sweep_le)) - 2*self.c_r / self.b * (1 - self.taper)))
            self.b_s = self.b / cos(radians(self.sweep_half))
            self.b_ref = 1.905
            self.AR = 7.5
            self.dihedral=3-0.1*self.sweep_quarter_chord-2 #deg
            self.y1ail = 0.65
            self.y2ail = 0.95
            self.xc_m = 0.35
            self.beta = (1 - 0.77**2)**0.5
            self.CL_alpha = 2*pi*self.AR/(2+(4+((self.AR*self.beta/0.95)**2)*(1+(tan(self.sweep_half)/self.beta)**2))**0.5)

            self.xc_mHT = 0.3  # NACA0012
            self.xc_mVT = 0.3
            self.t_c_HT = 0.12
            self.t_c_VT = 0.12

            self.HT_area = 12.001354834160356
            self.HT_span = 7.183719495281641
            self.HT_cr = 2.3365488682002415
            self.HT_ct = 1.004716013326104
            self.HT_MAC = 1.7591108472058603
            self.HT_AR = 4.3
            self.HT_taper = 0.43
            self.HT_quarter_sweep = 26.6 #deg

            self.VT_area = 7.047964254292777
            self.VT_span = 2.908187952
            self.VT_cr = 2.8511646488775373
            self.VT_ct = 1.995815254214276
            self.HT_MAC = 2.4486472866830615
            self.VT_AR = 1.2
            self.VT_taper = 0.7
            self.VT_quarter_sweep = 39.5 #deg

            self.FlapAreaRatio = 0.7768427586206897
            self.FlapChordRatio = 0.35
            self.FlapDeflectionTO = 15 #deg
            self.FlapDeflectionL = 35 #deg





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

    def updatesweep_half(self, sweep_half): self.sweep_half = sweep_half

    def updatesweep_quarter_chord(self, sweep_quarter_chord): self.sweep_quarter_chord = sweep_quarter_chord

    def updatesweep_le(self, sweep_te): self.sweep_te = sweep_te

    def updateb_s(self, b_s): self.b_s = b_s

    def updateb_ref(self, b_ref): self.b_ref = b_ref

    def updatet_r(self, t_r): self.t_r = t_r

    def updateAR(self, AR): self.AR = AR

    def updateWingLoading(self,WingLoading): self.WingLoading = WingLoading

    def updatedihedral(self, dihedral): self.dihedral = dihedral

    def updateCL_alpha(self, CL_alpha): self.CL_alpha = CL_alpha

    def updatey1ail(self,y1ail):
        self.y1ail = y1ail
    def updatey2ail(self,y2ail):
        self.y2ail = y2ail