#!/usr/bin/env python

import rospy

# import ros msgs
from std_msgs.msg import String

def main():
    # init 'trike' node
    rospy.init_node('trike', anonymous=True)

    # list subscribed topics

    # list published topics

    # define loop rate (in hz)
    rate = rospy.Rate(10)

    # node loop
    while not rospy.is_shutdown():
        # get some work done
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)

        # publish work

        # sleep until it's time to work again
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
