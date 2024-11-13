from math import sqrt,atan,tan,radians,cos

class Weight:
    def __init__(self):
            self.MTOW =23173
            self.M_fuel = 2845
            self.M_Payload = 7255
            self.OE_MTOW = 0.566492308
            self.OEW = 13127
            self.MZFW = 20328

            self.AirframeStructuralWeight = 0
            self.WingGroupWeight = 0
            self.BodyGroupWeight = 0
            self.HoriTailWeight = 0
            self.VertTailWeight = 0
            self.LandingGearWeight = 0
            self.SurfaceControlsWeight = 0
            self.NacelleWeight = 0
            self.PropulsionWeight = 0
            self.AirframeServicesAndEquipmentWeight = 0
            self.W_nose = 0

            self.XLEMAC = 0
            self.WingCG = 0
            self.OEWCG = 14.2




    def updateW_nose(self, W_nose):
        self.W_nose = W_nose

    def updateAirframeStructuralWeight(self,AirframeStructuralWeight):
        self.AirframeStructuralWeight = AirframeStructuralWeight

    def updateWingGroupWeight(self,WingGroupWeight):
        self.WingGroupWeight = WingGroupWeight

    def updateBodyGroupWeight(self,BodyGroupWeight):
        self.BodyGroupWeight = BodyGroupWeight

    def updateHori_Tail_Weight(self,HoriTailWeight):
        self.HoriTailWeight = HoriTailWeight

    def updateVert_Tail_Weight(self,VertTailWeight):
        self.VertTailWeight = VertTailWeight

    def updateLandingGearWeight(self,LandingGearWeight):
        self.LandingGearWeight = LandingGearWeight

    def updateSurfaceControlsWeight(self,SurfaceControlsWeight):
        self.SurfaceControlsWeight = SurfaceControlsWeight

    def updateNacelleWeight(self,NacelleWeight):
        self.NacelleWeight = NacelleWeight

    def updatePropulsionWeight(self,PropulsionWeight):
        self.PropulsionWeight = PropulsionWeight

    def updateAirframeServicesAndEquipmentWeight(self,AirframeServicesAndEquipmentWeight):
        self.AirframeServicesAndEquipmentWeight = AirframeServicesAndEquipmentWeight


    def updateOE_MTOW(self,OE_MTOW):
        self.OE_MTOW = OE_MTOW
    def updateMTOW(self,MTOW):
        self.MTOW = MTOW
    def updateM_fuel(self,M_fuel):
        self.M_fuel = M_fuel

    def updateM_Payload(self,M_Payload):
        self.M_Payload = M_Payload

    def updateOE_MTOW(self,OE_MTOW):
        self.OE_MTOW = OE_MTOW

    def updateMZFW(self,MZFW):
        self.MZFW = MZFW
    def updateOEW(self,OEW):
        self.OEW = OEW



    def updateXLEMAC(self,XLEMAC):
        self.XLEMAC = XLEMAC

    def updateOEWCG(self,OEWCG):
        self.OEWCG = OEWCG

    def updateWingCG(self,WingCG):
        self.WingCG = WingCG
