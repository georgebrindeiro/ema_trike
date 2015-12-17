#!/usr/bin/env python

import rospy
import ema.modules.control as control

# import ros msgs
from sensor_msgs.msg import Imu
from ema_common_msgs.msg import Stimulator

# import utilities
from math import pi
from tf import transformations

# global variables
angle = [0,0]
speed = [0,0]
speed_ref = 300
speed_err = [0,0]
time = [0,0]
pw_left = [0,0]
pw_right = [0,0]


def callback(data):
    # get timestamp
    time.append(data.header.stamp)

    # get angle position
    qx,qy,qz,qw = data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w
    euler = transformations.euler_from_quaternion([qx, qy, qz, qw], axes='syxz')
    if euler[0] >= 0:
        angle.append(euler[0]*(180/pi))
    else:
        angle.append(360+euler[0]*(180/pi))
        
    # get angular speed
    speed.append(data.angular_velocity.y*(180/pi))

    # get error
    speed_err.append(speed_ref - speed[-1])

    # print latest
    #print time[-1], angle[-1], speed[-1], speed_err[-1]

def main():
    # init control node
    controller = control.Control(rospy.init_node('control', anonymous=False))
    
    # get control config
    config_dict = rospy.get_param('/ema_trike/control')
    
    # list subscribed topics
    sub = rospy.Subscriber('imu/pedal', Imu, callback = callback)
    
    # list published topics
    pub = rospy.Publisher('stimulator/ccl_update', Stimulator, queue_size=10)
    
    # define loop rate (in hz)
    rate = rospy.Rate(10)
    
    # build basic stimulator message
    stimMsg = Stimulator()
    stimMsg.channel = [1, 2]
    stimMsg.mode = ['single', 'single']
    stimMsg.pulse_current = [6, 6]
    
    # node loop
    while not rospy.is_shutdown():
        # calculate control signal
        pwl, pwr = controller.calculate(angle[-1], speed[-1], speed_ref, speed_err)
        
        # send stimulator update
        stimMsg.pulse_width = [pw_left[-1], pw_right[-1]]
        pub.publish(stimMsg)
        
        # store control signal for plotting
        pw_left.append(pwl)
        pw_right.append(pwr)
        
        # wait for next control loop
        rate.sleep()
        
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
