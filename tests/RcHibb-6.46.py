from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *

Name = "canti"
L = 1
Beam1 = CantileverBeam(Name, L)
# equation is w0*sin(pi*x/L) w0 is taken as unity and L is taken as 1 arbitrarily
# change it according to the question
equation = "sin(pi*x/1)"
load1 = EquationLoad(equation,0,L,0,0)

Beam1.add_load(load1)
Beam1.plot_sfd_and_bmd()