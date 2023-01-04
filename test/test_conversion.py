"""
Fernando Jose Lavarreda Urizar
Module design to unit conversions
"""

import pytest
from conversion import conversion


TOLERANCE = 1e-4 #This means 0.0001 of difference respect values or in other words 0.01% error from results extracted from https://converter.eu/thermal_conductivity/#1_BTU/Hour-Foot-%C2%B0F_in_Watt/Meter-K and google conversions


#For the testing inputs/outputs there is a dictionary each Property (e.g TIME) maps to a tuple containing (units,) (inputs,) (expected outputs,)

TESTING_METRIC = {
           "TIME":(("ms", "h", "min"), (12, 1, 360), [0.012, 3600, 21_600]),
           "TEMPERATURE":(("°C", "°F"), (25, 89), [25, 31.6667]),
           "DISTANCE":(("mm", "cm", "ft", "yd"), (1200, 980, 465, 320), [1.2, 9.8, 141.732, 292.608]),
           "COND":(("kW/m°C", "Btu/(h*ft*°F)", "Btu/(h*in*°F)"), (690, 375, 480), [690_000, 648.5914521066567, 9962.364704358246]),
           "CONV":(("kW/m^2°C", "Btu/(h*in^2*°F)"), (622, 2), [622_000, 1635.3398586]),
           "SP":(("kJ/kg°C", "Btu/lbm°F"), (350, 420), [350_000, 1_758_456]),
           "DENSITY":(("g/cm^3", "lbm/ft^3", "lbm/in^3"), (0.069, 1.81041, 0.00249278), [69, 29, 69]),
           "DIFF":(("mm^2/s", "mm^2/ms", "ft^2/s", "in^2/s"), (69, 39, 420, 666), [69/1_000_000, 0.039, 39.0193, 0.429677]),
}


TESTING_IMPERIAL = {
           "TIME":(("ms", "h", "min"), (12, 1, 360), [0.012, 3600, 21_600]),
           "TEMPERATURE":(("°C", "°F"), (36, 89), [96.8, 89]),
           "DISTANCE":(("mm", "cm", "ft", "yd"), (1200, 980, 350, 850), [3.937008, 32.1522, 350, 2550]),
           "COND":(("kW/m°C", "Btu/(h*ft*°F)", "Btu/(h*in*°F)"), (89_000, 69_000, 420), [51457662.43387323, 69_000, 5040]),
           "CONV":(("kW/m^2°C", "Btu/(h*in^2*°F)"), (5.6, 321), [986.21701874, 46224]),
           "SP":(("kJ/kg°C", "Btu/lbm°F"), (3870, 241), [924.3336, 241]),
           "DENSITY":(("g/cm^3", "lbm/ft^3", "lbm/in^3"), (2, 569, 21), [124.855921183, 569, 36288]),
           "DIFF":(("mm^2/s", "mm^2/ms", "cm^2/s", "ft^2/s", "in^2/s"), (123, 220, 214, 984, 3410), [0.00132396, 2.36806029, 0.230348, 984, 23.68056]),
}



def test_metric():
    for test, description in TESTING_METRIC.items():
        results = []
        for subtest in range(len(description[0])):
            result = conversion.convert_metric(description[1][subtest], test, description[0][subtest])
            results.append(result)
        assert results == pytest.approx(description[2], TOLERANCE)



def test_imperial():
    for test, description in TESTING_IMPERIAL.items():
        results = []
        for subtest in range(len(description[0])):
            result = conversion.convert_imperial(description[1][subtest], test, description[0][subtest])
            results.append(result)
        assert results == pytest.approx(description[2], TOLERANCE)










