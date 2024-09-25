from math import pi
import numpy as np

def Clda(b1,b2):
    I = c/2*(b2**2 - b1**2) - d/3*(b2**3 - b1**3)
    Clda = 2*cla*tau*I/(S*b)
    return Clda

def P(Clda):
    P = -Clda/Clp*da*(2*V/b)
    return P


da_up = 20  #max deflection upward
da_down = 0.75*da_up    #max deflection down
da = 0.5*(da_up + da_down)*pi/180/2  #effective deflection at max deflection

cla = 2*pi  #airfoil lift curve slope
cd0 = 0.005 #airfoil zero-lift drag coefficient
tau = 0.43   #aileron effectiveness (from c_aileron/c)
c_apc = 0.22 #-
c_r = 4.41  #m
c_t = 1.39  #m
b = 21.75   #m
S = 63.1    #m^2
V = 60   #M/S
#228.3

P_needed = 0.21    #rad/s
#0.651


c = c_r
d = 2*(c_r - c_t)/b

I = c*b**3/24 - d*b**4/64 #integral of roll damping derivative
Clp = -4*(cla+cd0)/(S*b**2)*I

#ALSO CHECK UNITS IN ALL THE CALCULATIONS ABOVE AND BELOW

n = 2
i = 10**(-n)
b1min = 0.4
b1max = 0.8
b2min = 0.5
b2max = 0.95
b1_list = []
b2_list = []
for j in np.arange(b1min,b1max+i,i):
    b1_list.append(round(j,n))
for j in np.arange(b2min,b2max+i,i):
    b2_list.append(round(j,n))
dim_x = len(b1_list)
dim_y = len(b2_list)
B = np.ones((dim_x,dim_y))


for b1 in b1_list:
    for b2 in b2_list:
        if b2 > b1:
            #print(b1, b2)
            clda = Clda(b1*b/2,b2*b/2)
            #print(clda)
            p = P(clda)
            #print(p)
            if p > P_needed:
                x = b1_list.index(b1)
                y = b2_list.index(b2)
                B[x,y] = b2-b1

np.set_printoptions(threshold = np.inf)
#print(B)
b_min = np.min(B)
A = np.where((B <= b_min) & (B > 0))
print(np.transpose(A))
print(round(b_min,3))
#print(b1_list[A[-1,0]], b2_list[A[-1,1]])

