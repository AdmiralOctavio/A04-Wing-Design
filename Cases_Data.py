import math
import ADSEE_SC as ADSEE

def FreqUplink(f, Ratio):
    return f*Ratio
# CASE 1 - DOWNLINK

P_tx = 50  # W
T_sys = 135  # K
Ltx = 0.8
f = 22000000000.0  # Hz
h = 500000  # m
r = 6378000  # m
M = 597000000000000000000000000.0  # kg
Sw = 20  # deg
Pix_size = 0.1  # arcmin
B_pix = 8.0  # bits/pixel
D_tx = 0.2  # m
D_rx = 0.5  # m
eta = 0.55
d_E = 0.0  # m
d_S = 0.0  # m
theta_ES = 0.0  # deg
DC = 0.6
DLtime = 0.125
TurnAround = 221/240
alpha = math.radians(25)  # rad
e_tx = 0.1  # deg
L_space = 0.0
Loss_zen_dB = 0.035

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), ADSEE.Free_Space_Loss(f, r, alpha, h), L_space, ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.Data_rate_dB(M, r, h, B_pix, Sw, Pix_size, DC, DLtime))
print('Case 1 downlink received SNR:', SNR_rec)

# CASE 1 - UPLINK

P_tx = 400  # W
Tsys = 135  # K
Ltx = 0.7
f = FreqUplink(f, TurnAround)  # Hz
h = 500000  # m
r = 6378000  # m
M = 597000000000000000000000000.0  # kg
D_tx = 0.5  # m
D_rx = 0.2  # m
eta = 0.55
d_E = 0.0  # m
d_S = 0.0  # m
theta_ES = 0.0  # deg
DataRate = 100000000  # bit/s
alpha = math.radians(25)  # rad
e_tx = 0.01  # deg
L_space = 0.0
Loss_zen_dB = 0.035

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), ADSEE.Free_Space_Loss(f, r, alpha, h), L_space, ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.convert_to_dB(DataRate))
print('Case 1 uplink received SNR:', SNR_rec)

# CASE 2 - DOWNLINK

P_tx = 200  # W
T_sys = 135  # K
Ltx = 0.8
f = 22000000000.0  # Hz
h = 100000  # m
r = 1737500  # m
d = 376284500  # m
M = 7300000000000000000000000.0  # kg
Sw = 45  # deg
Pix_size = 0.1  # arcmin
B_pix = 8.0  # bits/pixel
D_tx = 4.2  # m
D_rx = 5.0  # m
eta = 0.55
d_E = 0.0  # m
d_S = 0.0  # m
theta_ES = 0.0  # deg
DC = 0.8
DLtime = 1/6
TurnAround = 221/240
alpha = math.radians(5)  # rad
e_tx = 0.1  # deg
L_space = 0.0
Loss_zen_dB = 0.035

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), ADSEE.Free_Space_Loss_Moon(d, f), L_space, ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.Data_rate_dB(M, r, h, B_pix, Sw, Pix_size, DC, DLtime))
print('Case 2 downlink received SNR:', SNR_rec)

# CASE 2 - UPLINK

P_tx = 400  # W
Tsys = 135  # K
Ltx = 0.7
f = FreqUplink(f, TurnAround)  # Hz
h = 100000  # m
r = 1737500  # m
d = 376284500  # m
M = 7300000000000000000000000.0  # kg
D_tx = 5.0  # m
D_rx = 4.2  # m
eta = 0.55
d_E = 0.0  # m
d_S = 0.0  # m
theta_ES = 0.0  # deg
DataRate = 10000000  # bit/s
alpha = math.radians(5)  # rad
e_tx = 0.01  # deg
L_space = 0.0
Loss_zen_dB = 0.035

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), ADSEE.Free_Space_Loss_Moon(d, f), L_space, ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.convert_to_dB(DataRate))
print('Case 2 uplink received SNR:', SNR_rec)

# CASE 3 - DOWNLINK

P_tx = 50  # W
T_sys = 135  # K
Ltx = 0.8
f = 84000000000.0  # Hz
h = 400000  # m
r = 3396000  # m
M = 64200000000000000000000000.0  # kg
Sw = 10.0  # deg
Pix_size = 0.05  # arcmin
B_pix = 8.0  # bits/pixel
D_tx = 2.0  # m
D_rx = 35.0  # m
eta = 0.55
d_E = 149000000000.0  # m 
d_S = 228000000000.0  # m
theta_ES = math.radians(20.0)  # deg
DC = 0.15
DLtime = 0.5
TurnAround = 749/880
alpha = math.radians(5)  # rad
e_tx = 0.1  # deg
Loss_zen_dB = 0.045
L_freeSpace = 0.0

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), L_freeSpace, ADSEE.Space_Loss(f, d_E, d_S, theta_ES), ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.Data_rate_dB(M, r, h, B_pix, Sw, Pix_size, DC, DLtime))
print('Case 3 downlink received SNR:', SNR_rec)

# CASE 3 - UPLINK

