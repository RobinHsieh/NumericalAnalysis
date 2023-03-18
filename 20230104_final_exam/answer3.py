import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np


# 讀資料
mat_contents = sio.loadmat("cceqs.mat")
sorted(mat_contents.keys())
Tc = mat_contents['Tc'][0]
e = mat_contents['e'][0]


"""answer block ~ answer block ~ answer block"""


# 3(a.) linear regression
def regression(x, y, n):
    x_sum = 0   # the sum of x
    y_sum = 0   # the sum of y
    xy_sum = 0  # the sum of x*y
    xx_sum = 0  # the sum of x^2
    st = 0    # sum of squares of residual between y and the mean
    sr = 0    # sum of squares of residual between data y and the y calculated with the linear model
    for i in range(n):
        x_sum = x_sum + x[i]
        y_sum = y_sum + y[i]
        xy_sum = xy_sum + x[i]*y[i]
        xx_sum = xx_sum + x[i]*x[i]
    x_mean = x_sum/n  # the mean of x
    ym = y_sum/n      # the mean of y
    a1 = (n*xy_sum - x_sum*y_sum)/(n*xx_sum - x_sum*x_sum)
    a0 = ym -a1*x_mean
    for i in range(n):
        st = st + (y[i]-ym)**2.
        sr = sr + (y[i]-a0-a1*x[i])**2
    syx = (sr/(n-2))**0.5  # standard error of the estimate
    r2 = (st-sr)/st        # coefficient of determination
    r = ((st-sr)/st)**0.5  # coefficient of correlation
    return a0, a1, syx, r2, r


a0, a1, syx, r2, r = regression(Tc, e, len(Tc))

x_array = np.linspace(-30, 35, 10)
y_array = a1 * x_array + a0

plt.figure(1)
linear_legend, = plt.plot(x_array, y_array, color='red', label="Y="+str(a1)+"X+"+str(a0))
plt.scatter(Tc, e)
plt.legend(handles=[linear_legend], loc="best")
plt.title("3(a.) Vapor Pressure vs Temperature (linear)")
plt.ylabel("Vapor Pressure (Pa)")
plt.xlabel("Temperature (degree Celsius)")


print("---------------------------------------------")


# 3(b.) best of fitting

e_ln = np.log(e)    # 轉為ln


def expolin(x):
    a0_local, a1_local, syx_local, r2_local, r_local = regression(Tc, e_ln, len(Tc))
    return np.exp(a0_local + a1_local * x)  # 轉回e


a0_v2, a1_v2, syx_v2, r2_v2, r_v2 = regression(Tc, e_ln, len(Tc))

x_array = np.linspace(-30, 35, 20)
y_array = expolin(x_array)

plt.figure(2)
exponential_legend, = plt.plot(x_array, y_array, color='red', label="Y=e**(" + str(a0_v2) + "+" + str(a1_v2) + "X))")
plt.scatter(Tc, e)
plt.legend(handles=[exponential_legend], loc="best")
plt.title("3(b.) Vapor Pressure vs Temperature (exponential)")
plt.ylabel("Vapor Pressure (Pa)")
plt.xlabel("Temperature (degree Celsius)")

"""answer block ~ answer block ~ answer block"""


# 確認資料
plt.figure(3)
plt.scatter(Tc, e)
plt.title("Vapor Pressure vs Temperature")
plt.ylabel("Vapor Pressure (Pa)")
plt.xlabel("Temperature (degree Celsius)")
plt.show()
