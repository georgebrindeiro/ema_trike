# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:41:18 2015

@author: Wall-e
"""
ramp_angle = 30.0


def phase(ang):
    ang_local = round(ang)
    return ang_local / 5


def femoral(angle, ang_speed, speed_ref):  # femoral esquerdo

    # Calculate initial and final angles based on angular speed    
    ang_initial = 300 - (ang_speed / speed_ref) * 35
    ang_final = ang_initial + 100
    if ang_final > 360:
        ang_final -= 360
    # print ang_initial
    # Stimulate if it is in the stimulation zone
    if ang_final > ang_initial:
        if ang_initial - ramp_angle < angle < ang_initial:
            print 'rampa subida 01'
            return 1 - ((ang_initial - angle) / ramp_angle)
        elif ang_initial <= angle <= ang_final:
            print 'um 01'
            return 1
        elif ang_final < angle < ang_final + ramp_angle:
            print 'rampa descida 01'
            return 1 - ((angle - ang_final) / ramp_angle)
        else:
            print 'zero 01'
            return 0
    else:
        if ang_initial - ramp_angle < angle < ang_initial:
            print 'rampa subida 02'
            return 1 - ((ang_initial - angle) / ramp_angle)
        elif ang_initial <= angle or angle <= ang_final:
            print 'um 02'
            return 1
        elif ang_final < angle < ang_final + ramp_angle:
            print 'rampa descida 02'
            return 1 - ((angle - ang_final) / ramp_angle)
        else:
            print 'zero 02'
            return 0


def gastrocnemius(angle, ang_speed, speed_ref):  # femoral direito
    # Calculate initial and final angles based on angular speed       
    ang_initial = 120 - (ang_speed / speed_ref) * 35
    ang_final = ang_initial + 100
    if ang_final > 360:
        ang_final -= 360

    # Stimulate if it is in the stimulation zone    
    if ang_final > ang_initial:
        if ang_initial - ramp_angle < angle < ang_initial:
            return 1 - ((ang_initial - angle) / ramp_angle)
        elif ang_initial < angle < ang_final:
            return 1
        elif ang_final < angle < ang_final + ramp_angle:
            return 1 - ((angle - ang_final) / ramp_angle)
        else:
            # print 'zero 03'
            return 0
    else:
        if ang_initial - ramp_angle < angle < ang_initial:
            return 1 - ((ang_initial - angle) / ramp_angle)
        elif ang_initial < angle or angle < ang_final:
            return 1
        elif ang_final < angle < ang_final + ramp_angle:
            return 1 - ((angle - ang_final) / ramp_angle)
        else:
            # print 'zero 04'
            return 0
