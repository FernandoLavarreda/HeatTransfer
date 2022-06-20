"""
Fernando Jose Lavarreda Urizar
Module design to test zeros and Transient Analysis
"""

import pytest
import transient_analysis.zeros as zeros



TOLERANCE = 1e-4

def test_c_lambdas():
    results = zeros.c_lambdas(0.02, 5)
    expected = [0.199501, 3.836921, 7.018436, 10.175433, 13.325192]
    assert results == pytest.approx(expected, TOLERANCE)
    
    results = zeros.c_lambdas(5, 5)
    expected = [1.989814, 4.713142, 7.617707, 10.622300, 13.678558]
    assert results == pytest.approx(expected, TOLERANCE)


def test_p_lambdas():
    results = zeros.p_lambdas(0.02, 6)
    expected = [0.140951, 3.147945, 6.286366, 9.426899, 12.567961, 15.709236]
    assert results == pytest.approx(expected, TOLERANCE)
    
    results = zeros.p_lambdas(5, 6)
    expected = [1.313837, 4.033567, 6.909595, 9.892752, 12.935222, 16.010658]
    assert results == pytest.approx(expected, TOLERANCE)
    
    results = zeros.p_lambdas(30, 6)
    expected = [1.520167, 4.561494, 7.605689, 10.654324, 13.708547, 16.769056]
    assert results == pytest.approx(expected, TOLERANCE)


def test_e_lambdas():
    results = zeros.e_lambdas(0.02, 6)
    expected = [0.244459, 4.497860, 7.727840, 10.905955, 14.067615, 17.221916]
    assert results == pytest.approx(expected, TOLERANCE)
    
    results = zeros.e_lambdas(5, 6)
    expected = [2.570431, 5.354031, 8.302929, 11.334825, 14.407971, 17.503428]
    assert results == pytest.approx(expected, TOLERANCE)
    
    results = zeros.e_lambdas(30, 6)
    expected = [3.037240, 6.076634, 9.120085, 12.169063, 15.224528, 18.286950]
    assert results == pytest.approx(expected, TOLERANCE)



