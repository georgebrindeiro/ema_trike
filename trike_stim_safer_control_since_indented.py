import serial
import time
import thread
import math
import numpy
import pylab
#import pickle

#from pylab import *

address = 1#1
addressButon = 7#0
global run
run = True

readingAngles = False
usingPort = False
command1 = 1 #get Euler angles
command2 = 33 #get gyro data
#port_IMU = "/dev/tty.usbmodemfd121"
#port_stim = "/dev/tty.usbserial-HMQYVD6B"
port_IMU = "/dev/ttyACM0"#"/dev/tty.usbmodemFD1231"
port_stim = "/dev/ttyUSB0"#"/dev/tty.usbserial-HMCX9Q6D"
time_lim = 5
filter_size = 20 ###
stim_max = 500
#femoral_max = 500
old_signal_gastrocnemius = 0
old_signal_femoral = 0
old_signal_gluteos_e = 0
old_signal_gluteos_d = 0
old_signal_hamstring_e = 0
old_signal_hamstring_d = 0
scale = 1.2
delay = 0.00

old_current = 0
old_pulse_width = 0

speed_ref = 300 ###
speed_actual = 0
speed_max = 1000

####################################
####################################
# Grafico
xRange = 500
xAchse=pylab.arange(0,xRange,1)
yAchse=pylab.array([0]*xRange)

fig = pylab.figure(1, figsize=(13,10))
ax = fig.add_subplot(411)
ax.grid(True)
ax.set_title("Realtime Cycling Plot")
ax.set_xlabel("")
ax.set_ylabel("Angle")
ax.axis([0,xRange,-1.5,1.5])
line1=ax.plot(xAchse,yAchse,'-')
#line2 = ax.plot(xAchse,yAchse,'-')
#line3=ax.plot(xAchse,yAchse,'-')
#line4=ax.plot(xAchse,yAchse,'-')

ax2 = fig.add_subplot(412)
ax2.grid(True)
ax2.set_title("")
ax2.set_xlabel("")
ax2.set_ylabel("Stimulation")
ax2.axis([0,xRange,-1.5,1.5])
line3=ax2.plot(xAchse,yAchse,'-')
line4=ax2.plot(xAchse,yAchse,'-')
line9=ax2.plot(xAchse,yAchse,'-')
line10=ax2.plot(xAchse,yAchse,'-')
line11=ax2.plot(xAchse,yAchse,'-')
line12=ax2.plot(xAchse,yAchse,'-')

ax3 = fig.add_subplot(413)
ax3.grid(True)
ax3.set_title("")
ax3.set_xlabel("")
ax3.set_ylabel("Speed")
ax3.axis([0,xRange,-1.5,1.5])
line5=ax3.plot(xAchse,yAchse,'-')
line6=ax3.plot(xAchse,yAchse,'-')
line8=ax3.plot(xAchse,yAchse,'-')

ax4 = fig.add_subplot(414)
ax4.grid(True)
ax4.set_title("")
ax4.set_xlabel("Time")
ax4.set_ylabel("Control")
ax4.axis([0,xRange,-1.5,1.5])
line7=ax4.plot(xAchse,yAchse,'-')

manager = pylab.get_current_fig_manager()

####################################
####################################

def RealtimePloter(arg):
  global values, speed, filtered_speed
  CurrentXAxis=pylab.arange(len(values)-xRange,len(values),1)
  line1[0].set_data(CurrentXAxis,pylab.array(values[-xRange:]))
