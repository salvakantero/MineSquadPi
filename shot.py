
# ==============================================================================
# .::Shot class::.
# Creates, destroys, and draws during its lifecycle a player-fired projectile.
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



class Shot(pygame.sprite.Sprite):
    # class variable - load bullet image once for all instances
    _bullet_image = None

    def __init__(self, player_x, player_y, vector, srf_map):
        super().__init__()
        self.vector = vector # direction and speed
        self.surface = srf_map # map surface
        # load image only once for all shot instances
        if Shot._bullet_image is None:
            Shot._bullet_image = pygame.image.load(constants.SPR_PATH + 'bullet.png').convert_alpha()
        self.image = Shot._bullet_image
        self.rect = self.image.get_rect()        
        # starting position        
        self.rect.x = player_x + (constants.HALF_TILE_SIZE // 2)
        self.rect.y = player_y + (constants.HALF_TILE_SIZE // 2)
        if vector.x > 0: self.rect.x += constants.TILE_SIZE # right
        elif vector.x < 0: self.rect.x -= constants.HALF_TILE_SIZE # left
        elif vector.y < 0: self.rect.y -= constants.HALF_TILE_SIZE # up
        elif vector.y > 0: self.rect.y += constants.TILE_SIZE # down        



    def update(self, camera):
        # moves the bullet according to the direction
        self.rect.move_ip(self.vector)
        # removes the bullet if it has reached the limits of the map
        if (self.rect.x < 0 or self.rect.x > constants.MAP_PIXEL_SIZE[0] or
            self.rect.y < 0 or self.rect.y > constants.MAP_PIXEL_SIZE[1]):
            self.kill()
            return
        # if the bullet is no longer visible on screen (camera view), remove it.
        # (this allows the player to shoot again)
        if not self._is_visible(camera):
            self.kill()



    # draws the bullet on the screen
    def draw(self, surface, camera):
        if not self._is_visible(camera):
            return
        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        surface.blit(self.image, (screen_x, screen_y))



    ##### auxiliary functions #####

    def _is_visible(self, camera):
        # Returns True if any part of the bullet rect intersects the camera viewport
        return (
            # right edge beyond camera left
            self.rect.x + self.rect.width > camera.x
            # left edge before camera right
            and self.rect.x < camera.x + constants.SCREEN_MAP_UNSCALED_SIZE[0]
            # bottom edge beyond camera top
            and self.rect.y + self.rect.height > camera.y
            # top edge before camera bottom
            and self.rect.y < camera.y + constants.SCREEN_MAP_UNSCALED_SIZE[1])
