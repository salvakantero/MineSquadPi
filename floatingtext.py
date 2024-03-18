
# ==============================================================================
# .::FloatingText class::.
# Generates a text in the play area with the score obtained (or other data) 
# that goes up and disappears at the top of the screen.
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

import constants
from font import Font


class FloatingText():
    def __init__(self, surface):
        self.surface = surface    
        self.font = Font('images/fonts/small_font.png', constants.PALETTE['YELLOW'], True)
        self.font2 = Font('images/fonts/small_font.png', constants.PALETTE['BROWN'], True) 
        self.acceleration = 0.05 
        self.x = 0
        self.y = 0    
        self.speed = 0
        self.text = ''


    # update the xy position (only if drawn inside the screen)
    def update(self):
        if self.y > 0:
            self.speed += self.acceleration
            self.y -= self.speed # decreases Y, goes upwards
            self.font2.render(self.text, self.surface, (self.x+1, self.y+1))
            self.font.render(self.text, self.surface, (self.x, self.y))
