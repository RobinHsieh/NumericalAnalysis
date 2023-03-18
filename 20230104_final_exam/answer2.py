import matplotlib.pyplot as plt
import numpy as np

# T : Parcel virtual temperature
# Tv : Environment virtual temperature
# Height : 0--LFC(Level of free convection, aka Zf)  top--EL(Equilibrium level, aka Zn)
Height, T, Tv = np.loadtxt("Sounding_data.txt", unpack="true")


"""answer block ~ answer block ~ answer block"""

gravity = 9.8
virtual_temperature_term = (T - Tv) / Tv  # array of f(x)


# 2(a.) trapezoid and simpson 1/3
def trapezoidal_multi(f, h, n):
    # f: function
    # h = (b - a) / n
    # n: n edges, n+1 data points

    total = f[0]
    for i in range(1, n):
        total = total + 2 * f[i]
    total = total + f[n]

    ans = h * total / 2
    return ans


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


ans_one = gravity * trapezoidal_multi(virtual_temperature_term, (7500. - 0.) / (len(Height) - 1), len(Height) - 1)
ans_two = gravity * simpson_one_third(virtual_temperature_term, (7500. - 0.) / (len(Height) - 1), len(Height) - 1)
print("2(a.) CAPE with the trapezoid = ", ans_one)
print("2(a.) CAPE with the simpson 1/3 = ", ans_two)


print("---------------------------------------------")


# 2(b.) romberg
def cubic_interpolation(x0, x, y):

    x = np.array(x)
    y = np.array(y)
    # remove non finite values
    # indexes = np.isfinite(x)
    # check if sorted
    if np.any(np.diff(x) < 0):
        indexes = np.argsort(x)
        x = x[indexes]
        y = y[indexes]

    size = len(x)
    xdiff = np.diff(x)
    ydiff = np.diff(y)

    # allocate buffer matrices
    Li = np.zeros(size)
    Li_1 = np.zeros(size-1)
    z = np.zeros(size)

    # fill diagonals Li and Li-1 and solve [L][y] = [B]
    Li[0] = np.sqrt(2*xdiff[0])
    Li_1[0] = 0.0
    B0 = 0.0 # natural boundary
    z[0] = B0 / Li[0]

    for i in range(1, size-1, 1):
        Li_1[i] = xdiff[i-1] / Li[i-1]
        Li[i] = np.sqrt(2*(xdiff[i-1]+xdiff[i]) - Li_1[i-1] * Li_1[i-1])
        Bi = 6*(ydiff[i]/xdiff[i] - ydiff[i-1]/xdiff[i-1])
        z[i] = (Bi - Li_1[i-1]*z[i-1])/Li[i]

    i = size - 1
    Li_1[i-1] = xdiff[-1] / Li[i-1]
    Li[i] = np.sqrt(2*xdiff[-1] - Li_1[i-1] * Li_1[i-1])
    Bi = 0.0 # natural boundary
    z[i] = (Bi - Li_1[i-1]*z[i-1])/Li[i]

    # solve [L.T][x] = [y]
    i = size-1
    z[i] = z[i] / Li[i]
    for i in range(size-2, -1, -1):
        z[i] = (z[i] - Li_1[i-1]*z[i+1])/Li[i]

    # find index
    index = x.searchsorted(x0)
    np.clip(index, 1, size-1, index)

    xi1, xi0 = x[index], x[index-1]
    yi1, yi0 = y[index], y[index-1]
    zi1, zi0 = z[index], z[index-1]
    hi1 = xi1 - xi0

    # calculate cubic
    f0 = zi0/(6*hi1)*(xi1-x0)**3 + zi1/(6*hi1)*(x0-xi0)**3 + (yi1/hi1 - zi1*hi1/6)*(x0-xi0) + (yi0/hi1 - zi0*hi1/6)*(xi1-x0)
    return f0


def trapEq(a, b, n):
    h = (b - a) / n
    x = a
    sum_tra = cubic_interpolation([x], Height, virtual_temperature_term)[0]  # x_array = Height, y_array = virtual_temperature_term
    for i in range(1, n):
        x = x + h
        sum_tra = sum_tra + 2 * cubic_interpolation([x], Height, virtual_temperature_term)[0]

    sum_tra = sum_tra + cubic_interpolation([b], Height, virtual_temperature_term)[0]
    Trap = (b - a) * sum_tra / (2 * n)
    return Trap


def I(j, k, a, b):
    if k == 1:
        n = 2 ** (j - 1)
        return trapEq(a, b, n)
    else:
        i_jk = ((4 ** (k-1)) * I(j + 1, k - 1, a, b) - I(j, k - 1, a, b)) / ((4 ** (k - 1)) - 1)
        return i_jk


def romberg(a, b, es):
    i_ter = 0
    while True:
        i_ter = i_ter + 1

        for k in range(2, i_ter + 2):
            j = 2 + i_ter - k

        ea = abs((I(1, i_ter + 1, a, b) - I(2, i_ter, a, b)) / I(1, i_ter + 1, a, b)) * 100
        if ea < es:
            break

    return I(1, i_ter + 1, a, b)


ans_three = gravity * romberg(0., 7500., 0.005)  # let es = 0,005
print("2(b.) CAPE with the romberg = ", ans_three)


"""answer block ~ answer block ~ answer block"""


fig = plt.figure(figsize=(16, 12))
plt.plot(T, Height)
plt.title("Temperature Profile")
plt.ylabel("Height")
plt.xlabel("Temperature (K)")
plt.show()
