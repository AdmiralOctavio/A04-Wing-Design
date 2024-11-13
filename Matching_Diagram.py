from matplotlib import pyplot as plt
import numpy as np
from math import sqrt, pi, ceil



#ISA calculator (under 11km)
def ISA(h, g, deltaT):
    T0 = 288.15 + deltaT
    T = T0 - 0.0065*h
    p = 101325*(T/T0)**(g/1.8655)
    rho = 1.225*(T/T0)**(g/1.8655-1)
    return p, T, rho

#lapse rate calculator
def lapserate(M,T,p,Bp):
    Tt = T*(1+0.2*M**2)
    pt = p*(1+0.2*M**2)**3.5
    theta = Tt/288.15
    delta = pt/101325
    
    a = delta*(1-(0.43+0.014*Bp)*np.sqrt(M))
    return a

#diagram limits calculators
def minspd(data,aero,misc):
    Vapp = data[0,0]
    h = data[0,1]
    deltaT = data[0,2]
    CLmax = data[0,3]
    Tfrac = data[0,4]
    B = data[0,5]
    A = misc[0]
    Bp = misc[1]
    g = misc[2]
    p, T, rho = ISA(h, g, deltaT)
    
    WpS_max = 1/B * rho/2 * (Vapp/1.23)**2 * CLmax
    return WpS_max

def landfdlen(data,aero,misc):
    Llf = data[1,0]
    h = data[1,1]
    deltaT = data[1,2]
    CLmax = data[1,3]
    Tfrac = data[1,4]
    B = data[1,5]
    A = misc[0]
    Bp = misc[1]
    g = misc[2]
    p, T, rho = ISA(h, g, deltaT)
    
    WpS_max = 1/B * Llf/0.45 * rho*CLmax/2
    return WpS_max

def maxspd(data,aero,misc,WpS_list):
    M = data[2,0]
    h = data[2,1]
    deltaT = data[2,2]
    CLmax = data[2,3]
    Tfrac = data[2,4]
    B = data[2,5]
    CD0 = aero[6,0]
    e = aero[6,1]
    A = misc[0]
    Bp = misc[1]
    g = misc[2]
    CL_LpD_max = sqrt(pi*e*A*CD0)
    p, T, rho = ISA(h, g, deltaT)

    a = lapserate(M,T,p,Bp)
    V = M*sqrt(401.8*T)
    T1 = CD0*rho*V**2 * 0.5
    T2 = 2/(pi*e*A*rho*V**2)
    TpW_min = B/a*(T1/(B*WpS_list) + B*WpS_list*T2)
    return TpW_min

def climbrate(data,aero,misc,WpS_list):
    c = data[3,0]
    h = data[3,1]
    deltaT = data[3,2]
    CLmax = data[3,3]
    Tfrac = data[3,4]
    B = data[3,5]
    CD0 = aero[3,0]
    e = aero[3,1]
    A = misc[0]
    Bp = misc[1]
    g = misc[2]
    CL_LpD_max = sqrt(pi*e*A*CD0)
    p, T, rho = ISA(h, g, deltaT)

    V = np.sqrt(WpS_list*2/(rho*CL_LpD_max))
    M = V/sqrt(401.8*T)
    a = lapserate(M,T,p,Bp)
    TpW_min = B/a*(c/V+2*CD0/CL_LpD_max)
    return TpW_min

def climbgrad(i,data,aero,misc,WpS_list):
    G = data[4+i,0]
    h = data[4+i,1]
    deltaT = data[4+i,2]
    CLmax = data[4+i,3]
    Tfrac = data[4+i,4]
    B = data[4+i,5]
    CD0 = aero[i,0]
    e = aero[i,1]
    A = misc[0]
    Bp = misc[1]
    g = misc[2]
    CL_LpD_max = sqrt(pi*e*A*CD0)
    p, T, rho = ISA(h, g, deltaT)

    V = np.sqrt(WpS_list*2/(rho*CL_LpD_max))
    M = V/sqrt(401.8*T)
    a = lapserate(M,T,p,Bp)
    TpW_min = 1/Tfrac*B/a*(G+2*CD0/CL_LpD_max)
    return TpW_min

def takofdlen(data,aero,misc,WpS_list):
    Lto = data[9,0]
    h = data[9,1]
    deltaT = data[9,2]
    CLmax = data[9,3]/1.13**2
    Tfrac = data[9,4]
    B = data[9,5]
    CD0 = aero[5,0]
    e = aero[5,1]
    A = misc[0]
    Bp = misc[1]
    g = misc[2]
    CL_LpD_max = sqrt(pi*e*A*CD0)
    p, T, rho = ISA(h, g, deltaT)

    V = np.sqrt(WpS_list*2/(rho*CLmax))
    M = V/sqrt(401.8*T)
    a = lapserate(M,T,p,Bp)
    TpW_min = 1.15*a*np.sqrt(1/Tfrac*WpS_list/(0.85*pi*Lto*rho*g*A*e)) + 1/Tfrac*4*11/Lto
    return TpW_min


