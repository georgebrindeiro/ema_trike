#IMU functions
#import serial
from ema.libs.yei import threespace_api as ts_api

class IMU:
    def __init__(self, port, address):
        self.serial_port = port
        self.address = address

########################################
# Calibration
########################################

    def calibrate(self):
        msg = ">" + str(self.address) + ",165\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados

            else:
                return 0
        except ValueError:
            return 0


########################################
# Set euler to YXZ
########################################

    def setEulerToYXZ(self):
        msg = ">" + str(self.address) + ",16,1\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados
            else:
                return 0
        except ValueError:
            return 0


########################################
# Tare with current orientation
########################################

    def tare(self):
        msg = ">" + str(self.address) + ",96\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados
            else:
                return 0
        except ValueError:
            return 0




########################################
# Check Buttons
########################################

    def checkButtons(self):

        try:
            if self.serial_port is not None:
                self.serial_port.write((">" + str(self.address) + ",250\n".encode())) #Get button state) # e escreve na porta
                dados = readData(self.serial_port)
                botao = dados.split(",")
                if len(botao) == 4:
                    botao = botao[3]
                    if (int(botao) == 1):
                        return 1
                    elif (int(botao) == 2):
                        return 2
                    else:
                        return 0

        except ValueError:
            return 'Error'



########################################
# Get Euler Angles
########################################

    def getEulerAngles(self):
        msg = ">" + str(self.address) + ",1\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados
            else:
                return 'Port error'
        except ValueError:
            return 'Error'

########################################
# Get Gyro Data
########################################

    def getGyroData(self):
        msg = ">" + str(self.address) + ",33\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados
            else:
                return 'Port error'
        except ValueError:
            return 'Error'


########################################
# Single Command
########################################

    def singleCommand(self, command):
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

def readData(port):
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

def test():
    device = ts_api.TSWLSensor(com_port='/dev/ttyACM0')

    ## If a connection to the COM port fails, None is returned.
    if device is not None:
        ## Now we can start getting information from the device.
        ## The class instances have all of the functionality that corresponds to the
        ## 3-Space Sensor device type it is representing.
        print("==================================================")
        print("Getting the filtered tared quaternion orientation.")
        quat = device.getTaredOrientationAsQuaternion()
        if quat is not None:
	    print(quat)
        print("==================================================")
        print("Getting the raw sensor data.")
        data = device.getAllRawComponentSensorData()
        if data is not None:
	    print("[%f, %f, %f] --Gyro\n"
	          "[%f, %f, %f] --Accel\n"
	          "[%f, %f, %f] --Comp" % data)
        print("==================================================")
        print("Getting the LED color of the device.")
        led = device.getLEDColor()
        if led is not None:
	    print(led)
        print("==================================================")

        ## Now close the port.
        device.close()
