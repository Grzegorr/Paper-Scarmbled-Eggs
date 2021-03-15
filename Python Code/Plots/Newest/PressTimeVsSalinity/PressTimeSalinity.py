import matplotlib.pyplot as plt

#Pressing the salt mill for 05. second each time to see the change
#in solenity in raw eggs, mixed well by the robot

variance = [0.36, 0.45, 1.4, 0.94, 0.51, 1.23, 0.82, 0.61]
means = [5.06, 7.2, 9.4, 11.3, 12.3, 14.6, 15.6, 17.22]
press_time = list(range(len(means)))
print(press_time)
for i in range(len(means)):
    press_time[i] = press_time[i] * 0.5

plt.title("Salinity Variance vs Mill Press Time")
plt.plot(press_time, variance, marker = ".")
plt.xlabel("Time pressing salt mill [s]")
plt.ylabel("Variance of salinity [mS]")
plt.savefig("VarVsTime.png")
plt.show()
plt.clf()

plt.title("Salinity Mean vs Mill Press Time")
plt.plot(press_time, means, marker = ".")
plt.xlabel("Time pressing salt mill [s]")
plt.ylabel("Mean of salinity [mS]")
plt.savefig("MeanVsTime.png")
plt.show()
plt.clf()

plt.title("Measured Salinity vs Mill Press Time")
plt.errorbar(press_time, means,variance, marker = 's')
plt.xlabel("Time pressing salt mill [s]")
plt.ylabel("Conductivity [mS]")
plt.savefig("SalinityErrorBar.png")
#plt.show()
plt.clf()