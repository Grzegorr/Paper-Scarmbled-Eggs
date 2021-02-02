import time
import serial
from math import pi
import numpy
import socket
import sys

import waypoints as wp
import kg_robot as kgr

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

    if task == "Current Workspace":
        print("Task: " + task)
        move_to_cooking_home(robot)
        tool_to_use(robot, "Spatula")
        tool_to_use(robot, "Gripper")
        tool_to_use(robot, "Spatula")
        tool_to_use(robot, "Gripper")
        tool_to_use(robot, "Spatula")
        tool_to_use(robot, "Gripper")

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
        stir_circle_relative(robot, 0.1, 0)


    time.sleep(3)

def move_to_cooking_home(robot):
    robot.movel(wp.cooking_home_l)

def move_to_home(robot):
    robot.movel(wp.robot_home_l)

#two options for the tool are "Spatula" and "Gripper"
#Its relative rotation so make sure you have the other tool in operation at the moment
def tool_to_use(robot, tool):
    if tool == "Gripper":
        robot.movej_rel([0, 0, 0, 0, 3.14, 0])
    if tool == "Spatula":
        robot.movej_rel([0, 0, 0, 0, -3.14, 0])

#stirring home must in the middle of the circle, spatula edge along x direction
def stir_circle_relative(robot, radius, height):
    #get current position
    stirring_home = robot.getl()
    for angle_number in range(18):
        angle = (2*3.14) * (angle_number/18)
        x = radius * numpy.cos(angle)
        y = radius * numpy.sin(angle)
        print(stirring_home)
        print([x,y,0,angle,0,0])
        new_pose = [sum(x) for x in zip(stirring_home, [x,y,0,angle,0,0])]
        print(new_pose)
        robot.movel(new_pose)#its element wise addition
        #print(stirring_home)
        print(robot.getl())
        print()




















if __name__ == '__main__': main()









