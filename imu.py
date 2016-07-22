#IMU functions
# import serial
import struct

class IMU:
    def __init__(self, port, address):     
        self.serial_port = port
        self.address = address

########################################
# Calibration
########################################
        
    def calibrate(self):
        msg = (">" + str(self.address) + ",165\n").encode()
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
        msg = (">" + str(self.address) + ",16,1\n").encode()
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
        msg = (">" + str(self.address) + ",96\n").encode()
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
                self.serial_port.write(((">" + str(self.address) + ",250\n").encode())) #Get button state) # e escreve na porta
                dados = readData(self.serial_port)
                botao = dados.decode("utf-8").split(",")
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
        msg = (">" + str(self.address) + ",1\n").encode()
        try:                
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados.decode("utf-8")
            else:
                return 'Port error'               
        except ValueError:
            return 'Error'

########################################
# Get Untared Quaternion
########################################

    def getUntaredQuaternion(self):
        msg = bytearray('\xf8\x03\x00\x03')
        # print msg[0]
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = bytearray(readData(self.serial_port))
                f = bytearray(dados[3:7])
                f.reverse()
                x = struct.unpack('f',f)
                f = bytearray(dados[7:11])
                f.reverse()
                y = struct.unpack('f',f)
                f = bytearray(dados[11:15])
                f.reverse()
                z = struct.unpack('f',f)
                f = bytearray(dados[15:19])
                f.reverse()
                w = struct.unpack('f',f)
                q = Quaternion(x[0],y[0],z[0],w[0])
                return q
            else:
                return 'Port error'
        except ValueError:
            print(ValueError.message)
            return 'Error'
            
########################################
# Get Gyro Data
########################################

    def getGyroData(self):
        msg = (">" + str(self.address) + ",33\n").encode()
        try:                
            if self.serial_port is not None:
                self.serial_port.write(msg) # e escreve na porta
                dados = readData(self.serial_port)
                return dados.decode("utf-8")
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
                    return dados.decode("utf-8")
                else:
                    return "No answer"
            else:
                return 'Port error'
            
        except ValueError:
            return 'Error'
        return dados
        
def readData(port):
    #dados = ''
    #data = ''
    #i = 1
    # while dados == "":
    #     port.flush()
    #     data = port.read(port.inWaiting()) # le da porta bytearray
    #     dados = data.decode()  # transforma bytearray em string
    #     i += 1
    #     if i > 700:
    #         dados = 'No answer'
    #         break
    try:
        port.flush()
        while port.inWaiting() == 0:
            #print "Waiting for response"
            pass

        data = port.read(port.inWaiting()) # le da porta bytearray
        return data
        #return dados
    except ValueError:
        print('Error reading data from the serial port')


class Quaternion:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w