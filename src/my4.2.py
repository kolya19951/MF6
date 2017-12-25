import random
from src.My32 import getResult
import pylab
from math import *
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

l = [[0, 2], [0, 2]]
N = 1000
h = 0.1
x = []
y = []
p = [0.25, 0.5, 0.75, 1]


def getAnalytic():
    result = np.zeros((len(x), len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            result[i][j] = sin(x[i]) * sin(y[j])
    return result


def getG(x, y):
    return sin(x) * sin(y)


def getF(x, y):
    return ((h ** 2) / 4) * 2 * sin(x) * sin(y)


i = l[0][0]
while (i < l[0][1]):
    x.append(i)
    i += h

j = l[1][0]
while (j < l[1][1]):
    y.append(j)
    j += h

U = np.zeros((len(x), len(y)))

for k1 in range(1, len(x)):
    for k2 in range(1, len(y)):
        for i in range(0, N):
            k1_ = k1
            k2_ = k2
            while 0 < k1_ and k1_ < len(x) - 1 and 0 < k2_ and k2_ < len(y) - 1:
                r = random.uniform(0, 1)
                if r < p[0] and r >=0 :
                    k1_ -= 1
                elif p[0] <= r and r < p[1]:
                    k1_ += 1
                elif p[1] <= r and r < p[2]:
                    k2_ -= 1
                elif p[2] <= r and r < p[3]:
                    k2_ += 1
            U[k1_][k2_] = U[k1_][k2_] + 1

        for j in range(0, len(x) - 1):
            U[k1][k2] = U[k1][k2] + getG(x[j], y[0]) * (U[j][0] / N) + getG(x[j], y[len(y) - 1]) * (
            U[j][len(y) - 1] / N)

        for j in range(0, len(y) - 1):
            U[k1][k2] = U[k1][k2] + getG(x[0], y[j]) * (U[0][j] / N) + getG(x[len(x) - 1], y[j]) * (
            U[len(y) - 1][j] / N)

        for j in range(0, len(x) - 1):
            U[j][0] = 0
            U[j][len(y) - 1] = 0

        for j in range(0, len(y) - 1):
            U[0][j] = 0
            U[len(x) - 1][j] = 0

for j in range(0, len(x)):
    U[j][0] = getG(x[j], y[0])
    U[j][len(y) - 1] = getG(x[j], y[len(y) - 1])

for j in range(0, len(y)):
    U[0][j] = getG(x[0], y[j])
    U[len(x) - 1][j] = getG(x[len(x) - 1], y[j])

U1 = getResult()

U = U + U1
UA = getAnalytic()
fig1 = pylab.figure()
axes = fig1.gca(projection='3d')
xi, yi = np.meshgrid(x, y)
print(xi.shape)
# axes.plot_surface(xi, yi, UA)
axes.plot_surface(xi, yi, U)
# axes.plot_surface(xi, yi, yA[ti.index(1.998)], cmap='viridis')
# print(np.linalg.norm(y - yA) / np.linalg.norm(yA))
pylab.show()
