import PlanformParameters
import SpeedsAndRange
import PropulsionParameters
import AerodynamicParameters
import FuselageParameters
import WeightParameters
import ClassII_Iteration

import matplotlib.pyplot as plt
import xlwt
import numpy as np

#from Wing_parameters import Wing_parametersFunction

Planform = PlanformParameters.Planform()
Miscellaneous = SpeedsAndRange.Miscellaneous()
Propulsion = PropulsionParameters.Propulsion()
Aerodynamics = AerodynamicParameters.Aerodynamics()
Fuselage = FuselageParameters.Fuselage()
Weight = WeightParameters.Weight()


#g = open("iteration" + str(0)+ ".dat", "w")  # Open file for writing

nmax = 10
prec = 5
form = '{:.'+str(prec)+'g}'

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Iteration Parameters")
sheet1.write(0, 0, "Variable")

np.set_printoptions(legacy='1.25')

for i in range(0,nmax+1):
    sheet1.write(0,i+1,"Value"+str(i))


PlanformData = vars(Planform)
PlanformDataString = str(PlanformData)
PlanformDataSplit = PlanformDataString.replace(':',',').replace("'",'').replace('{','').replace('}','').split(',')

MiscellaneousData = vars(Miscellaneous)
MiscellaneousDataString = str(MiscellaneousData)
MiscellaneousDataSplit = MiscellaneousDataString.replace(':',',').replace("'",'').replace('{','').replace('}','').split(',')

AerodynamicsData = vars(Aerodynamics)
AerodynamicsDataString = str(AerodynamicsData)
AerodynamicsDataSplit = AerodynamicsDataString.replace(':',',').replace("'",'').replace('{','').replace('}','').split(',')

FuselageData = vars(Fuselage)
FuselageDataString = str(FuselageData)
FuselageDataSplit = FuselageDataString.replace(':',',').replace("'",'').replace('{','').replace('}','').split(',')

WeightData = vars(Weight)
WeightDataString = str(WeightData)
WeightDataSplit = WeightDataString.replace(':',',').replace("'",'').replace('{','').replace('}','').split(',')

PropulsionData = vars(Propulsion)
PropulsionDataString = str(PropulsionData)
PropulsionDataSplit = PropulsionDataString.replace(':',',').replace("'",'').replace('{','').replace('}','').split(',')

row = 1
for j in range(0,len(PlanformDataSplit)):
    if (j%2 == 0):
        sheet1.write(row, 0, PlanformDataSplit[j])
        row += 1
for j in range(0,len(MiscellaneousDataSplit)):
    if(j%2 == 0):
        sheet1.write(row, 0, MiscellaneousDataSplit[j])
        row += 1
for j in range(0,len(AerodynamicsDataSplit)):
    if (j%2 == 0):
        sheet1.write(row, 0, AerodynamicsDataSplit[j])
        row += 1
for j in range(0,len(FuselageDataSplit)):
    if (j%2 == 0):
        sheet1.write(row, 0, FuselageDataSplit[j])
        row += 1
for j in range(0,len(WeightDataSplit)):
    if (j%2 == 0):
        sheet1.write(row, 0, WeightDataSplit[j])
        row += 1
for j in range(0,len(PropulsionDataSplit)):
    if (j%2 == 0):
        sheet1.write(row, 0, PropulsionDataSplit[j])
        row += 1
row = 1


for j in range(0,len(PlanformDataSplit)):
    if (j%2 != 0):
        sheet1.write(row, 1, '{:g}'.format(float(form.format(float(PlanformDataSplit[j])))))
        row += 1
for j in range(0,len(MiscellaneousDataSplit)):
    if(j%2 != 0):
        sheet1.write(row, 1, '{:g}'.format(float(form.format(float(MiscellaneousDataSplit[j])))))
        row += 1
for j in range(0,len(AerodynamicsDataSplit)):
    if (j%2 != 0):
        sheet1.write(row, 1, '{:g}'.format(float(form.format(float(AerodynamicsDataSplit[j])))))
        row += 1
for j in range(0,len(FuselageDataSplit)):
    if (j%2 != 0):
        sheet1.write(row, 1, '{:g}'.format(float(form.format(float(FuselageDataSplit[j])))))
        row += 1
