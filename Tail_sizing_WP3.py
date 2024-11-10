from math import sqrt, tan, atan, radians, pi
import numpy as np

S = 63.1 #m^2
C_r = 4.0044 #m
C_t = 1.4130 #m
taper_ratio = C_t/C_r
C_MAC = 2.915329 #m
X_LEMAC = 13.5288 #m
b = 23.295 #m - wingspan
L = 31.92992 #m - fuselage length

# OEW c.g. position w.r.t. the fuselage nose:  
X_OEW_CG = 14.18468925225589 #m
# X_v = 0.9*L #position of quarter-chord at the vertical tail MAC wrt nose
# X_h = 0.9*L #position of quarter-chord at the horizontal tail MAC wrt nose
X_h = 31.628 #m 
X_v = 30.202 #m

#horizontal tail values:
sweep_htail_c_over_4_list = np.array([30, 20, 25, 28, 30]) #dc9, bae146, fokker28, se-120 caravelle, bac111
sweep_htail_c_over_4 = np.average(sweep_htail_c_over_4_list) #max 40deg, min sweep_wing_c_over_4
std_sweep_h = np.std(sweep_htail_c_over_4_list)

A_h_list = np.array([4, 4, 3.5, 5, 5]) #dc9, bae146, Fokker28, se-120 caravelle, bac111
A_h = np.average(A_h_list)
std_A_h = np.std(A_h_list)

taper_h_list = np.array([0.3, 0.6, 0.5, 0.35, 0.4]) #dc9, bae146, Fokker28, se-120 caravelle, bac111
taper_h = np.average(taper_h_list) #on the lower side, so that it decreases the tail's weight
std_taper_h = np.std(taper_h_list)

V_h_list = np.array([0.96, 1.32, 1.07, 0.86, 1.48]) #dc9 s-80, dc9-50, fokker28, 
V_h = np.average(V_h_list)
std_V_h = np.std(V_h_list)

S_h = (V_h*S*C_MAC)/(X_h - X_OEW_CG)

b_h = sqrt(A_h * S_h)

C_avg_h = S_h/b_h

C_r_h = 2*C_avg_h/(1+taper_h)

C_t_h = taper_h * C_r_h

C_MAC_h = 2/3 * C_r_h * ((1 + taper_h + taper_h **2)/(1 + taper_h))

y_MAC_h = b_h/6 * ((1+2*taper_h)/(1+taper_h))

sweep_htail_LE = atan(tan(radians(sweep_htail_c_over_4)) - 2*C_r_h/b_h*(taper_h-1))

x_MAC_h = y_MAC_h * tan(sweep_htail_LE)

#vertical tail values:
sweep_vtail_c_over_4_list = np.array([35, 40, 43, 40]) #dc9, f28, bac111, bae146
sweep_vtail_c_over_4 = np.average(sweep_vtail_c_over_4_list) #max 50deg, min sweep_wing_LE
std_sweep_v = np.std(sweep_vtail_c_over_4_list)

A_v_list = np.array([1.2, 1.2, 1.2, 1.2]) #dc9, f28, bac111, bae146
A_v = np.average(A_v_list)
std_A_v = np.std(A_v_list)

taper_v_list = np.array([0.7, 0.7, 0.7, 0.7]) #dc9, f28, bac111, bae146
taper_v = np.average(taper_v_list)
std_taper_v = np.std(taper_v_list)

V_v_list = np.array([0.062, 0.079, 0.085, 0.038, 0.12])
V_v = np.average(V_v_list)
std_V_v = np.std(V_v_list)

S_v = (V_v*S*b)/(X_v - X_OEW_CG)

b_v = sqrt(A_v * S_v)

C_avg_v = S_v/b_v

C_r_v = 2*C_avg_v/(1+taper_v)

C_t_v = taper_v * C_r_v

C_MAC_v = 2/3 * C_r_v * ((1 + taper_v + taper_v **2)/(1 + taper_v))

y_MAC_v = b_v/6 * ((1+2*taper_v)/(1+taper_v))

sweep_vtail_LE = atan(tan(radians(sweep_vtail_c_over_4)) - 2*C_r_v/b_v*(taper_v-1))

x_MAC_v = y_MAC_v * tan(sweep_vtail_LE)

#printing everything nicely :)
print("Horizontal tail parameters:")
print("Horizontal tail area: ", S_h)
print("Horizontal tail span: ", b_h)
print("Horizontal tail root chord: ", C_r_h)
print("Horizontal tail tip chord: ", C_t_h)
print("Horizontal tail MAC: ", C_MAC_h)
print("Horizontail tail quarter chord sweep:", sweep_htail_c_over_4, "      ", "stdev: ", std_sweep_h)
print("Horizontail tail aspect ratio:", A_h, "      ","stdev: ", std_A_h)
print("Horizontail tail taper ratio:", taper_h,"      ", "stdev: ", std_taper_h)
print("Horizontail tail volume:", V_h,"      ", "stdev: ", std_V_h)
print("\n")
print("Vertical tail parameters:")
print("Vertical tail area: ", S_v)
print("Vertical tail root chord: ", C_r_v)
print("Vertical tail tip chord: ", C_t_v)
print("Vertical tail MAC: ", C_MAC_v)
print("Vertical tail quarter chord sweep:", sweep_vtail_c_over_4, "      ","stdev: ", std_sweep_v)
print("Vertical tail aspect ratio:", A_v,"      ", "stdev: ", std_A_v)
print("Vertical tail taper ratio:", taper_v,"      ", "stdev: ", std_taper_v)
print("Vertical tail volume:", V_v,"      ", "stdev: ", std_V_v)


# print(sweep_htail_LE*180/pi, x_MAC_h)
print(sweep_vtail_LE*180/pi, x_MAC_v)