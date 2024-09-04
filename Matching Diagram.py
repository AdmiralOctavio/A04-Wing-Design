from matplotlib import pyplot as plt
import numpy as np
from math import sqrt, pi, ceil



#ISA calculator (under 11km)
def ISA(h, deltaT):
    T0 = 288.15 + deltaT
    T = T0 - 0.0065*h
    p = 101325*(T/T0)**(g/1.8655)
    rho = 1.225*(T/T0)**(g/1.8655-1)
    return p, T, rho

#lapse rate calculator
def lapserate(M,T,p):
    Tt = T*(1+0.2*M**2)
    pt = p*(1+0.2*M**2)**3.5
    theta = Tt/288.15
    delta = pt/101325
    
    a = delta*(1-(0.43+0.014*Bp)*np.sqrt(M))
    return a

#diagram limits calculators
def minspd():
    Vapp = data[0,0]
    h = data[0,1]
    deltaT = data[0,2]
    CLmax = data[0,3]
    Tfrac = data[0,4]
    B = data[0,5]
    p, T, rho = ISA(h,deltaT)
    
    WpS_max = 1/B * rho/2 * (Vapp/1.23)**2 * CLmax
    return WpS_max

def landfdlen():
    Llf = data[1,0]
    h = data[1,1]
    deltaT = data[1,2]
    CLmax = data[1,3]
    Tfrac = data[1,4]
    B = data[1,5]
    p, T, rho = ISA(h,deltaT)
    
    WpS_max = 1/B * Llf/0.45 * rho*CLmax/2
    return WpS_max

def maxspd():
    M = data[2,0]
    h = data[2,1]
    deltaT = data[2,2]
    CLmax = data[2,3]
    Tfrac = data[2,4]
    B = data[2,5]
    CD0 = aero[3,0]
    e = aero[3,1]
    CL_LpD_max = sqrt(pi*e*A*CD0)
    p, T, rho = ISA(h,deltaT)

    a = lapserate(M,T,p)
    V = M*sqrt(401.8*T)
    T1 = CD0*rho*V**2 * 0.5
    T2 = 2/(pi*e*A*rho*V**2)
    TpW_min = B/a*(T1/(B*graph[:,0]) + B*graph[:,0]*T2)
    return TpW_min

def climbrate():
    c = data[3,0]
    h = data[3,1]
    deltaT = data[3,2]
    CLmax = data[3,3]
    Tfrac = data[3,4]
    B = data[3,5]
    CD0 = aero[3,0]
    e = aero[3,1]
    CL_LpD_max = sqrt(pi*e*A*CD0)
    p, T, rho = ISA(h,deltaT)

    V = np.sqrt(graph[:,0]*2/(rho*CL_LpD_max))
    M = V/sqrt(401.8*T)
    a = lapserate(M,T,p)
    TpW_min = B/a*(c/V+2*CD0/CL_LpD_max)
    return TpW_min

def climbgrad(i):
    G = data[4+i,0]
    h = data[4+i,1]
    deltaT = data[4+i,2]
    CLmax = data[4+i,3]
    Tfrac = data[4+i,4]
    B = data[4+i,5]
    CD0 = aero[i,0]
    e = aero[i,1]
    CL_LpD_max = sqrt(pi*e*A*CD0)
    p, T, rho = ISA(h,deltaT)

    V = np.sqrt(graph[:,0]*2/(rho*CL_LpD_max))
    M = V/sqrt(401.8*T)
    a = lapserate(M,T,p)
    TpW_min = 1/Tfrac*B/a*(G+2*CD0/CL_LpD_max)
    return TpW_min

def takofdlen():
    Lto = data[9,0]
    h = data[9,1]
    deltaT = data[9,2]
    CLmax = data[9,3]/1.13**2
    Tfrac = data[9,4]
    B = data[9,5]
    CD0 = aero[5,0]
    e = aero[5,1]
    CL_LpD_max = sqrt(pi*e*A*CD0)
    p, T, rho = ISA(h,deltaT)

    V = np.sqrt(graph[:,0]*2/(rho*CLmax))
    M = V/sqrt(401.8*T)
    a = lapserate(M,T,p)
    TpW_min = 1.15*a*np.sqrt(1/Tfrac*graph[:,0]/(0.85*pi*Lto*rho*g*A*e)) + 1/Tfrac*4*11/Lto
    return TpW_min



