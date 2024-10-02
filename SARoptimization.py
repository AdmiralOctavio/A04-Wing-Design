from math import sqrt
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

L_over_D = 15.9

C_dcruise = 0.00484
C_d0 = 0.0065
# Airfoil_selection.CL_cruise 
CL_cruise = 0.37594287624283806

# C_D0 = 
# C_Di = 
# C_Dcruise = 

# D = 1/2 * C_Dcruise * rho_cruise * V_cruise**2 * S

RF = M_cruise * L_over_D * a_cruise / TSFC 
SAR_MTOW = RF / W_MTOW
SAR_OE = RF / W_OE

print("SAR_MTOW = ",  SAR_MTOW, "       " , "SAR_OE = " , SAR_OE, "        ", "in cursed units")

print("SAR_MTOW = ",  SAR_MTOW*1000**2, "       " , "SAR_OE = " , SAR_OE*1000**2, "       " , "in m/kg")