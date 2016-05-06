#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on May 05 2016

@author: Lucas Fonseca
Channel 1: left
Channel 2: right"""

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
import threespace_api as ts_api
import glob


def get_port(device):
    """Get the serial port where the device is connected. Only available on Windows and OSX
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :return:
        The serial port where the device is connected
    """
    port = 0
    if sys.platform.startswith('darwin'):
        if device == 'imu':
            port = glob.glob('/dev/tty.usbmodem*')[0]
        elif device == 'stimulator':
            port = '/dev/tty.usbserial-HMQYVD6B'
    elif sys.platform.startswith('win'):
        ports = ts_api.getComPorts()
        for p in ports:
            if p[2] == 'DNG':
                port = p[0]
    return port


def read_angles():
    try:
        # Get angle position
        ang = IMUPedal.getEulerAngles()
        ang = ang.split(",")
        if len(ang) == 6:
            ang = float(ang[4])
            if ang >= 0:
                ang = (ang / math.pi) * 180
            else:
                ang = 360 - ((-ang / math.pi) * 180)
            angle.append(ang)
        else:
            print "Angular position data in wrong format"
    except ValueError:
        print 'Angle reading error'


def get_angular_speed():
    global counter, angSpeed
    try:
        # Get angular speed
        speed = IMUPedal.getGyroData()
        speed = speed.split(",")
        if len(speed) == 6:
            speed = float(speed[4])
            speed = speed / math.pi * 180
            # print speed
            # Filter speed
            angSpeed.append(int(round(speed)))
            if counter >= filter_size:
                angSpeed[-1] = int(round(numpy.mean(angSpeed[-filter_size:])))
                # print 'append'
                # print angSpeed[-1]
            else:
                pass
            # print counter
            # print speed
            # print angSpeed[-1]
        else:
            print "Angular speed data in wrong format"

        angSpeedRefHistory.append(speed_ref)
        errorHistory.append(speed_ref - angSpeed[-1])
        counter += 1
    except ValueError:
        print 'Angular speed reading error'


def read_buttons():
    global running
    try:
        if IMURemoteControl.checkButtons() == 2:
            running = False
            stim.stop()
    except ValueError:
        print 'Buttons reading error'


def read_sensors():
    global angSpeed
    while running:
        read_angles()
        get_angular_speed()
        read_buttons()
        time.sleep(0.001)
        # print angSpeed[-1]


# Main function
def main():
    global running, controlSignal, signal_channel
    this_instant = 501
    t0 = time.time()
    t1 = -1
    while running:
        try:
            # Control frequency
            t_diff = time.time() - t1
            if t_diff < period:
                if not (period - t_diff - 0.004) < 0:
                    time.sleep(period - t_diff - 0.004)
            t1 = time.time()
            time_stamp.append(time.time() - t0)

            # Get data from sensors
            control_angle.append(angle[-1])
            control_speed.append(angSpeed[-1])

            # Calculate error
            control_error.append(actual_ref_speed[this_instant] - angSpeed[-1])
            # print len(angSpeed)

            # Calculate control signal
            controlSignal.append(control.control(control_error[xRange:]))

            # Calculate stimulation signal
            signal_channel[0].append(
                (perfil.left_quad(angle[-1], angSpeed[-1], actual_ref_speed[this_instant])) * (controlSignal[-1]))
            signal_channel[1].append(
                (perfil.left_hams(angle[-1], angSpeed[-1], actual_ref_speed[this_instant])) * (controlSignal[-1]))
            signal_channel[2].append(
                (perfil.left_gluteus(angle[-1], angSpeed[-1], actual_ref_speed[this_instant])) * (controlSignal[-1]))
            signal_channel[3].append(
                (perfil.right_quad(angle[-1], angSpeed[-1], actual_ref_speed[this_instant])) * (controlSignal[-1]))
            signal_channel[4].append(
                (perfil.right_hams(angle[-1], angSpeed[-1], actual_ref_speed[this_instant])) * (controlSignal[-1]))
            signal_channel[5].append(
                (perfil.right_gluteus(angle[-1], angSpeed[-1], actual_ref_speed[this_instant])) * (controlSignal[-1]))

            # Signal double safety saturation
            # Electrical stimulation parameters settings
            for i in range(number_of_channels):
                if signal_channel[i][-1] > 1:
                    signal_channel[i][-1] = 1
                elif signal_channel[i][-1] < 0:
                    signal_channel[i][-1] = 0
                channel_stim[i] = signal_channel[i][-1] * channel_max[i]

            pulse_width = channel_stim

            # Electrical stimulator signal update
            if stimulation:
                stim.update(channels, pulse_width, current)

            # running = False
            this_instant += 1
        except ValueError:
            stim.stop()
            running=False


##########################################################################
##########################   PARAMETERS   ################################
##########################################################################

# IMU addresses
addressPedal = 0
addressRemoteControl = 1

# Reference speed
speed_ref = 150

# Desired control frequency
freq = 25
period = 1.0 / freq

# Debug mode, for when there's no stimulation
stimulation = True

# Experiment mode
ramps = False
speed_ref = 150  # Slow speed
fast_speed = 250
time_on_speed = 300

# Number of channels
number_of_channels = 6

# Max pulse width
channel_max = [0 for x in range(number_of_channels)]
channel_max[0] = 500
channel_max[1] = 500
channel_max[2] = 500
channel_max[3] = 500
channel_max[4] = 500
channel_max[5] = 500

# Angular speed moving average filter size
filter_size = 5

# Ports and addresses
# portIMU = 'COM4'  # Windows
# portIMU = '/dev/ttyACM0'  # Linux
portIMU = get_port('imu')  # Works on Mac. Should also work on Windows.
if stimulation:
    portStimulator = get_port('stimulator')  # Works only on Mac.
    # portStimulator = 'COM4'
# print portIMU

##########################################################################
##########################################################################
##########################################################################

# Initialize variables
xRange = freq * 20
angle = [0 for x in range(xRange)]
control_angle = [0 for x in range(xRange)]
angSpeed = [0 for x in range(xRange)]
control_speed = [0 for x in range(xRange)]
signal_channel = [[] for x in range(number_of_channels)]
for i in range(number_of_channels):
    signal_channel[i] = [0 for x in range(xRange)]
angSpeedRefHistory = [0 for x in range(xRange)]
control_ref_speed = [0 for x in range(xRange)]
actual_ref_speed = [0 for x in range(xRange)]
if ramps:
    for x in range(speed_ref):
        actual_ref_speed.append(x + 1)
    for x in range(time_on_speed):
        actual_ref_speed.append(speed_ref)
    for x in range(fast_speed - speed_ref):
        actual_ref_speed.append(speed_ref + x)
    for x in range(time_on_speed):
        actual_ref_speed.append(fast_speed)
    for x in range(fast_speed - speed_ref):
        actual_ref_speed.append(fast_speed - 1 - x)
    for x in range(time_on_speed):
        actual_ref_speed.append(speed_ref)
    for x in range(speed_ref - 1):
        actual_ref_speed.append(speed_ref - 1 - x)
    for x in range(1000):
        actual_ref_speed.append(1)
else:
    for x in range(4000):
        actual_ref_speed.append(speed_ref)
channel_stim = [0 for x in range(number_of_channels)]
controlSignal = [0 for x in range(xRange)]
errorHistory = [0 for x in range(xRange)]
control_error = [0 for x in range(xRange)]
time_stamp = []
wait_time = 0.000
running = False
reading = False
counter = 1
time_start = time.time()


##########################################################################
###############################   START   ################################
##########################################################################


try:
    print "Hello!"

    # Open ports
    serialPortIMU = serial.Serial(portIMU, timeout=1, baudrate=115200)
    serialPortStimulator = 0
    if stimulation:
        serialPortStimulator = serial.Serial(portStimulator, timeout=1, writeTimeout=1, baudrate=115200)

    # Construct objects
    IMUPedal = imu.IMU(serialPortIMU, addressPedal)
    IMURemoteControl = imu.IMU(serialPortIMU, addressRemoteControl)
    stim = 0
    if stimulation:
        stim = stimulator.Stimulator(serialPortStimulator)

    # Setting up
    print "EMA here!"
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
        if abs(calibrationError) < 1:
            break
        else:
            print 'reopenning port'
            serialPortIMU.close()
            time.sleep(0.1)
            serialPortIMU = serial.Serial(portIMU, timeout=1, baudrate=115200)
        print calibrationError
    print "Done"

    # Asking for user input
    channels = 0
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
    thread.start_new_thread(main, ())
    # thread.start_new_thread(plot, ())
    graph = realTimePlotter.RealTimePlotter(control_angle, signal_channel[0], signal_channel[1], angSpeed, angSpeed,
                                            controlSignal, actual_ref_speed, control_error, xRange, running)
    # while running:
    #     pass
    #    main()

    # Start real time plotter
    # realTimePlotter.RealTimePlotter(shown_angle, signal_femoral, signal_gastrocnemius, shown_speed,
    #                                 shown_control_signal, shown_ref_speed, shown_error, xRange, time_stamp)

    # Save the data
    t = time.localtime()
    date = [str(t[0]), str(t[1]), str(t[2]), str(t[3]), str(t[4]), str(t[5])]

    # Create folder
    folder = ''.join(date)
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        print 'Folder exists'

    with open(os.path.join(folder, 'data_angle'), 'w') as f:
        for s in angle:
            f.write(str(s) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_control_angle'), 'w') as f:
        for s in control_angle:
            f.write(str(s) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_ControlSpeed'), 'w') as f:
        for s in control_speed:
            f.write(str(s) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_angSpeed'), 'w') as f:
        for s in angSpeed:
            f.write(str(s) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_time'), 'w') as f:
        for s in time_stamp:
            f.write(str(s) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_channel_1'), 'w') as f:
        for s in signal_channel[0]:
            f.write(str(s * channel_max[0]) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_channel_2'), 'w') as f:
        for s in signal_channel[1]:
            f.write(str(s * channel_max[1]) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_channel_3'), 'w') as f:
        for s in signal_channel[2]:
            f.write(str(s * channel_max[1]) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_channel_4'), 'w') as f:
        for s in signal_channel[3]:
            f.write(str(s * channel_max[1]) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_channel_5'), 'w') as f:
        for s in signal_channel[4]:
            f.write(str(s * channel_max[1]) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_channel_6'), 'w') as f:
        for s in signal_channel[5]:
            f.write(str(s * channel_max[1]) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_control'), 'w') as f:
        for s in controlSignal:
            f.write(str(s * 1) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_control_error'), 'w') as f:
        for s in control_error:
            f.write(str(s * 1) + '\n')
    with open(os.path.join(folder, 'data_reference'), 'w') as f:
        for s in actual_ref_speed:
            f.write(str(s * 1) + '\n')
        f.close()
    with open(os.path.join(folder, 'data_parameters'), 'w') as f:
        f.write('Stimulation on: ' + str(stimulation * 1) + '\n')
        f.write('Speed reference: ' + str(speed_ref * 1) + '\n')
        f.write('Desired frequency: ' + str(freq * 1) + '\n')
        f.write('Ramps on reference: ' + str(ramps * 1) + '\n')
        f.write('Fast speed: ' + str(fast_speed * 1) + '\n')
        f.write('Time on speed; ' + str(time_on_speed * 1) + '\n')
        f.write('Filter size: ' + str(filter_size * 1) + '\n')
        f.write('Max pulse width in each channel: ' + '\n')
        for s in channel_max:
            f.write(str(s * 1) + '\n')
        f.close()

    # Finish
    print "Have a good day!"
    running = False
    if stimulation:
        stim.stop()
        serialPortStimulator.close()
    serialPortIMU.close()

except Exception as err:
    print "Error on the outer loop"
    print(err.args)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    # if serialPortIMU is not None:
    #     serialPortIMU.close()
