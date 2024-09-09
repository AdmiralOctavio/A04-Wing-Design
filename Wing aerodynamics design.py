import math
Mcr = 0.77 # Cruise mach number


Sweep = math.acos(1.16/(Mcr+0.5))

print(Sweep * 180 / math.pi)

Taper = 0.2 * (2 - Sweep)

print(Taper)
