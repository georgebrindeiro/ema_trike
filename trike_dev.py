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
import realTimePlotter


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

# Initialize global variables
# TODO: review
xRange = 500
values=[]
values = [0 for x in range(xRange)]
speed=[]
speed = [0 for x in range(xRange)]
filtered_speed = []
filtered_speed = [0 for x in range(xRange)]
signal_femoral = []
signal_femoral = [0 for x in range(xRange)]
signal_gastrocnemius = []
signal_gastrocnemius = [0 for x in range(xRange)]
signal_speed_ref = []
signal_speed_ref = [0 for x in range(xRange)]
signal_speed_actual = []
signal_speed_actual = [0 for x in range(xRange)]
error_speed = []
error_speed = [0 for x in range(xRange)]
time_stamp = []
time_lim = 5
filter_size = 20 ###
gastrocnemius_max = 500
femoral_max = 500
old_signal_gastrocnemius = 0
old_signal_femoral = 0
scale = 1.2
delay = 0.001
old_current = 0
old_pulse_width = 0
speed_ref = 300 ###
speed_actual = 0
speed_max = 1000

# Setting up
print "Hello, EMA here!"
print "Beginning calibration..."

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
print "Whenever you're ready, press button 1 (the left one)!"

ploter = realTimePlotter(ang, signal_femoral, signal_gastrocnemius, filtered_speed, speed, signal_speed_actual, signal_speed_ref, xRange)

# Wait until the user press the 'Start' button
while not (IMURemoteControl.checkButtons() == 1):
    pass

while not (IMURemoteControl.checkButtons() == 2):
    ang = IMUPedal.getEulerAngles()
    ang = ang.split()
    if len(ang) == 6:
        ang = float(ang[4])
        if ang >= 0:
            ang = (ang / math.pi) * 180
        else:
            ang = 360 - ((-(ang) / math.pi) * 180)
        values.append(ang)
    
    
    # TODO: main function

# Close ports
serialPortIMU.close()



















