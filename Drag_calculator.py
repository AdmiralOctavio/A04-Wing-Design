from math import sqrt, log, pi
import numpy as np

#Reynolds number
def Re(L):
    Re1 = float(rho*V*L/mu)
    Re2 = float(38.21*(L/k)**1.053)
    Re = min(Re1, Re2)
    return Re

#Skin friction coefficients
def CF_nose(a,L):
    dx = 0.0001
    Cf = 0
    ReL = Re(L)
    for x in np.arange(dx,a**2+dx,dx):
        Cf += sqrt(1+x)/((sqrt(x*(x+1)) + log(sqrt(x)+sqrt(x+1)))**0.2) * dx
    Cf *= 0.1776*a**0.4/((1+a**2)**1.5-1) * 1/ReL**0.2
    s = (a*sqrt(a**2+1) + log(a+sqrt(a**2+1)))/a**2
    return Cf, s
def CF_cyl(s,L):
    ReL = Re(L)
    r = s/L
    Cf = 0.074/ReL**0.2 * ((1+r)**0.8-r**0.8)
    return Cf
def Cf_plate_turb(L):
    ReL = Re(L)
    Cf = 0.455/((log(ReL)/log(10))**2.58 * (1+0.144*M**2)**0.65)
    #Cf = 0.074/ReL**0.2
    return Cf
def Cf_plate_lam(L):
    ReL = Re(L)
    Cf = 1.328/sqrt(ReL)
    return Cf
def CF_cone(s,L):
    ReL = Re(L)
    dx = 0.0001
    Cf = 0
    ReL = Re(L)
    for x in np.arange(dx,1+dx,dx):
        Cf += sqrt(1-x)/((s/L + sqrt(1+D**2/(4*L**2))*x)**0.2) * dx
    Cf *= 0.1184 * 1/ReL**0.2
    return Cf
def Cf_wing(cr,ct,b):
    du = 0.0001
    Cf = 0
    for u in np.arange(du,1+du,du):
        c = cr - (cr-ct)*u
        dCf = (p_lam_W*Cf_plate_lam(c)+(1-p_lam_W)*Cf_plate_turb(c))*du
        Cf += 2*dCf*c/(cr+ct)
    return Cf

#Wing-like sufrfaces
def S_wing(cr,ct,b):
    S = 1.07*2*(cr+ct)*b/2
    return S

#Parameters
scaling = 1 #For checking whether the size matters for the same RE - it should not
prec1 = 5 #Precision for Cf
prec2 = 2 #Precision for S

mu_v = [1.327*10**(-5),1.7894*10**(-5)] #Viscosity
V_v = [228.3,62.24] #Velocity
rho_v = [0.3795,1.225] #Density
T_v = [218.8,288.15] #Temperature

R  = 287 #Gas constant
k  = 0.634*10**(-5) #Roughness
p_lam_W = 0.1 #Proportion laminar wing
p_lam_fus = 0.05 #Proportion laminar fuselage - unused though
gma = 1.4 #Adiabatic consnant

#Sizes
#Fuselage
L1 = 5.23*scaling
L2 = 19.44*scaling
L3 = 7.26*scaling
D  = 2.90*scaling

#Wing
b  = 23.295*scaling
cr = 4.004*scaling
ct = 1.413*scaling

#Horizontal tail
b_HT = 7.865*scaling
cr_HT = 2.558*scaling
ct_HT = 1.100*scaling

#Vertical tail
b_VT = 3.051*scaling
cr_VT = 2.991*scaling
ct_VT = 2.094*scaling

#Engines
D_eng = 1.08*scaling
L_eng = 1.9*scaling

#Useful constants
a = 4*L1/D
L_tail = sqrt(L3**2 + D**2/4)



case = 1 #0 for cruise, 1 for TO/L

