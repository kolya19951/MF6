import numpy as np
from random import randint
import itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

h = 0.2
k = 1500

a1 = 0
b1 = 1
border = [[a1, b1], [a1, b1]]


def main():
    fValue = getResult()
    analyt = [(u[0], getU(u[0])) for u in fValue]

    X, Y, Z = getXYZFromResult(fValue)
    analX, analY, analZ = getXYZFromResult(analyt)

    fig = plt.figure()
    image1 = fig.add_subplot(111, projection='3d')
    plt.legend()
    image1.plot_trisurf(X, Y, Z, label="u")
    plt.show()
    fig = plt.figure()
    image2 = fig.add_subplot(111, projection='3d')
    plt.legend()
    image2.plot_trisurf(analX, analY, analZ, label="Analytic")
    plt.show()







def getAvarage(point):
    s = sum([getG(getPoints(list(point))[-1]) for i in range(k)])
    s = s / k
    return s


def getU(u):
    return u[0] * u[1]


def getAB(left, right):
    AB = [left]
    while left <= right:
        AB.append(left)
        left += h
    return AB


def getXYZFromResult(result):
    X = [x[0][0] for x in result]
    Y = [y[0][1] for y in result]
    Z = [z[1] for z in result]
    return X, Y, Z


def getResult():
    borderNew = [getAB(b[0], b[1]) for b in border]
    listS = list(itertools.product(*borderNew, repeat=1))
    return [(i, getAvarage(i)) for i in listS if not check(i)]


def check(p):
    if p[0] >= 1 or p[0] <= 0 or p[1] <= 0 or p[1] >= 1:
        return True


def getPoints(dot):
    dimension = len(dot)
    resultList = [list(dot)]
    while not check(dot):
        dir = randint(-dimension, dimension - 1)
        a = dir
        if dir < 0:
            a = dir + 1
        j = abs(a)
        s = h if not isinstance(h, list) else h[j]
        dot[j] += np.copysign(s, dir)
        resultList.append(list(dot))
    return resultList


def getG(u):
    if u[0] >= 1:
        return u[1]
    if u[1] >= 1:
        return u[0]
    else:
        return 0


main()
