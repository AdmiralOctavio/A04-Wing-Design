import matplotlib.pyplot as plt
import math as m
import numpy as np

m_TOW = 23177 #kg
m_fuel = 2848
m_platMTOW = 6355
m_plmax = 9302
m_despl = 7200
m_OE = 13130
m_OE2 = 12375
m_fullfuel = 3115

m_fuelmaxstructpl = m_TOW - m_OE - m_plmax

R_aux = 1363
R_ferry = 2963
R_design = 2019 #km
R_MTOW = 2574

L_over_D = 15.9
eta_eng = 0.35783466450161727
g = 9.81 #m/s^2
e_f = 44000000 #J/kg

R_maxstructpl= eta_eng*L_over_D*(e_f/g) * np.log((m_OE + m_plmax + m_fuelmaxstructpl)/(m_OE + m_plmax))/np.log(m.exp(1)) - R_aux
R_maxstructpl = int(R_maxstructpl/1000)

R_maxstructpl2= eta_eng*L_over_D*(e_f/g) * np.log((m_OE2 + m_platMTOW + m_fullfuel)/(m_OE + m_platMTOW))/np.log(m.exp(1)) - R_aux
R_maxstructpl2 = int(R_maxstructpl/1000)

#plotting the payload range diagram
#blue:
ranges = [0, R_maxstructpl, R_design, R_ferry]
payloadmasses = [m_plmax, m_plmax, m_despl, 0]
#orange:
rangesMTOW = [0, R_maxstructpl, R_MTOW, R_ferry]
payloadmassesMTOW = [m_plmax, m_plmax, m_platMTOW, 0]
#red:
rangeboth=[R_design, R_ferry]
payloadmassboth = []

x = [1000, 2000, 3000]
y = [2000, 4000, 6000, 8000]
xmin = 0
xmax = max(x)
ymin = 0
ymax = max(y)

# plt.subplot(131)
# plt.title('Payload-Range for design case')
# for i in range (0, 3):
#     plt.axvline(x[i], ymin, ymax, color = "black", linewidth = 0.25)
# for i in range(0, 4):
#     plt.axhline(y[i], xmin, xmax, color = "black", linewidth = 0.25)
# plt.plot(ranges, payloadmasses, color = "blue")
# plt.scatter(ranges, payloadmasses)
# plt.xlabel('Range [km]')
# plt.ylabel('Payload mass [kg]')
# # plt.plot()
# # plt.show()

# plt.subplot(132)
# plt.title('Payload-Range for full fuel case')
# for i in range (0, 3):
#     plt.axvline(x[i], ymin, ymax, color = "black", linewidth = 0.25)
# for i in range(0, 4):
#     plt.axhline(y[i], xmin, xmax, color = "black", linewidth = 0.25)
# plt.plot(rangesMTOW, payloadmassesMTOW, color = "orange")
# plt.scatter(rangesMTOW, payloadmassesMTOW)
# plt.xlabel('Range [km]')
# plt.ylabel('Payload mass [kg]')
# # plt.plot()
# # plt.show()

# plt.subplot(133)
# plt.title('Payload-Range for both cases')
# for i in range (0, 3):
#     plt.axvline(x[i], ymin, ymax, color = "black", linewidth = 0.25)
# for i in range(0, 4):
#     plt.axhline(y[i], xmin, xmax, color = "black", linewidth = 0.25)
# plt.plot(ranges, payloadmasses, color = "blue")
# plt.scatter(ranges, payloadmasses)
# plt.plot(rangesMTOW, payloadmassesMTOW, color = "orange")
# plt.scatter(rangesMTOW, payloadmassesMTOW)
# plt.xlabel('Range [km]')
# plt.ylabel('Payload mass [kg]')
# # plt.plot()
# plt.show()

rangeboth=[0, R_maxstructpl, R_design, R_MTOW, R_ferry]
payloadmassboth = [m_plmax, m_plmax, m_despl, m_platMTOW, 0]

plt.title('Payload-Range Diagram')
for i in range (0, 3):
    plt.axvline(x[i], ymin, ymax, color = "black", linewidth = 0.25)
for i in range(0, 4):
    plt.axhline(y[i], xmin, xmax, color = "black", linewidth = 0.25)
plt.plot(rangeboth, payloadmassboth, color = "blue")
plt.scatter(rangeboth, payloadmassboth)
plt.xlabel('Range [km]')
plt.ylabel('Payload mass [kg]')
# plt.plot()
plt.show()

# print(R_maxstructpl,"\n", m_OE,"\n", m_fuelmaxstructpl)