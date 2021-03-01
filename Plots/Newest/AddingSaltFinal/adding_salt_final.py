import statistics
import matplotlib.pyplot as plt

grams_to_time = 1.61/2.5

cooked_means = [5.55, 7.24, 8.96, 10.93, 11.96, 13.71]
cooked_variances = [0.63, 0.71, 0.93, 0.67, 1.51, 1.06]
cooked_salt_weight = list(range(len(cooked_means)))
for i in cooked_salt_weight:
    cooked_salt_weight[i] = cooked_salt_weight[i] * 0.3
#convert to salt mill
cooked_mill_time = cooked_salt_weight
for i in range(len(cooked_mill_time)):
    cooked_mill_time[i] = cooked_mill_time[i] / grams_to_time

raw_variances = [0.36, 0.45, 1.4, 0.94, 0.51, 1.23, 0.82, 0.61]
raw_means = [5.06, 7.2, 9.4, 11.3, 12.3, 14.6, 15.6, 17.22]
raw_press_time = list(range(len(raw_means)))
#print(press_time)
for i in range(len(raw_means)):
    raw_press_time[i] = raw_press_time[i] * 0.5

#plt.title("Measured Salinity vs Mill Pressing Time")
plt.errorbar(cooked_mill_time, cooked_means, cooked_variances, marker = 's', label = 'Cooked Eggs')
plt.errorbar(raw_press_time, raw_means, raw_variances, marker = 's', label = 'Raw Eggs')
plt.xlabel("Mill Pressing Time [s]")
plt.ylabel("Conductivity [mS]")
plt.legend(framealpha=1, frameon=True);
plt.savefig("AddedSaltFinal.png")
#plt.show()
plt.clf()