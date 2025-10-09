
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
    ANIMATION_SPEED = 0.12  # class constant for all explosions

    def __init__(self, pos=None, blast_animation=None):
        super().__init__()
        # initialize with default values for pooling
        self.frame_index = 0
        self.frames = None
        self.active = False
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
        self.frame_index += self.ANIMATION_SPEED
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



# object pool for explosion instances to reduce memory allocation overhead
class ExplosionPool:
    
    def __init__(self, pool_size=10):
        # create pool of pre-allocated explosion objects
        self.available = [Explosion() for _ in range(pool_size)]
        self.active = []
    
    

    # get an explosion from the pool or create new one if pool is empty
    def get_explosion(self, pos, blast_animation):
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
    
    

    # update pool - move inactive explosions back to available pool
    def update(self):
        # move inactive explosions back to pool in single pass
        still_active = []
        for explosion in self.active:
            if explosion.active:
                still_active.append(explosion)
            else:
                # reset explosion for reuse
                explosion.frame_index = 0
                explosion.frames = None
                self.available.append(explosion)
        self.active = still_active
    

    
    # clear all explosions and return them to the pool
    def clear(self):
        for explosion in self.active:
            explosion.active = False
            explosion.kill()
        self.update()  # reuse update logic to return to pool
    
    

    # get number of currently active explosions
    def get_active_count(self):
        return len(self.active)
