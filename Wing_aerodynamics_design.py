import math

import MassEstimate

Mcr = 0.77 # Cruise mach number
Wing_load = 3600 # Nm^-2
MTOW = MassEstimate.MTOW
nj = MassEstimate.nj
g = 9.81 # Gravitational constant
Sw = MTOW * g / Wing_load
AR = 7.5



Sweep = math.acos(1.16/(Mcr+0.5))
print(Sweep * 180 / math.pi, 'degrees')

Taper = 0.2 * (2 - Sweep)
print(Taper)

Span = math.sqrt(Sw*AR)
Root_chord = 2 * Sw / (1+Taper) / Span
Tip_chord = Taper * Root_chord
print(Span)
print(Root_chord,Tip_chord, 'metres')

print(MTOW,'kg', nj)

dihedral = 3 - Sweep * 180 / math.pi / 10 + 2

print(dihedral, 'degrees')