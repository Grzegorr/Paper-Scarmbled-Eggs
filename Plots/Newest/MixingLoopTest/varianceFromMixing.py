import statistics
import matplotlib.pyplot as plt
import numpy
from scipy.optimize import curve_fit


mixes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
variance = [1.44, 3.86, 2.59, 2.96, 2.14, 1.33, 0.8, 0.6, 1.69, 0.5, 0.54, 0.96, 1.17, 0.59, 0.21, 0.39, 0.33, 0.55, 0.43, 0.32]

plt.title("Variance vs Mixes")
plt.plot(mixes, variance, marker = ".")
plt.xlabel("Mixes")
plt.ylabel("Variance")
plt.savefig("VarVsMixes.png")
#plt.show()
plt.clf()


means = [5.88, 4.95, 4.99, 5.14, 5.2, 5.17, 5.38, 5.58, 4.91, 5, 5.05, 4.85, 5.14, 5.27, 5.63, 5.61, 5.66, 5.39, 5.43, 5.4]

plt.title("Mean vs Mixes")
plt.plot(mixes, means, marker = ".")
plt.xlabel("Mixes")
plt.ylabel("Mean")
plt.savefig("MeanVsMixes.png")
#plt.show()
plt.clf()


#New loop

variance = [1.85, 3.4, 2.35, 2.28, 2.22, 0.58, 1.66, 0.54, 0.81, 0.34, 0.78, 0.6, 0.39, 0.46, 0.75, 0.19, 0.21, 0.37, 0.19, 0.2, 0.25, 0.22, 0.17, 0.28, 0.23, 0.13, 0.14, 0.15, 0.15, 0.16 ]
means = [6.1, 5.59, 4.83, 4.76, 4.99, 4.84, 4.55, 4.06, 4.1, 4.59, 4.7, 4.8, 4.38, 4.71, 4.65, 5.24, 5.19, 4.84, 5.16, 5.13, 5.2, 5.17, 5.17, 5.19, 4.58, 4.82, 4.94, 5.01, 5.17, 5.2 ]
mixes = range(len(means))

plt.title("Salinity Variance vs Number of Mixes")
plt.plot(mixes, variance, marker = ".")
plt.xlabel("Mixes Number")
plt.ylabel("Salinity Variance [mS]")
plt.savefig("NewVarVsMixes.png")
#plt.show()
plt.clf()

plt.title("Salinity Mean vs Number of Mixes")
plt.plot(mixes, means, marker = ".")
plt.xlabel("Mixes Number")
plt.ylabel("Salinity Mean [mS]")
plt.ylim(0, 6.25)
plt.savefig("NewMeanVsMixes.png")
#plt.show()
plt.clf()

plt.title("Measured Salinity vs Number of Mixes")
plt.errorbar(mixes, means, variance, marker = 's')
plt.xlabel("Mixes Number")
plt.ylabel("Conductivity [mS]")
plt.savefig("NewSalinityErrorBar.png")
#plt.show()
plt.clf()


###EXPONENTIL CURVE FIT###

# define type of function to search
def model_func(x, a, k, b):
    return a * numpy.exp(-k*x) + b

x = numpy.array(mixes)
y = numpy.array(variance)
print(x)
print(y)

# curve fit
p0 = (1.,1.e-5,1.) # starting search koefs
opt, pcov = curve_fit(model_func, x, y, p0)
a, k, b = opt
# test result
x2 = numpy.linspace(0, 30, 250)
y2 = model_func(x2, a, k, b)
fig, ax = plt.subplots()
ax.plot(x2, y2, color='r', label='Fit. func: $f(x) = %.3f e^{-%.3f x} %+.3f$' % (a,k,b))
ax.plot(x, y, 'bo', label='Salinity variance measurements')
ax.legend(loc='best')
plt.xlabel("Mixes Number")
plt.ylabel("Salinity Variance [mS]")
#plt.show()
plt.savefig("NewExponentialMatch.png")


#result = numpy.polyfit(numpy.log(x), y, 1, w=numpy.sqrt(y))
# y ≈ result[0] * log(x) + result[1]
#mixes_match = range(0, 30, 0.1)
#variance_match = mixes_match.copy()
#for i in range(mixes_match):
#    variance_match[i] = result[0] * log(mixes_match[i]) + result[1]



#plt.title("Salinity Variance vs Number of Mixes")
#plt.plot(mixes, variance, marker = ".", label = "empirical data")
#plt.plot(mixes_match, variance_match, label = "exponential match")
#plt.xlabel("Mixes Number")
#plt.ylabel("Salinity Variance [mS]")
#plt.legend()
#plt.savefig("NewExponentialMach.png")
#plt.show()
#plt.clf()