#  line2[0].set_data(CurrentXAxis,pylab.array(filtered_speed[-xRange:]))
  line3[0].set_data(CurrentXAxis,pylab.array(signal_femoral[-xRange:]))
  line4[0].set_data(CurrentXAxis,pylab.array(signal_gastrocnemius[-xRange:]))
  # line9[0].set_data(CurrentXAxis,pylab.array(signal_gluteos_e[-xRange:]))
  # line10[0].set_data(CurrentXAxis,pylab.array(signal_gluteos_d[-xRange:]))
  # line11[0].set_data(CurrentXAxis,pylab.array(signal_hamstring_e[-xRange:]))
  # line12[0].set_data(CurrentXAxis,pylab.array(signal_hamstring_d[-xRange:]))
  line5[0].set_data(CurrentXAxis,pylab.array(filtered_speed[-xRange:]))
  line6[0].set_data(CurrentXAxis,pylab.array(speed[-xRange:]))
  line7[0].set_data(CurrentXAxis,pylab.array(signal_speed_actual[-xRange:]))
  line8[0].set_data(CurrentXAxis,pylab.array(signal_speed_ref[-xRange:]))
  ax2.axis([CurrentXAxis.min(),CurrentXAxis.max(),-0.2,1.2])
  ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-5,365])
  ax3.axis([CurrentXAxis.min(),CurrentXAxis.max(),-5,1200])
  ax4.axis([CurrentXAxis.min(),CurrentXAxis.max(),-1.2,1.2])
  manager.canvas.draw()

    
####################################
####################################

values=[]
values = [0 for x in range(xRange)]
speed=[]
speed = [0 for x in range(xRange)]

filtered_speed = []
filtered_speed = [0 for x in range(xRange)]

signal_femoral = []
signal_femoral = [0 for x in range(xRange)]

signal_gastrocnemius = []
signal_gastrocnemius = [0 for x in range(xRange)]

signal_gluteos_e = []
signal_gluteos_e = [0 for x in range(xRange)]

signal_gluteos_d = []
signal_gluteos_d = [0 for x in range(xRange)]

signal_hamstring_e = []
signal_hamstring_e = [0 for x in range(xRange)]

signal_hamstring_d = []
signal_hamstring_d = [0 for x in range(xRange)]

signal_speed_ref = []
signal_speed_ref = [0 for x in range(xRange)]

signal_speed_actual = []
signal_speed_actual = [0 for x in range(xRange)]

error_speed = []
error_speed = [0 for x in range(xRange)]

time_stamp = []
time_sensor = []
time_control = []
time_stimulator = []
t_zero = 0

####################################
####################################
def phase(ang):
    if (ang > 300) or (ang < 40):
        return 1
    elif (ang > 120) and (ang < 220):
        return 2
    else:
        return 0
    return
####################################
####################################
def femoral(phase): ### femoral esquerdo
    out = 0
    if phase == 0:
        out = float(0)/30
    elif phase == 1:
        out = float(30)/30
    elif phase == 2:
        out = float(0)/30
    elif phase == 3:
        out = float(0)/30
    elif phase == 4:
        out = float(0)/30
    elif phase == 5:
        out = float(0)/30
    elif phase == 6:
        out = float(0)/30
    elif phase == 7:
        out = float(0)/30
    elif phase == 8:
        out = float(25)/30
    elif phase == 9:
        out = float(25)/30
    out = out * scale
    return out
####################################
####################################
def gastrocnemius(phase): ##### femoral direito
    out = 0
#    if phase == 0:
#        out = float(15)/30
#    elif phase == 1:
#        out = float(5)/30
#    elif phase == 2:
#        out = float(5)/30
#    elif phase == 3:
#        out = float(5)/30
#    elif phase == 4:
#        out = float(4)/30
#    elif phase == 5:
#        out = float(5)/30
#    elif phase == 6:
#        out = float(7)/30
#    elif phase == 7:
#        out = float(10)/30
#    elif phase == 8:
#        out = float(20)/30
#    elif phase == 9:
#        out = float(25)/30
    # if phase <= 4:
    #     phase += 5
    # else:
    #     phase -= 5
        
    if phase == 0:
        out = float(0)/30
    elif phase == 1:
        out = float(0)/30
    elif phase == 2:
        out = float(30)/30
    elif phase == 3:
        out = float(0)/30
    elif phase == 4:
        out = float(0)/30
    elif phase == 5:
        out = float(0)/30
    elif phase == 6:
        out = float(0)/30
    elif phase == 7:
        out = float(0)/30
    elif phase == 8:
        out = float(25)/30
    elif phase == 9:
        out = float(25)/30
    out = out * scale
    return out
