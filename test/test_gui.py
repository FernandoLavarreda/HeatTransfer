"""
Fernando Jose Lavarreda Urizar
Module design to test parsing of input values from user in gui
"""

import pytest
import gui.inputs as gin


def test_read_int():
    assert gin.read_int("4") == 4
    
    with pytest.raises(ValueError):
        gin.read_int("4.")
    
    with pytest.raises(ValueError):
        gin.read_int("val5")


def test_read_float():
    assert gin.read_float("65.2") == pytest.approx(65.2, 1e-2)
    
    with pytest.raises(ValueError):
        gin.read_float("sdf.545")


def test_mapping():
    assert gin.mapping("4.", {"4.":45, "65":66, "as":33}) == 45
    
    with pytest.raises(ValueError):
        gin.mapping("4.", {"4":45, "65":66, "as":33})


def test_read_linspace():
    assert gin.read_linspace("_10_2_40") == [10, 25, 40]
    assert gin.read_linspace("_10_30_40") == [10+i for i in range(31)]
    assert gin.read_linspace("_100_50_50") == [100-i for i in range(51)]
    
    with pytest.raises(ValueError):
        gin.read_linspace("_10_2_")


def test_read_list():
    assert gin.read_list("10, 15, 46.3, 5879.26") == [10, 15, 46.3, 5879.26]
    assert gin.read_list("10 ; 15 ;46.3; 5879.26", sep=";") == [10, 15, 46.3, 5879.26]
    
    with pytest.raises(ValueError):
        gin.read_list("1212, 12a, 1245b")