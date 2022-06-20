"""
Fernando Jose Lavarreda Urizar
Gradient analysis for Unidemensional Transiet Heat Conduction
Spheres, Walls and Cylinders
"""

from typing import List, Tuple
from math import cos, sin, exp, pi
from .zeros import bessel, c_lambdas, e_lambdas, p_lambdas 



def biot(conv:float, length:float, cond:float)->float:
    """Determine the biot value of a system, parameter useful to determine if it is concentrated or no
       conv: convection constant of the system
       length: half the length of a wall or the entire value of the radius for a cylinder or sphere
       alternatively the equivalent length could be used which is Volume/Area
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
    assert lambdas, "No lambdas provided"
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
    assert lambdas, "No lambdas provided"
    accummulated_gradientes = []
    for i in lambdas:
        if position == 0:
            accummulated_gradientes.append(4*(sin(i)-i*cos(i))/(2*i-sin(2*i))*exp(-i**2*tau)) # Avoid zero division limit
        else:
            accummulated_gradientes.append(4*(sin(i)-i*cos(i))/(2*i-sin(2*i))*exp(-i**2*tau)*sin(i*position/radius)/(i*position/radius))
    return sum(accummulated_gradientes)



def gradient_c(lambdas:List[float], position:float, radius:float, tau:float)->float:
    """Function to obtain temperature gradient for a cylinder
       lambdas: list of lambdas for the system
       position: distance relative to the center of the cylinder
       radius: radius of the cylinder
       tau: adimensional time
    """
    assert lambdas, "No lambdas provided"
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



def temperature_g(gradient, st, at)->float:
    """
    Obtain the temperature of a point based on a temperature gradient
    gradient: (tx-at)/(st-at)
    where:
        at: temperature of the surroundings
        st: starting temperature of the body
        tx: temperature in that particualr coordinate
    """
    return gradient*(st-at)+at



def temp_profile(*, typ_:str, st:float, at:float, length:float, time_:float, nlambdas:int=6, dx:float=None, cond:float=None,\
                    conv:float=None, alfa:float=None, biot_:float=None, lambdas_:List[float]=None, coord:List[float]=None, \
                    cp:float=None, density:float=None, performant_coeff:List[float]=[], detailed:bool=False)->List[float]:
    """
    Obtain temperature profile for a wall
    typ_: Type of object to be analyzed
    st: starting temperature of the object
    at: temperature of the surroundings
    length: half the length of entire wall or whole radius of cylinder or radius of sphere
    time_: specific moment in time
    nlambdas: number of lambdas that will be taken into consideration
    dx: size of differentials, the 0 and border of object will always be included
    cond: conductivity constant system
    conv: convection constant of the system
    alfa: thermal diffusivity
        if no alfa provided:
            cp: specific heat of the material
            density: density of the material
    biot_: Biot of the system
        if no biot_ provided:
            conv and cond must be provided
    lambdas_: list with lambdas for the system, computations are greatly reduced if added
    coord: list of distances where to compute temperatures, if not provided dx must be provided
    performant_coeff: precomputed coefficients for the gradients of each coordinate
    detailed: determine whether to return alfa, biot and lambdas, useful to cut time for future calculations
    """
    
    assert not alfa == None or (not cp == None and not density == None), "Not enough parameters to define diffusivity"
    assert not biot == None or (not conv == None and not cond == None), "Not enough parameters to define biot"
    assert not coord == None or not dx == None, "Cant't determine coordinates to compute temperatures"
    #Currently supported types of objects with formulas for gradient and lambda determination
    typ = {
            'e': (gradient_e, e_lambdas),
            'c': (gradient_c, c_lambdas),
            'p': (gradient_p, p_lambdas),
            
          }
    assert typ_ in typ, f"Not supported. Supported types: {' '.join(list(typ.keys()))}"
    
    if alfa == None:
        alfa = cond/(cp*density)
    if biot_ == None:
        biot_sys = biot(conv, length, cond)
    else:
        biot_sys = biot_
    tau_ = tau(alfa, time_, length)
    #Set positions where to determine temperatures
    if coord:
        coordinates = coord
    else:
        coordinates = [0]
        curr = 1
        value = curr*dx
        while value<length:
            coordinates.append(value)
            curr+=1
            value = curr*dx
        coordinates.append(length)
    temperatures = []
    #---------------------------------------------
    
    if lambdas_:
        lambdas = lambdas_
    else:
        lambdas = typ[typ_][1](biot_sys, nlambdas)
    
    counter = 0
    if performant_coeff:
        for coordinate in coordinates:
            gradient = gradient_performant(performant_coeff[counter], lambdas, tau_)
            temperatures.append(temperature_g(gradient, st, at))
            counter+=1
    else:
        for coordinate in coordinates:
            gradient = typ[typ_][0](lambdas, coordinate, length, tau_)
            temperatures.append(temperature_g(gradient, st, at))
    if detailed:
        return alfa, lambdas, biot_sys, coordinates, temperatures
    return coordinates, temperatures



def gradient_p_coeff(lambdas:List[float], position:float, length:float)->float:
    """
       Obtain coefficients for the temperature gradient of a wall at a specific coordinate
       lambdas: list of lambdas for the system
       position: distance relative to the center of the sphere
       length: half the length of the wall
    """
    accummulated_gradientes = []
    for i in lambdas:
        accummulated_gradientes.append((4*sin(i))/(2*i+sin(2*i))*cos(i*position/length))
    return accummulated_gradientes



def gradient_e_coeff(lambdas:List[float], position:float, radius:float)->float:
    """
       Obtain coefficients for the temperature gradient of a sphere at a specific coordinate
       lambdas: list of lambdas for the system
       position: distance relative to the center of the sphere
       radius: radius of the sphere
    """
    accummulated_gradientes = []
    for i in lambdas:
        if position == 0:
            accummulated_gradientes.append(4*(sin(i)-i*cos(i))/(2*i-sin(2*i))) # Avoid zero division limit
        else:
            accummulated_gradientes.append(4*(sin(i)-i*cos(i))/(2*i-sin(2*i))*sin(i*position/radius)/(i*position/radius))
    return accummulated_gradientes



def gradient_c_coeef(lambdas:List[float], position:float, radius:float)->float:
    """
       Obtain coefficients for the temperature gradient of a cylinder at a specific coordinate
       lambdas: list of lambdas for the system
       position: distance relative to the center of the sphere
       radius: radius of the sphere
    """
    accummulated_gradientes = []
    for i in lambdas:
        accummulated_gradientes.append(2/i*bessel(i, 1)/(bessel(i, 0)**2+bessel(i, 1)**2)*bessel(i*position/radius, 0))
    return accummulated_gradientes



def gradient_performant(coefficients:List[float], lambdas:List[float], tau:float):
    """
       Improve the performance of gradient of temperature with once computed values. Particularly useful for cylinders,
       Also useful for walls and spheres with big lengths and radiuses that use small differentials. At the expense of memory
       coefficients: coefficients to determine the gradient same quantity as lambdas
       lambdas: list of lambdas for the system
       tau: adimensional time 
    """
    gradient = 0
    for i in range(len(coefficients)):
        gradient+=coefficients[i]*exp(-lambdas[i]**2*tau)
    return gradient



def temp_profiles(*, times:List[float], **profiles)->Tuple[List[float], List[List[float]]]:
    """
    Create multiple temperature profiles from timestamps caching relevant data
    times: list with times to create profiles
    profiles: check temp_profile arguments
    
    return coordinates and temperature profiles for each time
    """
    assert times, "No timestamps provided"
    coordinates = []
    temperatures = []
    
    #Add firt timestamp to coordinates Compute lambdas alfa and biot just once
    alfa, lambdas, biot_, coordinates, temp = temp_profile(time_=times[0], detailed=True, **profiles)
    typ = {
            'e': gradient_e_coeff,
            'c': gradient_c_coeef,
            'p': gradient_p_coeff,
            
          }
    temperatures.append(temp)
    profiles["alfa"] = alfa
    profiles["lambdas_"] = lambdas
    profiles["biot_"] = biot
    profiles["coord"] = coordinates
    profiles["performant_coeff"] = [typ[profiles["typ_"]](lambdas, coordinate, profiles["length"]) for coordinate in coordinates] #Obtain coefficients using the corresponding gradient function
    for stamp in times[1:]:
        _, temperatures_ = temp_profile(time_=stamp, **profiles)
        temperatures.append(temperatures_)
    return coordinates, temperatures



if __name__ == "__main__":
    #print(temp_profile(typ_='p', st=20, at=500, length=2, cond=110, conv=120, time_=800, dx=0.005, nlambdas=10, alfa=33.9e-6))
    #print(temp_profile(typ_='e', st=20, at=500, length=0.2, cond=110, conv=120, time_=420, dx=0.005, nlambdas=10, alfa=33.9e-6))
    #print(temp_profile(typ_='c', st=20, at=500, length=0.02, cond=110, conv=120, time_=420, dx=0.005, nlambdas=7, alfa=33.9e-6))
    print(temp_profile(typ_='p', st=20, at=500, length=0.02, cond=110, conv=120, time_=420, dx=0.005, nlambdas=7, alfa=33.9e-6))
    #print(temp_profile(typ_='p', st=20, at=500, length=0.02, cond=110, conv=120, time_=420, coord=[0, 0.01, 0.02], nlambdas=7, alfa=33.9e-6))
    #print(rs := temp_profile(typ_='c', st=600, at=200, length=0.1, cond=14.9, conv=80, time_=45*60, dx=0.005, nlambdas=7, cp=477, density=7900))
    #print(temp_profiles(times=[i+50 for i in range(1, 5800)], typ_='c', st=20, at=500, length=0.02, cond=110, conv=120, dx=0.005, nlambdas=7, alfa=33.9e-6))
    #print(temp_profiles(times=[i+50 for i in range(1,5800)], typ_='c', st=20, at=500, length=2.2, cond=110, conv=120, dx=0.005, nlambdas=7, alfa=33.9e-6))
    




