from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *

Name = "6.45"
L = 1
Beam1 = SimplySupportedBeam(Name, L)
# equation is w0*x**2/L**2 w0 is taken as unity and L is taken as 1 arbitrarily
# change it according to the question
equation = "(x**2)/1"
load_list = [EquationLoad(equation,0,L,0,1)]
support = Support(0,1)


for load in load_list :
    Beam1.add_load(load)
    print(load.equation)
Beam1.add_supports(support)
# Beam1.generate_sf_at_all_points()
# print(Beam1.supports[0].reaction1)

Beam1.plot_sfd_and_bmd()


# take the description of the beam

# print("Enter the equation of the load intensity w(x) in terms of x")
# equation = input(("w(x) = "))
# print("Equation of the load intensity w(x) is: ", equation)