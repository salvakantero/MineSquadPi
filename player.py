
# ==============================================================================
# .::Player class::.
# Create the main sprite and manage keyboard/mouse/joystick control, 
# movement and animation according to its state.
# ==============================================================================
#
#  This file is part of "Mine Squad Pi". Copyright (C) 2024 @salvakantero
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
import pygame.joystick
import constants
import enums
from shot import Shot


class Player(pygame.sprite.Sprite):
    def __init__(self, game, map, scoreboard):
        super().__init__()
        # common values
        self.ammo = 10 # unused ammunition collected
        self.score = 0 # current game score
        self.direction = pygame.math.Vector2(0.0) # direction of movement
        self.steps = -1 # check that the distance does not exceed the size of the tile.
        self.state = enums.IDLE # to know the animation to be applied
        self.facing_right = True # to know if the sprite needs to be mirrored
        self.invincible = False # invincible after losing a life or take a shield
        self.timer_from = 0 # tick number when the shield effect or x-ray effect begins
        self.timer_to = constants.TIME_REMAINING # time of shield, x-ray (20 secs.)

        # default values for Blaze
        self.energy = 10 # lives remaining
        self.speed = 1 # pixels per step

        # image/animation
        self.image_list = {
            # sequences of animations for the player depending on its status
            enums.IDLE: [
                pygame.image.load('images/sprites/player0.png').convert_alpha(),
                pygame.image.load('images/sprites/player1.png').convert_alpha()],
            enums.WALKING_X: [
                pygame.image.load('images/sprites/player2.png').convert_alpha(),
                pygame.image.load('images/sprites/player0.png').convert_alpha(),
                pygame.image.load('images/sprites/player3.png').convert_alpha(),
                pygame.image.load('images/sprites/player0.png').convert_alpha()],
            enums.WALKING_Y: [
                pygame.image.load('images/sprites/player2.png').convert_alpha(),
                pygame.image.load('images/sprites/player0.png').convert_alpha(),
                pygame.image.load('images/sprites/player3.png').convert_alpha(),
                pygame.image.load('images/sprites/player0.png').convert_alpha()],
        }
        self.frame_index = 0 # frame number
        self.animation_timer = 16 # timer to change frame
        self.animation_speed = 16 # frame dwell time
        self.image = self.image_list[self.state][0] # 1st frame of the animation
        self.rect = self.image.get_rect(topleft = ( # initial position
            constants.PLAYER_X_INI, constants.PLAYER_Y_INI))
        self.img_bullet = pygame.image.load('images/sprites/bullet.png').convert_alpha()
        # sounds
        self.sfx_shot = pygame.mixer.Sound('sounds/fx/sfx_shot.wav')
        self.sfx_shot.set_volume(0.7)
        self.sfx_no_ammo = pygame.mixer.Sound('sounds/fx/sfx_no_ammo.wav')
        self.sfx_no_ammo.set_volume(0.8)
        self.sfx_death = pygame.mixer.Sound('sounds/fx/sfx_death.wav') # touched by an enemy    
        # objects and others
        self.game = game
        self.map = map
        self.scoreboard = scoreboard


    # common code from joystick or keyboard to perform the shot
    def performs_shot(self):
        if self.ammo > 0:       
            if self.game.groups[enums.SHOT].sprite == None: # no shots on screen
                shot = Shot(self.rect, self.facing_right, self.img_bullet, 4)
                self.game.groups[enums.SHOT].add(shot)
                self.game.groups[enums.ALL].add(shot)
                self.sfx_shot.play()
                self.ammo -= 1
                self.scoreboard.invalidate()
        else: # no bullets
            self.sfx_no_ammo.play()


    # keyboard/mouse/joystick keystroke input
    def get_input(self):
        if self.steps < 0:
            if self.game.joystick is not None: # manages the joystick/joypad/gamepad
                # obtains the possible movement of the axes. A value greater than +-0.5 
                # is considered as intentional movement. The values obtained range from -1 to 1.
                axis_x = self.game.joystick.get_axis(0)
                axis_y = self.game.joystick.get_axis(1)
                # eliminates false movements
                if abs(axis_x) < 0.1: axis_x = 0.0
                if abs(axis_y) < 0.1: axis_y = 0.0            
                # press right
                if axis_x > 0.5:
                    self.direction.x = 1
                    self.facing_right = True
                # press left
                elif axis_x < -0.5:
                    self.direction.x = -1
                    self.facing_right = False
                # without lateral movement
                elif axis_x == 0.0:
                    self.direction.x = 0
                # press down
                if axis_y > 0.5:
                    self.direction.y = 1
                # press up
                elif axis_y < -0.5:
                    self.direction.y = -1
                # without vertical movement
                elif axis_y == 0.0:
                    self.direction.y = 0
                # press fire
                if self.game.joystick.get_button(0) or self.game.joystick.get_button(1):
                    self.performs_shot()
            else: # manages keystrokes
                key_state = pygame.key.get_pressed()
                # press up
                if key_state[self.game.config.up_key]:
                    self.direction.y = -1
                    self.steps += 1
                    self.facing_right = False
                    return
                # press down
                elif key_state[self.game.config.down_key]:
                    self.direction.y = 1
                    self.steps += 1
                    self.facing_right = True
                    return
                # press left
                elif key_state[self.game.config.left_key]:
                    self.direction.x = -1
                    self.steps += 1
                    self.facing_right = False
                    return
                # press right
                elif key_state[self.game.config.right_key]:
                    self.direction.x = 1
                    self.steps += 1
                    self.facing_right = True
                    return
                else:
                    self.direction.x = 0 # without horizontal movement
                    self.direction.y = 0 # without vertical movement
                
                # press fire or left mouse button
                if key_state[self.game.config.fire_key] or pygame.mouse.get_pressed()[0]:
                    self.performs_shot()

                #=================================================================
                # BETA trick
                #if key_state[pygame.K_KP_PLUS] or key_state[pygame.K_PLUS]:
                #    if self.lives < 99: 
                #        self.lives += 1
                #        self.scoreboard.invalidate() 
                # ================================================================          

        # number of steps
        if self.steps >= 0: 
            self.steps += 1
        # if it exceeds the tile size, it stops
        if self.steps >= constants.TILE_SIZE-1: 
            self.steps = -1


    # player status according to movement
    def get_state(self):
        if self.direction.x != 0: # is moving on x
            self.state = enums.WALKING_X
        elif self.direction.y != 0: # is moving on y
            self.state = enums.WALKING_Y
        else: # x does not change. Stopped
            self.state = enums.IDLE


    def horizontal_mov(self):
        # gets the new rect after applying the movement and check for collision
        x_temp = self.rect.x + (self.direction.x * self.speed)
        temp_rect = pygame.Rect((x_temp, self.rect.y),
            (constants.TILE_SIZE, constants.TILE_SIZE))

        collision = False # True if at least one tile collides
        index = -1 # index of the colliding tile to obtain its type
        # it is necessary to check all colliding tiles.
        for tile in self.map.tilemap_rect_list:
            index += 1
            if tile.colliderect(temp_rect):
                collision = True
                if self.direction.x < 0: # adjusts to the right of the tile
                    self.rect.left = tile.right
                elif self.direction.x > 0: # adjusts to the left of the tile
                    self.rect.right = tile.left
                break # stop the loop after the collision is detected
        if not collision:
            self.rect.x = x_temp # apply the new X position


    def vertical_mov(self):        
        # gets the new rectangle after applying the movement and check for collision
        y_temp = self.rect.y + (self.direction.y * self.speed)
        temp_rect = pygame.Rect((self.rect.x, y_temp), 
            (constants.TILE_SIZE, constants.TILE_SIZE))  

        collision = False # True if at least one tile collides
        index = -1 # index of the colliding tile to obtain its type
        # it is necessary to check all colliding tiles.
        for tile in self.map.tilemap_rect_list:
            index += 1
            if tile.colliderect(temp_rect):
                collision = True
                # obstacles, stops the player from all directions --------------      
                if self.map.tilemap_behaviour_list[index] == enums.OBSTACLE:
                    self.direction.y = 0
                # killer tile, one life less -----------------------------------           
                elif self.map.tilemap_behaviour_list[index] == enums.KILLER:
                    self.loses_life()
                    self.scoreboard.invalidate()
        if not collision:
            self.rect.y = y_temp # apply the new Y position


    def animate(self):
        # animation
        if (self.state == enums.IDLE):
            self.animation_speed = 16 # breathing
        else:
            self.animation_speed = 6 # running fast
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0 # reset the timer
            self.frame_index += 1 # next frame
        # exceeded the number of frames?
        if self.frame_index > len(self.image_list[self.state]) - 1:
            self.frame_index = 0 # reset the frame number
        # assigns image according to frame, status and direction
        if self.facing_right:
            self.image = self.image_list[self.state][self.frame_index]
        else: # reflects the image when looking to the left
            self.image = pygame.transform.flip(
                self.image_list[self.state][self.frame_index], True, False)
        # invincible effect (player blinks)
        if self.invincible:
            if (self.game.loop_counter >> 3) & 1 == 0: # % 8
                self.image.set_alpha(0) # visible
            else: 
                self.image.set_alpha(255) # no visible
        else:
            self.image.set_alpha(255)
    

    # subtracts one life and applies temporary invincibility
    def loses_life(self):
        if not self.invincible:
            self.energy -= 1
            self.sfx_death.play()
            self.invincible = True
            self.timer_from = pygame.time.get_ticks()
            self.timer_from -= (constants.TIME_REMAINING - 5000)  # 5 secs.


    # controls the hotspot time
    def check_timer(self):
        if self.invincible:
            if (pygame.time.get_ticks() - self.timer_from) >= self.timer_to:
                self.invincible = False


    def update(self):
        self.get_input()
        self.get_state()
        self.horizontal_mov()
        self.vertical_mov()
        self.animate()
        self.check_timer()