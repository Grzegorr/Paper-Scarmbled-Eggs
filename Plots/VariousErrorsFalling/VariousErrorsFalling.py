import matplotlib.pyplot as plt

iteration = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

salt_error = [1, 0.9, 0.7, 0.7, 0.5, 0.6, 0.5, 0.5, 0.45, 0.45]
mixing_error = [1, 0.9, 0.8, 0.8, 0.5,    0.4,0.45,0.5,0.3,0.4]




plt.title("Example plot only - no data here")
plt.plot(iteration, salt_error, label = "normalized salt error")
plt.plot(iteration, mixing_error, label = "normalized mixing error")
plt.ylabel("Error")
plt.xlabel("Iteration")
plt.legend(loc='upper right')
#plt.show()
plt.savefig("VariousErrorsFalling.png")
plt.clf()


