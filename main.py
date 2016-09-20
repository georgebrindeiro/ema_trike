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
import control
import thread
import sys
import os
import threespace_api as ts_api
import glob
import struct


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
            port = glob.glob('/dev/tty.usbmodemFD1211')[0]
        elif device == 'stimulator':
            # port = '/dev/tty.usbserial-HMQYVD6B'
            port = '/dev/tty.usbserial-HMCX9Q6D'
    elif sys.platform.startswith('win'):
        ports = ts_api.getComPorts()
        for p in ports:
            if p[2] == 'DNG':
                port = p[0]
    elif sys.platform.startswith('linux'):
        if device == 'imu':
            port = '/dev/ttyACM0'
        elif device == 'stimulator':
            port = '/dev/ttyUSB0'
    return port


def user_interface():
    global current, running, start, ui_serial_port, stimulation, stim
    # t0 = time.time()
    current_to_write = ""
    time.sleep(1)
    idle = True
    while running:
        while ui_serial_port.inWaiting() == 0:
            if not current_to_write == str(current[0]):
                if start:
                    current_to_write = str(current[0])
                    ui_serial_port.write(current_to_write)
                else:
                    current_to_write = str(current[0])
                    ui_serial_port.write(current_to_write + ' - Pronto')


        bytes_to_read = ui_serial_port.inWaiting()
        # print("Algo para ler.")
        data = ui_serial_port.read(1)
        if idle:
            if data == '2':
                decrease_current()
                idle = False
            elif data == '1':
                increase_current()
                idle = False
            elif data == '3':
                start = True
                idle = False
            elif data == '0':
                running = False
                idle = False
            elif data == '4' and stimulation:
                stimulation = False
                stim.update(119, [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0])
                print('no stim')
                idle = False
            elif data == '4' and not stimulation:
                stimulation = True
                print('yes stim')
                idle = False
        elif data == '5':
            idle = True
        # print data


def read_sensors():
    global angSpeed
    global counter, angSpeed
    serial_port = serial.Serial(port=portIMU, baudrate=115200, timeout=0.001)
    while running:
        bytes_to_read = serial_port.inWaiting()
        if bytes_to_read > 0:
            data = bytearray(serial_port.read(bytes_to_read))

            # angle
            b = ''.join(chr(i) for i in data[8:12])  # angle y
            ang = struct.unpack('>f', b)
            x = ang[0]
            # print(x)

            # angle
            b = ''.join(chr(i) for i in data[12:16])  # angle y
            ang = struct.unpack('>f', b)
            ang = ang[0]
            if ang >= 0:
                ang = (ang / math.pi) * 180
                if abs(x) > (math.pi*0.75):
                    ang = ang + 2*(90-ang)
            else:
                ang = 360 + ((ang / math.pi) * 180)
                if abs(x) > (math.pi*0.75):
                    ang = ang - 2*(ang-270)

            # print(ang)
            angle.append(ang)
            if counter >= filter_size and ((ang > 60 and ang < 120) or (ang > 240 and ang < 300)):
                angle[-1] = numpy.mean(angle[-filter_size:])
            # print(angle[-1])

            # angle speed
            b = ''.join(chr(i) for i in data[24:28])  # gyro y
            speed = struct.unpack('>f', b)
            speed = speed[0]
            speed = speed / math.pi * 180
            # print speed
            # Filter speed
            angSpeed.append(int(round(speed)))
            if counter >= filter_size:
                angSpeed[-1] = int(round(numpy.mean(angSpeed[-filter_size:])))
            angSpeedRefHistory.append(speed_ref)
            errorHistory.append(speed_ref - angSpeed[-1])


            counter += 1
    serial_port.close()


def check_angles(ang1, ang2):
    good_angle = False
    safety_range = 15
    if abs(ang1 - ang2) < safety_range:
        good_angle = True
    elif abs(ang1 - ang2) > (360 - safety_range):
        good_angle = True
    return good_angle


def increase_current():
    global current, current_limit
    if current[0] <= current_limit-2:
        temp = current[4]
        temp1 = current[1]
        # temp2 = current[2]
        # temp3 = current[5]
        current = [i+2 for i in current]
        current[4] = temp+1
        current[1] = temp1+1
        # current[2] = temp2
        # current[5] = temp3
        print(current)


def decrease_current():
    global current
    temp = current[4]
    temp1 = current[1]
    # temp2 = current[2]
    # temp3 = current[5]
    current = [i-2 for i in current]
    if current[4] <= 2:
        current[4] = 0
    else:
        current[4] = temp-1
    if current[1] <= 2:
        current[1] = 0
    else:
        current[1] = temp1-1
    # current[2] = temp2
    # current[5] = temp3
    print(current)


