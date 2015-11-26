#IMU functions
#import serial
from ema.libs.yei import threespace_api as ts_api

class IMU:
    def __init__(self, port, address):
        self.serial_port = port ## G: no need, get from config
        self.address = address ## G: no need, get from config

########################################
# Calibration
########################################

    def calibrate(self): ## G: beginGyroscopeAutoCalibration, need TSSensor (don't do for dongle)
        msg = ">" + str(self.address) + ",165\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados ## G: do we get the return value for this?

            else:
                return 0
        except ValueError:
            return 0


########################################
# Set euler to YXZ
########################################

    def setEulerToYXZ(self): ## G: setEulerAngleDecompositionOrder with angle_order = 1, need TSSensor (don't do for dongle)
        msg = ">" + str(self.address) + ",16,1\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados ## G: do we get the return value for this?
            else:
                return 0
        except ValueError:
            return 0


########################################
# Tare with current orientation
########################################

    def tare(self): ## G: tareWithCurrentOrientation, need TSSensor (don't do for dongle)
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

    def checkButtons(self): ## G: getButtonState, works with TSWLSensor (don't do for dongle)

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

    def getEulerAngles(self): ## G: getTaredOrientationAsEulerAngles, need TSSensor (don't do for dongle)
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

    def getGyroData(self): ## G: getNormalizedGyroRate, need TSSensor (don't do for dongle)
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
