# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:41:18 2015

@author: Wall-e
"""
############################################################
######################### Left leg #########################
############################################################

# Left quadriceps
left_quad_start_ang = 260
left_quad_range = 80

# Left gluteus
left_gluteus_start_ang = 0
left_gluteus_range = 80

# Left hamstrings
left_hams_start_ang = 85 # melhor valor para isquios
left_hams_range = 80

############################################################
######################## Right leg #########################
############################################################
# The right leg is the opposite of the left leg

# Right quadriceps
right_quad_start_ang = left_quad_start_ang - 180
right_quad_range = left_quad_range

# Right gluteus
# Make sure the angles are not negative nor greater than 360
if left_gluteus_start_ang > 180:
    right_gluteus_start_ang = left_gluteus_start_ang - 180
else:
    right_gluteus_start_ang = left_gluteus_start_ang + 180
right_gluteus_range = left_gluteus_range

# Right hamstrings
right_hams_start_ang = left_hams_start_ang + 180
right_hams_range = left_hams_range

def update_right_leg():
    global right_quad_start_ang, right_quad_range, right_hams_start_ang, right_hams_range, right_gluteus_start_ang, right_gluteus_range
    # Right quadriceps
    right_quad_start_ang = left_quad_start_ang - 180
    right_quad_range = left_quad_range

    # Right gluteus
    # Make sure the angles are not negative nor greater than 360
    if left_gluteus_start_ang > 180:
        right_gluteus_start_ang = left_gluteus_start_ang - 180
    else:
        right_gluteus_start_ang = left_gluteus_start_ang + 180
    right_gluteus_range = left_gluteus_range

    # Right hamstrings
    right_hams_start_ang = left_hams_start_ang + 180
    right_hams_range = left_hams_range


############################################################
############################################################
# How much the wheel must spin when in reference speed
correction_factor = 35

ramp_angle = 60


############################################################
############################################################
def left_quad(angle, ang_speed, speed_ref):

    # Calculate initial and final angles based on angular speed
    start_ang = left_quad_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + left_quad_range
    start_ang += 360
    end_ang += 360
    angle += 360
    # Stimulate if it is in the stimulation zone
    # if end_ang + ramp_angle > 360:
    #     angle += 360
    if end_ang < start_ang:
        end_ang += 360
        angle += 360

    if (start_ang - ramp_angle) < angle < start_ang:
        # print 1 - ((start_ang - angle) / ramp_angle)
        return 1 - ((start_ang - angle) / ramp_angle)
    elif start_ang <= angle <= end_ang:
        # print 1
        return 1
    elif end_ang < angle < (end_ang + ramp_angle):
        # print 1 - ((angle - end_ang) / ramp_angle)
        return 1 - ((angle - end_ang) / ramp_angle)
    else:
        # print 0
        return 0


def right_quad(angle, ang_speed, speed_ref):
    update_right_leg()
    # Calculate initial and final angles based on angular speed
    start_ang = right_quad_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + right_quad_range
    start_ang += 360
    end_ang += 360
    angle += 360
    # Stimulate if it is in the stimulation zone
    if end_ang < start_ang:
        end_ang += 360
        angle += 360
    if (start_ang - ramp_angle) < angle < start_ang:
        return 1 - ((start_ang - angle) / ramp_angle)
    elif start_ang <= angle <= end_ang:
        return 1
    elif end_ang < angle < (end_ang + ramp_angle):
        return 1 - ((angle - end_ang) / ramp_angle)
    else:
        return 0


def left_gluteus(angle, ang_speed, speed_ref):
    # Calculate initial and final angles based on angular speed
    start_ang = left_gluteus_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + left_gluteus_range
    start_ang += 360
    end_ang += 360
    angle += 360
    # Stimulate if it is in the stimulation zone
    if end_ang < start_ang:
        end_ang += 360
        angle += 360
    if (start_ang - ramp_angle) < angle < start_ang:
        return 1 - ((start_ang - angle) / ramp_angle)
    elif start_ang <= angle <= end_ang:
        return 1
    elif end_ang < angle < (end_ang + ramp_angle):
        return 1 - ((angle - end_ang) / ramp_angle)
    else:
        return 0


def right_gluteus(angle, ang_speed, speed_ref):
    update_right_leg()
    # Calculate initial and final angles based on angular speed
    start_ang = right_gluteus_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + right_gluteus_range
    start_ang += 360
    end_ang += 360
    angle += 360
    # Stimulate if it is in the stimulation zone
    if end_ang < start_ang:
        end_ang += 360
        angle += 360
    if (start_ang - ramp_angle) < angle < start_ang:
        return 1 - ((start_ang - angle) / ramp_angle)
    elif start_ang <= angle <= end_ang:
        return 1
    elif end_ang < angle < (end_ang + ramp_angle):
        return 1 - ((angle - end_ang) / ramp_angle)
    else:
        return 0


def left_hams(angle, ang_speed, speed_ref):
    # Calculate initial and final angles based on angular speed
    start_ang = left_hams_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + left_hams_range
    start_ang += 360
    end_ang += 360
    angle += 360
    # Stimulate if it is in the stimulation zone
    if end_ang < start_ang:
        end_ang += 360
        angle += 360
    if (start_ang - ramp_angle) < angle < start_ang:
        return 1 - ((start_ang - angle) / ramp_angle)
    elif start_ang <= angle <= end_ang:
        return 1
    elif end_ang < angle < (end_ang + ramp_angle):
        return 1 - ((angle - end_ang) / ramp_angle)
    else:
        return 0


def right_hams(angle, ang_speed, speed_ref):
    update_right_leg()
    # Calculate initial and final angles based on angular speed
    start_ang = right_hams_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + right_hams_range
    start_ang += 360
    end_ang += 360
    angle += 360
    # Stimulate if it is in the stimulation zone
    if end_ang < start_ang:
        end_ang += 360
        angle += 360
    if (start_ang - ramp_angle) < angle < start_ang:
        return 1 - ((start_ang - angle) / ramp_angle)
    elif start_ang <= angle <= end_ang:
        return 1
    elif end_ang < angle < (end_ang + ramp_angle):
        return 1 - ((angle - end_ang) / ramp_angle)
    else:
        return 0
