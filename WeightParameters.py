from math import sqrt,atan,tan,radians,cos

class Weight:
    def __init__(self):
            self.MTOW =23173
            self.M_fuel = 2845
            self.M_Payload = 7255
            self.OE_MTOW = 0.566492308
            self.OEW = 13127
            self.MZFW = 20328

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
