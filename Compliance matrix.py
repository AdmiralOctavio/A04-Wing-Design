from math import sqrt
from Matching_Diagram import TpW_max, WpS_min
from MassEstimate import MTOW,fuel,TSFC

T=218.8 #kelvin
p=23820 #Pa
R=287 #J/kg/K
gamma=1.4

C_L_cruise=0.7#TO_BE_DETERMINED

ro=p/R/T
a= sqrt(gamma*R*T)

def cruise_mach_number():
    M=sqrt(2*WpS_min/ro/C_L_cruise)/a
    print(M)
    
print(sqrt(2*WpS_min/ro/C_L_cruise)/a)
#cruise_mach_number()
speed=sqrt(2*WpS_min/ro/C_L_cruise)

thrust=MTOW*9.81*TpW_max/1000 #kN

print(WpS_min)
print(TpW_max)
print('Speed of sound', a)
print('Speed: ', speed)
print('Endurance: ',fuel*1000/TSFC/thrust)

print('Range: ', fuel*1000/TSFC/thrust*speed/1000) #km