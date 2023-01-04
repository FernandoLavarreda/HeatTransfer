#Unit conversion for Transient Heat transfer Interactions
#Fernando Lavarreda


METRIC = ["C", "m", "W/m°C", "W/m^2°C", "J/kg°C", "kg/m^3", "m^2/s", "s"]
IMPERIAL = ["F", "ft", "Btu/(h*ft*°F)", "Btu/(h*ft^2*°F)", "Btu/lbm°F", "lbm/ft^3", "ft^2/s", "s"]



def temp_conversion(temperature):
    return (temperature-32)/1.8


def temp_conversion2(temperature):
    return temperature*1.8+32


TIME = {
    "ms": 0.001,
    "s": 1,
    "min": 60,
    "h":  3600,
    "__imperial":1,
    "__metric":1,
}


METRIC_TEMPERATURE = {
    "°C": 1,
    "__imperial":temp_conversion,
}


METRIC_DISTANCE = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "__imperial":0.3048,
}


METRIC_COND = {
    "W/m°C": 1,
    "kW/m°C": 1000,
    "W/cm°C": 100,
    "__imperial":1.7295772056,
}


METRIC_CONV = {
    "W/m^2°C":1,
    "kW/m^2°C":1000,
    "W/cm^2°C":1e4,
    "__imperial":5.678263398,
}


METRIC_SP = {
    "J/kg°C":1,
    "kJ/kg°C":1000,
    "J/g°C":1000,
    "__imperial":4186.8,
}


METRIC_DENSITY = {
    "kg/m^3":1,
    "g/cm^3":1000,
    "__imperial":16.01846337,
}


METRIC_DIFF = {
    "m^2/s":1,
    "cm^2/s":1/1e4,
    "mm^2/s":1/1e6,
    "mm^2/ms":1/1000,
    "__imperial":0.0929030,
}


METRIC_TABLE = {
    "TEMPERATURE": METRIC_TEMPERATURE,
    "TIME":TIME,
    "DISTANCE":METRIC_DISTANCE,
    "COND":METRIC_COND,
    "CONV":METRIC_CONV,
    "SP":METRIC_SP,
    "DENSITY":METRIC_DENSITY,
    "DIFF":METRIC_DIFF,
}


IMPERIAL_TEMPERATURE = {
    "°F": 1,
    "__metric":temp_conversion2,
}


IMPERIAL_DISTANCE = {
    "in": 1/12,
    "ft": 1,
    "yd": 3,
    "__metric":3.28084,
}


IMPERIAL_COND = {
    "Btu/(h*ft*°F)": 1,
    "Btu/(h*in*°F)": 12,
    "__metric":1/METRIC_COND["__imperial"],
}


IMPERIAL_CONV = {
    "Btu/(h*ft^2*°F)":1,
    "Btu/(h*in^2*°F)":144,
    "__metric":1/METRIC_CONV["__imperial"],
}


IMPERIAL_SP = {
    "Btu/lbm°F":1,
    "__metric":1/METRIC_SP["__imperial"],
}


IMPERIAL_DENSITY = {
    "lbm/ft^3":1,
    "lbm/in^3":1728,
    "__metric":1/16.01846337,
}


IMPERIAL_DIFF = {
    "ft^2/s":1,
    "in^2/s":1/144,
    "__metric":10.76391111,
}


IMPERIAL_TABLE = {
    "TEMPERATURE":IMPERIAL_TEMPERATURE,
    "TIME":TIME,
    "DISTANCE":IMPERIAL_DISTANCE,
    "COND":IMPERIAL_COND,
    "CONV":IMPERIAL_CONV,
    "SP":IMPERIAL_SP,
    "DENSITY":IMPERIAL_DENSITY,
    "DIFF":IMPERIAL_DIFF,
}



def convert_metric(value:float, unit:str, from_:str)->float:
    """Conversion of units to the Metric system as defined by METRIC
    value: magnitude that wants to be transformed
    unit: any property from TEMPERATURE, DISTANCE, COND, CONV, SP, DENSITY, DIFF
    from_: original unit cm, mm, ft, in etc"""
    if unit in METRIC_TABLE:
        if from_ in METRIC_TABLE[unit]:
            return METRIC_TABLE[unit][from_]*value
        if from_ in IMPERIAL_TABLE[unit]:
            return imperial_metric(value, unit, from_)
        raise ValueError(f"{from_} to standard metric system not supported")
    raise ValueError(f"Unit {unit} not supported")



def convert_imperial(value:float, unit:str, from_:str)->float:
    """Conversion of units to the Metric system as defined by IMPERIAL
    value: magnitude that wants to be transformed
    unit: any property from TEMPERATURE, DISTANCE, COND, CONV, SP, DENSITY, DIFF
    from_: original unit in, yd, m, mm, cm"""
    if unit in IMPERIAL_TABLE:
        if from_ in IMPERIAL_TABLE[unit]:
            return IMPERIAL_TABLE[unit][from_]*value
        if from_ in METRIC_TABLE[unit]:
            return metric_imperial(value, unit, from_)
        raise ValueError(f"{from_} to standard imperial system not supported")
    raise ValueError(f"Unit {unit} not supported")


def metric_imperial(value:float, unit:str, from_:str)->float:
    metric = convert_metric(value, unit, from_)
    if unit == "TEMPERATURE":
        return IMPERIAL_TABLE[unit]["__metric"](metric)
    else:
        return convert_imperial(metric, unit, "__metric")


def imperial_metric(value:float, unit:str, from_:str)->float:
    imperial = convert_imperial(value, unit, from_)
    if unit == "TEMPERATURE":
        return METRIC_TABLE[unit]["__imperial"](imperial)
    else:
        return convert_metric(imperial, unit, "__imperial")


if __name__ == "__main__":
    print(convert_metric(1200, "DENSITY", "lbm/ft^3"))
    print(convert_imperial(86, "DISTANCE", "m"))
    print(convert_imperial(360, "TIME", "min"))













