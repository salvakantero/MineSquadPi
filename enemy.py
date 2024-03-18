
# ==============================================================================
# .::Enemy class::.
# Creates an enemy based on its graphics and characteristics. 
# It animates it and gives it movement based on a movement type 
# and boundary coordinates.
# Mobile platforms are also considered in this class, to save resources.
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

import pygame
import math
import enums
import constants


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data, player_rect, enemy_images):
        # enemy_data = (x1, y1, x2, y2, vx, vy, type)
        super().__init__()
        # from xy values
        self.x = self.x1 = enemy_data[0]
        self.y = self.y1 = enemy_data[1]
        # to xy values
        self.x2 = enemy_data[2]
        self.y2 = enemy_data[3]
        # speed (pixels per frame)
        self.vx = enemy_data[4]
        self.vy = enemy_data[5]
        # enemy type; Infected, Avirus, Pelusoid, Fanty, Platform
        self.type = enemy_data[6]
        # additional attributes for the enemy Fanty
        if self.type == enums.FANTY:            
            self.state = enums.IDLE          
            self.sight_distance = 64 # pixels/frame
            self.acceleration = 0.04 #0.05 # pixels/frame
            self.max_speed = 2 # pixels/frame
        # player's current position (some enemies look at the player)
        self.player = player_rect
        # images
        self.image_list = enemy_images
        self.frame_index = 0 # frame number
        self.animation_timer = 12 # timer to change frame
        self.animation_speed = 12 # frame dwell time
        self.image = self.image_list[0] # first frame
        self.rect = self.image.get_rect()


    # changes a sign value according to the sign of another value (used for the Fanty)
    def addsign (self, n, value):
        if n >= 0: return value
        else: return -value


    # calculates the distance between two points (used for the Fanty)
    def distance (self, x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1)


    # maintains a value within limits (used for the Fanty)
    def limit(self, val, min, max):
        if val < min: return min
        elif val > max: return max
        return val


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
        if self.type != enums.FANTY: # no fanty  
            self.x += self.vx
            self.y += self.vy
            if self.x == self.x1 or self.x == self.x2: # x limit reached
                self.vx = -self.vx
            if self.y == self.y1 or self.y == self.y2: # y limit reached
                self.vy = -self.vy
        else: # fanty
            if self.state == enums.IDLE:                
                if self.distance (self.player.x, self.player.y, self.x, self.y) <= self.sight_distance:                    
                    self.state = enums.CHASING # close to the player, chases him
            elif self.state == enums.CHASING:
                if self.distance (self.player.x, self.player.y, self.x, self.y) > self.sight_distance:                    
                    self.state = enums.RETREATING # away from the player, stops the chase and retreats
                else:
                    # moves according to the value of several variables
                    self.vx = self.limit(self.vx + self.addsign(self.player.x - self.x, self.acceleration), -self.max_speed, self.max_speed)
                    self.vy = self.limit(self.vy + self.addsign(self.player.y - self.y, self.acceleration), -self.max_speed, self.max_speed)
                    # applies the new position, but keeps it within the boundaries of the screen.
                    self.x = self.limit(self.x + self.vx, 0, constants.MAP_UNSCALED_SIZE[0])
                    self.y = self.limit(self.y + self.vy, 0, constants.MAP_UNSCALED_SIZE[1])
            else: # retreating; going back to the starting point
                self.x += self.addsign(self.x1 - int(self.x), 1)
                self.y += self.addsign(self.y1 - int(self.y), 1)
                # close to the player? chases him again!
                if self.distance(self.player.x, self.player.y, self.x, self.y) <= self.sight_distance:
                    self.state = enums.CHASING		

            if self.state == enums.RETREATING:
                # too close to the starting point? switch to IDLE
                if (self.x1 >= self.x-1 and self.x1 <= self.x+1) \
                and (self.y1 >= self.y-1 and self.y1 <= self.y+1):                    
                    self.state = enums.IDLE
                    self.x = self.x1
                    self.y = self.y1      
						
        # applies the calculated position and the corresponding frame
        self.rect.x = self.x
        self.rect.y = self.y
        self.animate()
