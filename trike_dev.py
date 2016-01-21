#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sat May 23 13:49:13 2015

@author: Wall-e
Channel 1: left
Channel 2: right"""


# imports
import serial
import imu
import stimulator
import perfil
import time
import math
import numpy
import realTimePlotter
import control
import thread
import sys
import os

# Ports and addresses
# portIMU = 'COM4'
# portIMU = '/dev/ttyACM0'
# portStimulator = '/dev/ttyUSB0'
# portIMU = '/dev/tty.usbmodemfd121'
portIMU = imu.get_port()
portStimulator = '/dev/tty.usbserial-HMQYVD6B'
addressPedal = 2
addressRemoteControl = 1

# Reference speed
speed_ref = 100

# Debug mode
stimulation = False

# Initialize variables
xRange = 500
# angle = []
angle = [0 for x in range(xRange)]
# angSpeed = []
# noinspection PyRedeclaration
angSpeed = [0 for x in range(xRange)]
# filtered_speed = []
# noinspection PyRedeclaration
filtered_speed = [0 for x in range(xRange)]
# signal_femoral = []
# noinspection PyRedeclaration
signal_femoral = [0 for x in range(xRange)]
# signal_gastrocnemius = []
# noinspection PyRedeclaration
signal_gastrocnemius = [0 for x in range(xRange)]
# angSpeedRefHistory = []
# noinspection PyRedeclaration
angSpeedRefHistory = [0 for x in range(xRange)]
# controlSignal = []
# noinspection PyRedeclaration
controlSignal = [0 for x in range(xRange)]
# errorHistory = []
# noinspection PyRedeclaration
errorHistory = [0 for x in range(xRange)]
time_stamp = []
filter_size = 20
gastrocnemius_max = 500
femoral_max = 500
wait_time = 0.001
running = False
reading = False
counter = 1
time_start = time.clock()


# Read angles
def read_angles():
    global reading
    # while running:
    try:
        # print 'reading'
        # Get angle position
        while reading:
            pass
        reading = True
        ang = IMUPedal.getEulerAngles()
        reading = False
        ang = ang.split(",")
        if len(ang) == 6:
            ang = float(ang[4])
            if ang >= 0:
                ang = (ang / math.pi) * 180
            else:
                ang = 360 - ((-ang / math.pi) * 180)
            angle.append(ang)
        else:
            print 'erro de leitura'
        time.sleep(wait_time)
    except ValueError:
        print 'Erro ao ler angulo'
        ##############################################


def get_angular_speed():
    global reading, counter

    # while running:
    try:
        # Get angular speed
        # while reading:
        #     pass
        reading = True
        speed = IMUPedal.getGyroData()
        reading = False
        speed = speed.split(",")
        if len(speed) == 6:
            speed = float(speed[4])
            speed = speed / math.pi * 180
            angSpeed.append(int(speed))
            angSpeedRefHistory.append(speed_ref)
            errorHistory.append(speed_ref - filtered_speed[-1])
            # Filter the speed
            # print counter
            if counter >= filter_size:
                # print 'append'
                filtered_speed.append(int(numpy.mean(angSpeed[-filter_size:])))
        else:
            print "Wrong response for angular speed"
        counter += 1
        time.sleep(wait_time)
    except ValueError:
        print 'Erro ao ler velocidade angular'
        ##############################################


def read_buttons():
    global running, reading
    # while running:
    try:
        while reading:
            pass
        reading = True
        if IMURemoteControl.checkButtons() == 2:
            running = False
        reading = False
        time.sleep(wait_time)
    except ValueError:
        print 'Erro ao ler botoes'


# Main function
def main():
    global running, controlSignal, signal_femoral, signal_gastrocnemius

    # while running:
    time_stamp.append(time.clock() - time_start)
    # print time_stamp[-1]
    # print len(time_stamp)
    # Calculate control signal
    controlSignal.append(control.control(errorHistory))
    # print len(controlSignal)

    # Calculate stimulation signal
    signal_gastrocnemius.append((perfil.gastrocnemius(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))
    signal_femoral.append((perfil.femoral(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))

    # Signal double safety saturation
    if signal_femoral[-1] > 1:
        signal_femoral[-1] = 1
    elif signal_femoral[-1] < 0:
        signal_femoral[-1] = 0
    if signal_gastrocnemius[-1] > 1:
        signal_gastrocnemius[-1] = 1
    elif signal_gastrocnemius[-1] < 0:
        signal_gastrocnemius[-1] = 0

    # Electrical stimulation parameters settings
    stim_femoral = signal_femoral[-1] * femoral_max
    stim_gastrocnemius = signal_gastrocnemius[-1] * gastrocnemius_max
    pulse_width = [stim_femoral, stim_gastrocnemius]

    # Electrical stimulator signal update
    if stimulation:
        stim.update(channels, pulse_width, current)

    # running = False


def read_sensors():
    while running:
        read_angles()
        get_angular_speed()
        read_buttons()
        main()
        # print len(angle)

    # Stop stimulator
    if stimulation:
        stim.stop()

    # Close ports
    if stimulation:
        serialPortStimulator.close()
    serialPortIMU.close()

try:
    # Open ports
    serialPortIMU = serial.Serial(portIMU, timeout=1, baudrate=115200)
    if stimulation:
        serialPortStimulator = serial.Serial(portStimulator, timeout=1, writeTimeout=1, baudrate=115200)

    # Construct objects
    IMUPedal = imu.IMU(serialPortIMU, addressPedal)
    IMURemoteControl = imu.IMU(serialPortIMU, addressRemoteControl)
    if stimulation:
        stim = stimulator.Stimulator(serialPortStimulator)

    # Setting up
    print "Hello, EMA here!"
    print "Beginning calibration..."
    calibrationError = 10
    while calibrationError > 0.1:
        ang_cal = []
        while len(ang_cal) < 6:
            IMUPedal.setEulerToYXZ()
            IMUPedal.calibrate()
            IMUPedal.tare()
            ang_cal = IMUPedal.getEulerAngles()
            ang_cal = ang_cal.split(",")
        calibrationError = float(ang_cal[3]) + float(ang_cal[4]) + float(ang_cal[5])
    print "Done"

    # Asking for user input
    if stimulation:
        freq = int(raw_input("Input frequency: "))
        channels = int(raw_input("Input channels: "))
        current_str = raw_input("Input current: ")
        current = [int(i) for i in (current_str.split(","))]

    # Initialize stimulator
    if stimulation:
        print "Initializing stimulator..."
        stim.initialization(freq, channels)
        print "Done"
    else:
        print "Stimulation is deactivated"

    # Ready to go. 
    print "Whenever you're ready, press button 1 (the left one)!"

    # Wait until the user presses the 'Start' button
    while not (IMURemoteControl.checkButtons() == 1):
        pass

    # Keep on until the user presses the "Stop" button
    print "Here we go!"

    # Start main function
    running = True
    thread.start_new_thread(read_sensors, ())
    # thread.start_new_thread(read_angles, ())
    # thread.start_new_thread(get_angular_speed, ())
    # thread.start_new_thread(main, ())
    # thread.start_new_thread(read_buttons, ())
    #    main()

    # Start real time plotter
    realTimePlotter.RealTimePlotter(angle, signal_femoral, signal_gastrocnemius, filtered_speed, angSpeed,
                                    controlSignal, angSpeedRefHistory, errorHistory, xRange)

    # Save the data
    with open("data_angle", 'w') as f:
        for s in angle:
            f.write(str(s) + '\n')
    with open("data_filteredAngSpeed", 'w') as f:
        for s in filtered_speed:
            f.write(str(s) + '\n')
    with open("data_time", 'w') as f:
        for s in time_stamp:
            f.write(str(s) + '\n')
    with open("data_femoral", 'w') as f:
        for s in signal_femoral:
            f.write(str(s * femoral_max) + '\n')
    with open("data_gastrocnemius", 'w') as f:
        for s in signal_gastrocnemius:
            f.write(str(s * gastrocnemius_max) + '\n')
    with open("data_control", 'w') as f:
        for s in controlSignal:
            f.write(str(s * 1) + '\n')

            # Finish
    print "Have a good day!"

except Exception as err:
    print "Error"
    print(err.args)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    # if serialPortIMU is not None:
    #     serialPortIMU.close()
