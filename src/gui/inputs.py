#GUI process user inputs
#Transient analysis
#Fernando Lavarreda

import re
from typing import List

def read_int(in_:str)->float:
    """
    Read user input to integer if failed return None
    """
    try:
        read = int(in_)
        return read
    except ValueError:
        raise ValueError("Not a whole number")


def read_float(in_:str)->float:
    """
    Read user input to float if failed return None
    """
    try:
        read = float(in_)
        return read
    except ValueError:
        raise ValueError("Not a decimal number")


def mapping(in_:str, mappings:dict):
    """
    Given an alias for an entry to another value return that other value
    """
    if in_ not in mappings:
        raise ValueError("Not a registered input")
    else:
        return mappings[in_]


def read_linspace(in_:str)->List[float]:
    """
    Process linearly spaced data given as sting input following a predefined format
    in_: string following _d+_d+_d+ where the first value indicates starting point, second value indicates number of intermediate values
    and last value indicates ending value
    Just accpet posititve integer values.
    End can be smaller than start, ending value may not be included
    """
    result = []
    match = re.search(r"(_\d+){3}", in_)
    if match == None:
        raise ValueError("Not properly formatted data")
    inp = match.group()
    digits = ["", "", ""]
    st = 0
    for value in inp[1:]:
        if value == "_":
            st+=1
            continue
        digits[st]+=value
    parsed = [int(d) for d in digits]
    dx = (parsed[-1]-parsed[0])/parsed[1]
    result.append(parsed[0])
    while len(result)<parsed[1]+1:
        result.append(result[-1]+dx)
    return result
    

def read_list(in_:str, sep=",")->List[float]:
    """
    Read a series of numbers presented by a user and separated by a character
    """
    separate = in_.split(sep)
    results = [read_float(inp) for inp in separate]
    return results






