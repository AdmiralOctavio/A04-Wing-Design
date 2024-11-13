from math import sqrt, acos, atan, tan, pi

def Wing_parametersFunction(Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight):
    #input
    S = Planform.wing_area   # wing area, m^2
    A = Planform.AR     # aspect ratio, -
    M_cr = Miscellaneous.VcrM # critical Mach number, -

    #calculations
    b = sqrt(A*S)       # wingspan, m
    L_cp4 = acos(1.16/(M_cr+0.5))   # quarter-chord sweep angle, rad
    D = 1 - 0.1*L_cp4*180/pi # dihedral angle, deg
    l = 0.2*(2 - L_cp4) # taper ratio, -
    c_r = 2*S/((1+l)*b) # root chord, m
    c_t = l*c_r         # tip chord, m
    L_LE = atan((c_r - c_t)/(2*b) + tan(L_cp4)) #leading edge sweep angle, rad
    MAC = 2/3 * c_r * (1+l+l**2)/(1+l)  # mean aerodynamic chord length, m
    y_MAC = b/6 * (1+2*l)/(1+l) # y coordinate of MAC, m
    x_MAC = y_MAC * tan(L_LE)   # x coordinate of LE MAC w/t LE root, m

    #print
    print('b = ', round(b,2), ' m')
    print('L_cp4 = ', round(L_cp4*180/pi,2), ' deg')
    print('D = ', round(D,2), ' deg')
    print('l = ', round(l,4))
    print('c_r = ', round(c_r,3), ' m')
    print('c_t = ', round(c_t,3), ' m')
    print('L_LE = ', round(L_LE*180/pi,2), ' deg')
    print('MAC = ', round(MAC,3), ' m')
    print('y_MAC = ', round(y_MAC,3), ' m')
    print('x_MAC = ', round(x_MAC,3), ' m')

    #Planform.updateb(b)
    # Planform.updateSweepLE(L_LE*180/pi)
    # Planform.updateDihedral(dihedral)
    # Planform.updateTaper(l)
    # Planform.updateCR(c_r)
    # Planform.updateMAC(MAC)
    # Planform.updateXMAC(x_MAC)
    # Planform.updateYMAC(y_MAC)

    #print(Planform.b)

    return b, L_cp4, D, l, c_r, c_t, L_LE, MAC, y_MAC, x_MAC

