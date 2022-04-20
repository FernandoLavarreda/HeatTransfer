"""
Fernando Jose Lavarreda Urizar
Gradient analysis for Unidemensional Transiet Heat Conduction
Spheres, Walls and Cylinders
"""

from typing import List
from zeros import bessel
from math import cos, sin, exp, pi


def biot(conv:float, length:float, cond:float)->float:
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
    


def gradient_p(lambdas:List[float], position:float, length:float, tau:float)->float:
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




def gradient_e(lambdas:List[float], position:float, radius:float, tau:float)->float:
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



def gradient_c(lambdas:List[float], position:float, radius:float, tau:float)->float:
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


def q_p(temp_profile:List[float], ts:float, length:float, area:float, d:float, cp:float)->float:
    """Analysis of heat transference for a wall  at a given moment in time
       temp_profile: temperature profile for the wall, from center to the exterior of the wall. More inputs lead to more accurate results
       the first value is taken as the center of the wall, therefore few values lead to errors in the results
       ts: starting temperature of the wall
       length: entire length of the wall
       area: area of cross section for the wall
       d: density of the wall
       cp: specific heat of the wall
    """
    analysis_l = length/2 #Since the profile is symmetrical and we are just analysing half 
    dx = analysis_l/len(temp_profile)
    Q = 0 #Heat gain or loss
    for i in range(1, len(temp_profile)):
        medium_t = (temp_profile[i]+temp_profile[i-1])/2
        dm = d*area*dx #Mass defferential for the wall
        du = dm*cp*(medium_t-ts)
        Q+=du
    
    #Too compensate for a small amount of temperatures in the profile an extrapolation of data will be done
    if dx*(len(temp_profile)-1)<length:
        missing_length = length-dx*(len(temp_profile)-1)
        extra_polateT = (temp_profile[-1]-temp_profile[-2])/dx*(missing_length+dx)+temp_profile[-2]
        medium_t = (extra_polateT+temp_profile[-1])/2
        dm = missing_length*area*d
        missing_q = cp*(extra_polateT-ts)*dm
        Q+=missing_q
    return 2*Q #Since the values are for half of the wall


def q_c(temp_profile:List[float], ts:float, radius:float, length:float, d:float, cp:float)->float:
    """Analysis of heat transference for a cylinder  at a given moment in time
       temp_profile: temperature profile for the cylinder, from ro to the exterior. More inputs lead to more accurate results
       the first value is taken as the center of the cylinder, therefore few values lead to errors in the results
       ts: starting temperature of the cylinder
       length: length of the cylinder
       radius: radius of the cylinder
       d: density of the cylinder
       cp: specific heat of the cylinder
    """
    dx = radius/len(temp_profile)
    Q = 0
    for i in range(1, len(temp_profile)):
        medium_t = (temp_profile[i]+temp_profile[i-1])/2
        dv = pi*((dx*i)**2-(dx*(i-1))**2)*length
        dm = d*dv
        du = dm*cp*(medium_t-ts)
        Q+=du
    #Too compensate for a small amount of temperatures in the profile an extrapolation of data will be done
    if dx*(len(temp_profile)-1)<radius:
        missing_length = radius-dx*(len(temp_profile)-1)
        extra_polateT = (temp_profile[-1]-temp_profile[-2])/dx*(missing_length+dx)+temp_profile[-2]
        medium_t = (extra_polateT+temp_profile[-1])/2
        dv = pi*(radius**2-(dx*(len(temp_profile)-1))**2)*length
        dm = dv*d
        missing_q = cp*(extra_polateT-ts)*dm
        Q+=missing_q
    return Q
    
    
    


def q_e(temp_profile:List[float], ts:float, radius:float, d:float, cp:float)->float:
    """Analysis of heat transference for a sphere  at a given moment in time
       temp_profile: temperature profile for the sphere, from ro to the exterior. More inputs lead to more accurate results
       the first value is taken as the center of the sphere, therefore few values lead to errors in the results
       ts: starting temperature of the sphere
       radius: radius of the sphere
       d: density of the sphere
       cp: specific heat of the sphere
    """
    dx = radius/len(temp_profile)
    Q = 0
    for i in range(1, len(temp_profile)):
        medium_t = (temp_profile[i]+temp_profile[i-1])/2
        dv = 4/3*pi*((dx*i)**3-(dx*(i-1))**3)
        dm = d*dv #Mass differential for the shpere
        du = dm*cp*(medium_t-ts)
        Q+=du
    #Too compensate for a small amount of temperatures in the profile an extrapolation of data will be done
    if dx*(len(temp_profile)-1)<radius:
        missing_length = radius-dx*(len(temp_profile)-1)
        extra_polateT = (temp_profile[-1]-temp_profile[-2])/dx*(missing_length+dx)+temp_profile[-2]
        medium_t = (extra_polateT+temp_profile[-1])/2
        dv = 4/3*pi*(radius**3-(dx*(len(temp_profile)-1))**3)
        dm = dv*d
        missing_q = cp*(extra_polateT-ts)*dm
        Q+=missing_q
    return Q
    


if __name__ == "__main__":
    pass
    








