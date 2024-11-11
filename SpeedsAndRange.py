from math import sqrt,atan,tan,radians,cos
import AerodynamicParameters
Aerodynamics = AerodynamicParameters.Aerodynamics()
class Miscellaneous:
    def __init__(self):
            self.densitySL = 1.225
            self.densityFL = 0.379597
            self.GustVelocity = 66
            self.VcrM = 0.77  # mach
            self.Velocity = self.VcrM*296.32
            self.EASVelocity = self.Velocity/sqrt(self.densitySL/self.densityFL)
            self.V_dive_EAS=166.89*1.5
            self.Range = 2963
            self.fcon = 0.05  # contingency fuel ratio
            self.Rdiv = 250  # km, divergence range
            self.Rnom = 2019  # km, Nominal
            self.tE = 2700  # loiter time
            self.hCR = 10668  # m, cruise height
            self.Mpl = 7200  # kg, design payload mass
            self.Rlost = (1 / 0.7 * Aerodynamics.LD * (self.hCR + self.Velocity ** 2 / (2 * 9.80665))) / 1000  # km, lost range from drag

