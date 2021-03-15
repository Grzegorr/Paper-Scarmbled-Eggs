import statistics
import matplotlib.pyplot as plt


time_mill = [0, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5 ]
salt_weight = [0.13, 0.14, 0.26, 0.42, 0.67, 0.63, 1.02, 1.31, 1.61]


plt.title("Salt Weight vs Mill Press Time")
plt.plot(time_mill, salt_weight, marker = ".")
plt.xlabel("Time mill press [s]")
plt.ylabel("Milled salt [g]")
plt.savefig("saltVsTime.png")
plt.show()
plt.clf()