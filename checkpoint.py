
#===============================================================================
# .::Checkpoint class::.
# System for loading/saving games
#===============================================================================
#
#  This file is part of "Red Planet Pi". Copyright (C) 2023 @salvakantero
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
import constants


class Checkpoint():
    def __init__(self):
        self.filename = 'checkpoint.dat'
        # defaults (these are the equivalent values at the start of a game)
        # allow a checkpoint to be loaded even if the file does not exist.
        self.data = {
            'map_number' : 0,
            'game_percent' : 0,
            'player_lives' : 10,
            'player_ammo' : 10,
            'player_keys' : 0,
            'player_TNT' : 0,
            'player_oxygen' : constants.MAX_OXYGEN,
            'player_stacked_TNT' : False,
            'player_facing_right' : True,
            'player_rect' : pygame.Rect(16,112, constants.TILE_SIZE, constants.TILE_SIZE),
            'player_score' : 0,
            'hotspot_data' : constants.HOTSPOT_DATA,
            'gate_data' : constants.GATE_DATA
        }


    # generates a new 'checkpoint.dat' with the current game data 
    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)


    # loads data from 'checkpoint.dat' if file exists
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                self.data = pickle.load(f)


        
