import time
import serial
import os
import signal
import sys

class ForceSensor:
    def __init__(self, config_dict):
        self.config_dict = config_dict
        self.devices = {}
        self.dongles = []
        self.forcesensors = []

        for name in config_dict['dev_names']:
            dev_type = config_dict['dev_type'][name]

            if dev_type == 'DNG':
                wired_port = config_dict['wired_port'][name]
                self.devices[name] = serial.Serial( port=wired_port,
                                                    baudrate = 115200,
                                                    parity=serial.PARITY_NONE,
                                                    stopbits=serial.STOPBITS_ONE,
                                                    bytesize=serial.EIGHTBITS,
                                                    timeout=1 )
                self.dongles.append(name)

            elif dev_type == 'WL':
                self.forcesensors.append(name)
                
                self.devices[name] = {'wireless_dng': config_dict['wireless_dng'][name],
                                      'wireless_id': config_dict['wireless_id'][name]}

    def getForce(self, name):
        # print "getting ", name
        
        wireless_dng = self.devices[self.devices[name]['wireless_dng']]
        wireless_id = self.devices[name]['wireless_id']
        
        force = wireless_dng.readline()
        msg_id = ""
        
        while msg_id != wireless_id:
            while len(force) == 0:
                # print "len(force) == 0"
                force = wireless_dng.readline()
                
            msg_id = force[0]
        
            if msg_id == wireless_id:
                break
            else:
                # print "msg_id != %s (%s), reading again" % (wireless_id, msg_id)
                force = wireless_dng.readline()
        
        return [0.0,float(force[1:]),0.0]
