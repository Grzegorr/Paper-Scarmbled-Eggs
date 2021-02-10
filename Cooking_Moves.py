import time
import serial
from math import pi
import numpy
import socket
import sys

import waypoints as wp
import kg_robot as kgr

#task = "Home Position"
#task = "Cooking Home Position"
#task = "First Test"
#task = "Test2"
task = "Get L and J"
#task = "Current Workspace"
#task = "Stirring Presentation"
#task = "Scrape Eggs"



def main():
    print("------------Configuring Burt-------------\r\n")
    robot = kgr.kg_robot(port=30010,db_host="169.254.250.80")
    #robot = kgr.kg_robot(port=30010,ee_port="COM32",db_host="192.168.1.50")
    print("----------------Hi Burt!-----------------\r\n\r\n")
    #print("------------Set Payload = 0kg------------\r\n\r\n")
    #robot.set_tcp([0,0,0])
    #robot.set_payload(0)


    if task == "Home Position":
        print("Task: " + task)
        move_to_home(robot)

    if task == "Cooking Home Position":
        print("Task: " + task)
        move_to_cooking_home(robot)

    if task == "Current Workspace":
        print("Task: " + task)
        pan_left_to_right(robot)


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

    if task == "Scrape Eggs":
        print("Task: " + task)
        move_to_cooking_home(robot)
        for angle in [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
            fold_eggs(robot, 0.05, angle, 0.1)


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
    robot.movel_tool([-1.5*r, 0, 0, 0, 0, 0])
    robot.movel_tool([0, 0, -h, 0, 0, 0])
    robot.movel_tool([0.5 * r, 0, 0, 0, 0, 0])
    robot.movel_tool([0, 0, 0, 0, 0, -angle_rad])

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
    input("Go to next step?")
    #Set tool to Gripper
    tool_to_use(robot, "Gripper")
    input("Go to next step?")
    # move behind the pan
    robot.translatel_rel([0.1, 0.2, -0.1, 0, 0, 0])
    input("Go to next step?")
    # press pan against a wall
    robot.translatel_rel([0, -0.2, 0, 0, 0, 0])
    input("Go to next step?")
    # Here the magnet should be turned on
    # Pull backfrom the wall
    robot.translatel_rel([0, 0.1, 0, 0, 0, 0])
    input("Go to next step?")
    # Drag to right
    robot.translatel_rel([-0.3, 0, 0, 0, 0, 0])
    input("Go to next step?")
    # Here the magnet should be switched of
    # Go back
    robot.translatel_rel([0, 0.1, 0, 0, 0, 0])
    input("Go to next step?")
    # Set tool to Spatula
    tool_to_use(robot, "Spatula")
    input("Go to next step?")
    # Go home
    move_to_cooking_home(robot)




if __name__ == '__main__': main()









