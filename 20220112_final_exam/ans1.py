import numpy as np
import matplotlib.pyplot as plt

# read file
with open(r"../chi_yangs_final_exam/obs_2021-03-18_12_00_00.SOUND") as a:  # ../上級目錄

    # skip first 2 line
    for i in range(2):
        a.readline()

    # read data
    data = a.readlines()  # type(data) == List[str]
    temperature_array = np.zeros(len(data))
    pressure_array = np.zeros(len(data))

    for i in range(0, len(data)):
        temperature_array[i] = data[i].split()[3]
        pressure_array[i] = data[i].split()[0]


# 1.(a) -----------------------------------------
def diff(x_array, y_array):
    ans = []
    for index in range(len(x_array)):
        if index == 0:
            delta_temp = y_array[index + 1] - y_array[index]
            delta_press = x_array[index + 1] - x_array[index]
            m = delta_temp / delta_press
        elif index == len(x_array) - 1:
            delta_temp = y_array[index] - y_array[index - 1]
            delta_press = x_array[index] - x_array[index - 1]
            m = delta_temp / delta_press
        else:
            delta_temp = y_array[index + 1] - y_array[index - 1]
            delta_press = x_array[index + 1] - x_array[index - 1]
            m = delta_temp / delta_press
        ans.append(m)
    return ans


temp_grad_array = diff(pressure_array, temperature_array)
print("1.\n (a):")
for i in range(0, len(temp_grad_array)):
    print("When P =", pressure_array[i], ", temperature gradient =", temp_grad_array[i])


print('------------------------------------------')
# 1.(b) -----------------------------------------


# Newton finite difference
def Newt(x, y, n, x_miss):
    fdd = np.zeros((n, n))
    fdd[0:n, 0] = y[0:n]
    for j in range(1, n, 1):
        for i in range(0, n - j, 1):
            fdd[i, j] = (fdd[i + 1, j - 1] - fdd[i, j - 1]) / (x[i + j] - x[i])
    y_interp = y[0]
    xterm = 1.0
    for order in range(1, n):
        xterm = xterm * (x_miss - x[order - 1])
        y_interp = y_interp + fdd[0, order] * xterm
    return y_interp


T_975 = Newt(pressure_array, temperature_array, 1, 975.0)
print('(b):At the level of 975hpa, the temperature =', T_975, '(Newton)')


print('------------------------------------------')
# 1.(c) -----------------------------------------


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

# x = pressure_array, y = temperature_array
cubic_ans = cubic_interpolation([975.0], pressure_array, temperature_array)
print('(c):At the level of 975hpa, the temperature =', cubic_ans[0], '(cubic)')
