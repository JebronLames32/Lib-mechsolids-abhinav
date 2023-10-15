from Lib_mechsolids_abhinav.Beam import *
from Lib_mechsolids_abhinav.math_functions import *

#creating a UI for the user to input the data
def createUI():
    print("Enter the name of the beam")
    name = input()
    print("Enter the length of the beam")
    L = float(input())
    print("Enter the number of loads")
    n = int(input())
    load_list = []
    for i in range(n):
        print("LOAD", i+1, ":")
        print("Enter the type of load (1 for point load, 2 for distributed load)")
        load_type = int(input())
        if(load_type == 1):
            print("Enter the magnitude of the point load")
            magnitude = float(input())
            print("Enter the distance from the left end of the beam")
            distance = float(input())
            load_list.append(PointLoad(magnitude, distance))
        elif(load_type == 2):
            print("Enter the start of the distributed load")
            start = float(input())
            print("Enter the end of the distributed load")
            end = float(input())
            print("Enter the magnitude of the load at the start")
            startLoad = float(input())
            print("Enter the magnitude of the load at the end")
            endLoad = float(input())
            load_list.append(DistributedLoad(start, end, startLoad, endLoad))
    print("Enter the position of the first support")
    position1 = float(input())
    print("Enter the position of the second support")
    position2 = float(input())
    support=Support(position1, position2)
    return name, L, load_list, support

# using the function createUI to create a UI for the user to input the data
name, L, load_list, support = createUI()
Beam1 = SimplySupportedBeam(name, L)
for load in load_list :
    Beam1.add_load(load)
Beam1.add_supports(support)
Beam1.plot_sfd()
Beam1.plot_bmd()
