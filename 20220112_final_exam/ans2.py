from scipy import integrate
from scipy.special import erf
import numpy as np


def q(z):
    qz = -6.01 * (z**8) + 4.92 * (z**7) - 0.024 * (z**4) + 0.13 * (z**3) - 0.37 * (z**2) - 1.88 * z + 20.00
    return qz


# (a).trapezoidal
def trapezoidal_multi(f, h, n):
    # f: function
    # h = (b - a) / n
    # n: n segments, n+1 data points

    total = f[0]
    for i in range(1, n):
        total = total + 2 * f[i]
    total = total + f[n]

    ans = h * total / 2
    return ans


# (b).simpson's 1/3
def simpson_one_third(f, h, n):
    # f: function
    # h = (b - a) / n
    # n: n segments

    total = f[0]
    for i in range(1, n, 2):
        total = total + 4 * f[i]
    for j in range(2, n-1, 2):
        total = total + 2 * f[j]
    total = total + f[n]

    ans = h * total / 3
    return ans


# (c).romberg
def TrapEq(a, b, n):
    h = (b - a) / n
    x = a
    sum_tra = q(x)
    for i in range(1, n):
        x = x + h
        sum_tra = sum_tra + 2 * q(x)

    sum_tra = sum_tra + q(b)
    Trap = (b - a) * sum_tra / (2 * n)
    return Trap


def I(j, k, a, b):
    if k == 1:
        n = 2 ** (j - 1)
        return TrapEq(a, b, n)
    else:
        i_jk = ((4 ** (k-1)) * I(j + 1, k - 1, a, b) \
            - I(j, k - 1, a, b)) / ((4 ** (k - 1)) - 1)
        return i_jk


def Romberg(a, b, es):
    i_ter = 0
    while True:
        i_ter = i_ter + 1

        for k in range(2, i_ter + 2):
            j = 2 + i_ter - k
            # print(I(j, k, a, b))

        ea = abs((I(1, i_ter + 1, a, b) - I(2, i_ter, a, b)) / I(1, i_ter + 1, a, b)) * 100
        #print('ea = ', ea)
        if ea < es:
            #print('iter = ', i_ter)
            break

    return I(1, i_ter + 1, a, b)



Pw = 1000**4
g = 9.8 * 0.001
para = 1 / (Pw * g)

x = np.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.])
q_x = q(x)

trap = trapezoidal_multi(q_x, (10 - 0) / (len(x) - 1), len(x) - 1)  # len(x) 個點，len(x)-1 個邊，單位換算:10000m = 10km
simp = simpson_one_third(q_x, (10 - 0) / (len(x) - 1), len(x) - 1)
romb = Romberg(0, 10, 0.05)
# simp = integrate.simps(fx,dx=1000)
# romb = integrate.romberg(q, 0, 10000)
# quad = float((integrate.quadrature(q, 0.0, 10000.0))[0])

print('2.')
print('(a):')
print('Trapezoid:', para * trap)
print("Simpson's 1/3:", para * simp)
print("Romberg:", para * romb)
# print('Trapezoid:', para * trap, '\nSimpson 1/3:', para * simp, '\nRomberg:', para * romb)
# print('----------------------------------------------')
# print('(b):')
# print('Gauss-quadrature:', para * quad)