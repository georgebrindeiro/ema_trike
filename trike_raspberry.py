import serial
import time
import thread
import math

#from pylab import *

address = 1
addressButon = 0
global run
run = True

readingAngles = False
usingPort = False
command = 1
port_IMU = "/dev/ttyACM0"
port_stim = "/dev/ttyUSB0"
time_lim = 5

old_current = 0
old_pulse_width = 0

def singleCommand(address, command):
    global serial_port
    out = 0
    try:    
        if serial_port_IMU is not None:
            dados = ""
            i=1
            serial_port_IMU.write(">" + address + "," + command + "\n") # e escreve na porta
            while dados == "":            
                serial_port_IMU.flush()
                data = serial_port_IMU.read(serial_port_IMU.inWaiting()) # le da porta bytearray
                dados = data.decode()  # transforma bytearray em string
                i += 1
                if i > 10000:
                    
                    break
            dados = dados.split(",")
            print dados
            if int(dados[0]) == 0:
                out = 1
            else:
                print "Did not get answer"
        else:
            print "Nao abriu a porta"
            pass
        
    except ValueError:
        pass
    return out
    
def getEulerAngles():
    global run, readingAngles, usingPort, channels, pulse_width, old_current, old_pulse_width
    print("Getting euler angles.")
    i = 1
    while (i<=10000) & run :
        t0 = time.clock()
        if not usingPort:
            usingPort = True            
            serial_port_IMU.write(msg) # e escreve na porta
            usingPort = False
        
        if not usingPort:
            dados = ""
#            current = 0
            while dados == "":
                usingPort = True
                serial_port_IMU.flush()
                data = serial_port_IMU.read(serial_port_IMU.inWaiting()) # le da porta bytearray
                dados = data.decode()  # transforma bytearray em string
                usingPort = False
                t = time.clock()
                if not dados == "":                
    #                print "Leitura: %i" %i
    #                print "Dados: " + dados
                    ang = dados.split(",")
                    if len(ang) == 6:
                        ang = float(ang[4])
                        if ang >= 0:
                            ang = (ang / math.pi) * 180
                        else:
                            ang = 360 - ((-(ang) / math.pi) * 180)
                            ######################################################################
                        print ang
#                        if (ang > 320) & (ang < 90):
                        if (ang < 240) & (ang > 135):
                            pulse_width = [0, 420]
#                            current = [4,6]
                            if (current != old_current) | (pulse_width != old_pulse_width):
                                old_current = current 
                                old_pulse_width = pulse_width
                                update(channels, pulse_width, current) #atualiza
#                        elif (ang > 90) & (ang < 250):
                        elif (ang > 315) | (ang < 60):
#                            current = [6,4]
                            pulse_width = [380, 0]
                            if (current != old_current) | (pulse_width != old_pulse_width):
                                old_current = current
                                old_pulse_width = pulse_width
                                update(channels, pulse_width, current) #atualiza
                        else:
#                            current = [0,0]
                            pulse_width = [0, 0]
                            if (current != old_current) | (pulse_width != old_pulse_width):
                                old_current = current
                                old_pulse_width = pulse_width
                                update(channels, pulse_width, current) #atualiza
                        
#                    else:
#                        continue
    #            print dados
            t=(t-t0)*1000
    #            print "tempo de resposta: %f" %t, "ms\n\n"
            i += 1  
            checkButtons()
    if run:
        serial_port_IMU.close()    
    readingAngles = False
    return

def checkButtons():
    global run, time_lim, serial_port, readingAngles, usingPort
#    print "Check buttons"
    try:  
#        print "Diff = " + str(tDiff)
        if serial_port_IMU is not None:
            i = 1
            j = 1
            
           
#        print "checando botoes"
        dados = ""
        if not usingPort:
                usingPort = True
                serial_port_IMU.write((">" + str(addressButon) + ",250\n".encode())) #Get button state) # e escreve na porta
                usingPort = False
        while dados == "":            
            
            if not usingPort:
                usingPort = True
                serial_port_IMU.flush()
                data = serial_port_IMU.read(serial_port_IMU.inWaiting()) # le da porta bytearray
                usingPort = False
            dados = data.decode()  # transforma bytearray em string
            j += 1
            if j > 10000:
#                        print "Sem resposta."
                break

        i += 1
#        print "Dados: " + dados
        botao = dados.split(",")
        if len(botao) == 4:
#                    print "botao"                    
            botao = botao[3]
#                    print botao
            if (int(botao) == 1) & (not readingAngles):
                print "botao 1"                        
                run = True                        
                thread.start_new_thread( getEulerAngles, () )
                readingAngles = True
                return 1
            elif (int(botao) == 2) & readingAngles:
                print "Good Bye!"
                run = False 
                return 2
    
#        else:
#            print("Comando perdido")
#        
#            print("==================================================")
          
    except ValueError:
        print "Erro. FIM DA EXECUCAO"
        serial_port_IMU.close()
        print("==================================================")
    return 0
    
def initialization(freq, channels):
#    try:
    
    #valores para teste#
    ts1 = round((1/float(freq))*1000)
    print ts1
    ts2 = 1.5
    main_time = int(round((ts1 - 1) / 0.5))
#    main_time = int(round(ts1))
    group_time = int(round((ts2 - 1.5) / 0.5))
    channel_stim = channels
    channel_lf = 0
    n_factor = 0
    check = int((n_factor + channel_stim + channel_lf + group_time + main_time)%8)
    
    init_1 = (1<<7) | (0<<6) | (check<<2) | (n_factor>>1)
    init_2 = ((n_factor&1)<<6) | (channel_stim>>2)
    init_3 = ((channel_stim & 3) << 5) | (channel_lf >> 3)
    init_4 = ((channel_lf & 7) << 4) | (group_time >> 3)
    init_5 =  ((group_time & 7) << 4) | (main_time >> 7)
    init_6 = main_time & 127