def MatchingDiagram(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight):
    #dimension of table (entries x functions)
    limit = 7000    #maximum W/S on diagram
    step = 100
    dimension = int(limit/step)

    #initialize graph for matching diagram - first column is W/S
    graph = np.zeros((dimension,8))
    WpS_list = np.arange(step,step*dimension+1,step)



    #ALL THE INPUT DATA

                        #value  #height     #deltaT #CLmax  #Tfrac  #mfrac
    data = np.array([[  1.23*Miscellaneous.V_stall,     0,          0,      Aerodynamics.CL_max_Landing,    0.0,    0.926],  #approach speed
                     [  1210,   0,          0,      Aerodynamics.CL_max_Landing,    0.0,    0.926],  #landing field length
                     [  0.77,   10668,      0,      Aerodynamics.CL_max_Cruise,    1.0,    0.95],  #cruise Mach number
                     [  12.7,   0,          0,      Aerodynamics.CL_max_Cruise,    1.0,    0.95],  #minimum climb rate
                     [  0.032,  0,          0,      Aerodynamics.CL_max_Landing,    1.0,    1.00],  #G_119
                     [  0,      0,          0,      Aerodynamics.CL_max_Takeoff,    0.5,    1.00],  #G_121a
                     [  0.024,  0,          0,      Aerodynamics.CL_max_Takeoff,    0.5,    1.00],  #G_121b
                     [  0.012,  0,          0,      Aerodynamics.CL_max_Cruise,    0.5,    1.00],  #G_121c
                     [  0.021,  0,          0,      Aerodynamics.CL_max_Landing,    0.5,    1.00],  #G_121d
                     [  1296,   0,          0,      Aerodynamics.CL_max_Takeoff,    0.5,    1.00]]) #take-off field length

                        #CD_0   #e
    aero = np.array([[  Aerodynamics.CD0_Landing_DOWN, Aerodynamics.e_Landing],     #DOWN, L    - G_119
                     [  Aerodynamics.CD0_Takeoff_DOWN, Aerodynamics.e_Takeoff],     #DOWN, TO   - G_121a
                     [  Aerodynamics.CD0_Takeoff_UP, Aerodynamics.e_Takeoff],     #UP, TO     - G_121b
                     [  Aerodynamics.CD0_Clean_UP, Aerodynamics.e_Clean],     #UP, CR     - G_121c    - also for every other calculation
                     [  Aerodynamics.CD0_Landing_UP, Aerodynamics.e_Landing],     #UP, L      - G_121d
                     [  Aerodynamics.CD0_Takeoff_DOWN, Aerodynamics.e_Takeoff],
                     [  Aerodynamics.CD0_Cruise, Aerodynamics.e_Clean]])    #DOWN, TO   - take-off field length

    A = Planform.AR     #aspect ratio
    Bp = Propulsion.BypassRatio      #bypass ratio
    g = 9.80665 #gravity

    misc = np.array([A,Bp,g])

    #reference aircraft W/S and T/W
    reference = np.array([[ 4910,   0.313],
                          [ 4690,   0.342],
                          [ 4040,   0.326],
                          [ 3830,   0.344],
                          [ 4340,   0.352],
                          [ 3790,   0.304],
                          [ 4730,   0.367],
                          [ 4980,   0.382]])



    #MAKING THE GRAPH

    #approach speed
    WpS_1 = minspd(data,aero,misc)
    plt.axvline(x = WpS_1, color = 'b', label = 'approach speed')

    #landing field length
    WpS_2 = landfdlen(data,aero,misc)
    plt.axvline(x = WpS_2, color = 'r', label = 'landing field length')

    #cruise Mach number
    graph[:,0] = maxspd(data,aero,misc,WpS_list)
    plt.plot(WpS_list, graph[:,0], color = 'g', label = 'cruise Mach number')

    #climb rate
    graph[:,1] = climbrate(data,aero,misc,WpS_list)
    plt.plot(WpS_list, graph[:,1], color = 'y', label = 'climb rate')

    #climb gradients
    lab = 'climb gradient'
    for i in range(0,5):
        graph[:,2+i] = climbgrad(i,data,aero,misc,WpS_list)
        plt.plot(WpS_list, graph[:,2+i], color = 'c', label = lab)
        lab = '_Hidden label'

    #take-off field length
    graph[:,7] = takofdlen(data,aero,misc,WpS_list)
    plt.plot(WpS_list, graph[:,7], color = 'm', label = 'take-off field length')

    #reference aircraft points
    lab = 'reference aircraft'
    for i in range(len(reference[:,0])):
        plt.plot(reference[i,0], reference[i,1], marker = 'o', color = 'k', label = lab)
        lab = '_Hidden label'
        


    #design point selection
    if WpS_1 < WpS_2:
        WpS_min = WpS_1 - WpS_1%step
    else:
        WpS_min = WpS_2 - WpS_2%step

    WpS_list = list(WpS_list)
    TpW_max = ceil(100*max(graph[WpS_list.index(WpS_min),:]))/100
    #print(WpS_min,TpW_max)
    plt.plot(WpS_min, TpW_max, marker = 'o', color = 'r', label = 'design point')


    #making the graph
    plt.title('Matching diagram')
    plt.legend()
    plt.xlabel('W/S [N/m^2]')
    plt.ylabel('T/W [N/N]')
    plt.xlim(0,dimension*step)
    plt.ylim(0,0.5)
    plt.grid()
    #plt.show()
    #plt.savefig('MatchingDiagram.jpg')

    Planform.updateWingLoading(WpS_min)
    Propulsion.updateTtoW(TpW_max)

    return WpS_min, TpW_max

#MatchingDiagram(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
