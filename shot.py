
# ==============================================================================
# .::Shot class::.
# Creates, destroys, and draws during its lifecycle a player-fired projectile.
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


class Shot(pygame.sprite.Sprite):
    def __init__(self, pos, facing_right, img_bullet, speed):
        super().__init__()
        self.facing_right = facing_right
        self.speed = speed # pixels per frame
        self.image = img_bullet
        # positions the bullet in front of the weapon
        self.rect = self.image.get_rect(center = pos.center)
        if facing_right: self.rect.x = pos.right
        else: self.rect.x = pos.left - self.rect.width
        
        
    def update(self):
        # moves the bullet according to the direction
        if self.facing_right: self.rect.x += self.speed
        else: self.rect.x -= self.speed 
        # eliminates the bullet if it has reached the sides of the screen
        if self.rect.x < 0 or self.rect.x > constants.MAP_UNSCALED_SIZE[0]:
            self.kill()