def SAR(wing_area=63.1,OEW=13127,MTOW=23173,AR=7.5,lambda_LE=27.2):

    from math import sqrt, cos, pi, radians, tan, atan
    import numpy as np
    import Airfoil_selection

    #Constants
    M_cruise = 0.77
    M_DD_min = 1.05*0.77
    h_cruise = 35000 #ft
    T_cruise = 218.808 #K
    gamma = 1.4
    R = 8.31446261815324 #J
    rho_cruise = 0.3796 #kg/m^3
    g = 9.80665 
    m_MTOW = 23173
    W_OE = OEW * g
    W_MTOW = MTOW * g
    a_cruise = sqrt(gamma * T_cruise * R)
    V_cruise = M_cruise * a_cruise
    Swet_over_S = 6
    B = 5.9
    C_fe = 0.0026
    TSFC = 22* B**(-0.19) #g s^-1 kN^-1
    t_over_c = 0.1
    ka = 0.935

    taper=0.35 #TAPER IS NOW FIXED
    Cd_cruise = Airfoil_selection.Cd_cruise
    C_d0 = 0.0065#Constant
    Cl_cruise = Airfoil_selection.Cl_cruise_airfoil
    CL_cruise = Airfoil_selection.CL_cruise

    #Calculating C_D0:

    C_D0_1stestimation = C_fe * Swet_over_S

    #Calculating the induced drag:
    delta_AR = 0.04 #adsee lecture 2 slide 66, NOT 65
    #clean config:

    AR_eff = AR + delta_AR
    e_initial = 4.61 * (1-0.045*AR_eff**0.68)*(cos(lambda_LE))**0.15 - 3.1

    K_initial = 1/(pi * e_initial * AR_eff)

    CD_initial = C_D0_1stestimation + K_initial * CL_cruise**2

    L_over_D = CL_cruise/CD_initial



    #estimating the range factor and the SAR:

    RF = M_cruise * L_over_D * a_cruise / TSFC 
    SAR_MTOW = RF / W_MTOW
    SAR_OE = RF / W_OE

    

    n = 1
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
            if M_DD>M_DD_min:
                B[x,y] = efficiency
            else:
                B[x,y]=0
                



    np.set_printoptions(threshold = np.inf)
    
    b_max = np.max(B) #print(B) - B contains the values
    A = np.where((B >= b_max)) #contains indices #print(np.transpose(A))
    
    position1 = A[0] #the index of the aspect ratio
    position2 = A[1] #the index of the sweep angle
    print(B[position1, position2])
    print(AR_list[int(position1)],180/pi*sweep_list[int(position2)])

    M_DD_1 = ka/cos(10.8*pi/180) - 0.1/(cos(10.8*pi/180)**2) - CL_cruise/(10*cos(10.8*pi/180)**3)

    print(M_DD_1, " ", M_DD_min)

   
    #Therefore,
    #AR_updated=AR_list[np.transpose(A)[0]]

    #UPDATING ALL WING PARAMETERS!!!!!
    sweep_LE_updated=180/pi*sweep_list[position2]
    AR_updated=AR_list[position1]
    b_updated=sqrt(AR_updated*wing_area)

    #sweep_quarter_chord_updated = 0.235695 * 180/pi #from function intersection
    dihedral_updated=3-0.1*sweep_quarter_chord_updated -2#deg
    
    root_chord_updated=2*wing_area/(1+taper)/b_updated
    chord_tip_updated=taper*root_chord_updated
    mac_updated=2/3*root_chord_updated*(1+taper+taper**2)/(1+taper)
    y_mac=b_updated/6*(1+2*taper)/(1+taper)
    x_mac=y_mac*tan(radians(sweep_LE_updated))
    # sweep_quarter_chord_updated= 180/pi*atan(tan(radians(sweep_LE_updated))+root_chord_updated/(2*b_updated)*()) #deg

    #sweep_LE_updated=sweep_list[np.transpose(A)[1]]*180/pi
    #sweep_quarter_chord_updated=degrees(atan(tan(radians(sweep_LE_updated))-0.4*2*/b*(1-taper))) #deg
    print(-1.6*wing_area/b_updated**2)
    # print('Aspect ratio: ', AR_updated)
    print("SAR_MTOW = ",  SAR_MTOW, "       " , "SAR_OE = " , SAR_OE, "        ", "in cursed units")
    print("SAR_MTOW = ",  SAR_MTOW*1000, "       " , "SAR_OE = " , SAR_OE*1000, "       " , "in km/kg")
    print('Max L/D: ',round(b_max,3))
    print('Span:',b_updated)
    print('Sweep LE: ',sweep_LE_updated )
    print('Sweep c/4: ',sweep_quarter_chord_updated )
    print('Dihedral: ',dihedral_updated )
    print('Taper: ',taper_updated)
    print('Root chord: ',root_chord_updated)
    print('Tip chord: ', chord_tip_updated)
    print('MAC: ',mac_updated)
    print('y_mac: ',y_mac)
    print('x_mac: ',x_mac)

SAR(wing_area=63.1,OEW=13127,MTOW=23173,AR=7.5,lambda_LE=27.2)