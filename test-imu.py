import threespace_api as ts_api
import time
import sys
import glob
import serial
import math

def get_port():
    """Get the serial port where the device is connected. Only available on Windows and OSX
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :return:
        The serial port where the device is connected
    """
    port = 0
    if sys.platform.startswith('darwin'):
        port = glob.glob('/dev/tty.usbmodem*')[0]
    elif sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(32)]
        for p in ports:
            try:
                s = serial.Serial(p)
                s.close()
                port = p
            except (OSError, serial.SerialException):
                pass
    return port

def threeaxisrot(r11, r12, r21, r31, r32):
    res0 = math.atan2(r31, r32)
    res1 = math.asin(r21)
    res2 = math.atan2(r11, r12)
    return res0, res1, res2

port = 'COM6'
addressPedal = 0
# device0 = ts_api.TSWLSensor(com_port=port)
dng_device = ts_api.TSDongle(com_port=port)
device0 = dng_device[addressPedal]

# If a connection to the COM port fails, None is returned.
if device0 is not None:
    cont = 0
    print(device0)
    # print(device1)
    device0.setStreamingTiming(interval=0,delay=0,duration=1000000,timestamp=True)

    # device0.setEulerAngleDecompositionOrder(2)
    device0.setCompassEnabled(0)
    device0.setFilterMode(10)
    device0.tareWithCurrentOrientation()
    # device0.setStreamingSlots(slot0='getTaredOrientationAsQuaternion')
    # device0.setStreamingSlots(slot0='getTaredOrientationAsEulerAngles')

    print("==================================================")
    print("Getting the streaming batch data.")
    start_time = time.time()
    old_time = 0
    new_time = 0

    data0 = 0
    t = 20
    while time.time() - start_time < t:
        # data0 = device0.getStreamingBatch()

        quat = device0.getTaredOrientationAsQuaternion()

        x = quat[0]
        y = quat[1]
        z = quat[2]
        w = quat[3]

        res = threeaxisrot(-2*(x*y - w*z), w*w - x*x + y*y - z*z, 2*(y*z + w*x), -2*(x*z - w*y), w*w - x*x - y*y + z*z)

        pitch = res[0]
        yaw = res[2]

        if pitch >= 0:
            pitch = (pitch / math.pi) * 180
        else:
            pitch = 360 + ((pitch / math.pi) * 180)

        if yaw >= 0:
            yaw = (yaw / math.pi) * 180
        else:
            yaw = 360 + ((yaw / math.pi) * 180)

        print pitch

        cont += 1

    # Now close the port.
    print 'time: ', time.time()-start_time
    print 'Frequency: ', cont/t
    device0.stopStreaming()
    device0.close()
    device0.close()
