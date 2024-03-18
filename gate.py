
# ==============================================================================
# .::Gate class::.
# Creates a door sprite at given coordinates. Is destroyed externally
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


class Gate(pygame.sprite.Sprite):
    def __init__(self, gate_data, gate_image):
        super().__init__()
        # gate_data = [x, y, visible?]
        self.x = gate_data[0]
        self.y = gate_data[1]
        # image
        self.image = gate_image
        self.rect = self.image.get_rect()
        # coordinates in tiles have to be converted to pixels
        self.rect.topleft = (self.x*constants.TILE_SIZE, self.y*constants.TILE_SIZE)

        # GATES does not need to be updated here