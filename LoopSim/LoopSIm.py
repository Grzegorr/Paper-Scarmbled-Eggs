import math

def controller_iteration(mean, variance, desired_mean, desired_variance, initial_time_mill, initial_time_stop):
    salt_mean = mean
    salt_variance = variance

    # parameters:
    mixing_sequence_time = 39.0
    total_cooking_time = 1100

    no_loop = math.ceil(total_cooking_time / (initial_time_stop + mixing_sequence_time))

    #mean computation
    mean_sal_error = desired_mean - salt_mean
    P_salt_mill = 0.35 * 0.7  # 3 is actual rate, 0.7 to avoid overshoot
    next_time_mill = initial_time_mill + P_salt_mill * mean_sal_error

    #variation computation
    variance_sal_error = desired_variance/salt_variance
    extra_mix = 6.7 * math.log(variance_sal_error)
    init_mixes_no = no_loop
    next_time_stop = ((init_mixes_no + extra_mix)*(40 + initial_time_stop)/(init_mixes_no)) - 40.0

    print("Demanded values: Mean - " + str(desired_mean) + " Variance - " + str(desired_variance))

    print("Initial mill time: " + str(initial_time_mill))
    print("Initial stop time: " + str(initial_time_stop))

    print("Measured mean: " + str(salt_mean))
    print("Measured variance: " + str(salt_variance))

    print("Next mill time: " + str(next_time_mill))
    print("Next stop time: " + str(next_time_stop))
    print()
    print()

    return next_time_mill, next_time_stop

def eggs_model(time_stop, mill_time):
    mean_egg = 6 + 4 * mill_time

    mixes = math.ceil(1100 / (time_stop + 39.0))
    var_egg = 2.8 * math.exp(-0.149 * mixes) + 0.069
    return mean_egg, var_egg

def cooking_iteration(desired_mean, desired_variance, initial_time_mill, initial_time_stop):
    mean_egg, var_egg = eggs_model(initial_time_stop, initial_time_mill)
    initial_time_mill, initial_time_stop = controller_iteration(mean_egg, var_egg, desired_mean, desired_variance, initial_time_mill, initial_time_stop)
    return initial_time_mill, initial_time_stop

def the_whole_loop(desired_mean, desired_variance):
    initial_time_mill = 0
    initial_time_stop = 120
    for n in range(20):
        initial_time_mill, initial_time_stop = cooking_iteration(desired_mean, desired_variance, initial_time_mill, initial_time_stop)


#the_whole_loop(10, 1.5)
controller_iteration(8.3, 2.8, 7.87, 0.3, 0, 120)