for j in range(0,len(WeightDataSplit)):
    if (j%2 != 0):
        sheet1.write(row, 1, '{:g}'.format(float(form.format(float(WeightDataSplit[j])))))
        row += 1
for j in range(0,len(PropulsionDataSplit)):
    if (j%2 != 0):
        sheet1.write(row, 1, '{:g}'.format(float(form.format(float(PropulsionDataSplit[j])))))
        row += 1
row = 1





with open("iteration" + str(0) + ".dat", "w") as fout:
    # fout.write(str(PlanformData))
    for j in range(0, len(PlanformDataSplit)):
        fout.write(PlanformDataSplit[j] + '\n')

    fout.write('\n')

    for j in range(0, len(MiscellaneousDataSplit)):
        fout.write(MiscellaneousDataSplit[j] + '\n')

    fout.write('\n')

    for j in range(0, len(AerodynamicsDataSplit)):
        fout.write(AerodynamicsDataSplit[j] + '\n')

    fout.write('\n')

    for j in range(0, len(FuselageDataSplit)):
        fout.write(FuselageDataSplit[j] + '\n')

    fout.write('\n')

    for j in range(0, len(PropulsionDataSplit)):
        fout.write(PropulsionDataSplit[j] + '\n')

    fout.write('\n')

    for j in range(0, len(WeightDataSplit)):
        fout.write(WeightDataSplit[j] + '\n')


