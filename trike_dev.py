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
import math
import numpy
import realTimePlotter
import control
import thread

# Initialize variables
xRange = 500
angle = []
angle = [0 for x in range(xRange)]
angSpeed = []
angSpeed = [0 for x in range(xRange)]
filtered_speed = []
filtered_speed = [0 for x in range(xRange)]
signal_femoral = []
signal_femoral = [0 for x in range(xRange)]
signal_gastrocnemius = []
signal_gastrocnemius = [0 for x in range(xRange)]
angSpeedRefHistory = []
angSpeedRefHistory = [0 for x in range(xRange)]
controlSignal = []
controlSignal = [0 for x in range(xRange)]
errorHistory = []
errorHistory = [0 for x in range(xRange)]
time_stamp = []
filter_size = 20 ###
gastrocnemius_max = 500
femoral_max = 500
speed_ref = 300 ###

# Ports and addresses
#portIMU = 'COM4'
portIMU = '/dev/tty.usbmodemfd121'
portStimulator = '/dev/tty.usbserial-HMQYVD6B'
addressPedal = 1
addressRemoteControl = 0


# Main function
def main():
    timeStart = time.clock()
    counter = 1
    while not (IMURemoteControl.checkButtons() == 2):
        
        # Get angle position
        ang = IMUPedal.getEulerAngles()
        ang = ang.split(",")
        if len(ang) == 6:
            ang = float(ang[4])
            if ang >= 0:
                ang = (ang / math.pi) * 180
            else:
                ang = 360 - ((-(ang) / math.pi) * 180)
            angle.append(ang)
        ##############################################
            
        # Get angular speed
        speed = IMUPedal.getGyroData()
        speed = speed.split(",")        
        if len(speed) == 6:            
            speed = float(speed[4])
            speed = speed/(math.pi) * 180
            angSpeed.append(speed)
            angSpeedRefHistory.append(speed_ref)
            errorHistory.append(speed_ref - filtered_speed[-1])
            time_stamp.append(time.clock()-timeStart)    
        ##############################################
                
        # Filter the speed
        if counter >= filter_size:
            filtered_speed.append(numpy.mean(angSpeed[-filter_size:]))
            
        # Calculate control signal
        controlSignal.append(control.control(errorHistory))              
        
        # Calculate stimulation signal
        signal_gastrocnemius.append((perfil.gastrocnemius(angle, speed))*(controlSignal[-1]))
        signal_femoral.append((perfil.femoral(angle, speed))*(controlSignal[-1]))
    
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
        stim_femoral = signal_femoral[-1]*femoral_max
        stim_gastrocnemius = signal_gastrocnemius[-1]*gastrocnemius_max    
        pulse_width = [stim_femoral,stim_gastrocnemius]
        
        # Electrical stimulator signal update
        stim.update(channels, pulse_width, current)
    
        counter += 1   
        
        
    # Stop stimulator
    stim.stop()
    
    # Close ports
    serialPortStimulator.close()
    serialPortIMU.close()
    
    
        
try:
    # Open ports
    serialPortIMU = serial.Serial(portIMU, timeout=1, writeTimeout=1, baudrate=115200)
    serialPortStimulator = serial.Serial(portStimulator, timeout=1, writeTimeout=1, baudrate=115200)
    
    # Construct objects
    IMUPedal = imu.IMU(serialPortIMU,addressPedal)
    IMURemoteControl = imu.IMU(serialPortIMU,addressRemoteControl)
    stim = stimulator.Stimulator(serialPortStimulator)
    
    # Setting up
    print "Hello, EMA here!"
    print "Beginning calibration..."
    calibrationError = 10
    while calibrationError > 0.1 :
        IMUPedal.setEulerToYXZ()
        IMUPedal.calibrate()
        IMUPedal.tare()
        ang = IMUPedal.getEulerAngles()
        ang = ang.split(",")
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
    
    # Ready to go. 
    print "Whenever you're ready, press button 1 (the left one)!"
    
    # Wait until the user presses the 'Start' button
    while not (IMURemoteControl.checkButtons() == 1):
        pass
    
    # Keep on until the user presses the "Stop" button
    print "Here we go!"
    
    # Start main function
    thread.start_new_thread(main, ())
#    main()

    # Start real time plotter
    realTimePlotter.RealTimePlotter(angle, signal_femoral, signal_gastrocnemius, filtered_speed, angSpeed, controlSignal, angSpeedRefHistory, errorHistory, xRange)
    
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
            f.write(str(s*femoral_max) + '\n')
    with open("data_gastrocnemius", 'w') as f:
        for s in signal_gastrocnemius:
            f.write(str(s*gastrocnemius_max) + '\n')   
    with open("data_control", 'w') as f:
        for s in controlSignal:
            f.write(str(s*1) + '\n')    
    
    # Finish
    print "Have a good day!"

except Exception as err:    
    print "Error"
    print(err.args)
    if serialPortIMU is not None:
        serialPortIMU.close()
















