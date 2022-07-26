"""
Fernando Jose Lavarreda Urizar
Funtions to find lambdas for Transient Heat Conduction
Functions for spheres, cylinders and walls

Example of call to the program:
    -e 10 2: this means sphere biot = 10 and 2 find two zeros
    -11: This shows Bessel functions from [0, 10], a higher value will be truncated to 11.
    
Codes:
    e = sphere, max biot 100_000.
    p = wall, max biot 100_000.
    c = cylinder, max biot 100. Max zeros 7 else truncated
"""

import sys
from functools import partial
from typing import List, Callable
from math import sin, cos, tan, factorial, pi


# Program limitations
MAX_BIOTE = 100_000
MAX_BIOTP = 100_000
MAX_BIOTC = 100
MAX_LAMBDASC = 7

def pared(lamb:float, biot:float)->float:
    """Function that defines the relationship between the biot and lambda for a wall"""
    return lamb*tan(lamb)-biot


def dpared(lamb:float)->float:
    """Derivative of pared function"""
    return tan(lamb)+lamb*1/(cos(lamb)**2)


def cilindro(lamb:float, biot:float)->float:
    """Function that defines the relationship between biot and lamda for a cylinders"""
    return lamb*(bessel(lamb, 1)/bessel(lamb, 0))-biot


def dcilindro(lamb:float)->float:
    """Derivative of cilindro function"""
    return (bessel(lamb, 1)/bessel(lamb, 0))+lamb*derivar(lamb, lambda x: (bessel(x, 1)/bessel(x, 0)))


def esfera(lamb:float, biot:float)->float:
    """Function that defines the relationship between biot anda lamda for a sphere"""
    return 1-lamb/tan(lamb)-biot


def desfera(lamb)->float:
    """Derivative of esfera function"""
    return -1/tan(lamb)+lamb/(sin(lamb)**2)


def newtons(fn:Callable[[float], float], dx:Callable[[float], float], xo:float, tolerancia:float=0.000001, maxiter:int=10000)->List[float]:
    """Definition of Newton's Method
    fn: Function that requires that takes as an argument a float value to evaluate
    dx: Function is the derivative from fn that requires that takes as an argument a float value to evaluate
    xo: Value where to start evaluation to find a zero
    tolerancia: acceptable error for the zero found, defined as distance of function(zero) to 0
    maxiter: maximum value of iterations before exiting function if zero has not been found Default value set to 10000 iterations, raises StopIteration
    returns a tuple with the zero and number of iterations
    """
    i = 0
    while abs(fn(xo))>tolerancia:
        xo -= fn(xo)/dx(xo)
        i+=1
        if i>=maxiter:
            raise StopIteration("Maximum number of iterations reached and no zero was found")
    return xo, i



def multiple_newtons(fn:Callable[[float], float], dx:Callable[[float], float], xo:float, number:int, step:float, tolerancia:float=0.000001, maxiter:int=10000)->List[float]:
    """Function to obtain multiple zeros from a function
       for fn, dx, xo, tolerancia check newtons documentation
       number: number of zeros to be found on the function
       step: distance from last zero to check for the next zero
       returns list with the zeros found on the function
       raises StopIteration if max iteration for a zero was reached
    """
    found = []
    for i in range(number):
        if found:
            zero, iteration = newtons(fn, dx, found[-1]+step, tolerancia=tolerancia, maxiter=maxiter)
        else:
            zero, iteration = newtons(fn, dx, xo, tolerancia=tolerancia, maxiter=maxiter)
        found.append(zero)
    return found



def bessel(x:float, degree:int, terms:int=120)->float:
    """Definition of Bessel function
       x: point of evaluation for bessel function. For 120 terms 35 is max value to evaluate with semi accurate results
       degree: degree of bessel function to evaluate. Value shouldn't be more than 10/11 for a regular computer
       terms: number of terms to use in bessel function calculation. Big terms value may cause OverflowError
    """
    if x>35:
        return sum([(x/2)**(i)*((-1)**i)/factorial(i)*(x/2)**(degree)/factorial(i+degree)*(x/2)**(i) for i in range(terms+48)])
    else:
        return sum([((-1)**i)/factorial(i)/factorial(i+degree)*(x/2)**(2*i+degree) for i in range(terms)])



