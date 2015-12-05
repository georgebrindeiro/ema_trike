#!/usr/bin/env python

import rospy

# import ros msgs
import ema.modules.stimulator as stimulator
#from ema_common_msgs.msg import Stimulator
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def main():
    # init stimulator node
    rospy.init_node('stimulator', anonymous=True)

    # get stimulator config
    stim_manager = stimulator.Stimulator(rospy.get_param('/ema/stimulator'))

    # list subscribed topics
    sub = {}
    for channel in range(1,9):
        sub[channel] = rospy.Subscriber('ch'+str(channel), String, callback)

    sub_all = rospy.Subscriber('all', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
