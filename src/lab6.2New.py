from random import randint
from math import sin
from math import copysign
import itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt


def getDs(p):
    if p[0] <= 0:
        return True
    if p[0] >= 1:
        return True
    if p[1] <= 0:
        return True
    if p[1] >= 1:
        return True
    else:
        return False


def getH(p):
    return [sin(p[0]) / (1 + sin(p[0])), 1.0 / (1 + sin(p[0])), 1.0 / (1 + sin(p[0])), sin(p[0]) / (1 + sin(p[0]))]


def getU(p):
    return p[0] * p[1]


def getG(u):
    if u[0] >= 1:
        return u[1]
    if u[1] >= 1:
        return u[0]
    else:
        return 0


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
        dot[j] += copysign(s, dir)
        resultList.append(list(dot))
    return resultList


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


def getSum(point, g, st, is_border, k):
    st = st(point) if callable(st) else st
    s = sum([g(getPointList(list(point), is_border, st)[-1]) for a in range(k)])
    return s/k


def getLap(g, dS, h, k, border=[]):
    S, dS = getLattice(dS, border, h) if not isinstance(dS, list) else dS
    return [(point, getSum(point, g, h, dS, k)) for point in S]


k = 1000
h = 0.05
bounds = [[0, 1], [0, 1]]

grid = getLattice(getDs, bounds, h)
fValue = getLap(getG, list(grid), getH, k)
analytic = [(p[0], getU(p[0])) for p in fValue]

analX = levelOffX(analytic)
analY = levelOffY(analytic)
analZ = levelOffZ(analytic)
X = levelOffX(fValue)
Y = levelOffY(fValue)
Z = levelOffZ(fValue)

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
