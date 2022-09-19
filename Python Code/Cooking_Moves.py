import time
import statistics
import math
from math import pi
import numpy
import socket
import sys
import statistics
from datetime import datetime


import waypoints as wp
import kg_robot as kgr
from SalenitySensor.SalenitySensor import SolenitySensor as salt_sensor



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#                                                            Choice of a pre-programed move - uncomment one
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------


task = "Final Demo"
#task = "Average Salinity Detection"
#task = "Salt loop experiment"
#task = "Cooking concept proof"
#task = "Home Position"
#task = "Cooking Home Position"
#task = "Callibration"
#task = "First Test"
#task = "Test2"
#task = "Get L and J"
#task = "Current Workspace"
#task = "Current Workspace2"
#task = "Stirring Presentation"
#task = "Scrape Eggs"
#task = "Set Mixing Procedure"
#task = "Single Salinity Test"
#task = "Add Salt"


def main():
    print("------------Configuring Burt-------------\r\n")
    robot = kgr.kg_robot(port=30010,db_host="169.254.114.206")
    print("----------------Hi Burt!-----------------\r\n\r\n")

    SALT = salt_sensor(70)

    if task == "Final Demo":
        print("Task: " + task)
        desired_mean = 10.2
        desired_variance = 0.7
        #standard initaial conditions
        #initial_time_mill = 0
        #initial_time_stop = 120
        initial_time_mill = 1.5
        initial_time_stop = 5
        cooking_loop(robot, SALT, desired_mean, desired_variance, initial_time_stop, initial_time_mill, if_cook ="True", if_test="True")

    if task == "Average Salinity Detection":
        print("Task: " + task)
        for d in range(12):
            salt_testing_loop(robot, SALT)


    if task == "Salt loop experiment":
        print("Task: " + task)
        desired_salt = 15
        salt_loop(robot, SALT, desired_salt)

    if task == "Cooking concept proof":
        print("Task: " + task)
        target_var = 0.1
        #initial mixing
        ###################standard_mix_procedure(robot, 10)
        mixing_loop(robot, SALT,target_var)
        exit()

        #add salt
        add_salt(robot, 0)
        #move to hot hob
        move_cold_to_hot(robot)
        #cooking moves
        standard_scrambling_procedure(robot, 10)
        #move to cold hob to cool down
        move_hot_to_cold(robot)

    if task == "Add Salt":
        print("Task: " + task)
        add_salt(robot, 0)
        add_salt(robot, 0.5)
        add_salt(robot, 1)

    if task == "Current Workspace":
        print("Task: " + task)
        SALT.resetData()
        for i in range(25):
            robot.translatel_rel([0, 0, 0.002, 0, 0, 0], vel = 0.1)
            robot.translatel_rel([0, 0, 0.01, 0, 0, 0])
            robot.translatel_rel([-0.005,0,0,0,0,0])
            robot.translatel_rel([0, 0, -0.01, 0, 0, 0])
            robot.translatel_rel([0, 0, -0.002, 0, 0, 0], vel = 0.1)
            SALT.getNextReading()
        data = SALT.returnData()
        print(data)

    if task == "Current Workspace2":
        print("Task: " + task)
        data = mass_salinity_test(robot,SALT)
        print(data)

    if task == "First Test":
        print("Task: " + task)
        robot.home()
        time.sleep(1)
        robot.translatel_rel([0, 0, 0.1])
        time.sleep(1)

    if task == "Test2":
        print("Task: " + task)
        robot.home()
        print(robot.getj())

    if task == "Get L and J":
        print("Task: " + task)
        print("J:")
        print(robot.getj())
        print("L:")
        print(robot.getl())

    if task == "Stirring Presentation":
        print("Task: " + task)
        move_to_mixing_home(robot)
        for i in range(1000):
            for angle in [0, 20, 40, 60, 80, 100, 120, 140, 160]:
                fold_eggs(robot, 0.13, angle, 0.07)
            for k in range(1):
                zigzag_stir_mix(robot,0.13,0.11)
            for j in range(1):
                move_to_mixing_home(robot)
                stir_circle_relative(robot, 0.1, 0.13, 0.001, 0.30, 1.5)

    if task == "Zigzag Presentation":
        print("Task: " + task)
        for i in range(1000):
            move_to_mixing_home(robot)
            stir_circle_relative(robot, 0.1, 0.13, 0.001, 0.30, 1.5)

    if task == "Scrape Eggs":
        print("Task: " + task)
        move_to_home(robot)
        for angle in [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
            fold_eggs(robot, 0.05, angle, 0.1)

    if task == "Set Mixing Procedure":
        print("Task: " + task)
        sequence_no = 1
        standard_mix_procedure(robot, sequence_no)

    if task == "Single Salinity Test":
        print("Task: " + task)
        data = mass_salinity_test(robot,SALT)
        data = numpy.array(data)
        print()
        print("Salinity Test")
        print("Data: " + str(list(data)))
        print("Mean: " + str(statistics.mean(data)))
        print("Variance: " + str(statistics.variance(data)))

time.sleep(3)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#                                                      Functions For Movement
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

def move_to_cooking_home(robot):
    robot.movel(wp.cooking_home_l)
    print("Move: Cooking Home")

def move_to_mixing_home(robot):
    robot.movel(wp.mixing_home_l)
    print("Move: Mixing Home")

def move_to_mixing_sensor_down_home(robot):
    robot.movel(wp.mixing_sensor_down_home_l)
    print("Move: Sensor Down")

def move_to_home(robot):
    robot.movel(wp.robot_home_l)
    print("Move: Home")

#lower left hob
def move_to_scrambling_home(robot):
    robot.movel(wp.scrambling_home_l)
    print("Move  Home")

def move_cold_to_hot(robot):
    move_to_mixing_home(robot)
    robot.movel_tool([0, 0, 0.13, 0, 0, 0])
    robot.translatel_rel([0, 0.33, 0, 0, 0, 0], vel=0.1)
    move_to_scrambling_home(robot)

def move_hot_to_cold(robot):
    move_to_scrambling_home(robot)
    robot.movel_tool([0, 0, 0.13, 0, 0, 0])
    robot.translatel_rel([0, -0.33, 0, 0, 0, 0], vel=0.1)
    move_to_mixing_home(robot)

def cooking_loop(robot, SALT, desired_mean, desired_variance, initial_time_stop, initial_time_mill, if_cook, if_test):
    # Heat used = 6
    mixing_sequence_time = 39.0
    # parameters:
    total_cooking_time = 1150
    time_salt = initial_time_mill
    # time_stop = 21
    time_stop = initial_time_stop
    no_loop = math.ceil(total_cooking_time / (time_stop + mixing_sequence_time))

    if if_cook == "True":
        # start at lower left hob
        move_to_scrambling_home(robot)  # yes, the names are switched
        #time.sleep(20)
        #cut_yolks(robot)
        move_hot_to_cold(robot)  # yes its another way around
        add_salt(robot, time_salt)

        # now cook
        for n in range(no_loop):
            now = datetime.now().time()  # time object
            print("now =", now)
            standard_mix_procedure(robot, 1)
            time.sleep(time_stop)

        move_cold_to_hot(robot)  # yes, its opposite then name

    if if_test == "True":
        input("Ready for testing part? Switch off thee hob, cool down the eggs and place eggs on 'hot' hob.")

        #Salt Measurements with robotic arm
        data = mass_salinity_test(robot, SALT)  # data is a list of measurements stored as floats
        salt_mean = statistics.mean(data)       # mean - number of salt indication
        salt_variance = statistics.variance(data)       # variance - measure of mixing

        #next parameters computation - salt
        mean_sal_error = desired_mean - salt_mean       # error for p controller for salt
        P_salt_mill = 0.35 * 0.8  # 0.35 is actual rate of adding salinity per second, 0.8 to avoid overshoot, should then not overshoot by safty margin of 0.2
        next_time_mill = initial_time_mill + P_salt_mill * mean_sal_error  # P controller adjusting time of pressing the mill

        # next parameters computation - mixing
        # The robot cooks for a given time by erforming mixing sequence(40 sec duration) and then stopping for a stop_time
        variance_sal_error = desired_variance/salt_variance     # an error by not linear - its how many time the variance is bigger than average
        extra_mix = 6.7 * math.log(variance_sal_error)      # 6.7 is time contsnt from mixes vs variance on raw eggs exponent matching (1/0.149)
        init_mixes_no = no_loop     # bad code reassignment, no of mixing sequences robot did during cooking
        next_time_stop = ((init_mixes_no + extra_mix)*(40 + initial_time_stop)/(init_mixes_no)) - 40.0  # now its translating new number of mixes into stop time before mixing

        print("Demanded values: Mean - " + str(desired_mean) + " Variance - " + str(desired_variance))

        print("Initial mill time: " + str(initial_time_mill))
        print("Initial stop time: " + str(initial_time_stop))

        print("Measured mean: " + str(salt_mean))
        print("Measured variance: " + str(salt_variance))

        print("Next mill time: " + str(next_time_mill))
        print("Next stop time: " + str(next_time_stop))

        return next_time_mill, next_time_stop


def salt_loop(robot, SALT, desired_salt):
    allowed_iteratons = 3
    gramsPerTime = 1.6/2.5
    conductTimesEggNoPerSalt = 3*5/0.9
    no_eggs = 3
    constant = 0.7
    P = constant / (conductTimesEggNoPerSalt / no_eggs *gramsPerTime)

    for i in range(allowed_iteratons):
        #sample salt
        data = salinity_test(robot, SALT)
        #compute error
        variance = statistics.variance(data)
        mean = statistics.mean(data)
        error = desired_salt - mean
        mill_time = error * P

        #printout
        print()
        print("****Salinity Loop printout****")
        print("data: " + str(data))
        print("mean: " + str(mean))
        print("variance: " + str(variance))
        print("error: " + str(error))
        print("mill_time: " + str(mill_time))
        print()

        #add salt
        add_salt(robot, mill_time)
        #mix
        standard_mix_procedure(robot,1)

    data = salinity_test(robot, SALT)
    # compute error
    variance = statistics.variance(data)
    mean = statistics.mean(data)
    error = desired_salt - mean
    mill_time = error * P

    # printout
    print()
    print("****Salinity Loop printout****")
    print("data: " + str(data))
    print("mean: " + str(mean))
    print("variance: " + str(variance))
    print("error: " + str(error))
    print("mill_time: " + str(mill_time))
    print()

def salt_testing_loop(robot, SALT):
    data = mass_salinity_test(robot, SALT)
    # compute stats
    variance = statistics.variance(data)
    mean = statistics.mean(data)

    # printout
    print()
    print("****Average Salt Printout****")
    print("data: " + str(data))
    print("mean: " + str(mean))
    print("variance: " + str(variance))
    print()

    add_salt(robot, 0.5)

    standard_mix_procedure(robot, 10)

def mixing_loop(robot, SALT, target_variance):
    variance = 99999
    # sample salt
    data = mass_salinity_test(robot, SALT)
    # compute stats
    variance = statistics.variance(data)
    mean = statistics.mean(data)

    # printout
    print()
    print("****Mixing Loop Printout****")
    print("data: " + str(data))
    print("mean: " + str(mean))
    print("variance: " + str(variance))
    print()


    while(variance > target_variance):
        # Mix
        standard_mix_procedure(robot, 1)
        # sample salt
        data = mass_salinity_test(robot, SALT)
        # compute stats
        variance = statistics.variance(data)
        mean = statistics.mean(data)

        # printout
        print()
        print("****Mixing Loop Printout****")
        print("data: " + str(data))
        print("mean: " + str(mean))
        print("variance: " + str(variance))
        print()

def mixing_loop_P(robot, SALT, target_variance):
    #Starting sequence of the loop
    variance = 99999
    P = -3
    # sample salt
    data = salinity_test(robot, SALT)
    # compute stats
    variance = statistics.variance(data)
    mean = statistics.mean(data)
    error = target_variance - variance
    mixing_times = P * error
    mixing_times = math.ceil(mixing_times)

    # printout
    print()
    print("****Proportional Mixing Loop Printout****")
    print("data: " + str(data))
    print("mean: " + str(mean))
    print("variance: " + str(variance))
    print()

    while (variance > target_variance):

        # Mix
        standard_mix_procedure(robot,mixing_times)
        # sample salt
        data = salinity_test(robot, SALT)
        # compute stats
        variance = statistics.variance(data)
        mean = statistics.mean(data)
        error = target_variance - variance
        mixing_times = P * error
        mixing_times = math.ceil(mixing_times)

        # printout
        print()
        print("****Proportional Mixing Loop Printout****")
        print("data: " + str(data))
        print("mean: " + str(mean))
        print("error: " + str(error))
        print("mixing_times: " + str(mixing_times))
        print("variance: " + str(variance))
        print()

def zigzag_stir_mix(robot, h, r):
    #start from cooking home
    robot.movel(wp.mixing_home_l)

    robot.movel_tool([0.25*r, 0.25*r, 0, 0, 0, 0])
    robot.movel_tool([0, 0, h*0.9, 0, 0, 0])
    robot.movel_tool([0.25*r, 0.25*r, 0, 0, 0, 0])
    robot.movel_tool([0, 0, h*0.1, 0, 0, 0])

    robot.movel_tool([-r, 0, 0, 0, 0, 0])
    robot.movel_tool([r, -0.25 * r, 0, 0, 0, 0])
    robot.movel_tool([-r, 0, 0, 0, 0, 0])
    robot.movel_tool([r, -0.25 * r, 0, 0, 0, 0])
    robot.movel_tool([-r, 0, 0, 0, 0, 0])
    robot.movel_tool([r, -0.25 * r, 0, 0, 0, 0])
    robot.movel_tool([-r, 0, 0, 0, 0, 0])
    robot.movel_tool([r, -0.25 * r, 0, 0, 0, 0])

    robot.movel_tool([0, r, 0, 0, 0, 0])
    robot.movel_tool([-0.25 * r, -r, 0, 0, 0, 0])
    robot.movel_tool([0, r, 0, 0, 0, 0])
    robot.movel_tool([-0.25 * r, -r, 0, 0, 0, 0])
    robot.movel_tool([0, r, 0, 0, 0, 0])
    robot.movel_tool([-0.25 * r, -r, 0, 0, 0, 0])
    robot.movel_tool([0, r, 0, 0, 0, 0])
    robot.movel_tool([-0.25 * r, -r, 0, 0, 0, 0])

    robot.movel_tool([0.5 * r, 0.5 * r, 0, 0, 0, 0]) #back to the middle
    robot.movel_tool([0, 0, -h, 0, 0, 0])
    robot.movel(wp.mixing_home_l)

def zigzag_stir_scramble(robot, h, r):
    #start from cooking home
    robot.movel(wp.scrambling_home_l)

    robot.movel_tool([0.5*r, 0.5*r, 0, 0, 0, 0])
    robot.movel_tool([0, 0, h, 0, 0, 0])

    robot.movel_tool([-r, 0, 0, 0, 0, 0])
    robot.movel_tool([r, -0.25 * r, 0, 0, 0, 0])
    robot.movel_tool([-r, 0, 0, 0, 0, 0])
    robot.movel_tool([r, -0.25 * r, 0, 0, 0, 0])
    robot.movel_tool([-r, 0, 0, 0, 0, 0])
    robot.movel_tool([r, -0.25 * r, 0, 0, 0, 0])
    robot.movel_tool([-r, 0, 0, 0, 0, 0])
    robot.movel_tool([r, -0.25 * r, 0, 0, 0, 0])

    robot.movel_tool([0, r, 0, 0, 0, 0])
    robot.movel_tool([-0.25 * r, -r, 0, 0, 0, 0])
    robot.movel_tool([0, r, 0, 0, 0, 0])
    robot.movel_tool([-0.25 * r, -r, 0, 0, 0, 0])
    robot.movel_tool([0, r, 0, 0, 0, 0])
    robot.movel_tool([-0.25 * r, -r, 0, 0, 0, 0])
    robot.movel_tool([0, r, 0, 0, 0, 0])
    robot.movel_tool([-0.25 * r, -r, 0, 0, 0, 0])

    robot.movel_tool([0.5 * r, 0.5 * r, 0, 0, 0, 0]) #back to the middle
    robot.movel_tool([0, 0, -h, 0, 0, 0])
    robot.movel(wp.scrambling_home_l)

def add_salt(robot, time_salt_mill):
    move_to_mixing_home(robot)
    robot.movel_tool([0, 0, 0.13, 0, 0, 0])
    robot.translatel_rel([0, 0.05, 0, 0, 0, 0], vel=0.1)
    robot.translatel_rel([-0.43, 0, 0, 0, 0, 0], vel=0.1)
    ##Now the pan is under salt
    robot.translatel_rel([0, 0.005, 0.147, 0, 0, 0], vel=0.1)
    robot.movej_rel([0, 0, 0, 0, 1.57, 0])
    robot.movej_rel([0.05, -0.147, 0, 0, 0, 0])
    robot.movej_rel([0, 0, -0.04, 0, 0, 0])
    time.sleep(time_salt_mill)

    robot.movej_rel([0, 0, 0.04, 0, 0, 0])
    robot.movej_rel([-0.05, 0.147, 0, 0, 0, 0])
    robot.movej_rel([0, 0, 0, 0, -1.57, 0])
    robot.translatel_rel([0, -0.005, -0.1, 0, 0, 0], vel=0.1)
    robot.translatel_rel([0.05, 0, 0, 0, 0, 0], vel=0.1)
    robot.translatel_rel([0, 0, -0.04, 0, 0, 0], vel=0.1)
    robot.translatel_rel([0.45, 0, 0, 0, 0, 0], vel=0.1)
    robot.translatel_rel([0, -0.1, 0, 0, 0, 0], vel=0.1)
    move_to_mixing_home(robot)

def standard_mix_procedure(robot, no_times):
    zigzag_no = 1
    stir_no = 1

    move_to_mixing_home(robot)
    for i in range(no_times):
#        for angle in [0, 20, 40, 60, 80, 100, 120, 140, 160]:
#            fold_eggs(robot, 0.133, angle, 0.08)
        for k in range(zigzag_no):
            zigzag_stir_mix(robot, h=0.13, r=0.122)
        for j in range(stir_no):
            move_to_mixing_home(robot)
            stir_circle_relative(robot, radius=0.09, height=0.128,  move_radius=0.001, move_vel=0.30, move_acc=1.5)
            move_to_mixing_home(robot)

def cut_yolks(robot):
    for angle in [0,10, 20, 30, 40, 50,  60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]:
        fold_eggs(robot, 0.133, angle, 0.085)

def standard_scrambling_procedure(robot, no_times):
    zigzag_no = 3
    stir_no = 1

    move_to_scrambling_home(robot)
    for i in range(no_times):
        for angle in [0, 20, 40, 60, 80, 100, 120, 140, 160]:
            fold_eggs(robot, 0.135, angle, 0.08)
        for k in range(zigzag_no):
            zigzag_stir_scramble(robot, 0.135, 0.11)
        for j in range(stir_no):
            move_to_scrambling_home(robot)
            stir_circle_relative(robot, 0.1, 0.135, 0.001, 0.30, 1.5)

def salinity_test(robot, SALT):
    move_to_mixing_home(robot)
    SALT.resetData()
    # h1 - down to work
    # h2 - down to pan
    # h3 - down to test eggs
    # h4 - dip into water
    # h5 - up to brush
    h1 = 0.32
    h2 = 0.0995
    h3 = 0.02
    h4 = 0.062
    h5 = 0.22

    offsets = [
        [-0.05, -0.05], [-0.05, -0.03], [-0.05, 0], [-0.05, 0.03], [-0.05, 0.05],
        [-0.03, -0.05], [-0.03, -0.03], [-0.03, 0], [-0.03, 0.03], [-0.03, 0.05],
        [0, -0.05], [0, -0.03], [0, 0], [0, 0.03], [0, 0.05],
        [0.03, -0.05], [0.03, -0.03], [0.03, 0], [0.03, 0.03], [0.03, 0.05],
        [0.05, -0.05], [0.05, -0.03], [0.05, 0], [0.05, 0.03], [0.05, 0.05]
    ]

    move_to_mixing_home(robot)
    robot.movej_rel([0, 0, 0, 0, 3.14, 0])
    # go down to work area
    robot.movel_tool([0, 0, -h1, 0, 0, 0])

    for offset in offsets:
        # test sequence start
        robot.movel_tool([0, 0, -h2, 0, 0, 0])
        robot.movel_tool([offset[0], offset[1], 0, 0, 0, 0])
        robot.movel_tool([0, 0, -h3, 0, 0, 0])
        time.sleep(3)
        SALT.getNextReading()
        robot.movel_tool([0, 0, h3, 0, 0, 0])
        robot.movel_tool([-offset[0], -offset[1], 0, 0, 0, 0])
        robot.movel_tool([0, 0, h2, 0, 0, 0])
        #brush
        robot.movel_tool([0, 0, h5, 0, 0, 0])
        robot.translatel_rel([0.05, -0.22, 0, 0, 0, 0])
        robot.translatel_rel([-0.05, 0.22, 0, 0, 0, 0])
        robot.movel_tool([0, 0, -h5, 0, 0, 0])

#    #that was the water immersion
#    robot.translatel_rel([0.37, 0, 0, 0, 0, 0])
#    robot.movel_tool([0, 0, -h4, 0, 0, 0])
#    time.sleep(1.5)
#    robot.movel_tool([0, 0, h4, 0, 0, 0])
#    robot.movel_tool([0, 0, -h4, 0, 0, 0])
#    time.sleep(1.5)
#    robot.movel_tool([0, 0, h4, 0, 0, 0])
#    robot.movel_tool([0, 0, -h4, 0, 0, 0])
#    time.sleep(1.5)
#    robot.movel_tool([0, 0, h4, 0, 0, 0])
#    robot.movej_rel([0, 0, 0, 0, 1, 0])
#    robot.movej_rel([0, 0, 0, 0, -1, 0])
#    robot.translatel_rel([-0.37, 0, 0, 0, 0, 0])
#
    robot.movel_tool([0, 0, h2, 0, 0, 0])
    robot.movel_tool([0, 0, h1, 0, 0, 0])
    robot.movej_rel([0, 0, 0, 0, -3.14, 0])
    data = SALT.returnData()
    #print(data)
    move_to_mixing_home(robot)
    return data

def mass_salinity_test(robot, SALT):
    move_to_mixing_home(robot)
    SALT.resetData()
    # h1 - down to work
    # h2 - down to pan
    # h3 - down to test eggs
    # h4 - dip into water
    # h5 - up to brush
    h1 = 0.32
    h2 = 0.0945
    h3 = 0.015
    h4 = 0.062
    h5 = 0.22

    offsets = [
        #[0.05, 0.05]
        [-0.06, -0.05], [-0.04, -0.05], [-0.02, -0.05], [0, -0.05], [0.02, -0.05], [0.04, -0.05], [0.06, -0.05]
    ]

    move_to_mixing_home(robot)
    robot.movej_rel([0, 0, 0, 0, 3.14, 0])
    # go down to work area
    #input("Syopped")
    robot.movel_tool([0, 0, -h1, 0, 0, 0], acc = 0.2)

    for offset in offsets:
        # test sequence start
        robot.movel_tool([0, 0, -h2, 0, 0, 0], acc = 0.2)
        robot.movel_tool([offset[0], offset[1], 0, 0, 0, 0], acc = 0.2)
        robot.movel_tool([0, 0, -h3, 0, 0, 0], acc = 0.2)
        #########
        time.sleep(1)
        for i in range(10):
            SALT.getNextReading()
            robot.translatel_rel([0, 0, 0.01, 0, 0, 0])
            robot.movel_tool([0, abs(offset[1])/9.0, 0, 0, 0, 0])
            robot.translatel_rel([0, 0, -0.01, 0, 0, 0])

        #########
        robot.movel_tool([0, 0, h3, 0, 0, 0], acc = 0.2)
        robot.movel_tool([0, -2 * 5.0 / 9.0 * abs(offset[1]), 0, 0, 0, 0], acc = 0.2)
        robot.movel_tool([-offset[0], -offset[1], 0, 0, 0, 0], acc = 0.2)
        robot.movel_tool([0, 0, h2, 0, 0, 0], acc = 0.2)
        # brush
        robot.movel_tool([0, 0, h5, 0, 0, 0], acc = 0.2)
        robot.translatel_rel([0.05, -0.22, 0, 0, 0, 0])
        robot.translatel_rel([-0.05, 0.22, 0, 0, 0, 0])
        move_to_mixing_sensor_down_home(robot)
        robot.movel_tool([0, 0, -h1, 0, 0, 0])

    robot.movel_tool([0, 0, h2, 0, 0, 0], acc = 0.2)
    robot.movel_tool([0, 0, h1, 0, 0, 0], acc = 0.2)
    robot.movej_rel([0, 0, 0, 0, -3.14, 0])
    data = SALT.returnData()
    # print(data)
    move_to_mixing_home(robot)
    return data

#stirring home must in the middle of the circle, spatula edge along x direction
def stir_circle_relative(robot, radius, height, move_radius, move_vel, move_acc):

    #Take care of the robot wrist angle
    for k  in range(4):
        joints = robot.getj()
        if joints[5] > 0:
            robot.movel_tool([0,0,0,0,0,-3.14])
        if joints[5] < -3.14:
            robot.movel_tool([0,0,0,0,0,0.5*3.14])



    # get current positionfor a center of a circle
    stirring_home = robot.getl()

    #iterate over 18 angles along te circle
    for angle_number in range(18):
        if angle_number == 0:
            print("Move: Starting Point on Circle")
            robot.translatel_rel([0, 0, -height * 0.9, 0, 0, 0])
            #angle to radians
            angle = (2*3.14) * (angle_number/16)

            #convoluted way to move to first point - could be improved greatly
            x = radius * numpy.cos(angle)
            y = radius * numpy.sin(angle)
            new_pose = [sum(x) for x in zip(stirring_home, [x,y,-height * 0.9,0,0,0])]#its element wise addition
            robot.movel(new_pose)

            #Move toward inner part of circle
            #robot.movel_tool([0, 0, 0, 0, 0, 2 * 3.14 / 36])

            #tool down
            robot.translatel_rel([0, 0, -height*0.1, 0, 0, 0])
        else:
            #previous_angle = (2 * 3.14) * ((angle_number-1) / 18)
            #previous_x = radius * numpy.cos(previous_angle)
            #previous_y = radius * numpy.sin(previous_angle)
            #print("previous_x" + str(previous_x))
            #print("previous_y" + str(previous_y))
            #angle = (2 * 3.14) * (angle_number / 18)
            #x = radius * numpy.cos(angle)
            #y = radius * numpy.sin(angle)
            #print("x: " + str(x))
            #print("y: " + str(y))
            #x_diff = x - previous_x
            #y_diff = y - previous_y
            #print("x_diff: " + str(x_diff))
            #print("y_diff: " + str(y_diff))
            robot.movel_tool([0, 0.31*radius, 0, 0.0007, 0, 2 * 3.14 / 16], vel = move_vel, acc = move_acc, radius = move_radius)
            #print(previous_angle - angle)
            #print()

    #lift the tool up
    robot.translatel_rel([0, 0, height, 0, 0, 0])

    joints = robot.getj()
    if joints[5] > 0:
        robot.movel_tool([0, 0, 0, 0, 0, -3.14])

#starting position is in th middle of the pan above by h
#r is how far from the middle the spatula comes down
def fold_eggs(robot,h, angle_deg, r):

    # Take care of the robot wrist angle
    joints = robot.getj()
    if joints[5] > 0:
        robot.movel_tool([0, 0, 0, 0, 0, -3.14])
    joints = robot.getj()
    if joints[5] > 0:
        robot.movel_tool([0, 0, 0, 0, 0, -3.14])

    #convert angle to radians
    angle_rad = angle_deg * 2 * 3.14 / 360.0

    robot.movel_tool([0, 0, 0, 0, 0, angle_rad])
    robot.movel_tool([r, 0, 0, 0, 0, 0])
    robot.movel_tool([0, 0, h, 0, 0, 0])
    robot.movel_tool([-2*r, 0, 0, 0, 0, 0])
    robot.movel_tool([0, 0, -h, 0, 0, 0])
    robot.movel_tool([r, 0, 0, 0, 0, 0])
    robot.movel_tool([0, 0, 0, 0, 0, -angle_rad])


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#                                                                   Old Functions
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#two options for the tool are "Spatula" and "Gripper"
#Its relative rotation so make sure you have the other tool in operation at the moment
def tool_to_use(robot, tool):
    if tool == "Gripper":
        robot.movej_rel([0, 0, 0, 0, 3.14, 0])
    if tool == "Spatula":
        robot.movej_rel([0, 0, 0, 0, -3.14, 0])

def pan_left_to_heat(robot):
    move_to_cooking_home(robot)
    #move behind the pan
    robot.translatel_rel([0.4, 0.2, -0.1, 0, 0, 0])
    #press pan against a wall
    robot.translatel_rel([0, -0.2, 0, 0, 0, 0])
    #Here the magnet should be turned on
    #Pull backfrom the wall
    robot.translatel_rel([0, 0.1, 0, 0, 0, 0])
    #Drag to heat
    robot.translatel_rel([-0.3, 0, 0, 0, 0, 0])
    #Here the magnet should be switched of
    #Go back
    robot.translatel_rel([0, 0.1, 0, 0, 0, 0])
    #Go home
    move_to_cooking_home(robot)

def pan_left_to_right(robot):
    #start from home
    move_to_cooking_home(robot)
    #input("Go to next step?")
    # move behind the pan
    robot.translatel_rel([0.2, 0.22, -0.1, 0, 0, 0])
    robot.translatel_rel([0, -0.09, -0.08, 0, 0, 0])
    robot.translatel_rel([-0.35, 0, 0, 0, 0, 0])
    robot.translatel_rel([0, 0, 0, 0, 0, 0.2])
    move_to_cooking_home(robot)

def callibration_pan_gripper(robot):
    move_to_home(robot)
    robot.translatel_rel([0.65, 0.1, -0.15, 0, 0, 0])
    robot.movel(wp.callibrate_left)
    input("Move to next calibration point?")
    robot.translatel_rel([0, 0, 0.3, 0, 0, 0])
    move_to_home(robot)
    robot.translatel_rel([-0.4, 0.1, -0.15, 0, 0, 0])
    robot.movel(wp.callibrate_right)
    input("Move to home?")
    robot.translatel_rel([0, 0, 0.3, 0, 0, 0])
    move_to_home(robot)



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#                                                                   Main
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__': main()









