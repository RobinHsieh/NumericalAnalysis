import numpy as np


def q(z):
    qz = -6.01 * (z**8) + 4.92 * (z**7) - 0.024 * (z**4) + 0.13 * (z**3) - 0.37 * (z**2) - 1.88 * z + 20.00
    return qz


def gauss_quadrature(f, a, b, n):
    x, w = _gauss_quadrature_weights(n)
    return (b - a) / 2 * np.sum(w * np.array([f((b - a) / 2 * xi + (a + b) / 2) for xi in x]))

def _gauss_quadrature_weights(n):
    if n == 2:
        x = [-np.sqrt(1/3)]
        w = [1]
    elif n == 3:
        x = [-np.sqrt(3/5)]
        w = [8/9]
    elif n == 4:
        x = [-np.sqrt(3/7 - 2/7 * np.sqrt(6/5)), -np.sqrt(3/7 + 2/7 * np.sqrt(6/5))]
        w = [(18 - np.sqrt(30)) / 36, (18 + np.sqrt(30)) / 36]
    elif n == 5:
        x = [-np.sqrt(5 + 2 * np.sqrt(10/7)) / 3, -np.sqrt(5 - 2 * np.sqrt(10/7)) / 3]
        w = [(322 - 13 * np.sqrt(70)) / 900, (322 + 13 * np.sqrt(70)) / 900]
    else:
        raise ValueError("Invalid number of sample points: {0}".format(n))
    return x, w


Pw = 1000**4
g = 9.8 * 0.001
para = 1 / (Pw * g)

x_array = np.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.])
q_x = q(x_array)


result = gauss_quadrature(q, 0, 10., 5)
print(para * result)