####################################
####################################
def gluteos_e(phase):  ## gluteos esquerdos
    out = 0
    if phase == 0:
        out = float(25)/30
    elif phase == 1:
        out = float(20)/30
    elif phase == 2:
        out = float(5)/30
    elif phase == 3:
        out = float(0)/30
    elif phase == 4:
        out = float(0)/30
    elif phase == 5:
        out = float(0)/30
    elif phase == 6:
        out = float(0)/30
    elif phase == 7:
        out = float(0)/30
    elif phase == 8:
        out = float(5)/30
    elif phase == 9:
        out = float(20)/30
    out = out * scale
    return out
####################################
####################################
def gluteos_d(phase):  ## gluteos direitos
    out = 0
    if phase <= 4:
        phase += 5
    else:
        phase -= 5
    if phase == 0:
        out = float(25)/30
    elif phase == 1:
        out = float(20)/30
    elif phase == 2:
        out = float(5)/30
    elif phase == 3:
        out = float(0)/30
    elif phase == 4:
        out = float(0)/30
    elif phase == 5:
        out = float(0)/30
    elif phase == 6:
        out = float(0)/30
    elif phase == 7:
        out = float(0)/30
    elif phase == 8:
        out = float(5)/30
    elif phase == 9:
        out = float(20)/30
    out = out * scale
    return out
####################################
####################################
def hamstring_e(phase):  ## hamstring esquerdos
    out = 0
    if phase == 0:
        out = float(0)/30
    elif phase == 1:
        out = float(10)/30
    elif phase == 2:
        out = float(25)/30
    elif phase == 3:
        out = float(25)/30
    elif phase == 4:
        out = float(10)/30
    elif phase == 5:
        out = float(0)/30
    elif phase == 6:
        out = float(0)/30
    elif phase == 7:
        out = float(0)/30
    elif phase == 8:
        out = float(0)/30
    elif phase == 9:
        out = float(0)/30
    out = out * scale
    return out
####################################
####################################
def hamstring_d(phase):  ## hamstring direito
    out = 0
    if phase <= 4:
        phase += 5
    else:
        phase -= 5
    if phase == 0:
        out = float(0)/30
    elif phase == 1:
        out = float(10)/30
    elif phase == 2:
        out = float(25)/30
    elif phase == 3:
        out = float(25)/30
    elif phase == 4:
        out = float(10)/30
    elif phase == 5:
        out = float(0)/30
    elif phase == 6:
        out = float(0)/30
    elif phase == 7:
        out = float(0)/30
    elif phase == 8:
        out = float(0)/30
    elif phase == 9:
        out = float(0)/30
    out = out * scale
    return out
####################################
####################################
def control(error):
    global error_speed
    signal = 0
    try:
        p = 1/float(5000)
        i = 1/float(100000)
        if (error[-2] > 0) & (error[-1] <= 0):
            inst_error = error[-1]
            error_speed = [0 for x in range(len(error))]
            error_speed[-1] = inst_error
            error = error_speed
        elif (error[-2] < 0) & (error[-1] >= 0):
            inst_error = error[-1]
            error_speed = [0 for x in range(len(error))]
            error_speed[-1] = inst_error
            error = error_speed
        signal = p*error[-1]+i*sum(error)
        if signal > 1:
            signal = 1
            error[-1] = 0
    except ValueError:
        pass
    return signal
####################################
####################################

def singleCommand(address, command):
    global serial_port
#    out = 0
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
#                out = 1
                return dados
            else:
                print "Did not get answer"
        else:
            print "Nao abriu a porta"
            pass
        
    except ValueError:
        pass
    return dados
    
def getEulerAngles():
    global run, readingAngles, usingPort, channels, pulse_width, old_current, old_pulse_width, old_signal_femoral, old_signal_gastrocnemius, old_signal_gluteos_e, old_signal_gluteos_d, old_signal_hamstring_e, old_signal_hamstring_d, current
    print("Getting euler angles.")
    i = 1
    
    t0 = time.time()
    t_zero = time.time()
    while run :
        
        time.sleep(.020)

        if not usingPort:
            usingPort = True
            serial_port_IMU.write(msg_com1) # e escreve na porta
            usingPort = False
          
        dados = ""
#            current = 0
        while dados == "":
            usingPort = True
            serial_port_IMU.flush()
            data = serial_port_IMU.read(serial_port_IMU.inWaiting()) # le da porta bytearray
            dados = data.decode()  # transforma bytearray em string
            usingPort = False
        if not dados == "":
