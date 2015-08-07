# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 12:00:28 2015

@author: Lucas
"""

import serial
import imu
import time

portIMU = '/dev/tty.usbmodemfd121'
addressPedal = 0
serialPortIMU = serial.Serial(portIMU, timeout=1, writeTimeout=1, baudrate=115200)
IMUPedal = imu.IMU(serialPortIMU,addressPedal)


while not raw_input('Press ENTER to continue'):
    ang = IMUPedal.getEulerAngles()
    print ang
        
serialPortIMU.close()


