#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 16:59:57 2015

@author: Wall-e
"""
import serial
import time
import modules.imu

imu = modules.imu

port = '/dev/ttyACM0'
address = 2
serialPort = serial.Serial(port, timeout=1, writeTimeout=1, baudrate=115200)
x = imu.IMU(serialPort,address)
print 'Calibration: ' + x.calibrate()

while True:
    print 'Euler angles: ' + x.getEulerAngles()
    time.sleep(0.01)

serialPort.close()
