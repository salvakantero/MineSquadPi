
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
        self.shadow_image = pygame.image.load(constants.SPR_PATH + 'hotspot_shadow.png').convert_alpha()
        self.rect = self.image.get_rect()
        # random coordinates in tiles (have to be converted to pixels)
        self.tile_x, self.tile_y = self._generate_position(tile_data)
        self.shadow_y = (self.tile_y * constants.TILE_SIZE) + 1 # shadow is always at the bottom of the tile
        self.rect.topleft = (self.tile_x * constants.TILE_SIZE, self.tile_y * constants.TILE_SIZE)   



    def update(self, camera):
        if not self._is_visible(camera):
            return
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
        if not self._is_visible(camera):
            return
        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        screen_shadow_y = self.shadow_y - camera.y
        surface.blit(self.shadow_image, (screen_x, screen_shadow_y))
        surface.blit(self.image, (screen_x, screen_y))



    ##### auxiliary functions #####

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
    

  
    # check if the hotspot is within the camera's view
    def _is_visible(self, camera):
        return (
            # check right edge
            self.rect.x + self.rect.width > camera.x
            # check left edge
            and self.rect.x < camera.x + constants.SCREEN_MAP_UNSCALED_SIZE[0]
            # check bottom edge
            and self.rect.y + self.rect.height > camera.y
            # check top edge
            and self.rect.y < camera.y + constants.SCREEN_MAP_UNSCALED_SIZE[1])

