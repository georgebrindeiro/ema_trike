#!/usr/bin/env python

import rospy

# import ros msgs
import ema.modules.imu as imu
from sensor_msgs.msg import Imu

import math

angle = []
angle = [0]

angSpeed = []
angSpeed = [0]

def main():
    global imu_manager

    # init 'imu' node
    rospy.init_node('imu', anonymous=True)

    # list published topics
    pub = rospy.Publisher('imu2', Imu, queue_size=10)
    pub3 = rospy.Publisher('imu3', Imu, queue_size=10)

    # config imu

    # fetch a group (dictionary) of parameters
    imu_manager = imu.IMU(rospy.get_param('/ema/imu'))

    print "Hello, EMA here!"

    autocalibrate()

    # define loop rate (in hz)
    rate = rospy.Rate(10)

    # node loop
    while not rospy.is_shutdown():
        # get some work done

        # Get angle position
        ang = imu_manager.getEulerAngles('pedal')

        if len(ang) == 3:
            ang = ang[1]
            if ang >= 0:
                ang = (ang / math.pi) * 180
            else:
                ang = 360 - ((-(ang) / math.pi) * 180)
            angle.append(ang)

        # Get angular speed
        speed = imu_manager.getGyroData('pedal')

        if len(speed) == 3:
            speed = float(speed[1])
            speed = speed/(math.pi) * 180
            angSpeed.append(speed)

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

        print "%d\t%d\t%.3f\t%.3f" % (len(angle),len(angSpeed),angle[-1],angSpeed[-1])

        # sleep until it's time to work again
        rate.sleep()

def autocalibrate():
    global imu_manager

    dev_names = imu_manager.config_dict['dev_names']
    dev_types = imu_manager.config_dict['dev_type']

    for name in dev_names:
        dev_type = dev_types[name]

        if dev_type == 'WL':
            print "Calibrating", name
            calibrationError = 10
            while calibrationError > 0.1 :
                ang = []
                while(len(ang) < 3):
                    imu_manager.setEulerToYXZ(name)
                    imu_manager.calibrate(name)
                    imu_manager.tare(name)
                    ang = imu_manager.getEulerAngles(name)
                calibrationError = ang[0] + ang[1] + ang[2]
                print "Error:", calibrationError
            print "Done"

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