def read_current_input():
    global current
    print current
    while running:

        more_or_less = raw_input("Current (m/l): ")
        temp = current[4]
        temp1 = current[1]
        # temp2 = current[2]
        # temp3 = current[5]
        if more_or_less == "m":
            current = [i+2 for i in current]
            current[4] = temp+1
            current[1] = temp1+1
            # current[2] = temp2
            # current[5] = temp3
        elif more_or_less == "l":
            current = [i-2 for i in current]
            if current[4] <= 2:
                current[4] = 0
            else:
                current[4] = temp-1
            if current[1] <= 2:
                current[1] = 0
            else:
                current[1] = temp1-1
            # current[2] = temp2
            # current[5] = temp3
        else:
            current = [int(i) for i in
                   (more_or_less.split(","))]
        print current


# Main function
def main():
    global running, controlSignal, signal_channel
    this_instant = xRange+1
    t0 = time.time()
    t1 = -1
    safety = 0
    while running:
        try:
            if not stimulation:
                time.sleep(0.001)
            # Control frequency
            # t_diff = time.time() - t1
            # if t_diff < period:
            #     if not (period - t_diff - 0.004) < 0:
            #         time.sleep(period - t_diff - 0.004)
            t1 = time.time()
            time_stamp.append(time.time() - t0)

            # Check if angles are good
            ang1 = angle[-1]
            ang2 = angle[-2]
            if not check_angles(ang1, ang2):
                if safety < 3:
                    safety = safety + 1
                    print("safety +")
                else:
                    print "Bad angles. Aborting."
                    print ang1
                    print ang2
                    if stimulation:
                        stim.stop()
                    running = False
                    break
            else:
                if not safety == 0:
                    print("safety zero")
                    safety = 0

            # Get data from sensors
            control_angle.append(ang1)
            control_speed.append(angSpeed[-1])

            # Calculate error
            if ramps:
                control_error.append(actual_ref_speed[this_instant] - angSpeed[-1])
            else:
                control_error.append(speed_ref - angSpeed[-1])
            # print len(angSpeed)

            # Calculate control signal
            controlSignal.append(control.control(control_error[xRange:]))

            # Calculate stimulation signal
            # print actual_ref_speed[this_instant]
            if ramps:
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
            else:
                signal_channel[0].append(
                    (perfil.left_quad(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))
                signal_channel[1].append(
                    (perfil.left_hams(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))
                signal_channel[2].append(
                    (perfil.left_gluteus(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))
                signal_channel[3].append(
                    (perfil.right_quad(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))
                signal_channel[4].append(
                    (perfil.right_hams(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))
                signal_channel[5].append(
                    (perfil.right_gluteus(angle[-1], angSpeed[-1], speed_ref)) * (controlSignal[-1]))

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
                # print pulse_width
                stim.update(channels, pulse_width, current)

            # running = False
            this_instant += 1
        except ValueError:
            stim.stop()
            running=False
    if stimulation:
        stim.stop()


##########################################################################
##########################   PARAMETERS   ################################
##########################################################################

# IMU addresses
addressPedal = 0
# addressRemoteControl = 3


# Desired control frequency
control_freq = 100
period = 1.0 / control_freq

# Debug mode, for when there's no stimulation
stimulation = False
ui_used = False
GUI = True

# Experiment mode
ramps = False
speed_ref = 350  # Slow speed
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
current_limit = 90

# Angular speed moving average filter size
filter_size = 5

# Ports and addresses
if ui_used:
    ui_port = '/dev/tty.usbmodemFA1341'
    # ui_port = '/dev/ui' # rPi
    ui_serial_port = serial.Serial(port=ui_port, baudrate=115200, timeout=0.01)
portIMU = 'COM6'  # Windows
# portIMU = '/dev/ttyACM0'  # Linux
# portIMU = '/dev/tty.usbmodemFA1331'
# portIMU = get_port('imu')  # Works on Mac. Should also work on Windows.
# portIMU = '/dev/imu' # rPi

if stimulation:
    portStimulator = get_port('stimulator')  # Works only on Mac.
    # portStimulator = '/dev/ttyUSB0' # rPi
    # portStimulator = '/dev/tty.usbserial-HMCX9Q6D' #get_port('stimulator')  # Works only on Mac.
    # portStimulator = 'COM4'
# print portIMU

##########################################################################
##########################################################################
##########################################################################

# Initialize variables
xRange = control_freq * 20
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
    # print actual_ref_speed
else:
    print 'Ramps off'
    for x in range(4000):
        actual_ref_speed.append(speed_ref)
    # print actual_ref_speed
channel_stim = [0 for x in range(number_of_channels)]
controlSignal = [0 for x in range(xRange)]
errorHistory = [0 for x in range(xRange)]
control_error = [0 for x in range(xRange)]
time_stamp = []
wait_time = 0.000
running = False
reading = False
start = False
counter = 1
time_start = time.time()


##########################################################################
###############################   START   ################################
##########################################################################


try:
    print "Hello!"

    # Open ports
    serialPortStimulator = 0
    if stimulation:
        serialPortStimulator = serial.Serial(portStimulator, timeout=1, writeTimeout=1, baudrate=115200)

    # Construct objects
    dng_device = ts_api.TSDongle(com_port=portIMU)
    IMUPedal = dng_device[addressPedal]
    IMUPedal.setEulerAngleDecompositionOrder(3)
    IMUPedal.setCompassEnabled(0)
    IMUPedal.setFilterMode(1)
    IMUPedal.setStreamingTiming(interval=0, delay=0, duration=0, timestamp=False)
    IMUPedal.setStreamingSlots(slot0='getTaredOrientationAsEulerAngles', slot1='getNormalizedGyroRate')
    IMUPedal.tareWithCurrentOrientation()
    IMUPedal.startStreaming()
    dng_device.close()
    # IMURemoteControl = imu.IMU(serialPortIMU, addressRemoteControl)
    stim = 0
    if stimulation:
        stim = stimulator.Stimulator(serialPortStimulator)

    # Setting up
    print "EMA here!"

    # Asking for user input
    channels = 0
    # if stimulation:
    freq = 30
    # int(raw_input("Input frequency: "))
    channels = 119  # 6 Channels
    # Channel 1: Left quads
    # Channel 2: Left hams
    # Channel 3: Left gluteus
    # Channel 4: Nothing
    # Channel 5: Right quads
    # Channel 6: Right hams
    # Channel 7: Right gluteus
    # Channel 8: Nothing

    #int(raw_input("Input channels: "))

    # Main frequencies used on trainings. Uncomment only the one to use.
    # current_str = '0,0,0,0,0,0'  # System check
    # current_str = '2,2,2,2,2,2'  # System check
    current_str = '60,25,59,60,25,59'
    # current_str = '30,0,29,30,0,29'
    # current_str = '60,28,58,60,28,58'
    # current_str = '68,38,62,68,38,62' # only 40hz or lower
    # current_str = '74,44,68,74,2,68' # only 30hz or lower

    # Other frequencies.
    # current_str = '2,0,0,2,0,0'
    # current_str = '60,32,58,60,32,58'
    # current_str = '74,44,68,ls74,44,68' # only 30hz or lower
    # current_str = '62,40,60,62,40,60'
    # current_str = '40,1,1,40,1,1'
    # current_str = '45,4,44,45,4,44'
    # current_str = '50,32,50,50,32,50'
    # current_str = '54,26,42,54,12,42'
    # current_str = '82,16,72,82,16,72'
    #raw_input("Input current: ")
    current = [int(i) for i in
               (current_str.split(","))]

    # Initialize stimulator
    if stimulation:
        print "Initializing stimulator..."
        stim.initialization(freq, channels)
        print "Done"
    else:
        print "Stimulation is deactivated"

    # Ready to go. 
    # print "Whenever you're ready, press button 1 (the left one)!"

    # Wait until the user presses the 'Start' button
    # while not (IMURemoteControl.checkButtons() == 1):
    #     pass

    running = True
    thread.start_new_thread(read_sensors, ())
    if ui_used:
        thread.start_new_thread(user_interface, ())

    print('Ready to go!')


    if ui_used:
        while not start:
            pass
    else:
        raw_input('Press ENTER to start')

    # Keep on until the user presses the "Stop" button
    print "Here we go!"

    # Start main function
    thread.start_new_thread(main, ())
    thread.start_new_thread(read_current_input, ())

    if GUI:
        import realTimePlotter
        graph = realTimePlotter.RealTimePlotter(control_angle, signal_channel[0], signal_channel[1], angSpeed, angSpeed,
                                            controlSignal, actual_ref_speed, control_error, xRange, running)

    else:
        if ui_used:
            while running:
                pass
        else:
            raw_input('Press ENTER to stop')

    try:
        if stimulation:
            stim.stop()
    except Exception:
        print "Can't stop stimulation"
    running = False
    time.sleep(0.2)

    if stimulation:
        stim.stop()

    if ui_used:
        ui_serial_port.write('Fim')

    dng_device = ts_api.TSDongle(com_port=portIMU)
    IMUPedal = dng_device[addressPedal]
    IMUPedal.stopStreaming()
    IMUPedal.close()
    dng_device.close()
    if ui_used:
        ui_serial_port.close()

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
        f.write('Desired frequency: ' + str(control_freq * 1) + '\n')
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

except Exception as err:
    print "Error on the outer loop"
    print(err.args)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    # if serialPortIMU is not None:
    #     serialPortIMU.close()
