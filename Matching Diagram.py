from matplotlib import pyplot as plt
import numpy as np
from math import sqrt, pi

CD0 = 0.0186 #variable
e = 0.787 #variable
A = 8.83 #variable
CL_LpD_max = sqrt(pi*e*A*CD0)


#ISA calculator (under 11km)
def ISA(h, deltaT):
    T0 = 288.15 + deltaT
    T = T0 - 0.0065*h
    p = 101325*(T/T0)**(5.25685)
    rho = 1.225*(T/T0)**(4.25685)
    return p, T, rho

#lapse rate calculator
def lapserate(M,T,p):
    Bp = 6 #variable
    Tt = T*(1+0.2*M**2)
    pt = p*(1+0.2*M**2)**3.5
    theta = Tt/288.15
    delta = pt/101325
    a = delta*(1-(0.43+0.014*Bp)*np.sqrt(M))
    #print(theta, delta, a)
    return a

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
    p, T, rho = ISA(h,deltaT)
    #print(T)
    a = lapserate(M,T,p)
    
    V = M*sqrt(401.8*T)
    T1 = CD0*rho*V**2 * 0.5
    T2 = 2/(pi*e*A*rho*V**2)
    #print(V, T1, T2)
    
    TpW_min = B/a*(T1/(B*graph[:,0]) + B*graph[:,0]*T2)
    return TpW_min

def climbrate():
    c = data[3,0]
    h = data[3,1]
    deltaT = data[3,2]
    CLmax = data[3,3]
    Tfrac = data[3,4]
    B = data[3,5]
    p, T, rho = ISA(h,deltaT)

    V = np.sqrt(graph[:,0]*2/(rho*CL_LpD_max)) #THIS DOES NOT WORK!!!
    M = V/sqrt(401.8*T)
    a = lapserate(M,T,p)
    TpW_min = B/a*(c/V+2*CD0/CL_LpD_max)
    return TpW_min



#dimension of table (entries x functions)
dimension = (70,10)
step = 100

#initialize graph for matching diagram - first column is W/S
graph = np.zeros(dimension)
graph[:,0] = np.arange(step,step*dimension[0]+1,step)

#print(graph)


                    #value  #height     #deltaT #CLmax  #Tfrac  #mfrac
data = np.array([[  70,     0,          0,      2.4,    0.0,    0.92],  #minimum speed
                 [  1599,   0,          0,      2.4,    0.0,    0.92],  #landing field length
                 [  0.77,   10300,      0,      1.6,    1.0,    0.95],  #maximum speed (mach)
                 [  6.7,    7400,       0,      1.6,    1.0,    0.95],  #minimum climb rate
                 [  0.32,   0,          0,      2.4,    1.0,    1.00],  #G_119
                 [  0,      0,          0,      2.0,    0.5,    1.00],  #G_121a
                 [  0.024,  0,          0,      2.0,    0.5,    1.00],  #G_121b
                 [  0.012,  0,          0,      1.6,    0.5,    1.00],  #G_121c
                 [  0.021,  0,          0,      2.4,    0.5,    1.00],  #G_121d
                 [  1740,   500,        13.1,   2.0,    0.5,    1.00]]) #take-off field length
#print(data)






#minimum speed
plt.axvline(x = minspd(), color = 'b')

#landing field length
plt.axvline(x = landfdlen(), color = 'r')

#cruise speed
graph[:,1] = maxspd()
plt.plot(graph[:,0], graph[:,1], color = 'g')
#print(graph[:,1])

#climb rate
graph[:,2] = climbrate()
plt.plot(graph[:,0], graph[:,2], color = 'y')
print(graph[:,2])




#climb gradients





#take-off field length




#making the graph
plt.title('Matching diagram')
plt.legend(('minimum speed','landing field length'))
plt.xlabel('W/S [N/m^2]')
plt.ylabel('T/W [N/N]')
plt.xlim(0,dimension[0]*step)
plt.ylim(0,0.5)
plt.show()
