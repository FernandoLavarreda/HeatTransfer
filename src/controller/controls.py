

from typing import List


def symmetry(xs:List[float], factor:float=-1):
    """Do a reflection of x values and y values to obtain full tempereture profile"""
    xo = []
    for i in range(len(xs), 0, -1):
        xo.append(xs[i-1]*factor)
    return xo


def msymmetry(xs:List[List[float]], factor:float=-1):
    symmetrics = []
    for x in xs:
        symmetrics.append(symmetry(x, factor=factor))
    return symmetrics


if __name__ == "__main__":
    print(symmetry(range(1, 10), range(1, 10)))