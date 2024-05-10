
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


class Shot(pygame.sprite.Sprite):
    def __init__(self, sprite_rect, map_rect, vector, img_bullet):
        super().__init__()
        self.vector = vector # direction and speed
        self.map_rect = map_rect # map surface
        self.image = img_bullet
        # starting position
        self.rect = self.image.get_rect(center = sprite_rect.center)
        if vector.x > 0: self.rect.x = sprite_rect.right
        elif vector.x < 0: self.rect.x = sprite_rect.left - self.rect.width
        elif vector.y < 0: self.rect.y -= sprite_rect.height
        elif vector.y > 0: self.rect.y += sprite_rect.height
        

    def update(self):
        # moves the bullet according to the direction
        self.rect.move_ip(self.vector)
        # removes the bullet if it has reached the limits of the screen
        if not self.map_rect.colliderect(self.rect):
            self.kill()