for i in range(1,nmax+1):
    #Wing_parametersFunction(Planform,Miscellaneous)
    #print (Planform.b)
    print(i)



        #     fout.write(str(j[0]) + "\n")
        # for j in MiscellaneousData:
        #     fout.write(str(j) + "\n")




    ClassII_Iteration.ClassIWeightEstimation(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)



    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)

    from Matching_Diagram import MatchingDiagram
    MatchingDiagram(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)
    #print(Miscellaneous.V_stall)
    #print(Planform.WingLoading)
    #print(Propulsion.Thrust_to_Weight)
    plt.show()

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)




    from Ailerons import AileronsFunction

    AileronsFunction(Planform, Miscellaneous, Propulsion, Aerodynamics, Fuselage, Weight)
    # print(Planform.y1ail)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)


    from HLD import LiftCoefficient
    LiftCoefficient(Planform, Miscellaneous, Propulsion, Aerodynamics, Fuselage, Weight)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)


    from SARoptimization import SAR

    SAR(Planform, Miscellaneous, Propulsion, Aerodynamics, Fuselage, Weight)
    # print(Planform.b)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)





    ClassII_Iteration.ClassIIWeightEstimation(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)


    ClassII_Iteration.CGPositions (Planform,Miscellaneous,Propulsion, Aerodynamics, Fuselage, Weight)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)

    
    print("Horizontal Tail Weight: ", Weight.HoriTailWeight)
    print("Vertical Tail Weight: ", Weight.VertTailWeight)
    print('Total tail weight: ',Weight.HoriTailWeight+Weight.VertTailWeight)
    from Tail_sizing_WP3 import horizontal_tail, vertical_tail

    horizontal_tail(Planform, Miscellaneous, Propulsion, Aerodynamics, Fuselage, Weight)
    vertical_tail(Planform, Miscellaneous, Propulsion, Aerodynamics, Fuselage, Weight)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)


    from Drag_calculator import Cf_Calculator

    Cf_Calculator(Planform, Miscellaneous, Propulsion, Aerodynamics, Fuselage, Weight)
    # print(Aerodynamics.Cf_tot_cr,Aerodynamics.Cf_tot_app,Aerodynamics.S_tot)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)


    from Class2Drag import Class2_Drag

    Class2_Drag(Planform, Miscellaneous, Propulsion, Aerodynamics, Fuselage, Weight)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)


    # print(Aerodynamics.CD0_Cruise)
    # print(Aerodynamics.S_W, Aerodynamics.S_HT, Aerodynamics.S_VT)
    # print(Aerodynamics.CD0_Landing_DOWN)
    # print(Aerodynamics.CD0_Landing_UP)
    # print(Aerodynamics.CD0_Takeoff_DOWN)
    # print(Aerodynamics.CD0_Takeoff_UP)
    # print(Aerodynamics.CD0_Clean_UP)
    # print(Aerodynamics.CD0_Cruise)



    from undercarriage import Undercarriage
    Undercarriage(Planform,Miscellaneous,Propulsion,Aerodynamics,Fuselage,Weight)

    Planform.updatePlanformDependencies(Weight)
    Propulsion.updatePropulsionDependencies(Miscellaneous,Weight)
    Miscellaneous.updateMiscellaneousDependencies(Planform, Aerodynamics, Weight)

    plt.close()

    #g = open("iteration" + str(i - 1) + ".dat", "w")  # Open file for writing

    PlanformData = vars(Planform)
    PlanformDataString = str(PlanformData)
    PlanformDataSplit = PlanformDataString.replace(':', ',').replace("'", '').replace('{', '').replace('}', '').split(',')

    MiscellaneousData = vars(Miscellaneous)
    MiscellaneousDataString = str(MiscellaneousData)
    MiscellaneousDataSplit = MiscellaneousDataString.replace(':', ',').replace("'", '').replace('{', '').replace('}','').split(',')

    AerodynamicsData = vars(Aerodynamics)
    AerodynamicsDataString = str(AerodynamicsData)
    AerodynamicsDataSplit = AerodynamicsDataString.replace(':', ',').replace("'", '').replace('{', '').replace('}','').split(',')

    FuselageData = vars(Fuselage)
    FuselageDataString = str(FuselageData)
    FuselageDataSplit = FuselageDataString.replace(':', ',').replace("'", '').replace('{', '').replace('}', '').split(',')

    WeightData = vars(Weight)
    WeightDataString = str(WeightData)
    WeightDataSplit = WeightDataString.replace(':', ',').replace("'", '').replace('{', '').replace('}', '').split(',')

    PropulsionData = vars(Propulsion)
    PropulsionDataString = str(PropulsionData)
    PropulsionDataSplit = PropulsionDataString.replace(':', ',').replace("'", '').replace('{', '').replace('}','').split(',')

    for j in range(0, len(PlanformDataSplit)):
        if (j % 2 != 0):
            sheet1.write(row, i+1, '{:g}'.format(float(form.format(float(PlanformDataSplit[j])))))
            row += 1
    for j in range(0, len(MiscellaneousDataSplit)):
        if (j % 2 != 0):
            sheet1.write(row, i+1, '{:g}'.format(float(form.format(float(MiscellaneousDataSplit[j])))))
            row += 1
    for j in range(0, len(AerodynamicsDataSplit)):
        if (j % 2 != 0):
            sheet1.write(row, i+1, '{:g}'.format(float(form.format(float(AerodynamicsDataSplit[j])))))
            row += 1
    for j in range(0, len(FuselageDataSplit)):
        if (j % 2 != 0):
            sheet1.write(row, i+1, '{:g}'.format(float(form.format(float(FuselageDataSplit[j])))))
            row += 1
    for j in range(0, len(WeightDataSplit)):
        if (j % 2 != 0):
            sheet1.write(row, i+1, '{:g}'.format(float(form.format(float(WeightDataSplit[j])))))
            row += 1
    for j in range(0, len(PropulsionDataSplit)):
        if (j % 2 != 0):
            sheet1.write(row, i+1, '{:g}'.format(float(form.format(float(PropulsionDataSplit[j])))))
            row += 1
    row = 1


    with open("iteration" + str(i) + ".dat", "w") as fout:
        # fout.write(str(PlanformData))
        for j in range(0, len(PlanformDataSplit)):
            fout.write(PlanformDataSplit[j] + '\n')

        fout.write('\n')

        for j in range(0, len(MiscellaneousDataSplit)):
            fout.write(MiscellaneousDataSplit[j] + '\n')

        fout.write('\n')

        for j in range(0, len(AerodynamicsDataSplit)):
            fout.write(AerodynamicsDataSplit[j] + '\n')

        fout.write('\n')

        for j in range(0, len(FuselageDataSplit)):
            fout.write(FuselageDataSplit[j] + '\n')

        fout.write('\n')

        for j in range(0, len(PropulsionDataSplit)):
            fout.write(PropulsionDataSplit[j] + '\n')

        fout.write('\n')

        for j in range(0, len(WeightDataSplit)):
            fout.write(WeightDataSplit[j] + '\n')

        #fout.write(str(Miscellaneous.WingloadEndCr))


book.save("Iterations.xls")
