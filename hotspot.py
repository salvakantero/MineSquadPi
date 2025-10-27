
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
    # class constants
    ANIMATION_TIMER_INIT = 2
    MAX_Y_OFFSET = 5

    # class variable shared by all instances (loaded once)
    _shadow_image = None

    def __init__(self, type, image, map_instance):
        super().__init__()
        self.type = type # LIFE, SHIELD, AMMO, BEACONS, CANDY, APPLE, CHOCOLATE, COIN
        self.y_offset = 0 # to animate the hotspot (up and down)
        self.going_up = True
        self.animation_timer = self.ANIMATION_TIMER_INIT
        # image
        self.image = image
        # load shadow once for all instances
        if Hotspot._shadow_image is None:
            Hotspot._shadow_image = pygame.image.load(constants.SPR_PATH + 'hotspot_shadow.png').convert_alpha()
        self.shadow_image = Hotspot._shadow_image
        self.rect = self.image.get_rect()
        # random coordinates in tiles (have to be converted to pixels)
        self.tile_x, self.tile_y = self._generate_position(map_instance)
        self.base_y = self.tile_y * constants.TILE_SIZE # pre-calculate base Y position
        self.shadow_y = self.base_y + 1 # shadow is always at the bottom of the tile
        self.rect.topleft = (self.tile_x * constants.TILE_SIZE, self.base_y)   



    def update(self, camera):
        if not self._is_visible(camera):
            return
        # movement (up and down)
        if self.animation_timer > 1: # time to change the offset
            self.animation_timer = 0
            if self.going_up:
                if self.y_offset < self.MAX_Y_OFFSET:
                    self.y_offset += 1
                else:
                    self.going_up = False
            else: # going down
                if self.y_offset > 0:
                    self.y_offset -= 1
                else:
                    self.going_up = True
        # apply the offset using pre-calculated base_y
        self.rect.y = self.base_y - self.y_offset
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

    def _generate_position(self, map_instance):
        max_attempts = 100  # prevent infinite loop
        rows = constants.MAP_TILE_SIZE[1]
        cols = constants.MAP_TILE_SIZE[0]

        for _ in range(max_attempts):
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            if map_instance.get_tile_type(col, row) == enums.TT_NO_ACTION:
                return col, row

        # fallback: build full list if random search fails
        available_tiles = []
        for row_index in range(rows):
            for col_index in range(cols):
                if map_instance.get_tile_type(col_index, row_index) == enums.TT_NO_ACTION:
                    available_tiles.append((row_index, col_index))

        if available_tiles:
            row, col = random.choice(available_tiles)
            return col, row

        # no available tiles, return a default position (should not happen)
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

