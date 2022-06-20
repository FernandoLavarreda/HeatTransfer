"""
Fernando Jose Lavarreda Urizar
Module design to test zeros and Transient Analysis
"""

import pytest
import zeros
import ganalysis


TOLERANCE = 1e-7

def test_c_lambdas():
    resutlts = zeros.c_lambdas(0.02, 5)
    expected = [0.444404, 3.832061, 7.015644, 10.173487, 13.323700]
    assert results == pytest.aprox(expected, TOLERANCE)
    
    resutlts = zeros.c_lambdas(5, 5)
    expected = [1.592473, 3.915693, 7.029991, 10.178211, 13.325805]
    assert results == pytest.aprox(expected, TOLERANCE)
    
    resutlts = zeros.c_lambdas(5, 3)
    expected = [2.088789, 4.227384, 7.099718]
    assert results == pytest.aprox(expected, TOLERANCE)


def test_p_lambdas():
    resutlts = zeros.p_lambdas(0.02, 6)
    expected = [0.140951, 3.147945, 6.286366, 9.426899, 12.567961, 15.709236]
    assert results == pytest.aprox(expected, TOLERANCE)
    
    resutlts = zeros.p_lambdas(5, 6)
    expected = [1.313837, 4.033567, 6.909595, 9.892752, 12.935222, 16.010658]
    assert results == pytest.aprox(expected, TOLERANCE)
    
    resutlts = zeros.p_lambdas(30, 6)
    expected = [1.520167, 4.561494, 7.605689, 10.654324, 13.708547, 16.769056]
    assert results == pytest.aprox(expected, TOLERANCE)


def test_e_lambdas():
    resutlts = zeros.e_lambdas(0.02, 6)
    expected = [0.244459, 4.497860, 7.727840, 10.905955, 14.067615, 17.221916]
    assert results == pytest.aprox(expected, TOLERANCE)
    
    resutlts = zeros.e_lambdas(5, 6)
    expected = [2.570431, 5.354031, 8.302929, 11.334825, 14.407971, 17.503428]
    assert results == pytest.aprox(expected, TOLERANCE)
    
    resutlts = zeros.e_lambdas(30, 6)
    expected = [3.037240, 6.076634, 9.120085, 12.169063, 15.224528, 18.286950]
    assert results == pytest.aprox(expected, TOLERANCE)



