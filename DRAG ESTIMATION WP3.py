# EXTRA DRAG DUE TO FLAPS BEING EXTENDED

Dflap = 35 # degrees
Fflap = 0.0074
Wf = 0.5
def d(x):
    cd = Fflap * x * Wf * (Dflap - 10)
    return cd

for i in range(20,36):
    print(d(i/100))




