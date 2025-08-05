
# ==============================================================================
# .::Explosion class::.
# Creates, destroys, and draws an explosion during its lifecycle.
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



class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, blast_animation):
        super().__init__()
        self.frame_index = 0 # frame number
        self.animation_speed = 0.12 # frame dwell time
        self.frames = blast_animation # image list
        self.image = self.frames[0] # first frame
        self.rect = self.image.get_rect(center = pos) # position



    # loads next frame of animation or ends
    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): # end of the animation
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)] # next frame



    # draws the explosion on the screen
    def draw(self, surface, camera):
        #surface.blit(self.image, self.rect)
        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        surface.blit(self.image, (screen_x, screen_y))