import time
import serial
from math import pi
import numpy
import socket
import sys

import waypoints as wp
import kg_robot as kgr

#task = "Home Position"
#task = "First Test"
#task = "Test2"
#task = "Get L and J"
#task = "Current Workspace"
task = "Stirring Presentation"



def main():
    print("------------Configuring Burt-------------\r\n")
    robot = kgr.kg_robot(port=30010,db_host="169.254.250.80")
    #robot = kgr.kg_robot(port=30010,ee_port="COM32",db_host="192.168.1.50")
    print("----------------Hi Burt!-----------------\r\n\r\n")


    if task == "Home Position":
        print("Task: " + task)
        move_to_home(robot)

    if task == "Current Workspace":
        print("Task: " + task)
        move_to_cooking_home(robot)
        robot.movel_tool([0,0,0,0,0,1.57])

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
        move_to_cooking_home(robot)
        stir_circle_relative(robot, 0.1, 0.12, 0.005, 0.45, 5)
        move_to_cooking_home(robot)
        stir_circle_relative(robot, 0.1, 0.12, 0.001, 0.05, 1)


    time.sleep(3)

def move_to_cooking_home(robot):
    robot.movel(wp.cooking_home_l)
    print("Move: Home")

def move_to_home(robot):
    robot.movel(wp.robot_home_l)
    print("Move: Cooking Home")

#two options for the tool are "Spatula" and "Gripper"
#Its relative rotation so make sure you have the other tool in operation at the moment
def tool_to_use(robot, tool):
    if tool == "Gripper":
        robot.movej_rel([0, 0, 0, 0, 3.14, 0])
    if tool == "Spatula":
        robot.movej_rel([0, 0, 0, 0, -3.14, 0])


#stirring home must in the middle of the circle, spatula edge along x direction
def stir_circle_relative(robot, radius, height, move_radius, move_vel, move_acc):

    #Take care of the robot wrist angle
    joints = robot.getj()
    if joints[5] > 0:
        robot.movel_tool([0,0,0,0,0,-3.14])
    joints = robot.getj()
    if joints[5] > 0:
        robot.movel_tool([0, 0, 0, 0, 0, -3.14])

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
            robot.movel_tool([0, 0, 0, 0, 0, 2 * 3.14 / 36])

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
            robot.movel_tool([0, 0.35*radius, 0, 0, 0, 2 * 3.14 / 18], vel = move_vel, acc = move_acc, radius = move_radius)
            #print(previous_angle - angle)
            #print()

    #lift the tool up
    robot.translatel_rel([0, 0, height, 0, 0, 0])

    joints = robot.getj()
    if joints[5] > 0:
        robot.movel_tool([0, 0, 0, 0, 0, -3.14])



if __name__ == '__main__': main()









