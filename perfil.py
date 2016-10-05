# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:41:18 2015

@author: Wall-e
"""
############################################################
######################### Left leg #########################
############################################################

# Left quadriceps
left_quad_start_ang = 280
left_quad_range = 95

# Left gluteus
left_gluteus_start_ang = 310
left_gluteus_range = 160

# Left hamstrings
left_hams_start_ang = 100 # melhor valor para isquios
left_hams_range = 105

ramps = 60

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


############################################################
############################################################
def left_quad(angle, ang_speed, speed_ref):

    # Calculate initial and final angles based on angular speed
    start_ang = left_quad_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + left_quad_range
    if end_ang > 360:
        end_ang -= 360
    # Stimulate if it is in the stimulation zone
    if ((angle > start_ang) and (angle < end_ang)) or (
                (end_ang < start_ang) and ((angle < end_ang) or (angle > start_ang))):
        return 1
    elif start_ang > angle > start_ang - ramps:
        return 1-(start_ang - angle)/ramps
    elif end_ang < angle < end_ang + ramps:
        return 1-(angle-end_ang)/ramps
    else:
        return 0


def right_quad(angle, ang_speed, speed_ref):
    update_right_leg()
    # Calculate initial and final angles based on angular speed
    start_ang = right_quad_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + right_quad_range
    if end_ang > 360:
        end_ang -= 360

    # Stimulate if it is in the stimulation zone
    if (angle > start_ang) and (angle < end_ang):
        return 1
    elif start_ang > angle > start_ang - ramps:
        return 1-(start_ang - angle)/ramps
    elif end_ang < angle < end_ang + ramps:
        return 1-(angle-end_ang)/ramps
    else:
        return 0


def left_gluteus(angle, ang_speed, speed_ref):
    # Calculate initial and final angles based on angular speed
    start_ang = left_gluteus_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + left_gluteus_range
    if end_ang > 360:
        end_ang -= 360
    # Stimulate if it is in the stimulation zone
    if ((angle > start_ang) and (angle < end_ang)) or (
                (end_ang < start_ang) and ((angle < end_ang) or (angle > start_ang))):
        return 1
    elif start_ang > angle > start_ang - ramps:
        return 1-(start_ang - angle)/ramps
    elif end_ang < angle < end_ang + ramps:
        return 1-(angle-end_ang)/ramps
    else:
        return 0


def right_gluteus(angle, ang_speed, speed_ref):
    update_right_leg()
    # Calculate initial and final angles based on angular speed
    start_ang = right_gluteus_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + right_gluteus_range
    if end_ang > 360:
        end_ang -= 360

    # Stimulate if it is in the stimulation zone
    if (angle > start_ang) and (angle < end_ang):
        return 1
    elif start_ang > angle > start_ang - ramps:
        return 1-(start_ang - angle)/ramps
    elif end_ang < angle < end_ang + ramps:
        return 1-(angle-end_ang)/ramps
    else:
        return 0


def left_hams(angle, ang_speed, speed_ref):
    # Calculate initial and final angles based on angular speed
    start_ang = left_hams_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + left_hams_range
    if end_ang > 360:
        end_ang -= 360

    # Stimulate if it is in the stimulation zone
    if (angle > start_ang) and (angle < end_ang):
        return 1
    elif start_ang > angle > start_ang - ramps:
        return 1-(start_ang - angle)/ramps
    elif end_ang < angle < end_ang + ramps:
        return 1-(angle-end_ang)/ramps
    else:
        return 0


def right_hams(angle, ang_speed, speed_ref):
    update_right_leg()
    # Calculate initial and final angles based on angular speed
    start_ang = right_hams_start_ang - (ang_speed / speed_ref) * correction_factor
    end_ang = start_ang + right_hams_range
    if end_ang > 360:
        end_ang -= 360
    # Stimulate if it is in the stimulation zone
    if ((angle > start_ang) and (angle < end_ang)) or (
                (end_ang < start_ang) and ((angle < end_ang) or (angle > start_ang))):
        return 1
    elif start_ang > angle > start_ang - ramps:
        return 1-(start_ang - angle)/ramps
    elif end_ang < angle < end_ang + ramps:
        return 1-(angle-end_ang)/ramps
    else:
        return 0
