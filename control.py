# -*- coding: utf-8 -*-
"""
Created on Sat May 23 17:55:13 2015

@author: Wall-e
"""

def control(error):
    signal = 0
    try:    
        p = 1/float(1000)
        i = 1/float(100000)
        
        # If there is a change of signal, reset
#        if ((error[-2] >= 0) and (error[-1] < 0)) or ((error[-2] < 0) and (error[-1] >= 0)):
#            errorTemp = [0 for x in range(len(error))]
#            errorTemp[-1] = error[-1]
#            error = errorTemp
        
        signal = 0.5 + p*error[-1]+i*sum(error)
        
#         saturation
        if signal > 1:
            signal = 1
            error[-1] = 0
        elif signal < 0:
            signal = 0
            error[-1] = 0
            
    except ValueError:
        return "Control error"
    return signal