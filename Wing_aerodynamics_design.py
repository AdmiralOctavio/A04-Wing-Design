import math

import MassEstimate

Mcr = 0.77 # Cruise mach number
Wing_load = 3600 # Nm^-2
MTOW = MassEstimate.MTOW
nj = MassEstimate.nj
g = 9.81 # Gravitational constant
Sw = MTOW * g / Wing_load
AR = 7.5


Sweep_quartchord = math.acos(1.16/(Mcr+0.5))
print(Sweep_quartchord * 180 / math.pi, 'degrees')

Taper = 0.2 * (2 - Sweep_quartchord)
print(Taper)

Span = math.sqrt(Sw*AR)
Root_chord = 2 * Sw / (1+Taper) / Span
Tip_chord = Taper * Root_chord
print(Span)
print(Root_chord,Tip_chord, 'metres')


print(MTOW,'kg', nj)

dihedral = 3 - Sweep_quartchord * 180 / math.pi / 10 - 2
print(dihedral, 'degrees')


# MAC of flaps thing

def MAC_flap(Wf):
    TF = 1 - (1 - 0.3161457369885578) * (Wf)
    root_chord = 4.41
    MAC = 2 / 3 * (1 + TF + TF ** 2) * 4.41 / (TF + 1)

    return root_chord, TF * root_chord

def quartchordsweeptoLEsweep(Sweepquartchord, c_r, b, tr ):
    Lambda_LE = math.atan(math.tan(Sweepquartchord) - c_r*(tr-1)/(2*b))
    return Lambda_LE

LE_sweep = math.degrees(quartchordsweeptoLEsweep(Sweep_quartchord,Root_chord, Span, Taper))

print(LE_sweep)