P_tx = 1000  # W
Tsys = 135  # K
Ltx = 0.7
f = FreqUplink(f, TurnAround)  # Hz
h = 400000  # m
r = 3396000  # m
M = 64200000000000000000000000.0  # kg
D_tx = 35.0  # m
D_rx = 2.0  # m
eta = 0.55
d_E = 149000000000.0  # m 
d_S = 228000000000.0  # m
theta_ES = math.radians(20.0)  # deg
DataRate = 1000000  # bit/s
alpha = math.radians(5)  # rad
e_tx = 0.01  # deg
Loss_zen_dB = 0.045
L_freeSpace = 0.0

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), L_freeSpace, ADSEE.Space_Loss(f, d_E, d_S, theta_ES), ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.convert_to_dB(DataRate))
print('Case 3 uplink received SNR:', SNR_rec)

# CASE 4 - DOWNLINK

P_tx = 200  # W
T_sys = 135  # K
Ltx = 0.8
f = 84000000000.0  # Hz
h = 500000  # m
r = 2439500  # m
M = 33000000000000000000000000.0  # kg
Sw = 10.0  # deg
Pix_size = 0.05  # arcmin
B_pix = 8.0  # bits/pixel
D_tx = 1.0  # m
D_rx = 35.0  # m
eta = 0.55
d_E = 149000000000.0  # m 
d_S = 28600000000.0  # m
theta_ES = math.radians(10.0)  # deg
DC = 0.4
DLtime = 0.75
TurnAround = 749/880
alpha = math.radians(5)  # rad
e_tx = 0.05  # deg
Loss_zen_dB = 0.045
L_freeSpace = 0.0

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), L_freeSpace, ADSEE.Space_Loss(f, d_E, d_S, theta_ES), ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.Data_rate_dB(M, r, h, B_pix, Sw, Pix_size, DC, DLtime))
print('Case 4 downlink received SNR:', SNR_rec)

# CASE 4 - UPLINK

P_tx = 1000  # W
Tsys = 135  # K
Ltx = 0.7
f = FreqUplink(f, TurnAround)  # Hz
h = 500000  # m
r = 2439500  # m
M = 33000000000000000000000000.0  # kg
D_tx = 35.0  # m
D_rx = 1.0  # m
eta = 0.55
d_E = 149000000000.0  # m 
d_S = 28600000000.0  # m
theta_ES = math.radians(10.0)  # deg
DataRate = 100000  # bit/s
alpha = math.radians(5)  # rad
e_tx = 0.005  # deg
Loss_zen_dB = 0.045
L_freeSpace = 0.0

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), L_freeSpace, ADSEE.Space_Loss(f, d_E, d_S, theta_ES), ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.convert_to_dB(DataRate))
print('Case 4 uplink received SNR:', SNR_rec)

# CASE 5 - DOWNLINK

P_tx = 100  # W
T_sys = 135  # K
Ltx = 0.8
f = 85000000000.0  # Hz
h = 2000000  # m
r = 60268000  # m
M = 56800000000000000000000000000.0  # kg
Sw = 20.0  # deg
Pix_size = 0.2  # arcmin
B_pix = 8.0  # bits/pixel
D_tx = 4.0  # m
D_rx = 35.0  # m
eta = 0.55
d_E = 149000000000.0  # m 
d_S = 1400000000000.0  # m
theta_ES = math.radians(10.0)  # deg
DC = 0.15
DLtime = 1.0
TurnAround = 749/880
alpha = math.radians(5)  # rad
e_tx = 0.1  # deg
Loss_zen_dB = 0.048
L_freeSpace = 0.0

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), L_freeSpace, ADSEE.Space_Loss(f, d_E, d_S, theta_ES), ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.Data_rate_dB(M, r, h, B_pix, Sw, Pix_size, DC, DLtime))
print('Case 5 downlink received SNR:', SNR_rec)

# CASE 5 - UPLINK

P_tx = 1000  # W
Tsys = 135  # K
Ltx = 0.7
f = FreqUplink(f, TurnAround)  # Hz
h = 2000000  # m
r = 60268000  # m
M = 56800000000000000000000000000.0  # kg
D_tx = 35.0  # m
D_rx = 4.0  # m
eta = 0.55
d_E = 149000000000.0  # m 
d_S = 1400000000000.0  # m
theta_ES = math.radians(10.0)  # deg
DataRate = 100000  # bit/s
alpha = math.radians(5)  # rad
e_tx = 0.01  # deg
Loss_zen_dB = 0.048
L_freeSpace = 0.0

SNR_rec = ADSEE.SNR_received(ADSEE.EIRP_dB(P_tx, Ltx, ADSEE.Trans_Antenna_Gain(f, D_tx, eta)), ADSEE.Trans_Antenna_Pointing_Loss(f, D_tx, e_tx), L_freeSpace, ADSEE.Space_Loss(f, d_E, d_S, theta_ES), ADSEE.Atm_loss(Loss_zen_dB, alpha), ADSEE.GoverT_receiver_dB(T_sys, f, eta, D_rx), ADSEE.convert_to_dB(DataRate))
print('Case 5 uplink received SNR:', SNR_rec)
