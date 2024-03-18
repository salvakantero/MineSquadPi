
# ==============================================================================
# .::MarqueeText class::.
# Generates a text that scrolls from right to left, 
# at a given position and speed.
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

class MarqueeText():
    def __init__(self, surface, font, y, speed, text, text_width):
        self.surface = surface    
        self.font = font
        self.x = surface.get_width() # to the far right
        self.y = y  
        self.speed = speed # in pixels
        self.text = text
        self.text_width = text_width # in pixels


    # update the xy position
    def update(self):
        # draws the text in the new position       
        self.x -= self.speed
        self.font.render(self.text, self.surface, (self.x, self.y))
        # resets when a certain number of pixels are shifted
        if self.x < -self.text_width: self.x = self.surface.get_width()