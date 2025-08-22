
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data, player_rect, enemy_images):
        # enemy_data = (type, map, speed, tile_x1, tile_y1, tile_x2, tile_y2)
        super().__init__()
        # enemy type: 
        # SCORPION, SNAKE, SOLDIER1
        # CRAB, PROJECTILE, SOLDIER2
        # SKIER, HABALI, SOLDIER3
        self.type = enemy_data[0]
        # speed (pixels per frame)
        self.speed = enemy_data[2]
        # from xy values
        self.x = self.x1 = enemy_data[3] * constants.TILE_SIZE
        self.y = self.y1 = enemy_data[4] * constants.TILE_SIZE
        # to xy values
        self.x2 = enemy_data[5] * constants.TILE_SIZE
        self.y2 = enemy_data[6] * constants.TILE_SIZE
        # player's current position (some enemies look at the player)
        self.player = player_rect
        # images
        self.image_list = enemy_images
        self.frame_index = 0 # frame number
        self.animation_timer = 12 # timer to change frame
        self.animation_speed = 12 # frame dwell time
        self.image = self.image_list[0] # first frame
        self.rect = self.image.get_rect()



    def animate(self):
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0 # reset the timer
            self.frame_index += 1 # next frame
        # exceeded the number of frames?
        if self.frame_index > len(self.image_list) - 1:
            self.frame_index = 0 # reset the frame number
        # assigns the original or inverted image:
        # moving to the right, or idle looking at the player
        if self.vx > 0 or (self.vx == 0 and self.player.x >= self.x):
            self.image = self.image_list[self.frame_index]
        # moving to the left, or idle looking at the player
        elif self.vx < 0 or (self.vx == 0 and self.player.x < self.x):
            self.image = pygame.transform.flip(self.image_list[self.frame_index], True, False)



    def update(self):
        # movement
        self.x += self.speed
        self.y += self.speed
        if self.x == self.x1 or self.x == self.x2: # x limit reached
            self.vx = -self.vx
        if self.y == self.y1 or self.y == self.y2: # y limit reached
            self.vy = -self.vy
        # applies the calculated position and the corresponding frame
        self.rect.x = self.x
        self.rect.y = self.y
        self.animate()



    # draws the enemy on the screen
    def draw(self, surface, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        surface.blit(self.image, (screen_x, screen_y))