
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
    def __init__(self, pos=None, blast_animation=None):
        super().__init__()
        # initialize with default values for pooling
        self.frame_index = 0 # frame number
        self.animation_speed = 0.12 # frame dwell time
        self.frames = blast_animation # image list
        self.active = False # pool management flag
        if pos is not None and blast_animation is not None:
            self.initialize(pos, blast_animation)
    
    
    # initialize/reset explosion for reuse from pool
    def initialize(self, pos, blast_animation):
        self.frame_index = 0
        self.frames = blast_animation
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.active = True



    # loads next frame of animation or ends
    def update(self):
        if not self.active:
            return
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): # end of the animation
            self.active = False
            self.kill()  # remove from sprite group
        else:
            self.image = self.frames[int(self.frame_index)] # next frame



    # draws the explosion on the screen
    def draw(self, surface, camera):
        if not self.active:
            return
        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        surface.blit(self.image, (screen_x, screen_y))


class ExplosionPool:
    """Object pool for explosion instances to reduce memory allocation overhead"""
    
    def __init__(self, pool_size=15):
        # create pool of pre-allocated explosion objects
        self.available = [Explosion() for _ in range(pool_size)]
        self.active = []
    
    
    def get_explosion(self, pos, blast_animation):
        """Get an explosion from the pool or create new one if pool is empty"""
        if self.available:
            explosion = self.available.pop()
            explosion.initialize(pos, blast_animation)
            self.active.append(explosion)
            return explosion
        else:
            # pool exhausted, create new explosion (fallback)
            explosion = Explosion(pos, blast_animation)
            self.active.append(explosion)
            return explosion
    
    
    def update(self):
        """Update pool - move inactive explosions back to available pool"""
        inactive_explosions = []
        for i, explosion in enumerate(self.active):
            if not explosion.active:
                inactive_explosions.append(i)
        
        # remove inactive explosions from active list and return to pool
        for i in reversed(inactive_explosions):  # reverse order to maintain indices
            explosion = self.active.pop(i)
            # reset explosion for reuse
            explosion.frame_index = 0
            explosion.active = False
            explosion.frames = None
            self.available.append(explosion)
    
    
    def clear(self):
        """Clear all explosions and return them to the pool"""
        for explosion in self.active:
            explosion.active = False
            explosion.kill()
            explosion.frame_index = 0
            explosion.frames = None
            self.available.append(explosion)
        self.active.clear()
    
    
    def get_active_count(self):
        """Get number of currently active explosions"""
        return len(self.active)