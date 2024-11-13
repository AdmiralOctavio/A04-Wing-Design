from math import sqrt,atan,tan,radians,cos

MTOW=23173 #kg
OEW=13127 #kg
M_fuel=2845 #kg
MAC=2.915 #m
yMAC=4.895 #m
xMAC=1.446 #m
c_r=4.00 #m
taper=0.352
b=23.3 #m
t_over_c=0.1
wing_area=63.1 #m^2
tail_area=22 #m^2
t_r=c_r*t_over_c
l_nacelle=1.90 #m

MZFW=MTOW-M_fuel


R_D= 2963 #km #ferry range (our interpretation of the 'maximum range')
sweep_le=16.46 #deg
sweep_halfc=atan(tan(radians(sweep_le))-c_r/b*(1-taper))

b_s=b/cos(sweep_halfc)
b_ref=1.905 #m #from Torenbeek

#Fuselage dimensions
b_f=2.90
h_f=2.90
fineness=4.5
l_f=31.93


#horizontal tail
c_r_horizontal=2.56 #m
c_t_horizontal=1.1 #m
b_horizontal=7.86 #m
sweep_le_horizontal=26.6 #deg
taper=c_t_horizontal/c_r_horizontal
x_38_horizontal=0.38*b_horizontal/2*tan(radians(sweep_le_horizontal))


position=x_38_horizontal+0.42*c_r_horizontal*(1-(1-taper)*0.38)-0.25*c_r_horizontal #m, w.r.t. the root quarter-chord
print(position)
l_t= (0.9*l_f-position) -(13.5288-0.42*b/2*tan(radians(sweep_le))+0.25*MAC) #m  #distance from wing root quarter point to horizontal tail root quarter point
print(l_t, "MUC")
ft_per_meter=0.3048

ro=0.379597 #kg/m^3
V_cruise=0.77*296.535
V_dive_EAS=166.89*1.5 #m/s #NOTE: 1.5 is chosen as the safety factor
print('V_dive_EAS [kts]: ',V_dive_EAS*1.94384)
CL_alpha=5.76 #1/rad
W_over_S=MTOW/63.1*9.81 #N/m^2
#11799.298864687804
A_main=40
A_nose=20
B_main=0.16
B_nose=0.1
C_main=0.019
C_nose=0
D_main=1.5*10**(-5)
D_nose=2*10**(-6)

u_hat=66*ft_per_meter #m/s

mu=2*W_over_S/ro/9.81/CL_alpha/MAC

K=0.88*mu/(5.3+mu)

u=K*u_hat


#MAXIMUM LOAD FACTOR
n_max1=2.5 #(more than 51000 lbs)
n_max2=1+ro*V_cruise*CL_alpha*u/2/W_over_S #From gusts
n_ult=1.5*max(n_max1,n_max2)



#AIRFRAME STRUCTURAL WEIGHT #NOTE: n_max might be too high
M_structural_formula=MTOW*0.447*sqrt(n_ult)*((b_f*h_f*l_f)/MTOW)**0.24


#WING GROUP
W_w=(MZFW*6.67/1000*b_s**0.75*(1+sqrt(b_ref/b_s))*n_ult**0.55*(b_s/t_r*wing_area/MZFW)**0.3)*0.9


#TAIL GROUP
#EAS=V_cruise/sqrt(1.225/ro)
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

M_structural_buildup=W_w+W_tail+W_f+W_LG+W_sc+W_n


#PROPULSION GROUP
W_e=1040 #kg
N_e=2
W_prop=1.15*1.18*N_e*W_e*0.453592**2



#AIRFRAME SERVICES AND EQUIPMENT
W_ba=0.4*85.34
W_APU=11.7*(W_ba**0.6)

        #LOW_SUBSONIC
W_INE_1=54.4+9.1*2+0.006*MTOW

        #HIGH_SUBSONIC
W_INE_2=0.347*OEW**(5/9)*R_D**0.25

W_HPE=0.011*OEW+181 

W_EL=0.02*MTOW+181

W_furnish=0.196*(MTOW-M_fuel)**0.91

W_air_conditioning=14*(19.44**1.28)

W_misc=0.01*OEW

W_airframe_services=W_ba+W_APU+W_INE_2+W_EL+W_furnish+W_air_conditioning+W_misc  #Excludes fuel and passengers

OEW_new=M_structural_buildup+W_prop+W_airframe_services


W_fuel=0.804*3.8*1000   #kg

W_pax=(75+18)*72  #kg

print("W_pay/W_OEW",7255/OEW)


#CG POSITION
x_f=0.435*l_f
x_tail=0.9*l_f #Subject to change
x_nose=0.5*MAC
x_airframe_services=x_f

x_wing=0.07*b/2*tan(radians(sweep_le))+(0.2+0.7*0.4)*(c_r-c_r*(1-taper)*0.35)
x_nacelle=-0.1*l_nacelle #w.r.t. the xLEMAC
x_prop=-0.4*l_nacelle

W_fuselage_group=W_f+W_nose+W_tail+W_airframe_services #Excludes main LG
X_fuselage_group=(W_f*x_f+x_tail*W_tail+x_nose*W_nose+x_airframe_services*W_airframe_services)/W_fuselage_group
W_wing_group=W_w+W_n+W_prop
X_wing_group=(W_w*x_wing+W_n*x_nacelle+W_prop*x_prop)/W_wing_group


X_OE=0.225*MAC
X_LEMAC=X_fuselage_group-X_OE+W_wing_group/W_fuselage_group*((X_wing_group-X_OE))
x_wg=(0.2+0.7*(0.6-0.2))*MAC+tan(sweep_le*3.14/180)*0.35*b/2-b/6*((1+2*taper)/1+taper)*tan(sweep_le*3.14/180)+X_LEMAC



print("X_LEMAC: ",X_LEMAC)
print('Horizontal tail root quarter chord position with respect to wing root quarter chord: ',l_t)
print('Wing c.g. position w.r.t the fuselage nose: ',X_wing_group+X_LEMAC)
print('OEW c.g. position w.r.t. the fuselage nose: ',X_OE+X_LEMAC)

print('Airframe structural weight (simple formula) [kg], fraction of MTOW: ',M_structural_formula,M_structural_formula/MTOW) 
print('Airframe structural weight (from build-up) [kg], fraction of MTOW: ',M_structural_buildup,M_structural_buildup/MTOW)
print('Operating empty weight (old+new) [kg]: ',OEW,OEW_new) 
print('Maximum manoeuvre load factor: ',n_max1)
print('Maximum gust load factor: ',n_max2)
print('Ultimate load factor: ',n_ult)



print('W_w/MTOW:',W_w)
print('W_tail/MTOW: ',W_tail)
print('W_f/MTOW ',W_f)
print('W_LG/MTOW: ', W_LG)
print('W_sc/MTOW ',W_sc)
print('W_n/MTOW: ',W_n)
print('W_prop/MTOW: ',W_prop)