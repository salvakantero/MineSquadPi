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
import random

# unit directions for random movement
_RANDOM_DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))



class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data, player_rect, enemy_images, map):
        super().__init__()
        self.map = map # get_tile_type()
        # enemy_data = (map, type, movement, tile_x1, tile_y1, tile_x2, tile_y2)
        # enemy type:
        # SCORPION, SNAKE, SOLDIER1
        # CRAB, PROJECTILE, SOLDIER2
        # SKIER, HABALI, SOLDIER3
        self.type = enemy_data[1]
        # movement type: HORIZONTAL, VERTICAL, RANDOM, CHASER
        self.movement = enemy_data[2]
        # health
        self.health = constants.ENEMY_LIFE[self.type]
        self.max_health = constants.ENEMY_LIFE[self.type]

        # respawn system
        self.is_dead = False
        self.death_time = 0
        self.respawn_delay = constants.ENEMY_RESPAWN_TIME
        self.original_data = enemy_data  # store original data for respawn
        
        # cache frequently used values
        self._tile_size = constants.TILE_SIZE
        self._activation_range_squared = constants.CHASER_ACTIVATION_RANGE * constants.CHASER_ACTIVATION_RANGE
        # from xy values
        self.x = self.x1 = enemy_data[3] * self._tile_size
        self.y = self.y1 = enemy_data[4] * self._tile_size
        # to xy values
        self.x2 = enemy_data[5] * self._tile_size
        self.y2 = enemy_data[6] * self._tile_size
        # speed
        self.vx = 0
        self.vy = 0
        # RANDOM/CHASER auxiliar variables
        self.is_active = False # whether the enemy is active or not
        self.is_paused = False # if the enemy is paused
        self.pause_timer = 0 # current pause timer
        self.target_x = 0 # target X position for current movement
        self.target_y = 0 # target Y position for current movement
        self.moving_to_target = False # if moving towards a target
        # player's current position (some enemies look at the player)
        self.player = player_rect
        # images
        self.image_list = enemy_images
        self.frame_index = 0  # frame number
        self.animation_timer = 0  # timer to change frame (start at 0)
        self.animation_speed = 18  # frame dwell time
        self.image = self.image_list[0]  # first frame


        self.rect = self.image.get_rect()

        # determine initial direction (moved here so self.rect exists before validation)
        if self.movement == enums.EM_HORIZONTAL:
            self.vx = 1 if self.x2 > self.x1 else -1
        elif self.movement == enums.EM_VERTICAL:
            self.vy = 1 if self.y2 > self.y1 else -1
        elif self.movement == enums.EM_RANDOM:
            self._set_random_direction()



    def animate(self):
        self.animation_timer += 1

        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            # cycle through frames 
            self.frame_index = (self.frame_index + 1) % len(self.image_list)
      
        self.image = self.image_list[self.frame_index]



    def update(self):
        # if dead, do not update movement or animation
        if self.is_dead:
            return

        # movement handling
        if self.movement == enums.EM_HORIZONTAL: self._update_horizontal_movement()
        elif self.movement == enums.EM_VERTICAL: self._update_vertical_movement()
        elif self.movement == enums.EM_RANDOM:   self._update_random_movement()
        elif self.movement == enums.EM_CHASER:   self._update_chaser_movement()

        # apply the calculated position and the corresponding frame
        self.rect.x = self.x
        self.rect.y = self.y
        self.animate()



    def draw(self, surface, camera):
        # do not draw if dead
        if self.is_dead:
            return

        if self._is_visible(camera):
            # draw the enemy on the screen with camera offset
            screen_x = self.x - camera.x
            screen_y = self.y - camera.y
            surface.blit(self.image, (screen_x, screen_y))



    ##### auxiliary functions #####

    # check whether a position is within the map boundaries and there are no obstacles.
    def _is_position_valid(self, x, y):        
        # check map limits
        if not (x >= 0 and y >= 0 and 
                x + self.rect.width <= constants.MAP_PIXEL_SIZE[0] and 
                y + self.rect.height <= constants.MAP_PIXEL_SIZE[1]):
            return False
                                  
        # check for obstacles in the way
        temp_rect = pygame.Rect(x, y, self.rect.width, self.rect.height)  
        points_to_check = [
            (temp_rect.left, temp_rect.top),
            (temp_rect.right - 1, temp_rect.top), 
            (temp_rect.left, temp_rect.bottom - 1),
            (temp_rect.right - 1, temp_rect.bottom - 1)]        
        for px, py in points_to_check:
            tile_x = px // self._tile_size
            tile_y = py // self._tile_size
            if self.map.get_tile_type(tile_x, tile_y) == enums.TT_OBSTACLE:
                return False                
        return True



    # sets a random direction for the RANDOM type
    def _set_random_direction(self):        
        # try directions in random order until a valid one is found
        dirs = list(_RANDOM_DIRECTIONS)
        random.shuffle(dirs)
        for dx, dy in dirs:
            tx = self.x + dx * self._tile_size
            ty = self.y + dy * self._tile_size
            if self._is_position_valid(tx, ty):
                self.vx, self.vy = dx, dy
                self.target_x, self.target_y = tx, ty
                self.moving_to_target = True
                self.is_paused = False
                self.pause_timer = 0
                return
        # no valid direction found - stay paused
        self.vx = self.vy = 0
        self.moving_to_target = False
        self.is_paused = True
        self.pause_timer = 0


    
    # check whether the player is within the activation range.
    def _is_player_in_range(self):
        if self.player is None:
            return False
             
        # calculate distance in tiles using cached values (optimized)
        enemy_tile_x = (self.x + self.rect.width // 2) // self._tile_size
        enemy_tile_y = (self.y + self.rect.height // 2) // self._tile_size
        player_tile_x = self.player.centerx // self._tile_size
        player_tile_y = self.player.centery // self._tile_size

        dx = enemy_tile_x - player_tile_x
        dy = enemy_tile_y - player_tile_y
        # use pre-calculated squared range for optimal performance
        return (dx * dx + dy * dy) <= self._activation_range_squared



    # updates the direction towards the player for CHASER type
    def _update_chaser_direction(self):
        if self.player is None:
            return

        # align to nearest tile using cached tile size
        self.x = round(self.x / self._tile_size) * self._tile_size
        self.y = round(self.y / self._tile_size) * self._tile_size

        # calculate distance in tiles using cached tile size
        enemy_tile_x = self.x // self._tile_size
        enemy_tile_y = self.y // self._tile_size
        player_tile_x = self.player.centerx // self._tile_size
        player_tile_y = self.player.centery // self._tile_size
        dx = player_tile_x - enemy_tile_x
        dy = player_tile_y - enemy_tile_y

        # determine target tile to move to using cached tile size
        target_x = self.x
        target_y = self.y

        # try to move towards the player, checking for obstacles
        horizontal_blocked = False
        vertical_blocked = False

        # check horizontal movement
        if dx != 0:
            if dx > 0:
                test_x = self.x + self._tile_size  # player is to the right
            else:
                test_x = self.x - self._tile_size  # player is to the left
            if self._is_position_valid(test_x, self.y):
                target_x = test_x
            else:
                horizontal_blocked = True

        # check vertical movement
        if dy != 0:
            if dy > 0:
                test_y = self.y + self._tile_size  # player is below
            else:
                test_y = self.y - self._tile_size  # player is above
            if self._is_position_valid(self.x, test_y):
                target_y = test_y
            else:
                vertical_blocked = True

        # decide which direction to move based on distance and obstacles
        if horizontal_blocked and vertical_blocked:
            # both directions blocked, stay in place
            self.moving_to_target = False
            self.vx = self.vy = 0
            return
        elif horizontal_blocked:
            # can only move vertically
            if target_y != self.y:
                self.target_x = self.x
                self.target_y = target_y
            else:
                self.moving_to_target = False
                self.vx = self.vy = 0
                return
        elif vertical_blocked:
            # can only move horizontally
            if target_x != self.x:
                self.target_x = target_x
                self.target_y = self.y
            else:
                self.moving_to_target = False
                self.vx = self.vy = 0
                return
        else:
            # both directions are valid, choose based on greater distance
            if abs(dx) > abs(dy):
                # prefer horizontal movement
                self.target_x = target_x
                self.target_y = self.y
            else:
                # prefer vertical movement
                self.target_x = self.x
                self.target_y = target_y

        # set velocity towards the target tile
        dx_target = self.target_x - self.x
        dy_target = self.target_y - self.y
        if dx_target != 0:
            self.vx = 1 if dx_target > 0 else -1
            self.vy = 0
        elif dy_target != 0:
            self.vx = 0
            self.vy = 1 if dy_target > 0 else -1
        else:
            self.vx = self.vy = 0
            self.moving_to_target = False
            return

        self.moving_to_target = True



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



    # handle horizontal movement
    def _update_horizontal_movement(self):
        self.x = self.x + self.vx   
        # determine left and right boundaries
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)        
        # detect when reaching either boundary and reverse direction
        if self.x <= min_x or self.x >= max_x:
            self.vx = -self.vx
            # ensure position stays within boundaries
            self.x = max(min_x, min(self.x, max_x))



    # handle vertical movement
    def _update_vertical_movement(self):        
        self.y = self.y + self.vy
        # determine upper and lower boundaries
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)        
        # detect when reaching either boundary and reverse direction
        if self.y <= min_y or self.y >= max_y:
            self.vy = -self.vy
            # ensure position stays within boundaries
            self.y = max(min_y, min(self.y, max_y))



    # handles random movement with pauses between changes of direction
    def _update_random_movement(self):
        if self.is_paused:
            self.pause_timer += 1
            self.vx = self.vy = 0
            if self.pause_timer >= constants.RANDOM_ENEMY_PAUSE_DURATION:
                self.is_paused = False
                self.pause_timer = 0
                self._set_random_direction()
            return

        # no target to move to - set a new random direction
        if not self.moving_to_target:
            self._set_random_direction()
            return

        # move towards the target tile
        self.x += self.vx
        self.y += self.vy
        # check if the target tile has been reached or passed
        reached = False
        if self.vx > 0 and self.x >= self.target_x: # moving right
            self.x = self.target_x
            reached = True
        elif self.vx < 0 and self.x <= self.target_x: # moving left
            self.x = self.target_x
            reached = True
        if self.vy > 0 and self.y >= self.target_y: # moving down
            self.y = self.target_y
            reached = True
        elif self.vy < 0 and self.y <= self.target_y: # moving up
            self.y = self.target_y
            reached = True
        # if reached the target tile, start a pause before the next move
        if reached:
            self.moving_to_target = False
            self.vx = self.vy = 0
            self.is_paused = True
            self.pause_timer = 0



    # manages the pursuit movement with activation zone and pauses
    def _update_chaser_movement(self):                
        # check if the player is in range
        player_in_range = self._is_player_in_range()
        
        # handle activation/deactivation
        if player_in_range and not self.is_active:
            # player enters range - activate enemy
            self.is_active = True
            self.is_paused = True
            self.pause_timer = 0
            self.moving_to_target = False
            self.vx = self.vy = 0
        elif not player_in_range and self.is_active:
            # player leaves range - deactivate enemy
            self.is_active = False
            self.is_paused = False
            self.pause_timer = 0
            self.moving_to_target = False
            self.vx = self.vy = 0

        # only move if active
        if self.is_active:
            # manage pauses and movement towards the player
            if self.is_paused:
                self.pause_timer += 1
                self.vx = self.vy = 0                
                if self.pause_timer >= constants.CHASER_ENEMY_PAUSE_DURATION:
                    # end the pause and start moving towards the player
                    self.is_paused = False
                    self.pause_timer = 0
                    # update direction towards the player
                    self._update_chaser_direction()
            else:
                # not paused - move towards the target tile
                if self.moving_to_target:
                    self.x += self.vx
                    self.y += self.vy                    
                    # check if the target tile has been reached or passed
                    reached = False
                    if self.vx > 0 and self.x >= self.target_x:  # moving right
                        self.x = self.target_x
                        reached = True
                    elif self.vx < 0 and self.x <= self.target_x:  # moving left
                        self.x = self.target_x
                        reached = True
                    elif self.vy > 0 and self.y >= self.target_y:  # moving down
                        self.y = self.target_y
                        reached = True
                    elif self.vy < 0 and self.y <= self.target_y:  # moving up
                        self.y = self.target_y
                        reached = True
                    # if reached the target tile, start a pause before the next move
                    if reached:
                        self.moving_to_target = False
                        self.vx = self.vy = 0
                        self.is_paused = True
                        self.pause_timer = 0



    # mark the enemy as dead and record the time
    def mark_as_dead(self):
        self.is_dead = True
        self.death_time = pygame.time.get_ticks()
        self.health = 0



    # check if the player is too close to the respawn position
    def is_player_near_respawn(self):
        if self.player is None:
            return False

        # calculate spawn position
        spawn_x = self.original_data[3] * self._tile_size
        spawn_y = self.original_data[4] * self._tile_size

        # calculate distance to player in tiles
        spawn_tile_x = spawn_x // self._tile_size
        spawn_tile_y = spawn_y // self._tile_size
        player_tile_x = self.player.centerx // self._tile_size
        player_tile_y = self.player.centery // self._tile_size

        dx = spawn_tile_x - player_tile_x
        dy = spawn_tile_y - player_tile_y
        distance_squared = dx * dx + dy * dy

        # check if player is within safe respawn distance (5 tiles)
        safe_distance_squared = constants.ENEMY_RESPAWN_SAFE_DISTANCE * constants.ENEMY_RESPAWN_SAFE_DISTANCE
        return distance_squared < safe_distance_squared



    # revive the enemy by restoring its original state
    def respawn(self):
        # restore initial position
        self.x = self.x1 = self.original_data[3] * self._tile_size
        self.y = self.y1 = self.original_data[4] * self._tile_size
        self.x2 = self.original_data[5] * self._tile_size
        self.y2 = self.original_data[6] * self._tile_size

        # restore health
        self.health = self.max_health
        self.is_dead = False
        self.death_time = 0

        # restore velocity and state
        self.vx = 0
        self.vy = 0
        self.is_active = False
        self.is_paused = False
        self.pause_timer = 0
        self.target_x = 0
        self.target_y = 0
        self.moving_to_target = False

        # restart animation
        self.frame_index = 0
        self.animation_timer = 0

        # determine initial direction based on movement type
        if self.movement == enums.EM_HORIZONTAL:
            self.vx = 1 if self.x2 > self.x1 else -1
        elif self.movement == enums.EM_VERTICAL:
            self.vy = 1 if self.y2 > self.y1 else -1
        elif self.movement == enums.EM_RANDOM:
            self._set_random_direction()

        # update rect
        self.rect.x = self.x
        self.rect.y = self.y





