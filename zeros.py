
import sys
from functools import partial
import matplotlib.pyplot as plt
from math import sin, cos, tan, factorial, pi

def pared(lamb, biot):
    return lamb*tan(lamb)-biot


def dpared(lamb):
    return tan(lamb)+lamb*1/(cos(lamb)**2)


def cilindro(lamb, biot):
    return lamb*(bessel(lamb, 1)/bessel(lamb, 0))-biot


def dcilindro(lamb):
    return (bessel(lamb, 1)/bessel(lamb, 0))+lamb*derivar(lamb, lambda x: (bessel(x, 1)/bessel(x, 0)))


def esfera(lamb, biot):
    return 1-lamb/tan(lamb)-biot


def desfera(lamb):
    return -1/tan(lamb)+lamb/(sin(lamb)**2)


def newtons(fn, dx, xo, tolerancia=0.000001):
    i = 0
    while abs(fn(xo))>tolerancia:
        xo -= fn(xo)/dx(xo)
        i+=1
    return xo, i


def multiple_newtons(fn, dx, xo, number, step, tolerancia=0.000001):
    found = []
    for i in range(number):
        if found:
            zero, iteration = newtons(fn, dx, found[-1]+step, tolerancia=tolerancia)
        else:
            zero, iteration = newtons(fn, dx, xo, tolerancia=tolerancia)
        found.append(zero)
    return found



def bessel(x, degree, terms=120):
    if x>35:
        return sum([(x/2)**(i)*((-1)**i)/factorial(i)*(x/2)**(degree)/factorial(i+degree)*(x/2)**(i) for i in range(terms+48)])
    else:
        return sum([((-1)**i)/factorial(i)/factorial(i+degree)*(x/2)**(2*i+degree) for i in range(terms)])



def derivar(x, func, diferencial=1e-8):
    return (func(x+diferencial)-func(x-diferencial))/(2*diferencial)





if __name__ == "__main__":
    args = sys.argv[1:]
    options = ("p", "c", "e")
    if len(args) >= 2:
        try:
            biot = float(args[1])
            zeros = 5
            step = 3.05
            if len(args) >= 3:
                zeros = int(args[2])
                if len(args) == 4:
                    step = float(args[3])
        except ValueError:
            print("argumentos invalidos")
        else:
            if args[0] == "p":
                if biot < 0.7:
                    zs = multiple_newtons(partial(pared, biot=biot), dpared, 0.2, zeros, step)
                elif biot < 2:
                    zs = multiple_newtons(partial(pared, biot=biot), dpared, 0.9, zeros, step)
                elif biot < 5:
                    zs = multiple_newtons(partial(pared, biot=biot), dpared, 1.25, zeros, step)
                elif biot <15:
                    zs = multiple_newtons(partial(pared, biot=biot), dpared, 1.4, zeros, step)
                elif biot<=100_000:
                    zs = multiple_newtons(partial(pared, biot=biot), dpared, pi/2-1e-8, zeros, pi)
                else:
                    print("No computable")
                    sys.exit()
                print(zs)
            elif args[0] == "c":
                if zeros>7:
                    zeros = 7
                if biot < 0.1:
                    zs = multiple_newtons(partial(cilindro, biot=biot), dcilindro, 0.2, zeros, step)
                elif biot < 0.7:
                    zs = multiple_newtons(partial(cilindro, biot=biot), dcilindro, 0.6, zeros, step)
                elif biot < 5:
                    zs = multiple_newtons(partial(cilindro, biot=biot), dcilindro, 2.2, zeros, step)
                elif biot <= 100:
                    zs = multiple_newtons(partial(cilindro, biot=biot), dcilindro, 2.4, zeros, step)
                else:
                    print("No computable")
                    sys.exit()
                print(zs)
            elif args[0] == "e":
                if biot < 0.01:
                    zs = multiple_newtons(partial(esfera, biot=biot), desfera, 0.2, zeros, pi)
                elif biot < 0.1:
                    zs = multiple_newtons(partial(esfera, biot=biot), desfera, 0.2, zeros, step)
                elif biot < 1.8:
                    zs = multiple_newtons(partial(esfera, biot=biot), desfera, 1.1, zeros, step)
                elif biot < 5:
                    zs = multiple_newtons(partial(esfera, biot=biot), desfera, 2.3, zeros, step)
                elif biot<45:
                    zs = multiple_newtons(partial(esfera, biot=biot), desfera, 3, zeros, pi)
                elif biot<=100_000:
                    zs = multiple_newtons(partial(esfera, biot=biot), desfera, pi-1e-8, zeros, pi)
                else:
                    print("No computable")
                    sys.exit()
                print(zs)
            else:
                print("geometria inexistente")
    else:
        #print("Input no valida")
        xs = [i/1000*35 for i in range(1000)]
        curvas = 2
        try:
            if args:
                curvas = int(args[0])
        except ValueError:
            curvas = 2
        
        for i in range(curvas):
            ys = [bessel(x, i) for x in xs]
            plt.plot(xs, ys, label=f"J{i}")
        plt.title("Curvas de Bessel")
        plt.ylabel("y")
        plt.xlabel("x")
        plt.grid()
        plt.legend()
        plt.show()
        
        

