#!/usr/bin/env python

import rospy

# import ros msgs
import serial
import ema.modules.imu as imu
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64

import serial
import ema.modules.imu
import ema.modules.stimulator
import time
import math
import numpy
import ema.modules.control
import thread
import sys
import os

xRange = 500
filter_size = 5 ###

angle = []
angle = [0]# for x in range(xRange)]

filtered_angle = []
filtered_angle = [0]# for x in range(xRange)]

angSpeed = []
angSpeed = [0]# for x in range(xRange)]

filtered_speed = []
filtered_speed = [0]# for x in range(xRange)]

def main():
    # init 'imu' node
    rospy.init_node('imu', anonymous=True)

    # list published topics
    pub = rospy.Publisher('imu2', Imu, queue_size=10)
    pub3 = rospy.Publisher('imu3', Imu, queue_size=10)
    pub_angle = rospy.Publisher('angle', Float64, queue_size=10)
    pub_angSpeed = rospy.Publisher('angSpeed', Float64, queue_size=10)

    # config imu

    # fetch a group (dictionary) of parameters
    imu_manager = imu.IMU(rospy.get_param('/ema/imu'))

    counter = 1

    print "Hello, EMA here!"

    print "Beginning calibration..."
    calibrationError = 10
    while calibrationError > 0.1 :
        print "error:", calibrationError
        ang = []
        while(len(ang) < 3):
            imu_manager.setEulerToYXZ('pedal') #IMUPedal.setEulerToYXZ()
            imu_manager.calibrate('pedal') #IMUPedal.calibrate()
            imu_manager.tare('pedal') #IMUPedal.tare()
            ang = imu_manager.getEulerAngles('pedal') #IMUPedal.getEulerAngles()
            #ang = ang.split(",")
        calibrationError = ang[0] + ang[1] + ang[2]#float(ang[3]) + float(ang[4]) + float(ang[5])
    print "Done"

    # Asking for user input
    try:
        freq=int(raw_input("Input frequency (default 50): "))
    except ValueError:
        print "Adopting default value: 50"
        freq = 50

    try:
        channels=int(raw_input("Input channels (default 3): "))
    except ValueError:
        print "Adopting default value: 3"
        channels = 3

    try:
        current_str = raw_input("Input current (default 6,6): ")
        current = [int(i) for i in (current_str.split(","))]
    except ValueError:
        print "Adopting default value: 6,6"
        current = [6,6]

    # define loop rate (in hz)
    rate = rospy.Rate(200)

    # node loop
    while not rospy.is_shutdown():
        # get some work done

        # Get angle position
        ang = imu_manager.getEulerAngles('pedal') #IMUPedal.getEulerAngles()
        #ang = ang.split(",")
        if len(ang) == 3:#6:
            ang = ang[1]#float(ang[4])
            if ang >= 0:
                ang = (ang / math.pi) * 180
            else:
                ang = 360 - ((-(ang) / math.pi) * 180)
            angle.append(ang)

            # Filter the speed
            if counter >= filter_size:
                filtered_angle.append(numpy.median(angle[-filter_size:]))

        # Get angular speed
        speed = imu_manager.getGyroData('pedal')
        if len(speed) == 3:
            speed = float(speed[1])
            speed = speed/(math.pi) * 180
            angSpeed.append(speed)

        # Filter the speed
            if counter >= filter_size:
                filtered_speed.append(numpy.median(angSpeed[-filter_size:]))
        # publish work
        ## send imu data
        imuMsg = Imu()
        imuMsg.header.stamp= rospy.Time.now()
        imuMsg.header.frame_id = 'base_link'

        orientation = imu_manager.getQuaternion('pedal')
        #print "orientation:",orientation

        imuMsg.orientation.x = orientation[0]
        imuMsg.orientation.y = orientation[1]
        imuMsg.orientation.z = orientation[2]
        imuMsg.orientation.w = orientation[3]
        imuMsg.orientation_covariance = [1, 0, 0, 0, 1, 0, 0, 0, 1]

        angular_velocity = imu_manager.getGyroData('pedal')
        #print "angular_velocity:",angular_velocity

        imuMsg.angular_velocity.x = angular_velocity[0]
        imuMsg.angular_velocity.y = angular_velocity[1]
        imuMsg.angular_velocity.z = angular_velocity[2]
        imuMsg.angular_velocity_covariance = [1, 0, 0, 0, 1, 0, 0, 0, 1]

        imuMsg.linear_acceleration.x = 0
        imuMsg.linear_acceleration.y = 0
        imuMsg.linear_acceleration.z = 0
        imuMsg.linear_acceleration_covariance = [1, 0, 0, 0, 1, 0, 0, 0, 1]

        pub.publish(imuMsg)

        ## send imu data
        imuMsg3 = Imu()
        imuMsg3.header.stamp= imuMsg.header.stamp
        imuMsg3.header.frame_id = 'base_link'

        orientation3 = imu_manager.getQuaternion('remote')
        #print "orientation:",orientation

        imuMsg3.orientation.x = orientation3[0]
        imuMsg3.orientation.y = orientation3[1]
        imuMsg3.orientation.z = orientation3[2]
        imuMsg3.orientation.w = orientation3[3]
        imuMsg3.orientation_covariance = [1, 0, 0, 0, 1, 0, 0, 0, 1]

        angular_velocity3 = imu_manager.getGyroData('remote')
        #print "angular_velocity:",angular_velocity

        imuMsg3.angular_velocity.x = angular_velocity3[0]
        imuMsg3.angular_velocity.y = angular_velocity3[1]
        imuMsg3.angular_velocity.z = angular_velocity3[2]
        imuMsg3.angular_velocity_covariance = [1, 0, 0, 0, 1, 0, 0, 0, 1]

        imuMsg3.linear_acceleration.x = 0
        imuMsg3.linear_acceleration.y = 0
        imuMsg3.linear_acceleration.z = 0
        imuMsg3.linear_acceleration_covariance = [1, 0, 0, 0, 1, 0, 0, 0, 1]

        pub3.publish(imuMsg3)

        angleMsg = Float64()
        angleMsg.data = filtered_angle[-1]

        pub_angle.publish(angleMsg)

        angSpeedMsg = Float64()
        angSpeedMsg.data = filtered_speed[-1]

        pub_angSpeed.publish(angSpeedMsg)

        print "%d\t%d\t%.3f\t%.3f\t%.3f\t%.3f" % (len(angle),len(angSpeed),angle[-1],filtered_angle[-1],angSpeed[-1],filtered_speed[-1])

        # sleep until it's time to work again
        rate.sleep()

        counter = counter + 1

    serialPortIMU.close()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
