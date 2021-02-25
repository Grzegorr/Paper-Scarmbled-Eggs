import statistics
import matplotlib.pyplot as plt


mixes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
variance = [1.44, 3.86, 2.59, 2.96, 2.14, 1.33, 0.8, 0.6, 1.69, 0.5, 0.54, 0.96, 1.17, 0.59, 0.21, 0.39, 0.33, 0.55, 0.43, 0.32]

plt.title("Variance vs Mixes")
plt.plot(mixes, variance, marker = ".")
plt.xlabel("Mixes")
plt.ylabel("Variance")
plt.savefig("VarVsMixes.png")
plt.show()
plt.clf()


means = [5.88, 4.95, 4.99, 5.14, 5.2, 5.17, 5.38, 5.58, 4.91, 5, 5.05, 4.85, 5.14, 5.27, 5.63, 5.61, 5.66, 5.39, 5.43, 5.4]

plt.title("Mean vs Mixes")
plt.plot(mixes, means, marker = ".")
plt.xlabel("Mixes")
plt.ylabel("Mean")
plt.savefig("MeanVsMixes.png")
plt.show()
plt.clf()