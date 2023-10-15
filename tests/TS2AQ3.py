from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *


Name = "Q3"
L = 6
Beam1 = SimplySupportedBeam(Name, L)
load1 = DistributedLoad(0,3,0,4)
load2 = DistributedLoad(3,6,4,4)
support = Support(0,3)

Beam1.add_load(load1)
Beam1.add_load(load2)
Beam1.add_supports(support)

Beam1.plot_sfd_and_bmd()