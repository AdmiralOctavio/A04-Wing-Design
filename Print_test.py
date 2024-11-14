import PlanformParameters
import SpeedsAndRange
import PropulsionParameters
import AerodynamicParameters
import FuselageParameters
import WeightParameters

Planform = PlanformParameters.Planform()
Miscellaneous = SpeedsAndRange.Miscellaneous()
Propulsion = PropulsionParameters.Propulsion()
Aerodynamics = AerodynamicParameters.Aerodynamics()
Fuselage = FuselageParameters.Fuselage()
Weight = WeightParameters.Weight()

PlanformData = vars(Planform)
PlanformDataString = str(PlanformData)
PlanformDataSplit = PlanformDataString.replace(':',',').replace("'",'').replace('{','').replace('}','').split(',')
print(PlanformData)
print(PlanformDataString)
print(PlanformDataSplit)

print(PlanformDataSplit[0])