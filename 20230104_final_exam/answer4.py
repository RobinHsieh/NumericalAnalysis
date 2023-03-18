import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, ifft


stnno, yyyymmddhh, Pressure, Rain, Temp, Wind = np.loadtxt("ground_station_data.txt",unpack="true")

# ------------------------------------------------------------

yf1 = fft(Temp)

k = 14
y1 = np.zeros(len(Temp), dtype=complex)  # 轉完的資料為complex形式
y1[0] = yf1[0]
y1[1:1 + k - 1] = yf1[1:1 + k - 1]
y1[len(Temp) - k:len(Temp)] = yf1[len(Temp) - k:len(Temp)]  #conjugate
yt1 = ifft(y1, len(Temp))

fig1 = plt.figure(figsize=(16,12))
plt.plot(Temp)
plt.plot(yt1, color="red")
plt.title("Month Temperature")
plt.ylabel("Temperature")
plt.xlabel("Data_per_hour")

# ------------------------------------------------------------

yf2 = fft(Pressure)

k = 14
y2 = np.zeros(len(Pressure), dtype=complex)  # 轉完的資料為complex形式
y2[0] = yf2[0]
y2[1:1 + k - 1] = yf2[1:1 + k - 1]
y2[len(Pressure) - k:len(Pressure)] = yf2[len(Pressure) - k:len(Pressure)]  #conjugate
yt2 = ifft(y2, len(Pressure))

fig2 = plt.figure(figsize=(16,12))
plt.plot(Pressure)
plt.plot(yt2, color="red")
plt.title("Month Pressure")
plt.ylabel("Pressure")
plt.xlabel("Data_per_hour")

# ------------------------------------------------------------

yf3 = fft(Wind)

k = 14
y3 = np.zeros(len(Wind), dtype=complex)  # 轉完的資料為complex形式
y3[0] = yf3[0]
y3[1:1 + k - 1] = yf3[1:1 + k - 1]
y3[len(Wind) - k:len(Wind)] = yf3[len(Wind) - k:len(Wind)]  #conjugate
yt3 = ifft(y3, len(Temp))

fig3 = plt.figure(figsize=(16,12))
plt.plot(Wind)
plt.plot(yt3, color="red")
plt.title("Month Wind")
plt.ylabel("Wind")
plt.xlabel("Data_per_hour")
plt.show()
