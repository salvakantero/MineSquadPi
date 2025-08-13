
# ==============================================================================
# .::Hotspot class::.
# Creates a hotspot sprite at random coordinates (is destroyed externally)
# and animates it with an up-and-down movement.
# ==============================================================================
#
#  This file is part of "Mine Squad Pi". Copyright (C) 2025 @salvakantero
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
import enums
import random



class Hotspot(pygame.sprite.Sprite):
    def __init__(self, type, image, tile_data):
        super().__init__()
        self.type = type # LIFE, SHIELD, AMMO, CANDY, APPLE, CHOCOLATE, COIN
        self.y_offset = 0 # to animate the hotspot (up and down)
        self.going_up = True
        self.animation_timer = 2 # timer to change position (frame counter)
        # image
        self.image = image
        self.rect = self.image.get_rect()
        # random coordinates in tiles (have to be converted to pixels)
        self.tile_x, self.tile_y = self._generate_position(tile_data)
        self.rect.topleft = (self.tile_x * constants.TILE_SIZE, self.tile_y * constants.TILE_SIZE)   



    def _generate_position(self, tile_data):
        available_tiles = []        
        for row_index, row in enumerate(tile_data):
            for col_index, tile in enumerate(row):
                # 0:no action, 1:obstacle, 2:mine, 3:killer
                if (tile == 0):
                    available_tiles.append((row_index, col_index))        
        # choose a random tile from the available ones
        if available_tiles:
            row, col = random.choice(available_tiles)
            return col, row
        else:
            # no available tiles, return a default position
            # this should not happen
            return -1, -1
    


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
        self.rect.y = (self.tile_y * constants.TILE_SIZE) - self.y_offset
        self.animation_timer += 1



    # draws the hotspot on the screen
    def draw(self, surface, camera):
        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        surface.blit(self.image, (screen_x, screen_y))