# -*- coding: utf-8 -*-
"""
Created on Thu Apr 09 14:53:04 2015

@author: Wall-e
"""

import serial
serial_port = serial.Serial("COM9", timeout=1, writeTimeout=1, baudrate=115200)

#msg = ">1,165\n".encode() #begin gyro auto-calibration
#msg = ">1,16,1\n".encode() #set euler to YXZ
#msg = ">1,96\n".encode() #Tare with current orientation
#msg = ">1,202\n".encode() #Get battery percent remaining
#msg = ">1,250\n".encode() #Get button state
print("==================================================")
print("Executando comando.")
try:    
    if serial_port is not None:
        dados = ""
        i=1
        serial_port.write(msg) # e escreve na porta
        while dados == "":            
            serial_port.flush()
            data = serial_port.read(serial_port.inWaiting()) # le da porta bytearray
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
    serial_port.close()
    print("==================================================")
    
print "FIM DA EXECUCAO"
serial_port.close()
print("==================================================")