import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from random import randint
import itertools


def getDs(p):
    if 1 <= abs(p[0]) + abs(p[1]):
        return True
    else:
        return False


def getG(a):
    if True == getDs(a):
        return 0
    else:
        return False


def getU(p):
    a = (1 - abs(p[0]) - abs(p[1]))
    return a


def getF(u):
    a = math.exp(-math.pow(u[0], 2) - math.pow(u[1], 2))
    return a


def getFirstSum(dot, g, h, b, k):
    s = sum([g(getPointList(list(dot), b, h)[-1]) for a in range(k)])
    s = s / k
    return s


def getLap(g, dS, h, k, bounds=[]):
    S, dS = getLattice(dS, bounds, h) if not isinstance(dS, list) else dS
    return [(point, getFirstSum(point, g, h, dS, k)) for point in S]


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


def getPointList(dot, b, h):
    dimension = len(dot)
    resultList = [list(dot)]
    while not b(dot):
        dir = randint(-dimension, dimension - 1)
        a = dir
        if dir < 0:
            a = dir + 1
        j = abs(a)
        s = h if not isinstance(h, list) else h[j]
        dot[j] += math.copysign(s, dir)
        resultList.append(list(dot))
    return resultList


def getSecondSum(point, g, F, h, dS, k):
    s = 0
    if len(point) == 1:
        a = 2
    else:
        a = 4
    b = math.pow(float(h), 2) / a
    for _ in range(k):
        pr = getPointList(list(point), dS, h)
        if g != 0:
            d = g(pr[-1])
        else:
            d = 0
        s = s + b * sum(F(c) for c in pr[1:-1]) + d
    return s / k


def Puasson(g, F, dS, h, k, border=[]):
    S, dS = getLattice(dS, border, h) if not isinstance(dS, list) else dS
    if F == 0:
        return getLap(g, dS, h, k, border)
    return [(point, getSecondSum(point, g, F, h, dS, k)) for point in S]


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


border = [[-1, 1], [-1, 1]]
h = 0.1
k = 100
fValue = Puasson(getG, getF, getDs, h, k, border)
analytic = [(p[0], getU(p[0])) for p in fValue]

analX = levelOffX(analytic)
analY = levelOffY(analytic)
analZ = levelOffZ(analytic)
X = levelOffX(fValue)
Y = levelOffY(fValue)
Z = levelOffZ(fValue)

fig = plt.figure()
image1 = fig.add_subplot(122, projection='3d')
image2 = fig.add_subplot(121, projection='3d')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=1.)
image2.plot_trisurf(analX, analY, analZ, label="аналітична")
image1.plot_trisurf(X, Y, Z, label="u")
plt.show()
