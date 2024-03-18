
# ==============================================================================
# .::Hotspot class::.
# Creates a hotspot sprite at given coordinates (is destroyed externally)
# and animates it with an up-and-down movement.
# ==============================================================================
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
import constants


class Hotspot(pygame.sprite.Sprite):
    def __init__(self, hotspot_data, image):
        super().__init__()
        # hotspot_data = [type, x, y, _]
        self.type = hotspot_data[0] # TNT, KEY, AMMO, OXYGEN, CHECKPOINT, BURGER, CAKE, DONUT 
        self.x = hotspot_data[1]
        self.y = hotspot_data[2]
        self.y_offset = 0 # to animate the hotspot (up and down)
        self.going_up = True
        self.animation_timer = 2 # timer to change position (frame counter)
        # image
        self.image = image
        self.rect = self.image.get_rect()
        # coordinates in tiles have to be converted to pixels
        self.rect.topleft = (self.x*constants.TILE_SIZE, self.y*constants.TILE_SIZE)   


    def update(self):
        # movement (up and down)
        if self.animation_timer > 1: # time to change the offset
            self.animation_timer = 0
            if self.going_up:
                if self.y_offset < 5: self.y_offset += 1
                else: self.going_up = False
            else: # going down
                if self.y_offset > 0: self.y_offset -= 1                
                else: self.going_up = True            
        # apply the offset
        self.rect.y = (self.y * self.rect.height) - self.y_offset
        self.animation_timer += 1