#                print "Leitura: %i" %i
#                print "Dados: " + dados
            ang = dados.split(",")
#            print dados
            if len(ang) == 6:
                ang = float(ang[4])
                if ang >= 0:
                    ang = (ang / math.pi) * 180
                else:
                    ang = 360 - ((-(ang) / math.pi) * 180)
                    ######################################################################
#                print ang
                values.append(ang)
                
#                        if (ang > 320) & (ang < 90):
                
                if not usingPort:
                    usingPort = True
                    serial_port_IMU.write(msg_com2) # e escreve na porta
                    usingPort = False
                dados = ""
                while dados == "":
                    usingPort = True
                    serial_port_IMU.flush()
                    data = serial_port_IMU.read(serial_port_IMU.inWaiting()) # le da porta bytearray
                    dados = data.decode()  # transforma bytearray em string
                    usingPort = False
                
                inst_speed = dados.split(",")
                if len(inst_speed) == 6:
                    inst_speed = float(inst_speed[4])
                    inst_speed = inst_speed/(math.pi) * 180
                    speed.append(inst_speed)
                    signal_speed_ref.append(speed_ref)
                    error_speed.append(speed_ref - filtered_speed[-1])
                    time_stamp.append(time.time()-t0)

                    time_sensor.append(time.time() - t_zero)
                    t_zero = time.time()

                    if i >= filter_size:
                            filtered_speed.append(numpy.mean(speed[-filter_size:]))
                            signal_speed_actual.append(control(error_speed))
                            signal_gastrocnemius.append((gastrocnemius(phase(ang)))*(1+signal_speed_actual[-1]))
                            signal_femoral.append((femoral(phase(ang)))*(1+signal_speed_actual[-1]))
                            signal_gluteos_e.append((gluteos_e(phase(ang)))*(1+signal_speed_actual[-1]))
                            signal_gluteos_d.append((gluteos_d(phase(ang)))*(1+signal_speed_actual[-1]))
                            signal_hamstring_e.append((hamstring_e(phase(ang)))*(1+signal_speed_actual[-1]))
                            signal_hamstring_d.append((hamstring_d(phase(ang)))*(1+signal_speed_actual[-1]))
            #                signal_gastrocnemius.append((gastrocnemius(phase(ang))+signal_speed_actual[-1])*signal_speed_actual[-1])
            #                signal_femoral.append((femoral(phase(ang))+signal_speed_actual[-1])*signal_speed_actual[-1])
                    
                            if (old_signal_femoral != signal_femoral[-1]) | (old_signal_gastrocnemius != signal_gastrocnemius[-1]) | (old_signal_gluteos_e != signal_gluteos_e[-1]) | (old_signal_gluteos_d != signal_gluteos_d[-1]) | (old_signal_hamstring_e != signal_hamstring_e[-1]) | (old_signal_hamstring_d != signal_hamstring_d[-1]):
                                
                                if signal_femoral[-1] > 1:
                                    signal_femoral[-1] = 1
                                stim_femoral = signal_femoral[-1]*stim_max
                                if signal_gastrocnemius[-1] > 1:
                                    signal_gastrocnemius[-1] = 1
                                stim_gastrocnemius = signal_gastrocnemius[-1]*stim_max
                                if signal_gluteos_e[-1] > 1:
                                    signal_gluteos_e[-1] = 1
                                stim_gluteos_e = signal_gluteos_e[-1]*stim_max
                                if signal_gluteos_d[-1] > 1:
                                    signal_gluteos_d[-1] = 1
                                stim_gluteos_d = signal_gluteos_d[-1]*stim_max
                                if signal_hamstring_e[-1] > 1:
                                    signal_hamstring_e[-1] = 1
                                stim_hamstring_e = signal_hamstring_e[-1]*stim_max
                                if signal_hamstring_d[-1] > 1:
                                    signal_hamstring_d[-1] = 1
                                stim_hamstring_d = signal_hamstring_d[-1]*stim_max
                                # pulse_width = [stim_gluteos_e, stim_gluteos_d, stim_femoral, stim_hamstring_e,
                                #                stim_gastrocnemius, stim_hamstring_d]
                                pulse_width = [stim_femoral, stim_gastrocnemius, 0, 0, 0, 0]
                                print pulse_width
            #                    print old_signal_femoral
            #                    print signal_femoral
            #                    print old_signal_gastrocnemius
            #                    print signal_gastrocnemius
                                old_signal_femoral = signal_femoral[-1]
                                old_signal_gastrocnemius = signal_gastrocnemius[-1]
                                old_signal_gluteos_e = signal_gluteos_e[-1]
                                old_signal_gluteos_d = signal_gluteos_d[-1]
                                old_signal_hamstring_e = signal_hamstring_e[-1]
                                old_signal_hamstring_d = signal_hamstring_d[-1]
            #                    print "updating..."
            #                    print channels
            #                    print pulse_width
            #                    print current

                                time_control.append(time.time() - t_zero)
                                t_zero = time.time()

                                update(channels, pulse_width, current)

                                time_stimulator.append(time.time() - t_zero)
                                t_zero = time.time()

            #                    print "Update DONE"
            #        if (ang < 230) & (ang > 120):
    #            pulse_width = [0, 500]