def derivar(x:float, func:Callable[[float], float], diferencial:float=1e-8)->float:
    """Derivation of a function be numeric methods
       x: point to derivate the function
       func: function to derivate, takes a float argument
       diferencial: half the distance between points of evaluation to obtain derivative. This is the delta
    """
    return (func(x+diferencial)-func(x-diferencial))/(2*diferencial)



def c_lambdas(biot:float, zeros:int, step:float=pi)->List[float]:
    """Determine the lambdas for a cylinder
    The function is limited to a biot of 100 and to a max of 7 zeros
    biot: biot of the system
    zeros: number of zeros desired
    step: distance to check for the next lambda
    """
    if biot>MAX_BIOTC:
        raise ValueError("Biot should be smaller than 100")
    if zeros>MAX_LAMBDASC:
        raise ValueError("No more than 7 zeros can be computed for cylinder")
    return multiple_newtons(partial(cilindro, biot=biot), dcilindro, 2.4, zeros, step)
    


def e_lambdas(biot:float, zeros:int, step:float=pi)->List[float]:
    """Determine the lambdas for a sphere
    The function is limited to a biot of 1e5
    biot: biot of the system
    zeros: number of zeros desired
    step: distance to check for the next lambda
    """
    if biot>MAX_BIOTE:
        raise ValueError("Biot should be smaller than 1e5")
    return multiple_newtons(partial(esfera, biot=biot), desfera, pi-1e-8, zeros, step)



def p_lambdas(biot:float, zeros:int, step:float=pi)->List[float]:
    """Determine the lambdas for a wall
    The function is limited to a biot of 1e5
    biot: biot of the system
    zeros: number of zeros desired
    step: distance to check for the next lambda
    """
    if biot>MAX_BIOTP:
        raise ValueError("Biot should be smaller than 1e5")
    return multiple_newtons(partial(pared, biot=biot), dpared, pi/2-1e-8, zeros, step)
    



if __name__ == "__main__":
    args = sys.argv[1:]
    options = ("p", "c", "e")
    if len(args) >= 2:
        try:
            biot = float(args[1])
            zeros = 5
            if len(args) >= 3:
                zeros = int(args[2])
        except ValueError:
            print("invalid arguments")
        else:
            if args[0] == "p":
                if biot<=100_000:
                    zs = p_lambdas(biot=biot, zeros=zeros)
                else:
                    print("No computable")
                    sys.exit()
                print(zs)
            elif args[0] == "c":
                if biot <= 100:
                    zs = c_lambdas(biot=biot, zeros=zeros)
                else:
                    print("No computable")
                    sys.exit()
                print(zs)
            elif args[0] == "e":
                if biot<=100_000:
                    zs = e_lambdas(biot=biot, zeros=zeros)
                else:
                    print("No computable")
                    sys.exit()
                print(zs)
            else:
                print("nonexistent geometry")
    else:
        #No more than Bessel 10 so 11 is max value for bessel computing
        import matplotlib.pyplot as plt
        xs = [i/1000*35 for i in range(1000)]
        curvas = 2
        try:
            if args:
                curvas = int(args[0])
                if curvas>11:
                    curvas = 11
                    print("No more than J10 can be accurately computed")
        except ValueError:
            curvas = 2
        
        for i in range(curvas):
            ys = [bessel(x, i) for x in xs]
            plt.plot(xs, ys, label=f"J{i}")
        plt.title("Curvas de Bessel")
        plt.ylabel("y")
        plt.xlabel("x")
        plt.grid()
        plt.legend()
        plt.show()
        
        

