from random import randint
import itertools
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt


def getU(p):
    return math.sin(p[0])


def getDs(p):
    if p[0] <= 0:
        return True
    if p[0] >= math.pi:
        return True
    else:
        return False


def getG(p):
    a = p[0]
    if a <= math.pi:
        return math.sin(p[0])
    if a >= 0:
        return math.sin(p[0])

def getF(p):
    a = math.sin(p[0])
    return a


def getPointList(dot, b, h):
    dimension = len(dot)
    resultList = [list(dot)]
    while not b(dot):
        dir = randint(-dimension, dimension - 1)
        a = dir
        if dir < 0:
            a = dir+1
        j = abs(a)
        s = h if not isinstance(h, list) else h[j]
        dot[j] += math.copysign(s, dir)
        resultList.append(list(dot))
    return resultList


def levelOffZ(val):
    Z = [z[1] for z in val]
    return Z


def levelOffX(val):
    X = [i[0][0] for i in val]
    return X


def levelOffY(val):
    if len(val[0][0]) != 1:
        Y = [y[0][1] for y in val]
    else:
        Y = [y[1] for y in val]
    return Y


def poisson(g, F, dS, h, k, bounds=[]):
    S, dS = getLattice(dS, bounds, h) if not isinstance(dS, list) else dS
    if F == 0: return getLap(g, dS, h, k, bounds)
    return [(point, getSum(point, g, F, h, dS, k)) for point in S]


def getLattice(f, border, h):
    border = [getDiapason(b[0], b[1], h) for b in border]
    listS = list(itertools.product(*border, repeat=1))
    dS = set(i for i in listS if f(i))
    return [i for i in listS if i not in dS], f


def getDiapason(b1, b2, increment):
    list = []
    while b1 <= b2:
        list.append(b1)
        b1 = b1 + increment
    return list


def getLap(g, dS, h, k, border=[]):
    S, dS = getLattice(dS, border, h) if not isinstance(dS, list) else dS
    return [(point, getSum(point, g, h, dS, k)) for point in S]


def getSum(point, g, F, h, dS, k):
    s = 0
    if len(point) == 1:
        a = 2
    else:
        a = 4
    b = math.pow(float(h), 2) / a
    for _aa in range(k):
        pr = getPointList(list(point), dS, h)
        if g != 0:
            d = g(pr[-1])
        else:
            d = 0
        s = s + b * sum(F(c) for c in pr[1:-1]) + d
    return s / k


h = 0.05
k = 1000
bounds = [[0, 2]]

fValue = poisson(getG, getF, getDs, h, k, bounds)
analytic = [(p[0], getU(p[0])) for p in fValue]


lapX = levelOffX(fValue)
lapY = levelOffY(fValue)
# Z = levelOffZ(fValue)
anX = levelOffX(analytic)
anY = levelOffY(analytic)
# Z = levelOffZ(analytic)
fig = plt.figure()
plt.plot(lapX, lapY, 'b-', label='u')
plt.plot(anX, anY, 'r', label='Analytic')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=4, mode="expand", borderaxespad=1.)
plt.show()