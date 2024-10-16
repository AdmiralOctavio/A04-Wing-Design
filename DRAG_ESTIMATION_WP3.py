# EXTRA DRAG DUE TO FLAPS BEING EXTENDED

Dflap = 35 # degrees
Fflap = 0.0074
cfc = 0.35
# Wf = 0.6 has been chosen

def d(Wf):
    cd = Fflap * cfc * Wf * (Dflap - 10)
    return cd

print(d(0.6))

# ZERO LIFT DRAG

Cd0 = 0.0192







