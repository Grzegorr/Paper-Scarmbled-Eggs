import statistics
import matplotlib.pyplot as plt



means = [5.55, 7.24, 8.96, 10.93, 11.96, 13.71]
variances = [0.63, 0.71, 0.93, 0.67, 1.51, 1.06]
salt_weight = list(range(len(means)))
for i in salt_weight:
    salt_weight[i] = salt_weight[i] * 0.3

plt.title("Measured Average Salinity vs Weight of Added Salt")
plt.plot(salt_weight, means, marker = ".")
plt.xlabel("Added salt [g]")
plt.ylabel("Average salinity [mS]")
plt.savefig("averageSalinity.png")
#plt.show()
plt.clf()

plt.title("Measured Variance of Salinity vs Weight of Added Salt")
plt.plot(salt_weight, variances, marker = ".")
plt.xlabel("Added salt [g]")
plt.ylabel("Salinity Variance [mS]")
plt.savefig("varianceSalinity.png")
#plt.show()
plt.clf()

plt.title("Measured Average Salinity vs Weight of Added Salt")
plt.errorbar(salt_weight, means,variances , marker = 's')
plt.xlabel("Added salt [g]")
plt.ylabel("Conductivity [mS]")
plt.savefig("CookedEggsSalinity.png")
#plt.show()
plt.clf()
