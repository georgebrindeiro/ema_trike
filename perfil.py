# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:41:18 2015

@author: Wall-e
"""

####################################
####################################
def phase(ang):
    if (ang > 342) | (ang < 18):
        return 0
    elif ang < 54:
        return 1
    elif ang < 90:
        return 2
    elif ang < 126:
        return 3
    elif ang < 162:
        return 4
    elif ang < 198:
        return 5
    elif ang < 234:
        return 6
    elif ang < 270:
        return 7
    elif ang < 306:
        return 8
    elif ang <= 342:
        return 9
    return    
####################################
####################################
def femoral(phase): ### femoral esquerdo
    out = 0
    if phase == 0:
        out = float(20)/30
    elif phase == 1:
        out = float(8)/30
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
        out = float(30)/30
    elif phase == 9:
        out = float(30)/30
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
    if phase <= 4:
        phase += 5
    else:
        phase -= 5
        
    if phase == 0:
        out = float(20)/30
    elif phase == 1:
        out = float(8)/30
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
        out = float(30)/30
    elif phase == 9:
        out = float(30)/30
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
    return out  
####################################
####################################