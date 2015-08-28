#!/usr/bin/env python

import rospy

# import ros msgs
from std_msgs.msg import String

def main():
    # init 'trike' node
    rospy.init_node('control', anonymous=True)

    # list subscribed topics
    ## add imu angle
    ## add imu speed

    # list published topics
    ## add stim signal updates

    # define loop rate (in hz)
    rate = rospy.Rate(10)

    # node loop
    while not rospy.is_shutdown():
        # get some work done
        ## get current angle position
        ## get current angle speed and filter it
        ## calculate control signal
        ## saturate and scale control signal

        # publish work
        ## send stim update

        # sleep until it's time to work again
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
