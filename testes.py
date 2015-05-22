# -*- coding: utf-8 -*-
"""
Created on Fri May 15 16:59:57 2015

@author: Wall-e
"""
import serial
import imu

port = 'COM5'
serialPort = serial.Serial(port, timeout=1, writeTimeout=1, baudrate=115200)
x = imu.IMU(serialPort,1)
print x.calibrate()
print x.get_euler_angles();
serialPort.close()