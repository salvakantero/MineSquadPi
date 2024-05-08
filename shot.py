
# ==============================================================================
# .::Shot class::.
# Creates, destroys, and draws during its lifecycle a player-fired projectile.
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
import constants


class Shot(pygame.sprite.Sprite):
    def __init__(self, pos, vector, img_bullet):
        super().__init__()
        self.vector = vector # direction and speed
        self.image = img_bullet
        # starting position
        self.rect = self.image.get_rect(center = pos.center)
        if vector.x > 0: self.rect.x = pos.right
        elif vector.x < 0: self.rect.x = pos.left - self.rect.width
        elif vector.y > 0: self.rect.y = pos.bottom + self.rect.height
        

    def update(self):
        # moves the bullet according to the direction
        if self.vector.x != 0: self.rect.x += self.vector.x
        elif self.vector.y != 0: self.rect.y += self.vector.y
        # removes the bullet if it has reached the limits of the screen
        if self.rect.x < 0 or self.rect.x > constants.MAP_UNSCALED_SIZE[0]:
            self.kill()