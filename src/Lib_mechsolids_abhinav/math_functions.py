from sympy import *

x=symbols('x')

# Distance is always spexified from the left side of the beam

class PointLoad:
    def __init__(self, load, distance):
        self.load = load
        self.dist = distance

        

##Considering only linearly distributed load
class DistributedLoad:
    #can enter either slope of the load or the start and end loads
    def __init__(self, start, end, startLoad=None, endLoad=None, slope=None):

        self.startLoad = startLoad

        self.endLoad = endLoad
        
        self.start = start

        self.end = end

        if slope is None:
            self.slope = (endLoad - startLoad) / (end - start)
        else:
            self.slope = slope

    #Calculate the load at point x
    def Value_of_load(self, x):
        return self.slope * (x - self.start) + self.startLoad

    #Calculate the area under the distributed load up until point x
    def Area_under_load(self, x=None):
        #If x is not specified, calculate the area under the entire distributed load
        if x is None:
            x = self.end
        #Area under the trapezoid or triangle
        return (self.startLoad + self.Value_of_load(x)) * (x - self.start) / 2

    #Calculate the equivalent point load of the distributed load up until point x
    def Equivalent_point_load(self, x=None):
        #If x is not specified, calculate the equivalent point load of the entire distributed load
        if x is None:
            x = self.end
        magnitude = self.Area_under_load(x)

        #Calculate the distance from the start of the distributed load to the equivalent point load (center of mass)
        # if(self.startLoad == self.Value_of_load(x)):
        #     Xcom = (x - self.start) / 2
        # else:
        try:
            Xcom = (1/3 * self.startLoad + 2/3 * self.Value_of_load(x)) * (x-self.start) / (self.Value_of_load(x) + self.startLoad)
        except ZeroDivisionError:
            Xcom = 0

        distance = self.start + Xcom

        #return PointLoad(magnitude, distance)
        return magnitude, distance


#Assuming that the loads act downwards (sign convention positive downwards)
def Moment_at_point(x, load_list):
    moment = 0
    for load in load_list:
        if isinstance(load, PointLoad):
            moment += load.load * (load.dist - x)
        elif isinstance(load, DistributedLoad) or isinstance(load, EquationLoad):
            moment += load.Equivalent_point_load()[0] * (load.Equivalent_point_load()[1] - x)
        else:
            raise TypeError("Load must be either a point load or a distributed load")
    return moment

def Reaction_at_point(x, load_list):
    force = 0
    for load in load_list:
        if isinstance(load, PointLoad):
            force += load.load
        elif isinstance(load, DistributedLoad) or isinstance(load, EquationLoad):
            force += load.Equivalent_point_load()[0]
        else:
            raise TypeError("Load must be either a point load or a distributed load")
    return force


class EquationLoad:

    def __init__(self, equation, start, end, startLoad=0, endLoad=None):
        self.equation = self.string_to_equation(equation)
        if(type(start) == str):
            start = symbols(start)
        if(type(end) == str):
            end = symbols(end)
        self.start = start
        self.end = end
        self.startLoad = startLoad
        self.endLoad = endLoad
        
        # if w0 and k are to be calculated
        w0 = Symbol('w0') # assumed to be the start load in the equationof form w0 + k*f(x)
        k = Symbol('k') # assumed to be the coeffecient to be calculated in the equation of form w0 + k*f(x)
        L = Symbol('L') # assumed to be the length of the beam

        if(w0 in self.equation.free_symbols):
            self.equation=self.equation.subs(w0,startLoad)
        if(k in self.equation.free_symbols):
            # Fx = (self.equation - startLoad)/k
            # valOfK = (self.endLoad-self.startLoad)/Fx.subs(x,end)
            # self.equation=self.equation.subs(k,valOfK)
            eqn = self.equation - endLoad
            # solve for k by substuting x=end
            valOfK = solve(eqn.subs(x,end),k)
            self.equation=self.equation.subs(k,valOfK[0])
        if(L in self.equation.free_symbols):
            self.equation=self.equation.subs(L,end-start)   
            
    # Integration of a equation given the limits and the variable with respect to which the integration is to be done
    def Integral_of_eqn(self, eqn, start=0, end=x, withrespectto=Symbol('x')):
        # # Testing the integral function
        # w0=Symbol('w0')
        # L=Symbol('L')
        # equation = w0*(x**2)/(L**2)
        # print(Integral_of_eqn(equation,0,L))
        # # output recieved is w0*L/3
        answer = integrate(eqn, (withrespectto, start, end))
        
        return answer

    # conversion of string to math equation
    def string_to_equation(self, string):
        # Testing the string to equation function
        # string = 'w0*x**2/L**2'
        # eqn = sympify(string)
        # print(eqn)
        equation = sympify(string)
        return equation
    

    def Equivalent_point_load(self, x=None):
        #If x is not specified, calculate the equivalent point load of the entire distributed load
        if x is None:
            x = self.end

        # the magnitude of the equivalent point load is the integral of the w(x) function
        magnitude = self.Integral_of_eqn(self.equation, self.start, x)
        # the distance of the equivalent point load is the integral of the x*w(x) function divided by the magnitude
        Xcom = self.Integral_of_eqn(self.equation * Symbol('x'), self.start, x) / magnitude
        distance = self.start + Xcom

        return magnitude, distance
    
    

##Calculate the load at the supports
#Assuming the support reaction to be upwards (sign convention positive upwards)
class Support:
    #position1 is the position of the support, position2 is the position of the second support if the beam is simply supported
    ##If the beam is simply supported, position1 is the left support and position2 is the right support
    #need to talk to sir about having multiple supports
    def __init__(self, position1,position2=None):   
        self.position1 = position1
        self.reaction1 = 0
        if(position2 is not None):
            self.position2 = position2
            self.reaction2 = 0


    def Reaction_at_support(self, load_list):
        for load in load_list:
            if not isinstance(load, PointLoad) and not isinstance(load, DistributedLoad) and not isinstance(load, EquationLoad):
                raise TypeError("Load must be either a point load or a distributed load or an equation load")

        #Case of simply supported beam
        if(self.position2 is not None):
            self.reaction1 = Moment_at_point(self.position2, load_list) / (self.position1 - self.position2)
            self.reaction2 = Moment_at_point(self.position1, load_list) / (self.position2 - self.position1)
            print("reactions:",self.reaction1, self.reaction2)
            # self.reaction1 = abs(self.reaction1)
            # self.reaction2 = abs(self.reaction2)

        #Case of cantilever beam

        # return self.reaction1, self.reaction2



##testing the functions
# load_list = [DistributedLoad(0, 3, 0, 4), DistributedLoad(3, 6, 4, 4)]
# load_list = [PointLoad(3, 3), PointLoad(6, 6)]
# support = Support(0,3)
# (support.Reaction_at_support(load_list))
# print(support.reaction1, support.reaction2)

# negative support reaction is possible only for pinned support and not for roller support. 
# Hence, it might be better to use absolute value of the support reaction.

# string = 'w0*x**2/L**2'
# eqn = sympify(string)
# print(eqn)
# L = Symbol('L')
# y = Symbol('y')
# if L in eqn.free_symbols:
#     print("yes")
# if y in eqn.free_symbols:
#     print("yes")

# print(Integral_of_eqn(eqn, 0, L, x))
    