#!/usr/bin/env python

import rospy

# import ros msgs
import serial
import modules.imu
from sensor_msgs.msg import Imu

import serial
import modules.imu
import modules.stimulator
import modules.perfil
import time
import math
import numpy
import modules.realTimePlotter
import modules.control
import thread
import sys
import os

imu = modules.imu

xRange = 500
filter_size = 20 ###

angle = []
angle = [0 for x in range(xRange)]

angSpeed = []
angSpeed = [0 for x in range(xRange)]

filtered_speed = []
filtered_speed = [0 for x in range(xRange)]

def main():
    # init 'imu' node
    rospy.init_node('imu', anonymous=True)

    # list published topics
    pub = rospy.Publisher('imu', Imu, queue_size=10)

    # config imu

    portIMU = '/dev/ttyACM0'
    addressPedal = 0
    counter = 1
    # Open ports
    serialPortIMU = serial.Serial(portIMU, timeout=1, writeTimeout=1, baudrate=115200)

    # Construct objects
    IMUPedal = imu.IMU(serialPortIMU,addressPedal)

    print "Hello, EMA here!"
    print "Beginning calibration..."
    calibrationError = 10
    while calibrationError > 0.1 :
        ang = []
        while(len(ang) < 6):
            IMUPedal.setEulerToYXZ()
            IMUPedal.calibrate()
            IMUPedal.tare()
            ang = IMUPedal.getEulerAngles()
            ang = ang.split(",")
            #print ang
        calibrationError = float(ang[3]) + float(ang[4]) + float(ang[5])
    print "Done"

    # Asking for user input
    try:
        freq=int(raw_input("Input frequency (default 50): "))
    except ValueError:
        print "Adopting default value: 50"
        freq = 50

    try:
        channels=int(raw_input("Input channels (default 3): "))
    except ValueError:
        print "Adopting default value: 3"
        channels = 3

    try:
        current_str = raw_input("Input current (default 6,6): ")
        current = [int(i) for i in (current_str.split(","))]
    except ValueError:
        print "Adopting default value: 6,6"
        current = [6,6]

    # define loop rate (in hz)
    rate = rospy.Rate(10)

    # node loop
    while not rospy.is_shutdown():
        # get some work done

        # Get angle position
        ang = IMUPedal.getEulerAngles()
        ang = ang.split(",")
        if len(ang) == 6:
            ang = float(ang[4])
            if ang >= 0:
                ang = (ang / math.pi) * 180
            else:
                ang = 360 - ((-(ang) / math.pi) * 180)
            angle.append(ang)
            print ang
        ##############################################

        # Get angular speed
            speed = IMUPedal.getGyroData()
            speed = speed.split(",")
            if len(speed) == 6:
                speed = float(speed[4])
                speed = speed/(math.pi) * 180
                angSpeed.append(speed)
        ##############################################

        # Filter the speed
                if counter >= filter_size:
                    filtered_speed.append(numpy.mean(angSpeed[-filter_size:]))
        # publish work
        ## send imu data

        # sleep until it's time to work again
        rate.sleep()

        counter = counter + 1

    serialPortIMU.close()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
