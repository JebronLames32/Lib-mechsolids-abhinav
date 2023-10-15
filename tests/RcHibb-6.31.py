from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *

Name = "canti"
L = 1
Beam1 = CantileverBeam(Name, L)

load1 = DistributedLoad(0,0.5,1,1)
load2 = DistributedLoad(0.5,1,1,0)

Beam1.add_load(load1)
Beam1.add_load(load2)

Beam1.plot_sfd_and_bmd()
