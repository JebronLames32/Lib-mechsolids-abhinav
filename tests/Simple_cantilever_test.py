# problem description:

# A cantilever 6m long carries load of 30, 70, 40 and 60 kN at a distance of
# 0,0.6, 1.5 and 2m respectively from the free end. Draw the SF and BM diagram for the
# cantilever.


from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *

Name = "canti"
L = 6
Beam1 = CantileverBeam(Name, L)
load1 = PointLoad(30, 6)
load2 = PointLoad(70, 5.4)
load3 = PointLoad(40, 4.5)
load4 = PointLoad(60, 3.6)

Beam1.add_load(load1)
Beam1.add_load(load2)
Beam1.add_load(load3)
Beam1.add_load(load4)
Beam1.plot_sfd_and_bmd()