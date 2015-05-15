#IMU functions
import serial

class IMU:
    def __init__(self, port):     
        self.serial_port = serial.Serial(port, timeout=1, writeTimeout=1, baudrate=115200)
        
    def calibrate(self):
        print("==================================================")
        print("Executando comando.")
        msg = ">1,165\n".encode()
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
                        print "Sem resposta."
                        break
        
                
                    
                print "Resposta: " + dados       
                      
            else:
                print("Comando perdido")
            
                print("==================================================")
                
        except ValueError:
            print "FIM DA EXECUCAO"
            self.serial_port.close()
            print("==================================================")

    def get_euler_angles(self):
        print("==================================================")
        print("Executando comando.")
        msg = ">1,1\n".encode()        
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
                        print "Sem resposta."
                        break
        
                
                    
                print "Resposta: " + dados       
                      
            else:
                print("Comando perdido")
            
                print("==================================================")
                
        except ValueError:
            print "FIM DA EXECUCAO"
            self.serial_port.close()
            print("==================================================")