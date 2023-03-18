import numpy as np


def newton_interpolation(x, y, x_evaluated, start, end):

    n = end - start + 1
    p = y[start:end + 1]
    for k in range(1, n):
        for i in range(n - 1, k - 1, -1):
            p[i] = (p[i] - p[i - 1]) / (x[i + start] - x[i - k + start])
    res = p[n - 1]
    for i in range(n - 2, -1, -1):
        res = res * (x_evaluated - x[i + start]) + p[i]
    return res


T_array = [0, 8, 16, 24, 32, 40]
o_array = [14.621, 11.873, 9.870, 8.418, 7.305, 6.413]

print("Linear interpolation = " + str(newton_interpolation(T_array, o_array, 27, 3, 4)))
print("Newton’s interpolating polynomial 4 order = " + str(newton_interpolation(T_array, o_array, 27, 1, 5)))

arr_a = np.array([[2*(T_array[2]-T_array[0]), (T_array[2]-T_array[1]), 0, 0],
                  [(T_array[2]-T_array[1]), 2*(T_array[3]-T_array[1]), (T_array[3]-T_array[2]), 0],
                  [0, (T_array[3]-T_array[2]), 2*(T_array[4]-T_array[2]), (T_array[4]-T_array[3])],
                  [0, 0, (T_array[4]-T_array[3]), 2*(T_array[5]-T_array[3])]])
arr_c = np.array([[0.],
                 [0.],
                 [0.],
                 [0.]])
for i in range(0, 4):
    two = i+2
    one = i+1
    zer = i
    arr_c[i, 0] = float(((o_array[two]-o_array[one])/(T_array[two]-T_array[one])) + ((o_array[zer]-o_array[one])/(T_array[one]-T_array[zer])))*6.0

d2f = np.linalg.inv(arr_a).dot(arr_c)


# i = 4
def f_i(x, i):
    c1 = d2f[i-2]/6/(T_array[i]-T_array[i-1])
    c2 = d2f[i-1]/6/(T_array[i]-T_array[i-1])
    c3 = (o_array[i-1]/(T_array[i]-T_array[i-1]))-d2f[i-2]*(T_array[i]-T_array[i-1])/6
    c4 = (o_array[i]/(T_array[i]-T_array[i-1]))-d2f[i-1]*(T_array[i]-T_array[i-1])/6
    t1 = c1 * (T_array[i] - x)**3
    t2 = c2 * (x - T_array[i-1])**3
    t3 = c3 * (T_array[i] - x)
    t4 = c4 * (x - T_array[i-1])
    return float(t1 + t2 + t3 + t4)


print("Cubic spline = " + str(f_i(27 ,4)))
