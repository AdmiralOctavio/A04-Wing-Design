import math
# import CGestimations

# X_aftcg = Xaftcg_calculator()

X_aftcg = 20
S = 63.1 #m^2
C_r = 3.870 #m
C_t = 1.547 #m
taper_ratio = C_t/C_r
C_MAC = 2.870 #m
b = 23.30 #m

L = 31 #m - fuselage length

n = 4 #number of reference planes from the Roskam Vh, Vv, Xh and Xh tables - jet transport a/c

#aspect ratios taken as middle of intervals given in ADSEE year 1 lecture

#horizontal tail stuff:
sweep_htail_c_over_4_list = [30, 22, 25]
sweep_htail_c_over_4 = sum(sweep_htail_c_over_4_list)/3 #max 40deg, min sweep_wing_c_over_4

A_h_list = [4, 3.5, 4]
A_h = sum(A_h_list)/3

taper_h_list = [0.3, 0.6, 0.5]
taper_h = sum(taper_h_list)/3 #on the lower side, so that it decreases the tail's weight

V_h_list = [0.96, 1.32, 1.07, 0.86]
V_h = sum(V_h_list)/n

# X_h_list = [18.714, 17.312, 14.386, 12.405] #chosen
# X_h = sum(X_h_list)/n
# S_h = (V_h*S*C_MAC)/(X_h - X_aftcg) #computed
# deltaX_h = X_h - X_aftcg

# S_h = (V_h*S*C_MAC)/(deltaX_h)

#vertical tail stuff:
sweep_vtail_c_over_4_list = [35, 40]
sweep_vtail_c_over_4 = sum(sweep_vtail_c_over_4_list)/2 #max 50deg, min sweep_wing_LE

A_v_list = [2, 1.2]
A_v = sum(A_v_list)/2

taper_v_list = [0.3, 0.7]
taper_v = sum(taper_v_list)/2 #lower than horiz

V_v_list = [0.062, 0.079, 0.085, 0.038]
V_v = sum(V_v_list)/n

# deltaX_v = X_v - X_aftcg
# X_v_list = [15.392, 14.082, 11.552, 9.936] #chosen 
# X_v = sum(X_v_list)/n
# S_v = (V_v*S*b)/(X_v - X_aftcg)

# S_v = (V_v*S*b)/(deltaX_v)

#iterating over values of deltaX_h and deltaX_h
l = round(3*L/4, 1)
l = int(l)
# print(l)
for i in range(1, 2*l, 1):
    deltaX_h = i/2
    deltaX_v = i/2 + 0.5
    S_h = (V_h*S*C_MAC)/(deltaX_h)
    S_v = (V_v*S*b)/(deltaX_v)
    print(round(S_h, 2), "    ", round(S_v, 2))

print(sweep_htail_c_over_4, "    ", sweep_vtail_c_over_4, "    ", taper_h, "    ", taper_v, "    ", A_h, "    ", A_v)