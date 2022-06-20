"""
Fernando Jose Lavarreda Urizar
Module design to test zeros and Transient Analysis
"""

import pytest
import transient_analysis.zeros as zeros
import transient_analysis.ganalysis as ganalysis


TOLERANCE = 1e-4 #This means 0.0001 of difference respect values or in other words 0.01% error from results extracted from Wolfram Alfa.

def test_c_lambdas():
    #Can't test more zeros due to Wolfram limitations
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


def test_max_lambdas():
    with pytest.raises(ValueError):
        zeros.c_lambdas(2, zeros.MAX_LAMBDASC+1)


def test_max_biots():
    with pytest.raises(ValueError):
        zeros.p_lambdas(zeros.MAX_BIOTP+1, 5)
    
    with pytest.raises(ValueError):
        zeros.e_lambdas(zeros.MAX_BIOTE+1, 5)
    
    with pytest.raises(ValueError):
        zeros.c_lambdas(zeros.MAX_BIOTC+1, 5)


def test_temp_profile():
    #Results compared to answers from heat transfer book  'Heat and Mass Transfer by Yunus A. Çengel and Afshin J. Ghajar.'
    #ganalysis.temp_profile(typ_='e', st=20, at=500, length=2, cond=110, conv=120, time_=800, dx=0.005, nlambdas=10, alfa=33.9e-6)
    rs = ganalysis.temp_profile(typ_='p', st=20, at=500, length=0.02, cond=110, conv=120, time_=420, dx=0.005, nlambdas=7, alfa=33.9e-6)[-1][-1]
    assert rs == pytest.approx(279, 1e-2)
    
    #Test coordinates
    rs = ganalysis.temp_profile(typ_='p', st=20, at=500, length=0.02, cond=110, conv=120, time_=420, coord=[0, 0.02], nlambdas=7, alfa=33.9e-6)[-1][-1]
    assert rs == pytest.approx(279, 1e-2)
    
    rs = ganalysis.temp_profile(typ_='c', st=600, at=200, length=0.1, cond=14.9, conv=80, time_=45*60, dx=0.005, nlambdas=7, cp=477, density=7900)[-1][0]
    assert rs == pytest.approx(364, 1e-2)
    
    rs = ganalysis.temp_profile(typ_='e', st=5, at=95, length=0.025, cond=0.627, conv=1200, time_=865, dx=0.005, nlambdas=7, alfa=0.151e-6)[-1][0]
    assert rs == pytest.approx(70, 1e-2)


def test_temp_profiles():
    rs = ganalysis.temp_profiles(times=[100, 865, 100], typ_='e', st=5, at=95, length=0.025, cond=0.627, conv=1200, dx=0.005, nlambdas=7, alfa=0.151e-6)
    assert rs[1][1][0] == pytest.approx(70, 1e-2)
    
    rs = ganalysis.temp_profiles(times=[100, 45*60, 3000], typ_='c', st=600, at=200, length=0.1, cond=14.9, conv=80, dx=0.005, nlambdas=7, cp=477, density=7900)
    assert rs[1][1][0] == pytest.approx(364, 1e-2)



