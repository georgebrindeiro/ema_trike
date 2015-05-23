# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:49:13 2015

@author: Wall-e
"""
# imports
import serial
import imu
import stimulator
import perfil
import time
import thread
import math
import numpy

# Ports and addresses
portIMU = ''
portStimulator = ''
addressPedal = 1
addressRemoteControl = 2

# Open ports
serialPortIMU = serial.Serial(portIMU, timeout=1, writeTimeout=1, baudrate=115200)
serialPortStimulator = serial.Serial(portStimulator, timeout=1, writeTimeout=1, baudrate=115200)

# Construct objects
IMUPedal = imu.IMU(serialPortIMU,addressPedal)
IMURemoteControl = imu.IMU(serialPortIMU,addressRemoteControl)
stim = stimulator.Stimulator(serialPortStimulator)

# Setting up
print "Hello, EMA here!"
print "Beggining calibration..."

calibrationError = 10
while calibrationError > 0.1 :
    IMUPedal.setEulerToYXZ()
    IMUPedal.calibrate()
    IMUPedal.tare()
    ang = IMUPedal.get_euler_angles()
    calibrationError = float(ang[3]) + float(ang[4]) + float(ang[5])

print "Done"

# Asking for user input
freq=int(raw_input("Input frequency: "))
channels=int(raw_input("Input channels: "))
current_str = raw_input("Input current: ")
current = [int(i) for i in (current_str.split(","))]

# Initialize stimulator
print "Initializing stimulator..."
stim.initialization(freq, channels)
print "Done"

# Ready to go
print "Whenever you're ready, press button 1 (the left one)"






















