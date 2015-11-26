#IMU functions
#import serial
from ema.libs.yei import threespace_api as ts_api

class IMU:
    def __init__(self, config_dict):
        self.config_dict = config_dict
        self.devices = {}

        for name in config_dict['dev_names']:
            dev_type = config_dict['dev_type'][name]

            if dev_type == 'DNG':
                wired_port = config_dict['wired_port'][name]
                self.devices[name] = ts_api.TSDongle(com_port=wired_port)

            elif dev_type == 'WL':
                imu_mode = config_dict['imu_mode'][name]

                if imu_mode == 'wired':
                    wired_port = config_dict['wired_port'][name]
                    self.devices[name] = ts_api.TSWLSensor(com_port=wired_port)

                if imu_mode == 'wireless':
                    wireless_dng = config_dict['wireless_dng'][name]
                    wireless_id = config_dict['wireless_id'][name]

                    self.devices[name] = ts_api.TSWLSensor(logical_id=wireless_id, dongle=self.devices[wireless_dng])

########################################
# Calibration
########################################

    def calibrate(self, name): ## G: beginGyroscopeAutoCalibration, need TSSensor (don't do for dongle)
        dev_type = self.config_dict['dev_type'][name]

        if dev_type == 'WL':
            #print 'calibrate: ', name
            return self.devices[name].beginGyroscopeAutoCalibration()

        else:
            print 'calibrate not defined for dev_type = ', dev_type
            return 0

########################################
# Set euler to YXZ
########################################

    def setEulerToYXZ(self, name): ## G: setEulerAngleDecompositionOrder with angle_order = 1, need TSSensor (don't do for dongle)
        dev_type = self.config_dict['dev_type'][name]

        if dev_type == 'WL':
            #print 'setEulerToYXZ: ', name
            return self.devices[name].setEulerAngleDecompositionOrder(angle_order=0x01)

        else:
            #print 'setEulerToYXZ not defined for dev_type = ', dev_type
            return 0

########################################
# Tare with current orientation
########################################

    def tare(self, name): ## G: tareWithCurrentOrientation, need TSSensor (don't do for dongle)
        dev_type = self.config_dict['dev_type'][name]

        if dev_type == 'WL':
            #print 'tare: ', name
            return self.devices[name].tareWithCurrentOrientation()

        else:
            print 'tare not defined for dev_type = ', dev_type
            return 0

########################################
# Check Buttons
########################################

    def checkButtons(self, name): ## G: getButtonState, works with TSWLSensor (don't do for dongle)
        dev_type = self.config_dict['dev_type'][name]

        if dev_type == 'WL':
            #print 'checkButtons: ', name
            return self.devices[name].getButtonState()

        else:
            print 'checkButtons not defined for dev_type = ', dev_type
            return 0

########################################
# Get Quaternion
########################################

    def getQuaternion(self, name):
        dev_type = self.config_dict['dev_type'][name]

        if dev_type == 'WL':
            #print 'getQuaternion: ', name
            return self.devices[name].getTaredOrientationAsQuaternion()

        else:
            print 'getQuaternion not defined for dev_type = ', dev_type
            return 0

########################################
# Get Euler Angles
########################################

    def getEulerAngles(self, name): ## G: getTaredOrientationAsEulerAngles, need TSSensor (don't do for dongle)
        dev_type = self.config_dict['dev_type'][name]

        if dev_type == 'WL':
            #print 'getEulerAngles: ', name
            return self.devices[name].getTaredOrientationAsEulerAngles()

        else:
            print 'getEulerAngles not defined for dev_type = ', dev_type
            return 0

########################################
# Get Gyro Data
########################################

    def getGyroData(self, name): ## G: getNormalizedGyroRate, need TSSensor (don't do for dongle)
        dev_type = self.config_dict['dev_type'][name]

        if dev_type == 'WL':
            #print 'getGyroData: ', name
            return self.devices[name].getNormalizedGyroRate()

        else:
            print 'getGyroData not defined for dev_type = ', dev_type
            return 0

########################################
# Single Command
########################################

    def singleCommand(self, command): ## G: equivalent to writeRead, but using command bytes directly. delete?
        try:
            if self.serial_port is not None:
                self.serial_port.write(">" + str(self.address) + "," + command + "\n") # e escreve na porta
                dados = readData(self.serial_port)
                dados = dados.split(",")
                if int(dados[0]) == 0:
                    return dados
                else:
                    return "No answer"
            else:
                return 'Port error'

        except ValueError:
            return 'Error'
        return dados

def readData(port): ## G: yei api doesn't do separate reading, no worries. delete.
    dados = ''
    data = ''
    i = 1
    while dados == "":
        port.flush()
        data = port.read(port.inWaiting()) # le da porta bytearray
        dados = data.decode()  # transforma bytearray em string
        i += 1
        if i > 700:
            dados = 'No answer'
            break
    return dados
