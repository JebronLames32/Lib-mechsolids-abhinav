from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *

Name = "canti"
L = 8
Beam1 = CantileverBeam(Name, L)

load1 = EquationLoad(x**2/8,0,8,0,8)

Beam1.add_load(load1)
Beam1.plot_sfd_and_bmd()