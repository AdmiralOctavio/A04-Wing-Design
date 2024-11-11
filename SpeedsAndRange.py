from math import sqrt,atan,tan,radians,cos

class Miscellaneous:
    def __init__(self):
            self.densitySL = 1.225
            self.densityFL = 0.379597
            self.GustVelocity = 66
            self.Velocity = 0.77*sqrt(1.4*287*218.8)
            self.EASVelocity = self.Velocity/sqrt(self.densitySL/self.densityFL)
            self.V_dive_EAS=166.89*1.5
            self.Range = 2963

