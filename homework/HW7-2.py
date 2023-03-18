import matplotlib.pyplot as plt
import numpy as np


x_array = [0.4, 0.8, 1.2, 1.6, 2, 2.3]
y_array = [800, 975, 1500, 1950, 2900, 3600]
y_log_array = np.log(y_array)

# plot
fig = plt.figure()

# ---------------------------

axes1 = fig.add_subplot(211)

func1, = axes1.plot(x_array, y_array, label="before")

plt.xlabel("x", fontsize=15)
plt.ylabel("y", fontsize=15)

plt.legend(handles=[func1], loc="best")

plt.tick_params(axis="both", labelsize=12, color="red")

# ---------------------------

axes2 = fig.add_subplot(212)

func2, = axes2.plot(x_array, y_log_array, label="after")

plt.xlabel("x", fontsize=15)
plt.ylabel("y", fontsize=15)

plt.legend(handles=[func2], loc="best")

plt.tick_params(axis="both", labelsize=12, color="red")
plt.show()
