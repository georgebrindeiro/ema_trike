# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 12:00:28 2015

@author: Lucas
"""

import serial
import imu
import math
import time

portIMU = '/dev/tty.usbmodemfa1331'
addressPedal = 3
serialPortIMU = serial.Serial(portIMU, timeout=1, writeTimeout=1, baudrate=115200)
IMUPedal = imu.IMU(serialPortIMU,addressPedal)

IMUPedal.calibrate()
# while not raw_input('Press ENTER to continue, or anything else and ENTER to stop'):

def convert(ang):
    x = ang.x
    y = ang.y
    z = ang.z
    w = ang.w

    heading = math.atan2(2*y*w-2*x*z,1-2*math.pow(y,2)-2*math.pow(z,2))
    attitude = math.asin(2*x*y + 2*z*w)
    bank = math.atan2(2*x*w-2*y*z,1-2*math.pow(x,2)-2*math.pow(z,2))

    return [heading,attitude,bank]

i=0
while i<100:
    i=i+1

    ang = IMUPedal.getUntaredQuaternion()

    euler = convert(ang)

    print euler[0]
    time.sleep(0.1)
    # print euler[1]
    # print euler[2]




# print IMUPedal.getEulerAngles()
        
serialPortIMU.close()


