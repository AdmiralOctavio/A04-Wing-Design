from math import sqrt, cos, pi, radians
# import Airfoil selection

M_cruise = 0.77
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

B = 9 
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
Mcr_unswept = 0.8133333
Mcr_swept = Mcr_unswept /cos(lambda_LE_2)

t_over_c = 0.1
ka = 0.935

e_3 = 4.61 * (1-0.045*AR_eff**0.68)*(cos(lambda_LE_2))**0.15 - 3.1

K_3 = 1/(pi * e_3 * AR_eff)

CD_3 = C_D0_1stestimation + K_3 * CL_cruise**2

L_over_D_3 = CL_cruise/CD_3

M_DD = ka/cos(lambda_LE_2) - t_over_c / (cos(lambda_LE_2))**2 - CL_cruise / (10*(cos(lambda_LE_2))**3)

#estimating the range factor and the SAR:

RF = M_cruise * L_over_D * a_cruise / TSFC 
SAR_MTOW = RF / W_MTOW
SAR_OE = RF / W_OE

print("SAR_MTOW = ",  SAR_MTOW, "       " , "SAR_OE = " , SAR_OE, "        ", "in cursed units")

print("SAR_MTOW = ",  SAR_MTOW*1000**2, "       " , "SAR_OE = " , SAR_OE*1000**2, "       " , "in m/kg")

print(e_initial, CD_initial)
print(e_2, CD_2)
print(e_3, CD_3)

print(CL_cruise/CD_initial)
print(CL_cruise/CD_2)
print(CL_cruise/CD_3)

print(M_DD, Mcr_swept)