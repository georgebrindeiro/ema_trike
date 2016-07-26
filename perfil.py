# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:41:18 2015

@author: Wall-e
"""


class Perfil():
    def __init__(self):
        ############################################################
        ######################### Left leg #########################
        ############################################################

        # Left quadriceps
        self.left_quad_start_ang = 250
        self.left_quad_range = 75

        # Left gluteus
        self.left_gluteus_start_ang = 20
        self.left_gluteus_range = 80

        # Left hamstrings
        self.left_hams_start_ang = 105
        self.left_hams_range = 80


        ############################################################
        ######################## Right leg #########################
        ############################################################
        # The right leg is the opposite of the left leg

        # Right quadriceps
        self.right_quad_start_ang = self.left_quad_start_ang - 180
        self.right_quad_range = self.left_quad_range

        # Right gluteus
        # Make sure the angles are not negative nor greater than 360
        if self.left_gluteus_start_ang > 180:
            self.right_gluteus_start_ang = self.left_gluteus_start_ang - 180
        else:
            self.right_gluteus_start_ang = self.left_gluteus_start_ang + 180
            self.right_gluteus_range = self.left_gluteus_range

        # Right hamstrings
        self.right_hams_start_ang = self.left_hams_start_ang + 180
        self.right_hams_range = self.left_hams_range

        ############################################################
        ############################################################
        # How much the wheel must spin when in reference speed
        self.correction_factor = 35

        ############################################################
        ############################################################

    def update_angles(self):
        ############################################################
        ######################## Right leg #########################
        ############################################################
        # The right leg is the opposite of the left leg

        # Right quadriceps
        self.right_quad_start_ang = self.left_quad_start_ang - 180
        self.right_quad_range = self.left_quad_range

        # Right gluteus
        # Make sure the angles are not negative nor greater than 360
        if self.left_gluteus_start_ang > 180:
            self.right_gluteus_start_ang = self.left_gluteus_start_ang - 180
        else:
            self.right_gluteus_start_ang = self.left_gluteus_start_ang + 180
            self.right_gluteus_range = self.left_gluteus_range

        # Right hamstrings
        self.right_hams_start_ang = self.left_hams_start_ang + 180
        self.right_hams_range = self.left_hams_range


    def left_quad(self, angle, ang_speed, speed_ref):
        # Calculate initial and final angles based on angular speed
        start_ang = self.left_quad_start_ang - (ang_speed / speed_ref) * self.correction_factor
        end_ang = start_ang + self.left_quad_range
        if end_ang > 360:
            end_ang -= 360
        # Stimulate if it is in the stimulation zone
        if ((angle > start_ang) and (angle < end_ang)) or (
                    (end_ang < start_ang) and ((angle < end_ang) or (angle > start_ang))):
            return 1
        else:
            return 0

    def right_quad(self, angle, ang_speed, speed_ref):
        # Calculate initial and final angles based on angular speed
        start_ang = self.right_quad_start_ang - (ang_speed / speed_ref) * self.correction_factor
        end_ang = start_ang + self.right_quad_range
        if end_ang > 360:
            end_ang -= 360

        # Stimulate if it is in the stimulation zone
        if (angle > start_ang) and (angle < end_ang):
            return 1
        else:
            return 0

    def left_gluteus(self, angle, ang_speed, speed_ref):
        # Calculate initial and final angles based on angular speed
        start_ang = self.left_gluteus_start_ang - (ang_speed / speed_ref) * self.correction_factor
        end_ang = start_ang + self.left_gluteus_range
        if end_ang > 360:
            end_ang -= 360
        # Stimulate if it is in the stimulation zone
        if ((angle > start_ang) and (angle < end_ang)) or (
                    (end_ang < start_ang) and ((angle < end_ang) or (angle > start_ang))):
            return 1
        else:
            return 0

    def right_gluteus(self, angle, ang_speed, speed_ref):
        # Calculate initial and final angles based on angular speed
        start_ang = self.right_gluteus_start_ang - (ang_speed / speed_ref) * self.correction_factor
        end_ang = start_ang + self.right_gluteus_range
        if end_ang > 360:
            end_ang -= 360

        # Stimulate if it is in the stimulation zone
        if (angle > start_ang) and (angle < end_ang):
            return 1
        else:
            return 0

    def left_hams(self, angle, ang_speed, speed_ref):
        # Calculate initial and final angles based on angular speed
        start_ang = self.left_hams_start_ang - (ang_speed / speed_ref) * self.correction_factor
        end_ang = start_ang + self.left_hams_range
        if end_ang > 360:
            end_ang -= 360

        # Stimulate if it is in the stimulation zone
        if (angle > start_ang) and (angle < end_ang):
            return 1
        else:
            return 0

    def right_hams(self, angle, ang_speed, speed_ref):
        # Calculate initial and final angles based on angular speed
        start_ang = self.right_hams_start_ang - (ang_speed / speed_ref) * self.correction_factor
        end_ang = start_ang + self.right_hams_range
        if end_ang > 360:
            end_ang -= 360
        # Stimulate if it is in the stimulation zone
        if ((angle > start_ang) and (angle < end_ang)) or (
                    (end_ang < start_ang) and ((angle < end_ang) or (angle > start_ang))):
            return 1
        else:
            return 0