##                            current = [4,6]
#            if (current != old_current) | (pulse_width != old_pulse_width):
#                old_current = current
#                old_pulse_width = pulse_width
#                update(channels, pulse_width, current) #atualiza
##                        elif (ang > 90) & (ang < 250):
#        elif (ang > 300) | (ang < 50):
##                            current = [6,4]
#            pulse_width = [380, 0]
#            if (current != old_current) | (pulse_width != old_pulse_width):
#                old_current = current
#                old_pulse_width = pulse_width
#                update(channels, pulse_width, current) #atualiza
#        else:
##                            current = [0,0]
#            pulse_width = [0, 0]
#            if (current != old_current) | (pulse_width != old_pulse_width):
#                old_current = current
#                old_pulse_width = pulse_width
#                update(channels, pulse_width, current) #atualiza
        
#        signal = control()
        
#                    else:
#                        continue
#            print dados

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
            elif (int(botao) == 1) & (readingAngles):
                print "================"
                print values[-1]
                print signal_femoral[-1]
                print signal_gastrocnemius[-1]
                print signal_speed_actual[-1]
                print filtered_speed[-1]
                print error_speed[-1]
                
            elif (int(botao) == 2) & readingAngles:
                print "Good Bye (saving data)!"
                run = False
                stop()
                with open("angles", 'w') as f:
                    for s in values:
                        f.write(str(s) + '\n')
                with open("speed", 'w') as f:
                    for s in speed:
                        f.write(str(s) + '\n')
                with open("time", 'w') as f:
                    for s in time_stamp:
                        f.write(str(s) + '\n')
                with open("time_sensor", 'w') as f:
                    for s in time_sensor:
                        f.write(str(s) + '\n')
                with open("time_control", 'w') as f:
                    for s in time_control:
                        f.write(str(s) + '\n')
                with open("time_stimulator", 'w') as f:
                    for s in time_stimulator:
                        f.write(str(s) + '\n')
                with open("fe", 'w') as f:
                    for s in signal_femoral:
                        f.write(str(s*stim_max) + '\n')
                with open("fd", 'w') as f:
                    for s in signal_gastrocnemius:
                        f.write(str(s*stim_max) + '\n')
                with open("ge", 'w') as f:
                    for s in signal_gluteos_e:
                        f.write(str(s*stim_max) + '\n')
                with open("gd", 'w') as f:
                    for s in signal_gluteos_d:
                        f.write(str(s*stim_max) + '\n')
                with open("he", 'w') as f:
                    for s in signal_hamstring_e:
                        f.write(str(s*stim_max) + '\n')
                with open("hd", 'w') as f:
                    for s in signal_hamstring_d:
                        f.write(str(s*stim_max) + '\n')
                with open("control", 'w') as f:
                    for s in signal_speed_actual:
                        f.write(str(s*stim_max) + '\n')
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
#    print ts1
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
        time.sleep(delay)
        serial_port_stim.flush()
        data = serial_port_stim.read(serial_port_stim.inWaiting()) # le da porta bytearray
        dados = data.decode()  # transforma bytearray em string
        i += 1
        if i > 10:
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
        data = ""
        
        while data == "":
