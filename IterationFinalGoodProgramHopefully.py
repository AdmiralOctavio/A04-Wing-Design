import PlanformParameters
import SpeedsAndRange
import PropulsionParameters
import AerodynamicParameters
import FuselageParameters
import WeightParameters

#from Wing_parameters import Wing_parametersFunction

Planform = PlanformParameters.Planform()
Miscellaneous = SpeedsAndRange.Miscellaneous()
Propulsion = PropulsionParameters.Propulsion()
Aerodynamics = AerodynamicParameters.Aerodynamics()
Fuselage = FuselageParameters.Fuselage()
Weight = WeightParameters.Weight()


#Wing_parametersFunction(Planform,Miscellaneous)
#print (Planform.b)

from Matching_Diagram import MatchingDiagram
MatchingDiagram(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
#print(Miscellaneous.V_stall)
#print(Planform.WingLoading)
#print(Propulsion.Thrust_to_Weight)

from Ailerons import AileronsFunction
AileronsFunction(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
#print(Planform.y1ail)

from Drag_calculator import Cf_Calculator
Cf_Calculator(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
#print(Aerodynamics.Cf_tot_cr,Aerodynamics.Cf_tot_app,Aerodynamics.S_tot)

from Class2Drag import Class2_Drag
Class2_Drag(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
#print(Aerodynamics.CD0_Cruise)


import ClassII_Iteration

ClassII_Iteration.ClassIWeightEstimation(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
ClassII_Iteration.ClassIIWeightEstimation(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)


from undercarriage import Undercarriage
Undercarriage(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)

from SARoptimization import SAR
SAR(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
#print(Planform.b)