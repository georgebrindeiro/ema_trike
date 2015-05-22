#IMU functions
#import serial

class IMU:
    def __init__(self, port, address):     
#        self.serial_port = serial.Serial(port, timeout=1, writeTimeout=1, baudrate=115200)
        self.serial_port = port
        self.address = address

########################################
# Calibration
########################################
        
    def calibrate(self):
#        print("==================================================")
#        print("Executando comando.")
        msg = ">" + str(self.address) + ",165\n".encode()
        try:                
            if self.serial_port is not None:
                dados = ""
                i=1
                self.serial_port.write(msg) # e escreve na porta
                while dados == "":            
                    self.serial_port.flush()
                    data = self.serial_port.read(self.serial_port.inWaiting()) # le da porta bytearray
                    dados = data.decode()  # transforma bytearray em string
                    i += 1
                    if i > 10000:
#                        print "Sem resposta."
                        dados = 'No answer'
                        break
                return dados
#                print "Resposta: " + dados       
#                print i
                      
            else:
                return 0
#                print("Comando perdido")
#                print("==================================================")                
        except ValueError:
            return 0
#            print "FIM DA EXECUCAO"
#            self.serial_port.close()
#            print("==================================================")
            
            
########################################
# Set euler to YXZ
########################################
        
    def setEulerToYXZ(self):
#        print("==================================================")
#        print("Executando comando.")
        msg = ">" + str(self.address) + ",16,1\n".encode()
        try:                
            if self.serial_port is not None:
                dados = ""
                i=1
                self.serial_port.write(msg) # e escreve na porta
                while dados == "":            
                    self.serial_port.flush()
                    data = self.serial_port.read(self.serial_port.inWaiting()) # le da porta bytearray
                    dados = data.decode()  # transforma bytearray em string
                    i += 1
                    if i > 10000:
#                        print "Sem resposta."
                        dados = 'No answer'
                        break
                return dados
#                print "Resposta: " + dados       
#                print i
                      
            else:
                return 0
#                print("Comando perdido")
#                print("==================================================")                
        except ValueError:
            return 0
#            print "FIM DA EXECUCAO"
#            self.serial_port.close()
#            print("==================================================")
            
            
########################################
# Tare with current orientation
########################################
        
    def tare(self):
#        print("==================================================")
#        print("Executando comando.")
        msg = ">" + str(self.address) + ",96\n".encode()
        try:                
            if self.serial_port is not None:
                dados = ""
                i=1
                self.serial_port.write(msg) # e escreve na porta
                while dados == "":            
                    self.serial_port.flush()
                    data = self.serial_port.read(self.serial_port.inWaiting()) # le da porta bytearray
                    dados = data.decode()  # transforma bytearray em string
                    i += 1
                    if i > 10000:
#                        print "Sem resposta."
                        dados = 'No answer'
                        break
                return dados
#                print "Resposta: " + dados       
#                print i
                      
            else:
                return 0
#                print("Comando perdido")
#                print("==================================================")                
        except ValueError:
            return 0
#            print "FIM DA EXECUCAO"
#            self.serial_port.close()
#            print("==================================================")




########################################
# Check Buttons
########################################

    def checkButtons(self):
        
    #    print "Check buttons"
        try:  
    #        print "Diff = " + str(tDiff)
            if self.serialPort is not None:
                i = 1
               
    #        print "checando botoes"
            dados = ""
            
            self.serialPort.write((">" + str(self.address) + ",250\n".encode())) #Get button state) # e escreve na porta
            while dados == "":            
                    self.serial_port.flush()
                    data = self.serial_port.read(self.serial_port.inWaiting()) # le da porta bytearray
                    dados = data.decode()  # transforma bytearray em string
                    i += 1
                    if i > 10000:
#                        print "Sem resposta."
                        dados = 'No answer'
                        return dados

    #        print "Dados: " + dados
            botao = dados.split(",")
            if len(botao) == 4:
    #                    print "botao"                    
                botao = botao[3]
    #                    print botao
                if (int(botao) == 1):                                    
                    return 1
                elif (int(botao) == 2):                  
                    return 2
                else:
                    return 0
    #        else:
    #            print("Comando perdido")
    #        
    #            print("==================================================")
              
        except ValueError:            
            return 'Error'



########################################
# Get Euler Angles
########################################

    def get_euler_angles(self):
#        print("==================================================")
#        print("Executando comando.")
        msg = ">" + str(self.address) + ",1\n".encode()        
        try:                
            if self.serial_port is not None:
                dados = ""
                i=1
                self.serial_port.write(msg) # e escreve na porta
                while dados == "":            
                    self.serial_port.flush()
                    data = self.serial_port.read(self.serial_port.inWaiting()) # le da porta bytearray
                    dados = data.decode()  # transforma bytearray em string
                    i += 1
                    if i > 10000:
#                        print "Sem resposta."
                        dados = 'No answer'
                        break
                return dados
#                print "Resposta: " + dados   
#                print i                   
            else:
                return 0
#                print("Comando perdido")            
#                print("==================================================")                
        except ValueError:
            return 0
#            print "FIM DA EXECUCAO"
#            self.serial_port.close()
#            print("==================================================")
            
            
########################################
# Single Command
########################################
            
    def singleCommand(self, command):
        try:    
            if self.serial_port is not None:
                dados = ""
                i=1
                self.serial_port.write(">" + str(self.address) + "," + command + "\n") # e escreve na porta
                while dados == "":            
                    self.serial_port.flush()
                    data = self.serial_port.read(self.serial_port.inWaiting()) # le da porta bytearray
                    dados = data.decode()  # transforma bytearray em string
                    i += 1
                    if i > 10000:
#                        print "Sem resposta."
                        dados = 'No answer'
                        break
                dados = dados.split(",")
#                print dados
                if int(dados[0]) == 0:
    #                out = 1
                    return dados
                else:
                    return "No answer"
            else:
                return 0
            
        except ValueError:
            return 0
        return dados