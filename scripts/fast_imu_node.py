#!/usr/bin/env python

import rospy

# import ros msgs
from ema.libs.yei import threespace_api as ts_api
from sensor_msgs.msg import Imu
from std_msgs.msg import Int8

def main():
    # init imu node
    rospy.init_node('imu', anonymous=False)

    # list published topics
    imu_names = ['pedal', 'remote']
    pub = {}
    pub['pedal'] = rospy.Publisher('imu/' + 'pedal', Imu, queue_size=10)
    pub['remote' + '_buttons'] = rospy.Publisher('imu/' + 'remote' + '_buttons', Int8, queue_size=10)

    # define loop rate (in hz)
    rate = rospy.Rate(50)
    
    # connect to dongle
    dongle = ts_api.TSDongle(com_port='/dev/ttyACM0')
    pedal = ts_api.TSWLSensor(logical_id=5, dongle=dongle)
    remote = ts_api.TSWLSensor(logical_id=0, dongle=dongle)
    
    # configure streaming timing
    pedal.setStreamingTiming(interval=0, duration=0xFFFFFFFF, delay=0)

    remote.setStreamingTiming(interval=0, duration=0xFFFFFFFF, delay=0)

    # configure streaming slots
    pedal.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
                            slot1='getNormalizedGyroRate')

    remote.setStreamingSlots(slot0='getButtonState')
        
    # start streaming
    pedal.startStreaming()
    remote.startStreaming()
    
    # node loop
    while not rospy.is_shutdown():
        
        # get pedal streaming data
        imuMsg = Imu()
        imuMsg.header.stamp = rospy.Time.now()
        imuMsg.header.frame_id = 'pedal_link'

        streaming_data = pedal.getStreamingBatch()
        
        idx = 0
        
        imuMsg.orientation.x = streaming_data[idx]
        imuMsg.orientation.y = streaming_data[idx+1]
        imuMsg.orientation.z = streaming_data[idx+2]
        imuMsg.orientation.w = streaming_data[idx+3]
            
        idx = idx + 4
            
        imuMsg.angular_velocity.x = streaming_data[idx]
        imuMsg.angular_velocity.y = streaming_data[idx+1]
        imuMsg.angular_velocity.z = streaming_data[idx+2]

        pub['pedal'].publish(imuMsg)
        
        # get remote streaming data
        streaming_data = remote.getStreamingBatch()
            
        buttons = Int8(streaming_data)
        
        pub['remote' + '_buttons'].publish(buttons)

        # sleep until it's time to work again
        rate.sleep()
        
    # cleanup
    pedal.stopStreaming()
    remote.stopStreaming()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
