import matplotlib.pyplot as plt
import numpy as np


# 颱風半徑和風速
radius, velocity = np.loadtxt("TCVt.txt", unpack="true")


"""answer block ~ answer block ~ answer block"""


# 1(a.) lagrange
def lagrange(x, y, f, n, x_miss):
    ans = 0.0
    for i in range(f, n+1):
        product = y[i]
        for j in range(f, n+1):
            if i != j:
                product = product * (x_miss - x[j]) / (x[i] - x[j])
        ans = ans + product
    return ans


ans_one = lagrange(radius, velocity, 0, len(radius)-1, 50.)
print("1(a.) Vt at 50km = ", ans_one, "(by lagrange)")


print("---------------------------------------------")


# 1(b.) cubic spline
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


# x = radius, y = velocity
ans_two = cubic_interpolation([50.], radius, velocity)
print("1(b.) Vt at 50km = ", ans_two[0], "(by cubic spline)")


print("---------------------------------------------")
# 1(c.) cubic spline


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


my_radius_array = np.linspace(0.5, 192.5, 200)
my_wind_array = cubic_interpolation(my_radius_array, radius, velocity)
wind_gradient_array_one = diff(my_radius_array, my_wind_array)
ans_three = max(wind_gradient_array_one)
print("1(c.) maximum of the wind gradient = ", ans_three)


print("---------------------------------------------")

# 1(d.) central difference

wind_gradient_array_two = diff(radius, velocity)
ans_four = max(wind_gradient_array_two)
print("1(d.) maximum of the wind gradient = ", ans_four)


"""answer block ~ answer block ~ answer block"""


# print(radius)
#
# print(velocity)

## 畫個圖
fig = plt.figure(figsize=(16,12))
plt.plot(radius, velocity)
plt.xlabel("x=radius", fontsize=20)
plt.ylabel("y=velocity", fontsize=20)
plt.show()