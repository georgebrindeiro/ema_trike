# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:41:18 2015

@author: Wall-e
"""

####################################
####################################
# not used right now
def phase(ang):
    angLocal = round(ang)
    return angLocal/5
#    if (ang > 342) | (ang < 18):
#        return 0
#    elif ang < 54:
#        return 1
#    elif ang < 90:
#        return 2
#    elif ang < 126:
#        return 3
#    elif ang < 162:
#        return 4
#    elif ang < 198:
#        return 5
#    elif ang < 234:
#        return 6
#    elif ang < 270:
#        return 7
#    elif ang < 306:
#        return 8
#    elif ang <= 342:
#        return 9
#    return    
####################################
####################################
def femoral(angle, angSpeed, speed_ref): ### femoral esquerdo
    
    # Calculate initial and final angles based on angular speed    
    angInitial = 300-(angSpeed/speed_ref)*35
    angFinal = angInitial + 100
    if angFinal > 360:
        angFinal -= 360
#        print angInitial
    # Stimulate if it is in the stimulation zone    
    if ((angle > angInitial) and (angle < angFinal)) or ((angFinal < angInitial) and ((angle < angFinal) or (angle > angInitial))):
        return 1
    else:
        return 0
#    out = 0
#    if phase == 0:
#        out = float(20)/30
#    elif phase == 1:
#        out = float(8)/30
#    elif phase == 2:
#        out = float(0)/30
#    elif phase == 3:
#        out = float(0)/30
#    elif phase == 4:
#        out = float(0)/30
#    elif phase == 5:
#        out = float(0)/30
#    elif phase == 6:
#        out = float(0)/30
#    elif phase == 7:
#        out = float(0)/30
#    elif phase == 8:
#        out = float(30)/30
#    elif phase == 9:
#        out = float(30)/30
#    return out  
####################################
####################################
def gastrocnemius(angle, angSpeed, speed_ref): ##### femoral direito
    # Calculate initial and final angles based on angular speed       
    angInitial = 120-(angSpeed/speed_ref)*35
    angFinal = angInitial + 100
    if angFinal > 360:
        angFinal -= 360

    # Stimulate if it is in the stimulation zone    
    if (angle > angInitial) and (angle < angFinal):
        return 1
    else:
        return 0
#    out = 0
##    if phase == 0:
##        out = float(15)/30
##    elif phase == 1:
##        out = float(5)/30
##    elif phase == 2:
##        out = float(5)/30
##    elif phase == 3:
##        out = float(5)/30
##    elif phase == 4:
##        out = float(4)/30
##    elif phase == 5:
##        out = float(5)/30
##    elif phase == 6:
##        out = float(7)/30
##    elif phase == 7:
##        out = float(10)/30
##    elif phase == 8:
##        out = float(20)/30
##    elif phase == 9:
##        out = float(25)/30
#    if phase <= 4:
#        phase += 5
#    else:
#        phase -= 5
#        
#    if phase == 0:
#        out = float(20)/30
#    elif phase == 1:
#        out = float(8)/30
#    elif phase == 2:
#        out = float(0)/30
#    elif phase == 3:
#        out = float(0)/30
#    elif phase == 4:
#        out = float(0)/30
#    elif phase == 5:
#        out = float(0)/30
#    elif phase == 6:
#        out = float(0)/30
#    elif phase == 7:
#        out = float(0)/30
#    elif phase == 8:
#        out = float(30)/30
#    elif phase == 9:
#        out = float(30)/30
#    return out    
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