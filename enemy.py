
# ==============================================================================
# .::Enemy class::.
# Creates an enemy based on its graphics and characteristics. 
# It animates it and gives it movement based on a movement type 
# and boundary coordinates.
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

import constants
import enums



class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data, player_rect, enemy_images):
        # enemy_data = (map, type, movement, tile_x1, tile_y1, tile_x2, tile_y2)
        super().__init__()
        # enemy type: 
        # SCORPION, SNAKE, SOLDIER1
        # CRAB, PROJECTILE, SOLDIER2
        # SKIER, HABALI, SOLDIER3
        self.type = enemy_data[1]
        # movement type: HORIZONTAL, VERTICAL, RANDOM, CHASER
        self.movement = enemy_data[2]
        # from xy values
        self.x = self.x1 = enemy_data[3] * constants.TILE_SIZE
        self.y = self.y1 = enemy_data[4] * constants.TILE_SIZE
        # to xy values
        self.x2 = enemy_data[5] * constants.TILE_SIZE
        self.y2 = enemy_data[6] * constants.TILE_SIZE
        # speed of movement
        self.speed = 1
        self.vx = 0
        self.vy = 0
        if self.movement == enums.EM_HORIZONTAL:
            # determine initial direction based on x1 and x2 positions
            self.vx = self.speed if self.x2 > self.x1 else -self.speed
        elif self.movement == enums.EM_VERTICAL:
            # determine initial direction based on y1 and y2 positions
            self.vy = self.speed if self.y2 > self.y1 else -self.speed
        # player's current position (some enemies look at the player)
        self.player = player_rect
        # images
        self.image_list = enemy_images
        self.frame_index = 0  # frame number
        self.animation_timer = 12  # timer to change frame
        self.animation_speed = 12  # frame dwell time
        self.image = self.image_list[0]  # first frame
        self.rect = self.image.get_rect()



    def animate(self):
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0  # reset the timer
            self.frame_index = (self.frame_index + 1) % len(self.image_list)  # cycle through frames        
        # assigns the original or flipped image based on movement direction
        current_frame = self.image_list[self.frame_index]
        # moving to the right
        if self.vx >= 0: self.image = current_frame
        # moving to the left
        else: self.image = pygame.transform.flip(current_frame, True, False)



    # check if enemy is visible within camera bounds
    def _is_visible(self, camera):
        return (
            # check right edge
            self.x + self.rect.width > camera.x and
            # check left edge
            self.x < camera.x + constants.SCREEN_MAP_UNSCALED_SIZE[0] and
            # check bottom edge
            self.y + self.rect.height > camera.y and
            # check top edge
            self.y < camera.y + constants.SCREEN_MAP_UNSCALED_SIZE[1])
        


    def update(self):   
        # movement handling
        if self.movement == enums.EM_HORIZONTAL: self._update_horizontal_movement()
        elif self.movement == enums.EM_VERTICAL: self._update_vertical_movement()
        # apply the calculated position and the corresponding frame
        self.rect.x = self.x
        self.rect.y = self.y
        self.animate()



    def _update_horizontal_movement(self):
        # handle horizontal movement with boundary checking
        self.x += self.vx
        # determine left and right boundaries
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)        
        # detect when reaching either boundary and reverse direction
        if self.x <= min_x or self.x >= max_x:
            self.vx = -self.vx
            # ensure position stays within boundaries
            self.x = max(min_x, min(self.x, max_x))



    def _update_vertical_movement(self):
        # handle vertical movement with boundary checking
        self.y += self.vy
        # determine upper and lower boundaries
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)        
        # detect when reaching either boundary and reverse direction
        if self.y <= min_y or self.y >= max_y:
            self.vy = -self.vy
            # ensure position stays within boundaries
            self.y = max(min_y, min(self.y, max_y))



    def draw(self, surface, camera):
        if not self._is_visible(camera):
            return
        # draw the enemy on the screen with camera offset
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        surface.blit(self.image, (screen_x, screen_y))
