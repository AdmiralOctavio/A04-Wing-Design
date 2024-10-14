from math import sqrt,atan,tan,radians,cos

MTOW=23173 #kg
OEW=13127 #kg
M_fuel=2845 #kg
MAC=3.16 #m
c_r=3.87 #m
taper=0.4
b=23.3 #m
t_over_c=0.1
wing_area=63.1 #m^2
tail_area=22 #m^2
t_r=c_r*t_over_c
Lambda_LE=4.6 #deg
Lambda_halfc=atan(tan(radians(Lambda_LE))-c_r/b*(1-taper))
MZFW=MTOW-M_fuel


b_s=b/cos(Lambda_halfc)
b_ref=1.905 #m


b_f=2.90
h_f=2.90
fineness=4.5
l_f=31.93

l_t= 15 #m  #distance from wing root quarter-point to horizontal tail root

ft_per_meter=0.3048

ro=0.379597 #kg/m^3
V=0.77*sqrt(1.4*287*218.8)
V_dive_EAS=166.89*1.5 #m/s #NOTE: Subject to change
CL_alpha=5.76 #1/rad
W_over_S=MTOW/63.1 #kg/m^2

A_main=40
A_nose=20
B_main=0.16
B_nose=0.1
C_main=0.019
C_nose=0
D_main=1.5*10**(-5)
D_nose=2*10**(-6)

u_hat=38*ft_per_meter #m/s

mu=2*W_over_S/ro/9.81/CL_alpha/MAC

K=0.88*mu/(5.3+mu)

u=K*u_hat


#MAXIMUM LOAD FACTOR
n_max=1+ro*V*CL_alpha*u/2/W_over_S
n_ult=1.5*n_max


#AIRFRAME STRUCTURAL WEIGHT #NOTE: n_max might be too high
M_s=MTOW*sqrt(1.5*n_max)*((b_f*h_f*l_f)/MTOW)**0.24


#WING GROUP
W_w=(MZFW*6.67/1000*b_s**0.75*(1+sqrt(b_ref/b_s))*n_ult**0.55*(b_s/t_r*wing_area/MZFW)**0.3)*0.9


#TAIL GROUP
EAS=V/sqrt(1.225/ro)
W_tail=0.64*(n_ult*tail_area**2)**0.75



#BODY GROUP 
S_f_wet=3.14*b_f*l_f*(1-2/fineness)**0.666667*(1+1/fineness**2)
W_f=0.23*sqrt(V_dive_EAS*l_t/(b_f+h_f))*S_f_wet**1.2


#LANDING GEAR GROUP
W_main=1.08*(A_main+B_main*(MTOW/0.453592)**0.75+C_main*(MTOW/0.453592)+D_main*(MTOW/0.453592)**1.5)
W_nose=1.08*(A_nose+B_nose*(MTOW/0.453592)**0.75+C_nose*MTOW/0.453592+D_nose*(MTOW/0.453592)**1.5)
W_LG=(W_main+W_nose)*0.453592


#SURFACE CONTROLS GROUP
W_sc=0.64*1.2*0.768*MTOW**0.666667

#NACELLE GROUP
W_n=0.065*0.453592*0.4*MTOW

#PROPULSION GROUP
W_e=1724 #kg
N_e=2
W_prop=1.15*1.18*N_e*W_e*0.453592**2



print(MTOW*2.20462)
print(2.1+24000/(MTOW*2.20462+10000))

print(n_max)
print('M_s/MTOW: ',M_s/MTOW)
print('Half-chord sweep angle: ',Lambda_halfc*180/3.14)
print('W_w/MTOW:',W_w/MTOW)
print('EAS: ',EAS)
print('W_tail/MTOW: ',W_tail/MTOW)
print('W_tail [kg]: ',W_tail)
print('Cruise speed: ', V)
print("Fuselage weight [kg]: ",W_f)
print('W_f/MTOW ',W_f/MTOW)
print('W_LG/MTOW: ', W_LG/MTOW)
print('W_sc/MTOW ',W_sc/MTOW)
print('W_n/MTOW: ',W_n/MTOW)
print('W_prop/MTOW: ',W_prop/MTOW)