#            print "reading"
            time.sleep(delay)
            serial_port_stim.flush()
            data = serial_port_stim.read(serial_port_stim.inWaiting()) # le da porta bytearray
    #        dados = data.decode()  # transforma bytearray em string
            i += 1
            if i > 10:
                print "no answer"
                break
            
#        dados = data.decode()  # transforma bytearray em string
#        print "resposta: " + dados
        
    except ValueError:
        print("Error (stop)")
        
    return
    
def update(channels, width, current):
    
    try:
#        print "beggining update"
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
            init_b[i*3+1] = (mode<<5) | (int(pulse_width[i])>>7)
            init_b[i*3+2] = (int(pulse_width[i]) & 127)
            init_b[i*3+3] = pulse_current[i]
        
#        print(init_1)
#        print(init_2)
#        print(init_3)
#        print(init_4)
        
#        init(1) = init_b(1)

        init = bytearray(init_b)
        
        i=0
        
        
#        print "requesting update"
        serial_port_stim.flush()
        serial_port_stim.write(init) # e escreve na porta
        dados = ""
#        print "escreveu"
        while dados == "":
#            print "reading"
            time.sleep(delay)
            data = serial_port_stim.read(serial_port_stim.inWaiting()) # le da porta bytearray
            dados = data.decode()  # transforma bytearray em string
            i += 1
#            print "esperando resposta"
            if i > 10:
                print "no answer on update"
                break
            
        dados = data.decode()  # transforma bytearray em string
#        print "resposta: " + dados
#        print data
                    
#
#        serial_port_stim.flush()
#        data = serial_port_stim.read(1) # le da porta bytearray
#        t = time.clock()
            
        dados = data.decode()  # transforma bytearray em string
#        print "resposta:" + dados
#            print dados
        
#            print "tempo de resposta: %f" %t, "ms\n\n"
        i+=1
              
    except ValueError:
        print("Error (update)")
        
    return

    
msg_com1 = ">" + str(address) + "," + str(command1) + "\n".encode() #transforma o comando de string para bytearray
msg_com2 = ">" + str(address) + "," + str(command2) + "\n".encode() #transforma o comando de string para bytearray
    
serial_port_IMU = serial.Serial(port_IMU, timeout=1, writeTimeout=1, baudrate=115200)
serial_port_stim = serial.Serial(port_stim, timeout=1, writeTimeout=1, baudrate=115200)

print("==================================================")

def startRunning():
    while not (checkButtons() == 1):
        pass
#            print "Updating..."
#            update(channels,pulse_width,current)
#            print "DONE"
    while run:
        pass
    return

try:
    
    if serial_port_IMU is not None:
        print "Beggining calibration..."
        error = 10
        while error > 0.1 :
            singleCommand(str(address),"16,1")
            singleCommand(str(address),"165")
            singleCommand(str(address),"96")
            dados = singleCommand(str(address),"1")
            error = float(dados[3]) + float(dados[4]) + float(dados[5])
#        if singleCommand(str(address),"16,0") & singleCommand(str(address),"165"):
        print "Calibration done."
                      
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
#            pulse_width_str = raw_input("Input pulse width: ")
#            pulse_width = [int(i) for i in (pulse_width_str.split(","))]
#            old_pulse_width = pulse_width
            current_str = raw_input("Input current: ")
            current = [int(i) for i in (current_str.split(","))]
            old_current = current
#            print "Updating..."
#            update(channels,pulse_width,current)
#            print "DONE"
#            print channels
#            print pulse_width
#            print current
            print "Whenever you're ready, press button 1 (the left one)"
            timer = fig.canvas.new_timer(interval=10)
            timer.add_callback(RealtimePloter, ())
        #            timer2 = fig.canvas.new_timer(interval=10)
            #timer2.add_callback(dataInput, ())
            timer.start()
        #            timer2.start()
            thread.start_new_thread(startRunning, ())
            pylab.show()
#            print "passou"
            
            #stop()
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
