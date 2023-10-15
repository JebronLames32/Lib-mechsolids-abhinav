from Lib_mechsolids_abhinav.math_functions import *
import numpy as np
from matplotlib import rcParams
import matplotlib.pyplot as plt


class Beam():

    def __init__(self, id, L):
        self.length = L
        self.name = id
        self.load = [] # list of loads
        

    def add_load(self, load):
        self.load.append(load)

    def add_supports(self, supports):
        self.supports = supports

    def remove_load(self, load):
        self.load.remove(load)

    # def remove_supports(self, supports):
    #     self.supports.remove(supports)

    
    def generate_sf_at_point(self, x):
        """
        generate_sf_at_point is a function that takes in a value of x and returns the value of sfd at that point. 
        It does this by iterating through the list of loads and adding the load at that point to the sfd.

        While traversing from left to right, the function checks if the point is within the range of a load. If it is, it adds the load to the sfd.
        --> If it is a point load, it adds the load to the sfd.
        --> If it is a distributed load, it adds the area under the curve to the sfd.
        --> If it is a support, it adds the reaction at that point to the sfd.

        Parameters:
        self (SimplySupportedBeam): The SimplySupportedBeam object.
        x (float): The value of x at which the sfd is to be calculated.

        Returns:
        sfd (float): The value of shear force at the point x.
        """
        sfd = 0
        for load in self.load :
            if(isinstance(load, PointLoad)):
                if(x>=load.dist):
                    sfd -= load.load
                
            elif(isinstance(load, DistributedLoad)):
                if(x >= load.start and x<=load.end):
                    sfd -= load.Area_under_load(x)
                elif(x > load.end):
                    sfd -= load.Area_under_load()

            elif(isinstance(load,EquationLoad)):
                val = x - load.start
                area = load.Integral_of_eqn(load.equation)
                if(x >= load.start and x<=load.end):
                    # print("area",area.subs(Symbol('x'), val))
                    sfd -= area.subs(Symbol('x'), val)
                elif(x > load.end):
                    sfd -= area.subs(Symbol('x'), load.end-load.start)

        if(isinstance(self, SimplySupportedBeam)):
            support = self.supports
            if(isinstance(support, Support)):
                if(x >= support.position1):
                    sfd += support.reaction1
                if(x >= support.position2):
                    sfd += support.reaction2

        elif(isinstance(self, CantileverBeam)):
            sfd += self.wall_force
        
        # print(sfd)
        return sfd
        

    def generate_sf_at_all_points(self):
        """
        generate_sf_at_all_points is a function that generates a list of values of sfd at continuous points on the beam.
        We use the generate_sf_at_point function to generate the sfd at each point.
        We break the beam into 2001 points and generate the shear force at each point.

        Parameters:
        self (SimplySupportedBeam): The SimplySupportedBeam object.

        Returns:
        x (list): A list of 2001 values of x.
        V (list): A list of 2001 values of shear force for each value of x.
        """
        # sfd = []
        N = 2001
        x = np.linspace(0,self.length,N)

        if(isinstance(self, SimplySupportedBeam)):
            # need to run the function for the support reactions as we need it already calculated in the next function.
            self.supports.Reaction_at_support(self.load)

        elif(isinstance(self, CantileverBeam)):
            self.wall_force = Reaction_at_point(0,self.load)

        sf_at_points = np.vectorize(self.generate_sf_at_point)
        V = sf_at_points(x)
        return x, V

    def generate_bm_at_point(self, x):
        """
        generate_bm_at_point is a function that takes in a value of x and returns the value of bmd at that point. 
        It does this by iterating through the list of loads and adding the load at that point to the BM.

        While traversing from left to right, the function checks if the point is within the range of a load. If it is, it adds the moment of the load to the BM.
        --> If it is a point load, it adds the load to the BM.
        --> If it is a distributed load, it adds the area under the curve to the BM.
        --> If it is a support, it adds the reaction at that point to the BM.

        Parameters:
        self (SimplySupportedBeam): The SimplySupportedBeam object.
        x (float): The value of x at which the bmd is to be calculated.

        Returns:
        bmd (float): The value of bending moment at the point x.
        """
        bmd = 0
        for load in self.load :
            if(isinstance(load, PointLoad)):
                if(x>=load.dist):
                    bmd -= load.load * (x - load.dist)
                
            elif(isinstance(load, DistributedLoad) or isinstance(load, EquationLoad)):
                if(x >= load.start and x<=load.end):
                    Equiv_point_load_mag, Equiv_point_load_dist = load.Equivalent_point_load(x)
                    bmd -= Equiv_point_load_mag * (x - Equiv_point_load_dist)
                elif(x > load.end):
                    Equiv_point_load_mag, Equiv_point_load_dist = load.Equivalent_point_load()
                    bmd -= Equiv_point_load_mag * (x - Equiv_point_load_dist)

            # alterrnative method
            # elif(isinstance(load,EquationLoad)):
            #     val = x - load.start
            #     V = load.Integral_of_eqn(load.equation, load.start, x)
            #     M = V.Integral_of_eqn(V)
            #     if(x >= load.start and x<=load.end):
            #         bmd -= M.subs(x, val)
            #     elif(x > load.end):
            #         bmd -= M.subs(x, load.end-load.start)

        if(isinstance(self, SimplySupportedBeam)):
            support = self.supports
            if(isinstance(support, Support)):
                if(x >= support.position1):
                    bmd += support.reaction1 * (x - support.position1)
                if(x >= support.position2):
                    bmd += support.reaction2 * (x - support.position2)

        elif(isinstance(self, CantileverBeam)):
            bmd += self.wall_force * x
            bmd += self.wall_moment
        
        return bmd

    def generate_bm_at_all_points(self):
        """
        generate_bm_at_all_points is a function that generates a list of values of bmd at continuous points on the beam.
        We use the generate_bm_at_point function to generate the bmd at each point.
        We break the beam into 1001 points and generate the bending moment at each point.

        Parameters:
        self (SimplySupportedBeam): The SimplySupportedBeam object.

        Returns:
        x (list): A list of 1001 values of x.
        M (list): A list of 1001 values of bending moment for each value of x.
        """
        N = 1001
        x = np.linspace(0,self.length,N)

        if(isinstance(self, SimplySupportedBeam)):
            # need to run the function for the support reactions as we need it already calculated in the next function.
            self.supports.Reaction_at_support(self.load)

        elif(isinstance(self, CantileverBeam)):
            self.wall_force = Reaction_at_point(0,self.load)
            self.wall_moment = -1*Moment_at_point(0,self.load)

        bm_at_points = np.vectorize(self.generate_bm_at_point)
        M = bm_at_points(x)
        return x, M

    def get_important_points(self, x, V, shear = True):
        """
        get_important_points is a function that returns a list of important points on the beam.
        These points are the points at which the sfd is discontinuous or non-differentiable.
        It includes all points at which a load is applied, the start and end of a distributed load, and the position of the supports.

        Parameters:
        self (SimplySupportedBeam): The SimplySupportedBeam object.
        x (list): A list of 1001 values of x.
        V (list): A list of 1001 values of shear force for each value of x.

        Returns:
        important_points_x (list): A list of important points on the beam.
        important_points_y (list): A list of the values of shear force at the important points.
        """
        important_points_x = []
        for load in self.load:
            if(isinstance(load, PointLoad)):
                important_points_x.append(load.dist)
            elif(isinstance(load, DistributedLoad)):
                important_points_x.append(load.start)
                important_points_x.append(load.end)
            elif(isinstance(load, EquationLoad)):
                important_points_x.append(load.start)
                important_points_x.append(load.end)

        if(isinstance(self, SimplySupportedBeam)):
            important_points_x.append(self.supports.position1)
            if(self.supports.position2 != None):
                important_points_x.append(self.supports.position2)

        elif(isinstance(self, CantileverBeam)):
            important_points_x.append(0)
        #remove duplicates from the list
        important_points_x = list(dict.fromkeys(important_points_x))
        # print(important_points_x)
        
        ### Not necessary but do uncomment if you want to plot the discontinuous points and the ticks are already not showint it.
        ##find the discontinuous points so that we can make ticks for both points.
        ##np.diff returns the difference between the adjacent elements in the array.
        ## np.where returns the indices of the elements in the array that satisfy the condition.
        ## we are subtracting a small valut epsilon from the x value of the discontinuous point so that we can plot the ticks on both sides of the discontinuity.
        # pos = np.where(np.abs(np.diff(V)) >= 0.1)
        # for i in pos:
        #     x_discontinuous = x[i+1] - np.finfo(np.float32).eps
        #     important_points_x = np.append(important_points_x, x_discontinuous)
        
        important_points_x.sort()
        
        important_points_y = []
        if(shear):
            for x in important_points_x:
                important_points_y.append(self.generate_sf_at_point(x))
                # print(self.generate_sf_at_point(x))
        else:
            for x in important_points_x:
                important_points_y.append(self.generate_bm_at_point(x))
                # print(self.generate_bm_at_point(x))

        return important_points_x, important_points_y

    def plot_sfd(self):
        """
        plot_sfd is a function that plots the shear force diagram of the beam.

        Parameters:
        self (SimplySupportedBeam): The SimplySupportedBeam object.

        Returns:
        None
        """
        rcParams['font.size']=16
        rcParams['mathtext.fontset']='cm'

        x, V = self.generate_sf_at_all_points()
        V = np.array(V, dtype=float)
        print("done till here")
        # print(V)

        #fig, axes = plt.subplots(1,2,tight_layout=True)

        fig = plt.figure()
        ax1 = fig.add_axes([0.1,0.1,0.8,0.8])

        #plt.subplot(1,2,1)
        ax1.plot(x,V,'blue')
        ax1.set_xlabel(r'$x\;\; [{\rm m}]$',fontsize=20)
        ax1.set_ylabel(r'$V\;\; [{\rm N}]$',fontsize=20)
        ax1.axhline(y=0,color='k')
        ax1.axvline(x=0,color='k')
        ax1.fill_between(x,V,color='blue',alpha=0.2)

        #make a list of important points
        important_points_x, important_points_y = self.get_important_points(x, V)
        # print(V[-2])
        important_points_y.append(V[-2])
        important_points_y = np.array(important_points_y, dtype=float)
        
        ax1.set_yticks(important_points_y, minor=False)
        ax1.set_xticks(important_points_x, minor=False)
        
        
        ax1.grid(True)
        plt.show()

        # ax2.plot(x,M)
        # ax2.set_xlabel(r'$x\;\; [{\rm m}]$',fontsize=20)
        # ax2.set_ylabel(r'$M\;\; [{\rm N}\cdot {\rm m}]$',fontsize=20)
        # ax2.axhline(y=0,color='k')
        # ax2.axvline(x=0,color='k')
        # ax2.fill_between(x,M,color='blue',alpha=0.2)
        # ax2.set_yticks([0,-18], minor=False)
        # ax2.set_xticks([3,6], minor=False)
        # ax2.grid(True)

    def plot_bmd(self):
        """
        plot_bmd is a function that plots the bending moment diagram of the beam.

        Parameters:
        self (SimplySupportedBeam): The SimplySupportedBeam object.

        Returns:
        None
        """
        rcParams['font.size']=16
        rcParams['mathtext.fontset']='cm'

        x, M = self.generate_bm_at_all_points()
        M = np.array(M, dtype=float)
        print(M[:5])

        fig = plt.figure()
        ax2 = fig.add_axes([0.1,0.1,0.8,0.8])
        ax2.plot(x,M)
        ax2.set_xlabel(r'$x\;\; [{\rm m}]$',fontsize=20)
        ax2.set_ylabel(r'$M\;\; [{\rm N}\cdot {\rm m}]$',fontsize=20)
        ax2.axhline(y=0,color='k')
        ax2.axvline(x=0,color='k')
        ax2.fill_between(x,M,color='blue',alpha=0.2)

        #make a list of important points
        # important_points_x, important_points_y = self.get_important_points(x, M)
        # print(V[-2])
        # important_points_y.append(M[-2])
        # important_points_y = np.array(important_points_y, dtype=float)
        
        # replace the nan values with 0
        M = np.nan_to_num(M)

        max = np.max(M)
        print(max)
        # min = np.min(M)
        maxindex = np.array(M).argmax()
        # minindex = np.array(M).argmin()

        important_points_x = [x[maxindex]]
        important_points_y = [max]
        important_points_x = np.array(important_points_x, dtype=float)
        important_points_y = np.array(important_points_y, dtype=float)
        
        ax2.set_yticks(important_points_y, minor=False)
        ax2.set_xticks(important_points_x, minor=False)

        # ax2.set_yticks([0,-18], minor=False)
        # ax2.set_xticks([3,6], minor=False)
        ax2.grid(True)
        plt.show()

    def plot_sfd_and_bmd(self):

        rcParams['font.size']=12
        rcParams['mathtext.fontset']='cm'

        x, V = self.generate_sf_at_all_points()
        V = np.array(V, dtype=float)

        fig = plt.figure()

        ax1 = fig.add_axes([0.1,0.55,0.4,0.4])
        ax2 = fig.add_axes([0.1,0.1,0.4,0.4])

        ax1.plot(x,V,'blue')
        ax1.set_xlabel(r'$x\;\; [{\rm m}]$',fontsize=20)
        ax1.set_ylabel(r'$V\;\; [{\rm N}]$',fontsize=20)
        ax1.axhline(y=0,color='k')
        ax1.axvline(x=0,color='k')
        ax1.fill_between(x,V,color='blue',alpha=0.2)

        #make a list of important points
        important_points_x, important_points_y = self.get_important_points(x, V)
        important_points_y.append(V[-2])
        important_points_y = np.array(important_points_y, dtype=float)
        
        ax1.set_yticks(important_points_y, minor=False)
        ax1.set_xticks(important_points_x, minor=False)
        ax1.grid(True)
        
        
        # bmd calculation from here
        x, M = self.generate_bm_at_all_points()
        M = np.array(M, dtype=float)

        ax2.plot(x,M)
        ax2.set_xlabel(r'$x\;\; [{\rm m}]$',fontsize=20)
        ax2.set_ylabel(r'$M\;\; [{\rm N}\cdot {\rm m}]$',fontsize=20)
        ax2.axhline(y=0,color='k')
        ax2.axvline(x=0,color='k')
        ax2.fill_between(x,M,color='blue',alpha=0.2)

        
        # replace the nan values with 0
        M = np.nan_to_num(M)

        max = np.max(M)
        print(max)
        # min = np.min(M)
        maxindex = np.array(M).argmax()
        # minindex = np.array(M).argmin()

        #make a list of important points
        important_points_x, important_points_y = self.get_important_points(x, M, False)

        
        important_points_y.append(M[-2])
        important_points_x = np.array(important_points_x, dtype=float)
        important_points_y = np.array(important_points_y, dtype=float)
        # remove nan values
        important_points_y = important_points_y[np.logical_not(np.isnan(important_points_y))]

        
        ax2.set_yticks(important_points_y, minor=False)
        ax2.set_xticks(important_points_x, minor=False)

        # ax2.set_yticks([0,-18], minor=False)
        # ax2.set_xticks([3,6], minor=False)
        ax2.grid(True)


        plt.show()


class SimplySupportedBeam(Beam):        

    def __init__(self, id, L):
        super().__init__(id, L)
        self.supports = 0 #A single definition should all supports.
    
    def add_supports(self, supports):
        self.supports = supports

    # test the functions
    # Beam1 = SimplySupportedBeam("Beam1", 6)
    # Beam1.add_load(DistributedLoad(0, 3, 0, 4))
    # Beam1.add_load(DistributedLoad(3, 6, 4, 4))
    # Beam1.add_supports(Support(0,3))

    # Beam1.plot_bmd()
    # Beam1.plot_sfd()

class CantileverBeam(Beam):

    def __init__(self, id, L):
        super().__init__(id, L)
        # assuming wall is always at x coordinate 0
        self.wall_force = 0         
        self.wall_moment = 0