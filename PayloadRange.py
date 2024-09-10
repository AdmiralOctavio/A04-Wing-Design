import matplotlib.pyplot as plt
import math as m
import numpy as np

m_TOW = 23177 #kg
m_fullfuel = 2848
m_platMTOW = 6355
m_plmax = 9302
m_despl = 7200
m_OE = 13130

m_fuelmaxstructpl = m_TOW - m_OE - m_plmax

R_aux = 1363
R_ferry = 2963
R_MTOW = 2019 #km

L_over_D = 15.9
eta_eng = 0.35783466450161727
g = 9.81 #m/s^2
e_f = 44000000 #J/kg

R_maxstructpl= eta_eng*L_over_D*(e_f/g) * np.log((m_OE + m_plmax + m_fuelmaxstructpl)/(m_OE + m_plmax))/np.log(m.exp(1)) - R_aux

print(R_maxstructpl/1000,"\n", m_OE,"\n", m_fuelmaxstructpl)