#!/usr/bin/env python

import rospy

# import ros msgs
import ema.modules.imu as imu
from sensor_msgs.msg import Imu

def main():
    # init imu node
    rospy.init_node('imu', anonymous=True)

    # get imu config
    imu_manager = imu.IMU(rospy.get_param('/ema/imu'))

    # list published topics
    pub = {}
    for name in imu_manager.imus:
        pub[name] = rospy.Publisher(name, Imu, queue_size=10)

    # define loop rate (in hz)
    rate = rospy.Rate(10)

    # node loop
    while not rospy.is_shutdown():

        try:
            timestamp = rospy.Time.now()
            frame_id = 'base_link'

            ## send imu data
            imuMsg = Imu()
            imuMsg.header.stamp = timestamp
            imuMsg.header.frame_id = frame_id

            for name in imu_manager.imus:
                orientation = imu_manager.getQuaternion(name)

                imuMsg.orientation.x = orientation[0]
                imuMsg.orientation.y = orientation[1]
                imuMsg.orientation.z = orientation[2]
                imuMsg.orientation.w = orientation[3]

                angular_velocity = imu_manager.getGyroData(name)

                imuMsg.angular_velocity.x = angular_velocity[0]
                imuMsg.angular_velocity.y = angular_velocity[1]
                imuMsg.angular_velocity.z = angular_velocity[2]

                linear_acceleration = imu_manager.getAccelData(name)

                imuMsg.linear_acceleration.x = -linear_acceleration[0]
                imuMsg.linear_acceleration.y = -linear_acceleration[1]
                imuMsg.linear_acceleration.z = -linear_acceleration[2]

                pub[name].publish(imuMsg)
        except TypeError:
            print 'TypeError occured!'

        # sleep until it's time to work again
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
