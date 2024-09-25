fcr = 0   # flap-to-chord ratio
fd = 50    # flap deflection angle in degrees
Sfr = 0.6
# given a t/c of 0.14:

def d1(x): #contribution of the flap chord to the flap drag
    c = 179.32*x**4 - 111.6*x**3 + 28.929*x**2 + 2.3705*x - 0.0089
    return c

def d2(y): #contribution of the flap deflection angle to the flap drag
    d = - 3.9877 * 10**(-12) * y**6 + 1.1685 * 10**(-9) * y**5 - 1.2846 * 10**(-7) * y**4 + 6.1742 * 10**(-6) * y**3 - 9.89444 * 10**(-5) * y**2 + 6.8324 * 10**(-4) * y - 3.892 * 10**(-4)
    return d

for i in range(8,40,4):
    cd = Sfr * d2(fd) * d1(i/100)
    print(i/100, cd)
