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
# portIMU = '/dev/tty.usbmodemFA131'
portIMU = imu.get_port()
portStimulator = '/dev/tty.usbserial-HMQYVD6B'
addressPedal = 5
addressRemoteControl = 4

# Reference speed
speed_ref = 250
fast_speed = 300
time_on_speed = 3000

# Frequency
freq = 25
period = 1.0/freq
print period

# Debug mode
stimulation = False

# Light mode
ramps = True

# Run with filtered seed
run_with_filtered_speed = True

# Initialize variables
xRange = freq * 20
angle = [0 for x in range(xRange)]
# noinspection PyRedeclaration
shown_angle = [0 for x in range(xRange)]
# noinspection PyRedeclaration
angSpeed = [0 for x in range(xRange)]
# noinspection PyRedeclaration
shown_speed = [0 for x in range(xRange)]
# noinspection PyRedeclaration
filtered_speed = [0 for x in range(xRange)]
# noinspection PyRedeclaration
signal_femoral = [0 for x in range(xRange)]
# noinspection PyRedeclaration
signal_gastrocnemius = [0 for x in range(xRange)]
# noinspection PyRedeclaration
angSpeedRefHistory = [0 for x in range(xRange)]
# noinspection PyRedeclaration
shown_ref_speed = [0 for x in range(xRange)]
# noinspection PyRedeclaration
actual_ref_speed = [0 for x in range(xRange)]
if ramps:
    for x in range(speed_ref):
        actual_ref_speed.append(x+1)
    for x in range(time_on_speed):
        actual_ref_speed.append(speed_ref)
    for x in range(fast_speed - speed_ref):
        actual_ref_speed.append(speed_ref+x)
    for x in range(time_on_speed):
        actual_ref_speed.append(fast_speed)
    for x in range(fast_speed - speed_ref):
        actual_ref_speed.append(fast_speed-1-x)
    for x in range(time_on_speed):
        actual_ref_speed.append(speed_ref)
    for x in range(speed_ref-1):
        actual_ref_speed.append(speed_ref-1-x)
    for x in range(1000):
        actual_ref_speed.append(1)
else:
    for x in range(4000):
        actual_ref_speed.append(speed_ref)
# noinspection PyRedeclaration
controlSignal = [0 for x in range(xRange)]
# noinspection PyRedeclaration
shown_control_signal = [0 for x in range(xRange)]
# noinspection PyRedeclaration
errorHistory = [0 for x in range(xRange)]
# noinspection PyRedeclaration
shown_error = [0 for x in range(xRange)]
time_stamp = []
filter_size = 5
gastrocnemius_max = 500
femoral_max = 500
wait_time = 0.000
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
        speed_test = -1
        while speed_test < 0:
            reading = True
            speed = IMUPedal.getGyroData()
            reading = False
            # bkp_speed = speed
            speed = speed.split(",")
            if len(speed) == 6:
                speed = float(speed[4])
                speed = speed / math.pi * 180
                speed_test = speed
            else:
                print "Wrong response for angular speed"
        if run_with_filtered_speed:
            if counter >= filter_size:
                # print 'append'
                angSpeed.append(int(round(speed)))
                angSpeed[-1] = int(round(numpy.mean(angSpeed[-filter_size:])))
                filtered_speed.append(angSpeed[-1])
            else:
                angSpeed.append(int(round(speed)))
        else:
            angSpeed.append(int(round(speed)))
            if counter >= filter_size:
                # print 'append'
                filtered_speed.append(int(round(numpy.mean(angSpeed[-filter_size:]))))

        angSpeedRefHistory.append(speed_ref)
        errorHistory.append(speed_ref - filtered_speed[-1])
        # Filter the speed
        # print counter


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
    this_instant = 501
    t0 = time.clock()
    t1 = -1
    while running:
        # Get time
        t_diff = time.clock() - t1
        if t_diff < period:
            time.sleep(period-t_diff-0.004)
            # continue
        t1 = time.clock()
        time_stamp.append(time.clock() - t0)

        # get other data
        shown_angle.append(angle[-1])
        shown_control_signal.append(controlSignal[-1])
        # shown_error.append(errorHistory[-1])
        # shown_ref_speed.append(angSpeedRefHistory[-1])
        shown_error.append(actual_ref_speed[this_instant] - filtered_speed[-1])
        shown_ref_speed.append(actual_ref_speed[this_instant])
        shown_speed.append(angSpeed[-1])

        # Calculate control signal
        controlSignal.append(control.control(shown_error[xRange:]))

        # Calculate stimulation signal
        # signal_gastrocnemius.append((perfil.gastrocnemius(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))
        # signal_femoral.append((perfil.femoral(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))
        signal_gastrocnemius.append((perfil.gastrocnemius(angle[-1], angSpeed[-1], shown_ref_speed[-1])) * (controlSignal[-1]))
        signal_femoral.append((perfil.femoral(angle[-1], angSpeed[-1], shown_ref_speed[-1])) * (controlSignal[-1]))

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
        this_instant += 1

def read_sensors():
    while running:
        read_angles()
        get_angular_speed()
        read_buttons()
        # main()
        # print len(angle)

    # Stop stimulator
    if stimulation:
        stim.stop()

    # Close ports
    if stimulation:
        serialPortStimulator.close()
    serialPortIMU.close()
    time.sleep(wait_time)

try:
    print "Hello!"

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
    thread.start_new_thread(main, ())
    # thread.start_new_thread(read_buttons, ())
    #    main()

    # Start real time plotter
    # realTimePlotter.RealTimePlotter(angle, signal_femoral, signal_gastrocnemius, angSpeed,
    #                                 controlSignal, angSpeedRefHistory, errorHistory, xRange)
    realTimePlotter.RealTimePlotter(shown_angle, signal_femoral, signal_gastrocnemius, shown_speed,
                                    shown_control_signal, shown_ref_speed, shown_error, xRange, time_stamp)

    # Save the data
    with open("data_angle", 'w') as f:
        for s in angle:
            f.write(str(s) + '\n')
    with open("data_filteredAngSpeed", 'w') as f:
        for s in filtered_speed:
            f.write(str(s) + '\n')
    with open("data_usedSpeed", "w") as f:
        for s in angSpeed:
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
