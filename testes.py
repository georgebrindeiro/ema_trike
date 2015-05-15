# -*- coding: utf-8 -*-
"""
Created on Fri May 15 16:59:57 2015

@author: Wall-e
"""

import imu

x = imu.IMU('COM4')
x.calibrate()
x.get_euler_angles();