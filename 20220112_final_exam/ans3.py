from os.path import dirname, join as pjoin
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np


def regression(x,y,n):
    x_sum = 0  # the sum of x
    y_sum = 0  # the sum of y
    xy_sum = 0 # the sum of x*y
    xx_sum = 0 # the sum of x^2
    st = 0    # sum of squares of residual between y and the mean
    sr = 0    # sum of squares of residual between data y and the y calculated with the linear model
    for i in range(n):
        x_sum = x_sum + x[i]
        y_sum = y_sum + y[i]
        xy_sum = xy_sum +x[i]*y[i]
        xx_sum = xx_sum +x[i]*x[i]
    x_mean = x_sum/n # the mean of x
    ym = y_sum/n # the mean of y
    #print(ym)
    a1 = (n*xy_sum - x_sum*y_sum)/(n*xx_sum - x_sum*x_sum)
    a0 = ym -a1*x_mean
    for i in range(n):
        st = st + (y[i]-ym)**2.
        sr = sr + (y[i]-a0-a1*x[i])**2
    #print(sr)
    #print(n)
    syx = (sr/(n-2))**0.5 #standard error of the estimate
    r2 = (st-sr)/st       #coefficient of determination
    r = ((st-sr)/st)**0.5 #coefficient of correlation
    return a0, a1, syx, r2, r



#讀資料
mat_contents = sio.loadmat(r"../chi_yangs_final_exam/cceqs.mat")
sorted(mat_contents.keys())
#print(mat_contents)
Tc = mat_contents['Tc'][0]
e = mat_contents['e'][0]

print(Tc)

a0, a1, syx, r2, r = regression(Tc, e, len(Tc))

x_array = np.linspace(-30, 35, 10)
y_array = a1 * x_array + a0

plt.plot(x_array, y_array)
print(a0, a1, syx, r2, r)



#確認資料

plt.scatter(Tc,e)
plt.title("Vapor Pressure vs Temperature")
plt.ylabel("Vapor Pressure (Pa)")
plt.xlabel("Temperature (degree Celsius)")
plt.show()

