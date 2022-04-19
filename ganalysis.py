"""
Fernando Jose Lavarreda Urizar
Gradient analysis for Unidemensional Transiet Heat Conduction
Spheres, Walls and Cylinders
"""

from typing import List
from zeros import bessel
from math import cos, sin, exp


def biot(conv:float, length:float, cond:float)->float
    """Determine the biot value of a system, parameter useful to determine if it is concentrated or no
       conv: convection constant of the system
       length: half the length of a wall or the entire value of the radius for a cylinder or sphere
       cond: thermal conductivity constant for the system
    """
    return conv/cond*length


def tau(alfa:float, time_:float, length:float)->float:
    """Determine Fourier Constant (Adimensional Time)
       alfa: thermal diffusivity of the object
       time_: time of the system
       length: half the total length of the wall, or the entire value of the radius for a cylinder or sphere
    """
    return alfa*time_/length**2
    


def gradient_p(lambdas=List[float], position:float, length:float, tau:float)->float:
    """Function to obtain temperature gradient for a wall
       lambdas: list of lambdas for the system
       position: distance relative to the center of the wall
       length: half the total length of wall
       tau: adimensional time
    """
    accummulated_gradientes = []
    for i in lambdas:
        accummulated_gradientes.append((4*sin(i))/(2*i+sin(2*i))*exp(-i**2*tau)*cos(i*position/length))
    return sum(accummulated_gradientes)




def gradient_e(lambdas=List[float], position:float, radius:float, tau:float)->float:
    """Function to obtain temperature gradient for a sphere
       lambdas: list of lambdas for the system
       position: distance relative to the center of the sphere
       radius: radius of the sphere
       tau: adimensional time
    """
    accummulated_gradientes = []
    for i in lambdas:
        accummulated_gradientes.append(4*(sin(i)-i*cos(i))/(2*i-sin(2*i))*exp(-i**2*tau)*sin(i*position/radius)/(i*position/radius))
    return sum(accummulated_gradientes)



def gradient_c(lambdas=List[float], position:float, radius:float, tau:float)->float:
    """Function to obtain temperature gradient for a cylinder
       lambdas: list of lambdas for the system
       position: distance relative to the center of the cylinder
       radius: radius of the cylinder
       tau: adimensional time
    """
    accummulated_gradientes = []
    for i in lambdas:
        accummulated_gradientes.append(2/i*bessel(i, 1)/(bessel(i, 0)**2+bessel(i, 1)**2)*exp(-i**2*tau)*bessel(i*position/radius, 0))
    return sum(accummulated_gradientes)




if __name__ == "__main__":
	pass








