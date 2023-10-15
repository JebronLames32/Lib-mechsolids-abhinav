# problem description:
# A cantilever of length 2m carries a UDL of 3 kN/m. Draw the SF and BM diagram.

from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *

Name = "canti"
L = 2
Beam1 = CantileverBeam(Name, L)
load1 = DistributedLoad(0, 2, 3, 3)

Beam1.add_load(load1)
Beam1.plot_sfd_and_bmd()