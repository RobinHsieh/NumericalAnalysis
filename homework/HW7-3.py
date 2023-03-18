def newton_interpolation(x, y, order, x_evaluated):

    p = y.copy()
    for k in range(1, order):
        for i in range(order - 1, k - 1, -1):
            p[i] = (p[i] - p[i - 1]) / (x[i] - x[i - k])
    resolution = p[order - 1]
    for i in range(order - 2, -1, -1):
        resolution = resolution * (x_evaluated - x[i]) + p[i]
    return resolution


x_array = [1, 2, 3, 5, 7, 8]
f_of_x_array = [3, 6, 19, 99, 291, 444]

print("Newton’s interpolating polynomial:")
print("1 order = " + str(newton_interpolation(x_array, f_of_x_array, 1, 4)))
print("2 order = " + str(newton_interpolation(x_array, f_of_x_array, 2, 4)))
print("3 order = " + str(newton_interpolation(x_array, f_of_x_array, 3, 4)))
print("4 order = " + str(newton_interpolation(x_array, f_of_x_array, 4, 4)))
