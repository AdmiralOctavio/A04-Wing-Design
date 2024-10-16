from math import sqrt, log, pi
import numpy as np

def Re(L):
    Re1 = float(rho*V*L/mu)
    Re2 = float(38.21*(L/k)**1.053)
    Re = min(Re1, Re2)
    #print(round(Re*10**(-6),2))
    return Re

def CF_nose(a,L):
    dx = 0.0001
    Cf = 0
    ReL = Re(L)
    for x in np.arange(dx,a**2+dx,dx):
        Cf += sqrt(1+x)/((sqrt(x*(x+1)) + log(sqrt(x)+sqrt(x+1)))**0.2) * dx
        #print(Cf)
    Cf *= 0.0888*a**1.4/((1+a**2)**1.5-1) * 1/ReL**0.2
    s = (a*sqrt(a**2+1) + log(a+sqrt(a**2+1)))/a**2
    return Cf, s

def Cf_cyl(s,L):
    ReL = Re(L)
    r = s/L
    #print(ReL)
    #print(r)
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
    #r = s/L
    #Cf = 0.0592/0.72/ReL**0.2 * ((1+r)**1.8 - r**1.8 - 1.8*r**0.8)
    dx = 0.0001
    Cf = 0
    ReL = Re(L)
    for x in np.arange(dx,1+dx,dx):
        Cf += sqrt(1-x)/((s/L + sqrt(1+D**2/(4*L**2))*x)**0.2) * dx
        #print(Cf)
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

def S_wing(cr,ct,b):
    S = 1.07*2*(cr+ct)*b/2
    return S

scaling = 1
prec1 = 5
prec2 = 2

mu_v = [1.327*10**(-5),1.7894**(-5)]
V_v = [228.3,62.24]
rho_v = [0.3795,1.225]
T_v = [218.8,288.15]

R  = 287
k  = 0.634*10**(-5)
p_lam_W = 0.1
p_lam_fus = 0.05
gma= 1.4


L1 = 5.23*scaling
L2 = 19.44*scaling
L3 = 7.26*scaling
D  = 2.90*scaling

b  = 23.3*scaling
cr = 3.87*scaling
ct = 1.47*scaling

b_HT = 7.865*scaling
cr_HT = 2.558*scaling
ct_HT = 1.100*scaling

b_VT = 3.051*scaling
cr_VT = 2.991*scaling
ct_VT = 2.094*scaling

D_eng = 1.08*scaling
L_eng = 1.9*scaling


a = 4*L1/D
L_tail = sqrt(L3**2 + D**2/4)



case = 1 #0 for cruise, 1 for TO/L



for case in range(case,case+1):
    mu = mu_v[case]
    V  = V_v[case]
    rho= rho_v[case]/scaling
    T  = T_v[case]

    M = V/sqrt(gma*R*T)

    Cf_nose, s1 = CF_nose(a,L1)
    s = s1*L1
    Cf_fus = Cf_cyl(s,L2)
    s += L2
    Cf_cone = CF_cone(s,L_tail)

    Cf_W = Cf_wing(cr,ct,b)
    Cf_HT = Cf_wing(cr_HT,ct_HT,b_HT)
    Cf_VT = Cf_wing(cr_VT,ct_VT,b_VT*2)/2

    Cf_eng = 2*Cf_cyl(0,L_eng)


    #S_nose = pi*D**2/6/a**2 * ((1+a)**1.5-1) #this is wrong, check formula
    S_nose = pi*D**2/(6*a**2) * ((1+a**2)**1.5-1)
    S_fus = pi*D*L2
    S_cone = pi*D*L_tail/2
    S_W = S_wing(cr,ct,b)
    S_HT = S_wing(cr_HT,ct_HT,b_HT)
    S_VT = S_wing(cr_VT,ct_VT,b_VT*2)/2
    S_eng = 2*pi*D_eng*L_eng
    S_wet = S_nose + S_fus + S_cone + S_W + S_HT + S_VT + S_eng

    print('\t','Cf\t\t','Swet')
    print('Nose\t',round(Cf_nose,prec1), '\t', round(S_nose,prec2))
    print('Fuselage',round(Cf_fus,prec1), '\t', round(S_fus,prec2))
    print('Cone\t',round(Cf_cone,prec1), '\t', round(S_cone,prec2))
    print('Wing\t',round(Cf_W,prec1), '\t', round(S_W,prec2))
    print('H tail\t',round(Cf_HT,prec1), '\t', round(S_HT,prec2))
    print('V tail\t',round(Cf_VT,prec1), '\t', round(S_VT,prec2))
    print('Engines\t',round(Cf_eng,prec1), '\t', round(S_eng,prec2))
    print('Swet =', round(S_wet,prec2))

    #TEST
    S_ref = (cr+ct)*b/2
    Cf = (S_nose*Cf_nose + S_fus*Cf_fus + S_cone*Cf_cone + S_W*Cf_W + S_HT*Cf_HT + S_VT*Cf_VT + S_eng*Cf_eng)/S_wet
    CD = Cf*S_wet/S_ref
    print('Cf =', round(Cf,prec1))
    print('CD0 =', round(CD,prec1))