#Loop in case we change our mind and make both cases in a single run
for case in range(0,2):
    mu = mu_v[case]
    V  = V_v[case]
    rho= rho_v[case]/scaling
    T  = T_v[case]

    M = V/sqrt(gma*R*T)

    #Cf calculation for all parts
    Cf_nose, s1 = CF_nose(a,L1)
    s = s1*L1
    Cf_cyl = CF_cyl(s,L2)
    s += L2
    Cf_cone = CF_cone(s,L_tail)
    Cf_W = Cf_wing(cr,ct,b)
    Cf_HT = Cf_wing(cr_HT,ct_HT,b_HT)
    Cf_VT = Cf_wing(cr_VT,ct_VT,b_VT*2)/2
    Cf_eng = 2*CF_cyl(0,L_eng)

    #S calculation for all parts
    S_nose = pi*D**2/(6*a**2) * ((1+a**2)**1.5-1)
    S_cyl = pi*D*L2
    S_cone = pi*D*L_tail/2
    S_W = S_wing(cr,ct,b)
    S_HT = S_wing(cr_HT,ct_HT,b_HT)
    S_VT = S_wing(cr_VT,ct_VT,b_VT*2)/2
    S_eng = 2*pi*D_eng*L_eng
    S_tot = S_nose + S_cyl + S_cone + S_W + S_HT + S_VT + S_eng

    S_fus = S_nose + S_cyl + S_cone
    Cf_fus = (Cf_nose*S_nose + Cf_cyl*S_cyl + Cf_cone*S_cone)/S_fus

    #Printing
    print('\n')
    if case == 0:
        print('Cruise','Cf\t\t','Swet')
    if case == 1:
        print('Approach','Cf\t\t','Swet')
    print('\n')
    print('Nose\t',round(Cf_nose,prec1), '\t', round(S_nose,prec2))
    print('Cylinder',round(Cf_cyl,prec1), '\t', round(S_cyl,prec2))
    print('Cone\t',round(Cf_cone,prec1), '\t', round(S_cone,prec2))
    print('Fuselage',round(Cf_fus,prec1), '\t', round(S_fus,prec2))
    print('Wing\t',round(Cf_W,prec1), '\t', round(S_W,prec2))
    print('H tail\t',round(Cf_HT,prec1), '\t', round(S_HT,prec2))
    print('V tail\t',round(Cf_VT,prec1), '\t', round(S_VT,prec2))
    print('Engines\t',round(Cf_eng,prec1), '\t', round(S_eng,prec2))
    print('Stot =', round(S_tot,prec2))

    #Check overal values
    S_ref = (cr+ct)*b/2
    Cf = (S_nose*Cf_nose + S_fus*Cf_fus + S_cone*Cf_cone + S_W*Cf_W + S_HT*Cf_HT + S_VT*Cf_VT + S_eng*Cf_eng)/S_tot
    CD = Cf*S_tot/S_ref
    print('Cf =', round(Cf,prec1))
    print('CD0 =', round(CD,prec1))

    if case == 1:
        Cf_nose_app = Cf_nose
        Cf_cyl_app = Cf_cyl
        Cf_cone_app = Cf_cone
        Cf_fus_app = Cf_fus
        Cf_W_app = Cf_W
        Cf_HT_app = Cf_HT
        Cf_VT_app = Cf_VT
        Cf_eng_app = Cf_eng
        Cf_tot_app = Cf

    elif case == 0:
        Cf_nose_cr = Cf_nose
        Cf_cyl_cr = Cf_cyl
        Cf_cone_cr = Cf_cone
        Cf_fus_cr = Cf_fus
        Cf_W_cr = Cf_W
        Cf_HT_cr = Cf_HT
        Cf_VT_cr = Cf_VT
        Cf_eng_cr = Cf_eng
        Cf_tot_cr = Cf


#Note on the obtained values
'''
Other method - just use formulas (approximate whole fuselage with cylinder and wing with MAC:
L = 31.93m
MAC = 3.16m

FOR CRUISE:
Refus = 20871018
Cflamfus = 0.000092
CFturbfus = 0.00182
Cffus = 0.001738 (9.8% smaller)
Rewing = 20631645
Cflamwing = 0.000292
Cfturbwing = 0.002543
Cfwing = 0.002318 (2.2% smaller)

FOR LANDING:
Refus = 136049565
Cflamfus = 0.000114
CFturbfus = 0.002033
Cffus = 0.001937 (7.0% smaller)
Rewing = 13464348
Cflamwing = 0.000362
Cfturbwing = 0.002856
Cfwing = 0.002607 (2.4% smaller)

Conclusion: Results are valid.
'''
