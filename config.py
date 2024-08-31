
# ==============================================================================
# .::Configuration class::.
# Save/Load the configuration file.
# Makes the configuration accessible from the attributes of the class.
# ==============================================================================
#
#  This file is part of "Mine Squad Pi". Copyright (C) 2024 @salvakantero
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================

import pygame
import pickle
import os
import enums


class Configuration():
    def __init__(self):
        self.filename = 'config.dat'
        self.data = { 
            # default values
            'screen_mode' : 0, # 0 = window, 1 = 4:3(800x600), 2 = 16:9(1280x720)
            'scanlines' : True,
            'view' : 1, # 0 = isometric, 1 = zenithal
            'control' : enums.CT_CLASSIC # 0 = classic, 1 = gamer, 2 = retro, 3 = joypad
        }
        # default values for controls (classic layout)
        self.up_key = pygame.K_UP
        self.down_key = pygame.K_DOWN
        self.left_key = pygame.K_LEFT
        self.right_key = pygame.K_RIGHT
        # the following values are independent of the layout
        self.flag_key = pygame.K_f
        self.fire_key = pygame.K_SPACE
        self.mute_key = pygame.K_m


    # generates a new 'config.dat' with the current configuration
    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)


    # loads data from 'config.dat' if file exists
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                self.data = pickle.load(f)
            self.apply_controls()


    # assigns the keys corresponding to the selected layout
    def apply_controls(self):
        if self.data['control'] == enums.CT_CLASSIC or self.data['control'] == enums.CT_JOYSTICK:
            self.up_key = pygame.K_UP
            self.down_key = pygame.K_DOWN
            self.left_key = pygame.K_LEFT
            self.right_key = pygame.K_RIGHT
        elif self.data['control'] == enums.CT_GAMER:
            self.up_key = pygame.K_w
            self.down_key = pygame.K_s
            self.left_key = pygame.K_a
            self.right_key = pygame.K_d
        elif self.data['control'] == enums.CT_RETRO:
            self.up_key = pygame.K_q
            self.down_key = pygame.K_a
            self.left_key = pygame.K_o
            self.right_key = pygame.K_p
    

    # create a joystick/joypad/gamepad object
    def prepare_joystick(self):
        joystick = None
        if self.data['control'] == enums.CT_JOYSTICK:
            if pygame.joystick.get_count() > 0:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
            else:
                self.data['control'] == enums.CT_CLASSIC
        return joystick
    
