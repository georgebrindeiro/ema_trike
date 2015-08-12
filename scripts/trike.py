#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # fetch config file to initialize system variables
    xRange = rospy.get_param("xRange")
    filter_size = rospy.get_param("filter_size")
    gastrocnemius_max = rospy.get_param("gastrocnemius_max")
    femoral_max = rospy.get_param("femoral_max")
    speed_ref = rospy.get_param("speed_ref")
    portIMU = rospy.get_param("portIMU")
    portStimulator = rospy.get_param("portStimulator")
    addressPedal = rospy.get_param("addressPedal")
    addressRemoteControl = rospy.get_param("addressRemoteControl")

    # Initialize realTimePlotter lists
    angle,angSpeed,angSpeedRefHistory,filtered_speed, \
        signal_femoral,signal_gastrocnemius, \
        controlSignal,errorHistory = [[0 for x in range(xRange)] for v in range(8)]
    time_stamp = []

    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