#dimension of table (entries x functions)
dimension = (70,10)
step = 100

#initialize graph for matching diagram - first column is W/S
graph = np.zeros(dimension)
graph[:,0] = np.arange(step,step*dimension[0]+1,step)



#ALL THE INPUT DATA

                    #value  #height     #deltaT #CLmax  #Tfrac  #mfrac
data = np.array([[  60,     0,          0,      2.3,    0.0,    0.85],  #minimum speed
                 [  1210,   0,          0,      2.3,    0.0,    0.85],  #landing field length
                 [  0.77,   10668,      0,      1.5,    1.0,    0.95],  #maximum speed (mach)
                 [  12.7,   0,          0,      1.5,    1.0,    0.95],  #minimum climb rate
                 [  0.032,  0,          0,      2.3,    1.0,    1.00],  #G_119
                 [  0,      0,          0,      1.9,    0.5,    1.00],  #G_121a
                 [  0.024,  0,          0,      1.9,    0.5,    1.00],  #G_121b
                 [  0.012,  0,          0,      1.5,    0.5,    1.00],  #G_121c
                 [  0.021,  0,          0,      2.3,    0.5,    1.00],  #G_121d
                 [  1296,   0,          0,      1.9,    0.5,    1.00]]) #take-off field length

                    #CD_0   #e
aero = np.array([[  0.0822, 0.984],     #DOWN, L    - G_119
                 [  0.0562, 0.892],     #DOWN, TO   - G_121a
                 [  0.0387, 0.892],     #UP, TO     - G_121b
                 [  0.0192, 0.823],     #UP, CR     - G_121c    - also for every other calculation
                 [  0.0647, 0.984],     #UP, L      - G_121d
                 [  0.0562, 0.892]])    #DOWN, TO   - take-off field length

A = 7.5     #aspect ratio
Bp = 9      #bypass ratio
g = 9.80665

reference = np.array([[ 4910,   0.313],
                      [ 4690,   0.342],
                      [ 4040,   0.326],
                      [ 3830,   0.344],
                      [ 4340,   0.352],
                      [ 3790,   0.304],
                      [ 4730,   0.367],
                      [ 4980,   0.382]])



#MAKING THE GRAPH

#minimum speed
WpS_1 = minspd()
plt.axvline(x = WpS_1, color = 'b', label = 'minimum speed')

#landing field length
WpS_2 = landfdlen()
plt.axvline(x = WpS_2, color = 'r', label = 'landing field length')

#cruise speed
graph[:,1] = maxspd()
plt.plot(graph[:,0], graph[:,1], color = 'g', label = 'maximum speed')

#climb rate
graph[:,2] = climbrate()
plt.plot(graph[:,0], graph[:,2], color = 'y', label = 'climb rate')

#climb gradients
lab = 'climb gradient'
for i in range(0,5):
    graph[:,3+i] = climbgrad(i)
    plt.plot(graph[:,0], graph[:,3+i], color = 'c', label = lab)
    lab = '_Hidden label'

#take-off field length
graph[:,8] = takofdlen()
plt.plot(graph[:,0], graph[:,8], color = 'm', label = 'take-off field length')

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
WpS_list = list(graph[:,0])
TpW_max = ceil(100*max(graph[WpS_list.index(WpS_min),1:]))/100
print(WpS_min,TpW_max)
plt.plot(WpS_min, TpW_max, marker = 'o', color = 'r', label = 'design point')



#making the graph
plt.title('Matching diagram')
plt.legend()
plt.xlabel('W/S [N/m^2]')
plt.ylabel('T/W [N/N]')
plt.xlim(0,dimension[0]*step)
plt.ylim(0,0.5)
plt.grid()
plt.show()


