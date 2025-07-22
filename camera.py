
# ==============================================================================
# .::Camera class::.
# Allows to show only the portion of the map where the player is located.
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

import constants


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

        # cache frequently used values
        self.half_map_width = constants.MAP_UNSCALED_SIZE[0] // 2
        self.half_map_height = constants.MAP_UNSCALED_SIZE[1] // 2
        self.max_x = constants.MAP_PIXEL_SIZE[0] - constants.MAP_UNSCALED_SIZE[0]
        self.max_y = constants.MAP_PIXEL_SIZE[1] - constants.MAP_UNSCALED_SIZE[1]
    
    def update(self, player_x, player_y):
        # updates the camera position based on the player's position
        # the camera should be centered on the player
        # the camera cannot go beyond the map boundaries
        target_x = player_x - self.half_map_width
        self.x = max(0, min(target_x, self.max_x))
        target_y = player_y - self.half_map_height   
        self.y = max(0, min(target_y, self.max_y))