#        
#        print(group_time)
#        print(init_1)
#        print(init_2)
#        print(init_3)
#        print(init_4)
#        print(init_5)
#        print(init_6)
    
    init = bytearray([init_1, init_2, init_3, init_4, init_5, init_6])
    
    dados = ""
    i=1
    serial_port_stim.write(init) # e escreve na porta
    while dados == "":   
#            print "reading"
        serial_port_stim.flush()
        data = serial_port_stim.read(serial_port_stim.inWaiting()) # le da porta bytearray
        dados = data.decode()  # transforma bytearray em string
        i += 1
        if i > 10000:
            print "no answer"
            break        
        
    dados = data.decode()  # transforma bytearray em string
#        print "resposta: " + dados
#        print data
        
#    except ValueError:
#        print("Error (initialization)")
        
    return
    
def stop():
    try:
        stop_1 = 192
        stop = bytearray([stop_1])  
        i=1
        serial_port_stim.write(stop) # e escreve na porta
        data = 0
        while not data:   
#            print "reading"
            serial_port_stim.flush()
            data = serial_port_stim.read(serial_port_stim.inWaiting()) # le da porta bytearray
    #        dados = data.decode()  # transforma bytearray em string
            i += 1
            if i > 10000:
#                print "no answer"
                break        
            
#        dados = data.decode()  # transforma bytearray em string
#        print "resposta: " + dados
        
    except ValueError:
        print("Error (stop)")
        
    return
    
def update(channels, width, current):
    
    try:
        
        #valores para teste#
#        for i in width:
#            pulse_width(i) = width
        pulse_width = width
        pulse_current = current
        mode = 0
#        a = sum(pulse_width)
#        print type(width[0])
#        pulse_width = [200]
#        pulse_current = [4]
        check = int((mode + sum(pulse_width) + sum(pulse_current))%32)
        init_b = []
        for i in range(len(width)*3+1):
            init_b.append(0)
        init_b[0] = (1<<7) | (1<<5) | (check) 
        for i in range(len(width)):         
            init_b[i*3+1] = (mode<<5) | (pulse_width[i]>>7)
            init_b[i*3+2] = (pulse_width[i] & 127)
            init_b[i*3+3] = pulse_current[i]
        
#        print(init_1)
#        print(init_2)
#        print(init_3)
#        print(init_4)
        
#        init(1) = init_b(1)

        init = bytearray(init_b)
        
        i=0
        
        
        t0 = time.clock()
        serial_port_stim.write(init) # e escreve na porta
        dados = ""
    
        while dados == "":   
#            print "reading"
            serial_port_stim.flush()
            data = serial_port_stim.read(serial_port_stim.inWaiting()) # le da porta bytearray
            dados = data.decode()  # transforma bytearray em string
            i += 1
            if i > 10000:
#                print "no answer"
                break        
            
        dados = data.decode()  # transforma bytearray em string
#        print "resposta: " + dados
#        print data
                    
#        
#        serial_port_stim.flush()
#        data = serial_port_stim.read(1) # le da porta bytearray
        t = time.clock()
            
        dados = data.decode()  # transforma bytearray em string
#        print "resposta:" + dados
#            print dados
        
        t=(t-t0)*1000
#            print "tempo de resposta: %f" %t, "ms\n\n"
        i+=1
              
    except ValueError:
        print("Error (update)")
        
    return
    
msg = ">" + str(address) + "," + str(command) + "\n".encode() #transforma o comando de string para bytearray
    
serial_port_IMU = serial.Serial(port_IMU, timeout=1, writeTimeout=1, baudrate=115200)
serial_port_stim = serial.Serial(port_stim, timeout=1, writeTimeout=1, baudrate=115200, dsrdtr=True)

print("==================================================")


try:  
    
    if serial_port_IMU is not None:
        print "Beggining calibration..."
        if singleCommand(str(address),"16,1") & singleCommand(str(address),"165") & singleCommand(str(address),"96"):
            print "Calibration done."
            singleCommand(str(address),"1")
                      
#            thread.start_new_thread( checkButtons, () )
#            thread.start_new_thread( getEulerAngles, () )
#            run = False
                      
            if serial_port_stim is not None:
                print "Hello!"
                freq=int(raw_input("Input frequency: "))
                channels=int(raw_input("Input channels: "))
                print "Initilizing..."
                initialization(freq, channels)
                print "DONE"
                pulse_width_str = raw_input("Input pulse width: ")
                pulse_width = [int(i) for i in (pulse_width_str.split(","))]
                old_pulse_width = pulse_width
                current_str = raw_input("Input current: ")
                current = [int(i) for i in (current_str.split(","))]
                old_current = current
                print "Whenever you're ready, press button 1 (the left one)"  
            while not (checkButtons() == 1):
                pass
            print "Updating..."
            update(channels,pulse_width,current)
            print "DONE"            
            while run:
               
                
#                raw_input("Press any key")  
#                print "Stopping..."
                
                 
                                
                
                pass
            stop()
            print "Good Bye!" 
        serial_port_stim.close()
    else:
        print("Comando perdido")
    
        print("==================================================")
        
except ValueError:
    print "ERRO. FIM DA EXECUCAO"
    serial_port_IMU.close()
    serial_port_stim.close()
    
print "FIM DA EXECUCAO"



