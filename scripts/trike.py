#!/usr/bin/env python

import rospy

# import ros msgs
from std_msgs.msg import String

def main():
    # init 'trike' node
    rospy.init_node('trike', anonymous=True)

    # list subscribed topics

    # list published topics
    pub = rospy.Publisher('chatter', String, queue_size=10)

    # fetch config params (don't forget to load trike.yaml to param server)
    fetch_config()

    # init realTimePlotter lists
    init_realtimeplotter_lists()

    # define loop rate (in hz)
    rate = rospy.Rate(10)

    # node loop
    while not rospy.is_shutdown():
        # get some work done
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)

        # publish work
        pub.publish(hello_str)

        # sleep until it's time to work again
        rate.sleep()

def fetch_config():
    global xRange
    global filter_size
    global gastrocnemius_max
    global femoral_max
    global speed_ref
    global portIMU
    global portStimulator
    global addressPedal
    global addressRemoteControl

    # init variables fetched from param server
    xRange = rospy.get_param("xRange")
    filter_size = rospy.get_param("filter_size")
    gastrocnemius_max = rospy.get_param("gastrocnemius_max")
    femoral_max = rospy.get_param("femoral_max")
    speed_ref = rospy.get_param("speed_ref")
    portIMU = rospy.get_param("portIMU")
    portStimulator = rospy.get_param("portStimulator")
    addressPedal = rospy.get_param("addressPedal")
    addressRemoteControl = rospy.get_param("addressRemoteControl")

def init_realtimeplotter_lists():
    global angle
    global angSpeed
    global angSpeedRefHistory
    global filtered_speed
    global signal_femoral
    global signal_gastrocnemius
    global controlSignal
    global errorHistory
    global time_stamp

    # init realTimePlotter lists with zeros
    angle,\
        angSpeed,\
        angSpeedRefHistory,\
        filtered_speed,\
        signal_femoral,\
        signal_gastrocnemius,\
        controlSignal,\
        errorHistory = [[0 for x in range(xRange)] for v in range(8)]

    # init time_stamp as an empty list
    time_stamp = []

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
