import random

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


def getG():
    return 0


def getF(x, y):
    return ((h ** 2) / 4) * 2 * sin(x) * sin(y)




def getResult():
    i = l[0][0]
    while (i < l[0][1]):
        x.append(i)
        i += h

    j = l[1][0]
    while (j < l[1][1]):
        y.append(j)
        j += h

    U = np.zeros((len(x), len(y)))

    for k1 in range(0, len(x)):
        for k2 in range(0, len(y)):
            for i in range(0, N):
                k1_ = k1
                k2_ = k2
                while 0 < k1_ and k1_ < len(x) - 1 and 0 < k2_ and k2_ < len(y) - 1:
                    r = random.uniform(0, 1)
                    if r < p[0]:
                        k1_ -= 1
                    elif p[0] <= r and r < p[1]:
                        k2_ += 1
                    elif p[1] <= r and r < p[2]:
                        k1_ += 1
                    elif p[2] <= r and r < p[3]:
                        k2_ -= 1
                    if 0 < k1_ and k1_ < len(x) and 0 < k2_ and k2_ < len(y):
                        U[k1][k2] = U[k1][k2] + getF(x[k1_], y[k2_])
            U[k1][k2] = U[k1][k2] / N
    return U

def main():

    U = getResult()
    # UA = getAnalytic()
    fig1 = pylab.figure()
    axes = fig1.gca(projection='3d')
    xi, yi = np.meshgrid(x, y)
    print(xi.shape)
    # axes.plot_surface(xi, yi, UA)
    axes.plot_surface(xi, yi, U)
    # axes.plot_surface(xi, yi, yA[ti.index(1.998)], cmap='viridis')
    # print(np.linalg.norm(y - yA) / np.linalg.norm(yA))
    pylab.show()

# main()