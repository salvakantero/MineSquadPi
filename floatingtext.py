
# ==============================================================================
# .::FloatingText class::.
# Generates a text in the play area with the score obtained (or other data) 
# that goes up and disappears at the top of the screen.
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
from font import Font



class FloatingText():
    def __init__(self, text, x, y, surface): 
        self.font = Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['WHITE2'], True)
        self.font2 = Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['BLACK1'], True) 
        self.text = text
        self.x = x
        self.y = y    
        self.speed = 0
        self.acceleration = 0.03
        self.surface = surface   



    # update the xy position (only if drawn inside the screen)
    def update_and_draw(self, camera):  
        if self.y > camera.y:        
            self.speed += self.acceleration
            self.y -= self.speed # decreases Y, goes upwards
        else:
            self.kill()



    # draws the explosion on the screen
    def draw(self, camera):
        x = self.x - camera.x
        y = self.y - camera.y      
        self.font2.render(self.text, self.surface, (x+1, y+1))
        self.font.render(self.text, self.surface, (x, y))        
