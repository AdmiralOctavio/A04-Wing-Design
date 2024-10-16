from math import sqrt, cos, pi, radians
import numpy as np
# import Airfoil selection

M_cruise = 0.77
M_DD_min = 1.05*0.77
h_cruise = 35000 #ft
T_cruise = 218.808 #K
gamma = 1.4
R = 8.31446261815324 #J
rho_cruise = 0.3796 #kg/m^3
S = 63.1 #m^2
g = 9.80665
m_OE = 13127 
m_MTOW = 23173
W_OE = m_OE * g
W_MTOW = m_MTOW * g

a_cruise = sqrt(gamma * T_cruise * R)
V_cruise = M_cruise * a_cruise

B = 5.9
TSFC = 22* B**(-0.19) #g s^-1 kN^-1

# L_over_D = 15.9

# C_dcruise = 0.00484
Cd_cruise = 0.005149
C_d0 = 0.0065
# Airfoil_selection.CL_cruise 
Cl_cruise = 0.450622
CL_cruise = 0.37594287624283806

#Calculating C_D0:

Swet_over_S = 6
C_fe = 0.0026

C_D0_1stestimation = C_fe * Swet_over_S

#Calculating the induced drag:
AR_initial = 7.5
delta_AR = 0.04 #adsee lecture 2 slide 66, NOT 65
lambda_LE = radians(27.2)
#clean config:

AR_eff = AR_initial + delta_AR
e_initial = 4.61 * (1-0.045*AR_eff**0.68)*(cos(lambda_LE))**0.15 - 3.1

K_initial = 1/(pi * e_initial * AR_eff)

CD_initial = C_D0_1stestimation + K_initial * CL_cruise**2

L_over_D = CL_cruise/CD_initial

#changing parameters:

#   I. changing the aspect ratio, keeping the sweep angle constant

AR_new = 8.15 #but same sweep - biggest jump in L/D, tested values were AR = [8, 9, 7.9, 8.1, 8.2 and 8.15] - we narrowed it down
AR_eff_2 = AR_new + delta_AR
e_2 = 4.61 * (1-0.045*AR_eff_2**0.68)*(cos(lambda_LE))**0.15 - 3.1

K_2 = 1/(pi * e_2 * AR_eff_2)

CD_2 = C_D0_1stestimation + K_2 * CL_cruise**2

L_over_D_2 = CL_cruise/CD_2

#   II. changing the sweep angle, keeping the aspect ratio constant

lambda_LE_2 = radians(20)
Mcr_unswept_3 = 0.8133333
Mcr_swept_3 = Mcr_unswept_3 /cos(lambda_LE_2)

t_over_c = 0.1
ka = 0.935

e_3 = 4.61 * (1-0.045*AR_eff**0.68)*(cos(lambda_LE_2))**0.15 - 3.1

K_3 = 1/(pi * e_3 * AR_eff)

CD_3 = C_D0_1stestimation + K_3 * CL_cruise**2

L_over_D_3 = CL_cruise/CD_3

M_DD = ka/cos(lambda_LE_2) - t_over_c / (cos(lambda_LE_2))**2 - CL_cruise / (10*(cos(lambda_LE_2))**3)

#   III. changing both the sweep angle and the aspect ratio

# Mcr_unswept = 
# Mcr_swept = 
# lambda_max = 



#estimating the range factor and the SAR:

RF = M_cruise * L_over_D * a_cruise / TSFC 
SAR_MTOW = RF / W_MTOW
SAR_OE = RF / W_OE

# print("SAR_MTOW = ",  SAR_MTOW, "       " , "SAR_OE = " , SAR_OE, "        ", "in cursed units")

# print("SAR_MTOW = ",  SAR_MTOW*1000, "       " , "SAR_OE = " , SAR_OE*1000, "       " , "in km/kg")

# print(e_initial, CD_initial)
# print(e_2, CD_2)
# print(e_3, CD_3)

# print(CL_cruise/CD_initial)
# print(CL_cruise/CD_2)
# print(CL_cruise/CD_3)

# print(M_DD, Mcr_swept)

n = 0
i = 10**(-n)
AR_lower= 5
AR_upper =10
sweep_lower = 5*pi/180
sweep_upper = 30*pi/180
AR_list = []
sweep_list = []
for j in np.arange(AR_lower,AR_upper+i,i):
    AR_list.append(round(j,n))
for j in np.arange(sweep_lower,sweep_upper+i,i):
    sweep_list.append(j)
dim_x = len(AR_list)
dim_y = len(sweep_list)
B = np.zeros((dim_x,dim_y))
C=np.zeros((dim_x,dim_y))



for b1 in AR_list:
    for b2 in sweep_list:
        #print(b1, b2)
        e_initial = 4.61 * (1-0.045*(b1+delta_AR)**0.68)*(cos(b2))**0.15 - 3.1
        K_initial = 1/(pi * e_initial * (b1+delta_AR))
        efficiency=CL_cruise/(C_D0_1stestimation + K_initial * CL_cruise**2)
        M_DD = ka/cos(b2) - 0.1/(cos(b2)**2) - CL_cruise/(10*cos(b2)**3)
        x = AR_list.index(b1)
        y = sweep_list.index(b2)
        if M_DD>=M_DD_min:
            B[x,y] = efficiency
        else:
            B[x, y]=0
            



np.set_printoptions(threshold = np.inf)
#print(B) - B contains the values
b_max = np.max(B)
A = np.where((B >= b_max)) #contains indices
print(np.transpose(A))
print(round(b_max,3))
#print(AR_list[[-1,0]], sweep_list[A[-1,1]])
print(B[1,1])
print(AR_list[1],180/pi*sweep_list[1])

#for i in range (100):
   # print(': ',round(AR_list[np.transpose(A)[i,0]],3),'b2: ',round(sweep_list[np.transpose(A)[i,1]],3))

M_DD_1 = ka/cos(11*pi/180) - 0.1/(cos(11*pi/180)**2) - CL_cruise/(10*cos(11*pi/180)**3)

print(M_DD_1, " ", M_DD_min)

#The surface area of the wing is kept constant (matching diagram).
#Therefore,
#AR_updated=AR_list[np.transpose(A)[0]]
sweep_LE_updated=180/pi*sweep_list[0]
b_updated=sqrt(AR_list[36]*wing_area)


sweep_quarter_chord_updated=0.0007162*180/pi #deg
dihedral_updated=3-0.1*sweep_quarter_chord_updated -2#deg
taper_updated=0.4-0.2*sweep_quarter_chord_updated*pi/180
root_chord_updated=2*wing_area/(1+taper_updated)/b_updated
chord_tip_updated=taper_updated*root_chord_updated
mac_updated=2/3*root_chord_updated*(1+taper_updated+taper_updated**2)/(1+taper_updated)
y_mac=b_updated/6*(1+2*taper_updated)/(1+taper_updated)
x_mac=y_mac*tan(radians(sweep_LE_updated))

#sweep_LE_updated=sweep_list[np.transpose(A)[1]]*180/pi
#sweep_quarter_chord_updated=degrees(atan(tan(radians(sweep_LE_updated))-0.4*2*/b*(1-taper))) #deg
#print(AR_updated)root_chord_updated
print(-1.6*wing_area/b_updated**2)
print('Span:',b_updated)
print('Sweep c/4: ',sweep_quarter_chord_updated )
print('Dihedral: ',dihedral_updated )
print('Taper: ',taper_updated)
print('Root chord: ',root_chord_updated)
print('Tip chord: ', chord_tip_updated)
print('MAC: ',mac_updated)
print('y_mac: ',y_mac)
print('x_mac: ',x_mac)
