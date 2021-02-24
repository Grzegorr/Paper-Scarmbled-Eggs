import time
import statistics
import serial
from math import pi
import numpy
import socket
import sys


import waypoints as wp
import kg_robot as kgr
from SalenitySensor.SalenitySensor import SolenitySensor as salt_sensor



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#                                                            Choice of a pre-programed move - uncomment one
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------


#task = "Salt loop experiment"
task = "Cooking concept proof"
#task = "Home Position"
#task = "Cooking Home Position"
#task = "Callibration"
#task = "First Test"
#task = "Test2"
#task = "Get L and J"
#task = "Current Workspace"
#task = "Stirring Presentation"
#task = "Scrape Eggs"
#task = "Set Mixing Procedure"
#task = "Single Salenity Test"
#task = "Add Salt"


def main():
    print("------------Configuring Burt-------------\r\n")
    robot = kgr.kg_robot(port=30010,db_host="169.254.250.80")
    #robot = kgr.kg_robot(port=30010,ee_port="COM32",db_host="192.168.1.50")
    print("----------------Hi Burt!-----------------\r\n\r\n")

    SALT = salt_sensor(25)

    if task == "Salt loop experiment":
        print("Task: " + task)
        desired_salt = 15
        salt_loop(robot, SALT, desired_salt)

    if task == "Cooking concept proof":
        print("Task: " + task)
        target_var = 1
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
        add_salt(robot, 2.5)

    if task == "Home Position":
        print("Task: " + task)
        move_to_home(robot)

    if task == "Cooking Home Position":
        print("Task: " + task)
        move_to_cooking_home(robot)

    if task == "Callibration":
        print("Task: " + task)
        callibration_pan_gripper(robot)

    if task == "Current Workspace":
        print("Task: " + task)
        move_hot_to_cold(robot)
        move_cold_to_hot(robot)

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

    if task == "Single Salenity Test":
        print("Task: " + task)
        salinity_test(robot,SALT)

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

def mixing_loop(robot, SALT, target_variance):
    variance = 99999
#    # sample salt
#    data = salinity_test(robot, SALT)
#    # compute stats
#    variance = statistics.variance(data)
#    mean = statistics.mean(data)
#
#    # printout
#    print()
#    print("****Mixing Loop Printout****")
#    print("data: " + str(data))
#    print("mean: " + str(mean))
#    print("variance: " + str(variance))
#    print()


    while(variance > target_variance):
        # Mix
        standard_mix_procedure(robot, 2)
        # sample salt
        data = salinity_test(robot, SALT)
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

def zigzag_stir_mix(robot, h, r):
    #start from cooking home
    robot.movel(wp.mixing_home_l)

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
    robot.movel_tool([0, 0, 0.133, 0, 0, 0])
    robot.translatel_rel([0, 0.05, 0, 0, 0, 0], vel=0.1)
    robot.translatel_rel([-0.43, 0, 0, 0, 0, 0], vel=0.1)
    ##Now the pan is under salt
    robot.translatel_rel([0, 0.005, 0.15, 0, 0, 0], vel=0.1)
    robot.movej_rel([0, 0, 0, 0, 1.57, 0])
    robot.movej_rel([0.05, -0.15, 0, 0, 0, 0])
    robot.movej_rel([0, 0, -0.06, 0, 0, 0])
    time.sleep(time_salt_mill)

    robot.movej_rel([0, 0, 0.04, 0, 0, 0])
    robot.movej_rel([-0.05, 0.15, 0, 0, 0, 0])
    robot.movej_rel([0, 0, 0, 0, -1.57, 0])
    robot.translatel_rel([0, -0.005, -0.15, 0, 0, 0], vel=0.1)
    robot.translatel_rel([0.53, 0, 0, 0, 0, 0], vel=0.1)
    robot.translatel_rel([0, -0.1, 0, 0, 0, 0], vel=0.1)
    move_to_mixing_home(robot)

def standard_mix_procedure(robot, no_times):
    zigzag_no = 3
    stir_no = 1

    move_to_mixing_home(robot)
    for i in range(no_times):
#        for angle in [0, 20, 40, 60, 80, 100, 120, 140, 160]:
#            fold_eggs(robot, 0.133, angle, 0.08)
        for k in range(zigzag_no):
            zigzag_stir_mix(robot, 0.133, 0.11)
        for j in range(stir_no):
            move_to_mixing_home(robot)
            stir_circle_relative(robot, 0.1, 0.133, 0.001, 0.30, 1.5)
            move_to_mixing_home(robot)

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
    h1 = 0.32
    h2 = 0.0995
    h3 = 0.02
    h4 = 0.062

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

    robot.translatel_rel([0.37, 0, 0, 0, 0, 0])
    robot.movel_tool([0, 0, -h4, 0, 0, 0])
    time.sleep(1.5)
    robot.movel_tool([0, 0, h4, 0, 0, 0])
    robot.movel_tool([0, 0, -h4, 0, 0, 0])
    time.sleep(1.5)
    robot.movel_tool([0, 0, h4, 0, 0, 0])
    robot.movel_tool([0, 0, -h4, 0, 0, 0])
    time.sleep(1.5)
    robot.movel_tool([0, 0, h4, 0, 0, 0])
    robot.movej_rel([0, 0, 0, 0, 1, 0])
    robot.movej_rel([0, 0, 0, 0, -1, 0])
    robot.translatel_rel([-0.37, 0, 0, 0, 0, 0])

    robot.movel_tool([0, 0, h2, 0, 0, 0])
    robot.movel_tool([0, 0, h1, 0, 0, 0])
    robot.movej_rel([0, 0, 0, 0, -3.14, 0])
    data = SALT.returnData()
    #print(data)
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

            #angle to radians
            angle = (2*3.14) * (angle_number/18)

            #convoluted way to move to first point - could be improved greatly
            x = radius * numpy.cos(angle)
            y = radius * numpy.sin(angle)
            new_pose = [sum(x) for x in zip(stirring_home, [x,y,0,0,0,0])]#its element wise addition
            robot.movel(new_pose)

            #Move toward inner part of circle
            #robot.movel_tool([0, 0, 0, 0, 0, 2 * 3.14 / 36])

            #tool down
            robot.translatel_rel([0, 0, -height, 0, 0, 0])
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
            robot.movel_tool([0, 0.3*radius, 0, 0, 0, 2 * 3.14 / 18], vel = move_vel, acc = move_acc, radius = move_radius)
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









