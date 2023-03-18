def lagrange_interpolation(x, y, order, x_evaluated):

    resolution = 0
    for i in range(order):
        term = y[i]
        for j in range(order):
            if i != j:
                term *= (x_evaluated - x[j]) / (x[i] - x[j])
        resolution += term
    return resolution


x_array = [1, 2, 3, 5, 7, 8]
f_of_x_array = [3, 6, 19, 99, 291, 444]

print("Lagrange interpolating polynomial:")
print("1 order = " + str(lagrange_interpolation(x_array, f_of_x_array, 1, 4)))
print("2 order = " + str(lagrange_interpolation(x_array, f_of_x_array, 2, 4)))
print("3 order = " + str(lagrange_interpolation(x_array, f_of_x_array, 3, 4)))
print("4 order = " + str(lagrange_interpolation(x_array, f_of_x_array, 4, 4)))