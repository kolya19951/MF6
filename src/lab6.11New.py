import numpy as np
from random import randint
import itertools
import matplotlib.pyplot as plt

k = 500
h = 0.01
border = [[0, np.pi]]


def g(u):
    if u[0] >= 1:
        return 8
    else:
        return 0


def getU(u):
    return 8 * (u[0])


def getXYZFromResult(result):
    X = [x[0][0] for x in result]
    Y = [y[1] for y in result]
    return X, Y


def getResult():
    borderNew = [getAB(b[0], b[1]) for b in border]
    listS = list(itertools.product(*borderNew, repeat=1))
    return [(i, getAvarage(i)) for i in listS if not check(i)]


def getLattice(f, border):
    border = [getAB(b[0], b[1]) for b in border]
    listS = list(itertools.product(*border, repeat=1))
    dS = set(i for i in listS if f(i))
    return [i for i in listS if i not in dS], f


def getAB(left, right):
    AB = [left]
    while left <= right:
        AB.append(left)
        left += h
    return AB


def getAvarage(point):
    s = sum([g(getPoints(list(point))[-1]) for a in range(k)])
    s = s / k
    return s


def check(u):
    if u[0] <= 0 or u[0] >= 1:
        return True
    else:
        return False


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


fValue = getResult()
analyt = [(u[0], getU(u[0])) for u in fValue]

X, Y = getXYZFromResult(fValue)
analX, analY = getXYZFromResult(analyt)
fig = plt.figure()
plt.plot(X, Y, 'b-', label='u')
plt.plot(analX, analY, 'r', label='Analytic')
plt.legend()
plt.show()
