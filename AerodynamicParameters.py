from math import sqrt,atan,tan,radians,cos,pi


class Aerodynamics:
    def __init__(self):
            self.CL_alpha = 5.76

            self.cd0airfoil = 0.00486
            self.clCruiseAirfoil = 0.4756492527004301
            self.clCruise = 0.37594287624283806

            self.CL_max_Landing = 2.3
            self.CL_max_Takeoff = 1.9
            self.CL_max_Cruise = 2.291372534

            self.CD0_Landing_DOWN = 0.0822  #Landing = flap cnfiguration, DOWN = gear
            self.CD0_Landing_UP = 0.0647
            self.CD0_Takeoff_DOWN = 0.0562
            self.CD0_Takeoff_UP = 0.0387
            self.CD0_Cruise = 0.0192 #Zero lift drag coefficient, clean, at CRUISE
            self.CD0_Clean_UP = 0.026470848979104598

            self.e_Takeoff = 0.892    #for different flap configurations
            self.e_Landing = 0.984
            self.e_Clean = 0.8280596821832961

            self.Cf_nose_app = 0.00454
            self.Cf_cyl_app = 0.00165
            self.Cf_cone_app = 0.00191
            self.Cf_fus_app = 0.00207
            self.Cf_W_app = 0.00266
            self.Cf_HT_app = 0.00284
            self.Cf_VT_app = 0.00135
            self.Cf_eng_app = 0.00615
            self.Cf_tot_app = 0.00289

            self.Cf_nose_cr = 0.00417
            self.Cf_cyl_cr = 0.00152
            self.Cf_cone_cr = 0.00176
            self.Cf_fus_cr = 0.00190
            self.Cf_W_cr = 0.00236
            self.Cf_HT_cr = 0.00252
            self.Cf_VT_cr = 0.00120
            self.Cf_eng_cr = 0.00564
            self.Cf_tot_cr = 0.00262

            self.S_nose = 32.6
            self.S_cyl = 177.11
            self.S_cone = 33.72
            self.S_fus = 243.44
            self.S_W = 135.02
            self.S_HT = 30.78
            self.S_VT = 16.6
            self.S_eng = 12.89
            self.S_tot = 438.74

            self.IFtail = 1.04
            self.IFwing = 1.0
            self.IFfuselage = 1.0
            self.IFnacelle = 1.3

            self.S_Anose = 0.17057  # m^2 (frontal area of nose gear)
            self.S_Agear = 0.55643  # m^2 (frontal area of landing gear)
            self.D_nose = 18*0.0254  # m tire diameter
            self.D_main = 33*0.0254  # m tire diameter
            self.W_nose = 4.25*0.0254  # m tire width
            self.W_main = 9.75*0.0254  # m tire width
            self.Nose_x = 8.06  # m nose gear x-position
            self.strut = 1.56  # m nose gear strut length
            self.DeltaCDs = 0.58  # from graph for nose gear

            self.CD_excrFrac = 0.05
            self.CD_cruise = 0.03267672670773851

            self.LD = 15.6  # Lift drag ratio
            self.alphaStall = 19.32
            self.alphaZeroLift = -1.0  # degrees



    def updateCL_max_Cruise(self, CL_max_Cruise):
            self.CL_max_Cruise = CL_max_Cruise
    def updateCf_nose_cr(self,Cf_nose_cr):
            self.Cf_nose_cr = Cf_nose_cr
    def updateCf_cyl_cr(self, Cf_cyl_cr):
            self.Cf_cyl_cr = Cf_cyl_cr
    def updateCf_cone_cr(self, Cf_cone_cr):
            self.Cf_cone_cr = Cf_cone_cr
    def updateCf_fus_cr(self, Cf_fus_cr):
            self.Cf_fus_cr = Cf_fus_cr
    def updateCf_W_cr(self, Cf_W_cr):
            self.Cf_W_cr = Cf_W_cr
    def updateCf_HT_cr(self, Cf_HT_cr):
            self.Cf_HT_cr = Cf_HT_cr
    def updateCf_VT_cr(self, Cf_VT_cr):
            self.Cf_VT_cr = Cf_VT_cr
    def updateCf_eng_cr(self, Cf_eng_cr):
            self.Cf_eng_cr = Cf_eng_cr
    def updateCf_tot_cr(self, Cf_tot_cr):
            self.Cf_tot_cr = Cf_tot_cr

    def updateCf_nose_app(self,Cf_nose_app):
            self.Cf_nose_app = Cf_nose_app
    def updateCf_cyl_app(self, Cf_cyl_app):
            self.Cf_cyl_app = Cf_cyl_app
    def updateCf_cone_app(self, Cf_cone_app):
            self.Cf_cone_app = Cf_cone_app
    def updateCf_fus_app(self, Cf_fus_app):
            self.Cf_fus_app = Cf_fus_app
    def updateCf_W_app(self, Cf_W_app):
            self.Cf_W_app = Cf_W_app
    def updateCf_HT_app(self, Cf_HT_app):
            self.Cf_HT_app = Cf_HT_app
    def updateCf_VT_app(self, Cf_VT_app):
            self.Cf_VT_app = Cf_VT_app
    def updateCf_eng_app(self, Cf_eng_app):
            self.Cf_eng_app = Cf_eng_app
    def updateCf_tot_app(self, Cf_tot_app):
            self.Cf_tot_app = Cf_tot_app

    def updateS_nose(self,S_nose):
            self.S_nose = S_nose
    def updateS_cyl(self, S_cyl):
            self.S_cyl = S_cyl
    def updateS_cone(self, S_cone):
            self.S_cone = S_cone
    def updateS_fus(self, S_fus):
            self.S_fus = S_fus
    def updateS_W(self, S_W):
            self.S_W = S_W
    def updateS_HT(self, S_HT):
            self.S_HT = S_HT
    def updateS_VT(self, S_VT):
            self.S_VT = S_VT
    def updateS_eng(self, S_eng):
            self.S_eng = S_eng
    def updateS_tot(self, S_tot):
            self.S_tot = S_tot

    def updateCD0_Landing_DOWN(self,CD0_Landing_DOWN):
            self.CD0_Landing_DOWN = CD0_Landing_DOWN
    def updateCD0_Landing_UP(self,CD0_Landing_UP):
            self.CD0_Landing_UP = CD0_Landing_UP
    def updateCD0_Takeoff_DOWN(self,CD0_Takeoff_DOWN):
            self.CD0_Takeoff_DOWN = CD0_Takeoff_DOWN
    def updateCD0_Takeoff_UP(self,CD0_Takeoff_UP):
            self.CD0_Takeoff_UP = CD0_Takeoff_UP
    def updateCD0_Cruise(self,CD0_Cruise):
            self.CD0_Cruise = CD0_Cruise
    def updateCD0_Clean_UP(self, CD0_Clean_UP):
            self.CD0_Clean_UP = CD0_Clean_UP
    def updatee_Landing(self, e_Landing):
            self.e_Landing = e_Landing
    def updatee_Takeoff(self, e_Takeoff):
            self.e_Takeoff = e_Takeoff
    def updatee_Clean(self, e_Clean):
            self.e_clean = e_Clean
            
    def updatealphaStall(self, alphaStall):
            self.alphaStall = alphaStall
    def updateLD(self, LD):
            self.LD = LD

    def updateCL_max_Landing(self, CL_max_Landing):
        self.CL_max_Landing = CL_max_Landing

    def updateCL_max_Takeoff(self, CL_max_Takeoff):
        self.CL_max_Takeoff = CL_max_Takeoff

    def updateCL_max_Cruise(self, CL_max_Cruise):
        self.CL_max_Cruise = CL_max_Cruise




            




