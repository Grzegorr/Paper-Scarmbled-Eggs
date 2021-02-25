import statistics
import matplotlib.pyplot as plt

#Test example - well mixed
salt = [5.65, 5.20, 6.83, 5.92, 5.63, 5.52, 5.19, 5.94, 4.98, 6.54, 6.59, 5.25, 5.50]

average = sum(salt)/len(salt)
print("Average: " + str(average))
variance = statistics.variance(salt)
print("Variance: " + str(variance))


print("#####################################################")
print("#                                                   #")
print("#   Manual tests on salt adding                     #")
print("#                                                   #")
print("#####################################################")

salt_amounts = [0, 0.3, 0.6, 0.9]

salt0 = [6.5, 7.07, 6.48, 3.32, 6.13, 5.98, 6.11, 5.66, 5.51, 5.57, 6.93, 5.79]
variance0 = statistics.variance(salt0)
mean0 = statistics.mean(salt0)

salt1 = [7, 8.42, 9.32, 9.67, 6.57, 5.48, 9.14, 8.85, 7.26]
variance1 = statistics.variance(salt1)
mean1 = statistics.mean(salt1)

salt2 = [9.08, 9.54, 8.26, 9.14, 9.36, 9.15, 10.43, 9.25, 7.58, 7.66]
variance2 = statistics.variance(salt2)
mean2 = statistics.mean(salt2)

salt3 = [12.31, 11.15, 10.85, 12.48, 10.97, 11.31, 11.4, 11.36]
variance3 = statistics.variance(salt3)
mean3 = statistics.mean(salt3)

variances = [variance0,variance1,variance2,variance3]
means = [mean0,mean1,mean2,mean3]

plt.title("Conductivity vs salt content")
plt.plot(salt_amounts, variances, label = "variances")
plt.plot(salt_amounts, means, label = "means")
plt.xlabel("Salt [g]")
plt.legend(loc='upper right')
plt.savefig("SaltContentVSConductivity_manual.png")
#plt.show()
plt.clf()


plt.title("Conductivity vs salt content")
plt.errorbar(salt_amounts, means,variances , marker = 's')
plt.xlabel("Salt [g]")
plt.ylabel("Conductivity [mS]")
plt.savefig("SaltContentVSConductivity_manual2.png")
#plt.show()
plt.clf()





print("#####################################################")
print("#                                                   #")
print("#                 Change in mixing                  #")
print("#                                                   #")
print("#####################################################")


mix_no = [1, 3, 5, 7, 11]

salt0 = [4.1, 7.69, 7.76, 7.22, 5.85, 1.56, 6.64, 761, 0.88, 1.63, 7.78, 2.04, 7.44]
variance0 = statistics.variance(salt0)
mean0 = statistics.mean(salt0)

salt1 = [7.87, 2.49, 2.36, 6.03, 4.76, 5.66, 7.45, 3.72, 6.72, 2.13, 6.47]
variance1 = statistics.variance(salt1)
mean1 = statistics.mean(salt1)

salt3 = [6.81, 3.34, 3.06, 6.79, 5.50, 3.15, 7.98, 4.96]
variance3 = statistics.variance(salt3)
mean3 = statistics.mean(salt3)

salt5 = [4.60, 6.23, 6.91, 7.01, 3.06, 4.92, 5.94, 6.90, 6.58, 6.92, ]
variance5 = statistics.variance(salt5)
mean5 = statistics.mean(salt5)

salt7 = [6.96, 5.72, 4.81, 5.46, 4.10, 5.90, 5.35, 6.69, 6.81, 6.71]
variance7 = statistics.variance(salt7)
mean7 = statistics.mean(salt7)

salt11 = [6.50, 7.07, 6.48, 3.32, 6.13, 5.98, 6.11, 5.66, 5.51, 5.61, 5.57, 6.93, 5.79]
variance11 = statistics.variance(salt11)
mean11 = statistics.mean(salt11)

variances = [variance1,variance3,variance5,variance7,variance11]
means = [mean1,mean3,mean5, mean7, mean11]

plt.title("Conductivity vs mixing")
plt.plot(mix_no, variances, label = "variances")
plt.plot(mix_no, means, label = "means")
plt.xlabel("Number of mixing seq")
plt.legend(loc='upper right')
plt.savefig("SaltContentVSMixing_manual.png")
#plt.show()
plt.clf()

plt.title("Conductivity vs mixing")
plt.errorbar(mix_no, means,variances , marker = 's')
plt.xlabel("Number of mixing seq")
plt.ylabel("Conductivity [mS]")
plt.savefig("SaltContentVSMixing_manual2.png")
#plt.show()
plt.clf()





