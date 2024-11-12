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