
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
        self.y = 0
    
    def update(self, player_y):
        # attempt to centre the player vertically
        target_y = player_y - constants.MAP_UNSCALED_SIZE[1] // 2
        # camera limits
        max_camera_y = constants.MAP_TILE_SIZE[1] * constants.TILE_SIZE - constants.MAP_UNSCALED_SIZE[1]
        self.y = max(0, min(target_y, max_camera_y))