from math import pi
import numpy as np

def Clda(b1,b2,c,d,cla,tau,S,b):
    I = c/2*(b2**2 - b1**2) - d/3*(b2**3 - b1**3)
    Clda = 2*cla*tau*I/(S*b)
    return Clda

def P(Clda,Clp,da,V,b):
    P = -Clda/Clp*da*(2*V/b)
    return P


def AileronsFunction(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight):
    da_up = 25  #max deflection upward - deg
    da_down = 0.75*da_up    #max deflection down - deg
    da = 0.5*(da_up + da_down)*pi/180  #effective deflection at max deflection - rad

    cla = 2*pi  #airfoil lift curve slope
    cd0 = Aerodynamics.cd0airfoil #airfoil zero-lift drag coefficient
    tau = 0.55   #aileron effectiveness (from c_aileron/c)
    c_apc = 0.35 # -
    c_r = Planform.c_r  #m
    c_t = Planform.c_t  #m
    b = Planform.b   #m
    S = Planform.wing_area    #m^2
    V = 1.13*Miscellaneous.V_stall   #M/S

    P_needed = 0.561    #rad/s (45 deg in 1.4s)

    c = c_r
    d = 2*(c_r - c_t)/b

    I = c*b**3/24 - d*b**4/64 #integral of roll damping derivative
    Clp = -4*(cla+cd0)/(S*b**2)*I

    n = 3
    i = 10**(-n)
    b1min = 0.55
    b1max = 0.8
    b2min = 0.8
    b2max = 0.9
    b1_list = []
    b2_list = []
    for j in np.arange(b1min,b1max+i,i):
        b1_list.append(round(j,n))
    for j in np.arange(b2min,b2max+i,i):
        b2_list.append(round(j,n))
    dim_x = len(b1_list)
    dim_y = len(b2_list)
    B = np.ones((dim_x,dim_y))
    P_calc = np.ones((dim_x,dim_y))


    for b1 in b1_list:
        for b2 in b2_list:
            if b2 > b1:
                #print(b1, b2)
                clda = Clda(b1*b/2,b2*b/2,c,d,cla,tau,S,b)
                #print(clda)
                p = P(clda,Clp,da,V,b)
                #print(p)
                if p > P_needed:
                    x = b1_list.index(b1)
                    y = b2_list.index(b2)
                    B[x,y] = round(b2-b1,n)
                    P_calc[x,y] = p

    np.set_printoptions(threshold = np.inf)
    #print(B)
    b_min = round(np.min(B),n)
    # print('Minimum size (*b/2):', round(b_min,n))
    A = np.where((B <= b_min) & (B > 0))
    #print(A)
    A = np.transpose(A)
    #print(A)
    choice = A[-1]
    #print(choice)

    b1_choice = b1_list[choice[0]]
    b2_choice = b2_list[choice[1]]
    # print('Starting position (*b/2):', b1_choice)
    # print('Ending position (*b/2):', b2_choice)

    clda_choice = Clda(b1_choice*b/2,b2_choice*b/2,c,d,cla,tau,S,b)
    P_choice = P(clda_choice,Clp,da,V,b)
    # print('Best:')
    # print('Clda = ',clda_choice)
    # print('Clp = ',Clp)
    # print('P = ',P_choice)

    Planform.updatey1ail(b1_choice)
    Planform.updatey2ail(b2_choice)

    return b1_choice, b2_choice

#AileronsFunction(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
