
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
    def __init__(self, who_is, game, map, scoreboard):
        super().__init__()
        # common values
        self.who_is = who_is # Blaze = 0, Piper = 1, Norman = 2 
        self.ammo = 10 # unused ammunition collected
        self.score = 0 # current game score
        self.direction = pygame.math.Vector2(0.0) # direction of movement
        self.steps = -1 # check that the distance does not exceed the size of the tile.
        self.state = enums.PS_IDLE_UP # to know the animation to be applied
        self.look_at = enums.D_UP # where the player looks
        self.invincible = False # invincible after losing a life or take a shield
        self.timer_from = 0 # tick number when the shield effect or binoculars effect begins
        self.timer_to = constants.TIME_REMAINING # time of shield, binoculars (20 secs.)
        # character-specific values
        self.energy, self.speed = self.set_player_attributes()
        # sequences of animations for the player depending on its status
        self.load_player_images(self.who_is)
        self.frame_index = 0 # frame number
        self.animation_timer = 16 # timer to change frame
        self.animation_speed = 16 # frame dwell time
        self.image = self.image_list[self.state][0] # 1st frame of the animation
        self.rect = self.image.get_rect(topleft = ( # initial position
            constants.PLAYER_X_INI, constants.PLAYER_Y_INI))
        # FX sounds
        self.load_sounds()
        # objects and others
        self.game = game
        self.map = map
        self.scoreboard = scoreboard


    # set energy and speed based on player type
    def set_player_attributes(self):
        if self.who_is == enums.PL_PIPER:   return  8, 2
        elif self.who_is == enums.PL_BLAZE: return 12, 1
        else:                               return 16, 0


    # Load player images for animations
    def load_player_images(self, who_is):
        # sequences of animations for the player depending on its status
        path = 'images/sprites/player/' + str(who_is) + '/'
        self.image_list = {
            #----------------------------------------------------------#
            enums.PS_IDLE_UP: [
                pygame.image.load(path + 'player0.png').convert_alpha(),
                pygame.image.load(path + 'player1.png').convert_alpha()],
            enums.PS_WALK_UP: [
                pygame.image.load(path + 'player2.png').convert_alpha(),
                pygame.image.load(path + 'player0.png').convert_alpha(),
                pygame.image.load(path + 'player3.png').convert_alpha(),
                pygame.image.load(path + 'player0.png').convert_alpha()],
            #----------------------------------------------------------#
            enums.PS_IDLE_DOWN: [
                pygame.image.load(path + 'player4.png').convert_alpha(),
                pygame.image.load(path + 'player5.png').convert_alpha()],
            enums.PS_WALK_DOWN: [
                pygame.image.load(path + 'player6.png').convert_alpha(),
                pygame.image.load(path + 'player4.png').convert_alpha(),
                pygame.image.load(path + 'player7.png').convert_alpha(),
                pygame.image.load(path + 'player4.png').convert_alpha()],
            #----------------------------------------------------------#
            enums.PS_IDLE_LEFT: [
                pygame.image.load(path + 'player8.png').convert_alpha(),
                pygame.image.load(path + 'player9.png').convert_alpha()],
            enums.PS_WALK_LEFT: [
                pygame.image.load(path + 'player10.png').convert_alpha(),
                pygame.image.load(path + 'player8.png').convert_alpha(),
                pygame.image.load(path + 'player11.png').convert_alpha(),
                pygame.image.load(path + 'player8.png').convert_alpha()],
            #----------------------------------------------------------#
            enums.PS_IDLE_RIGHT: [
                pygame.image.load(path + 'player12.png').convert_alpha(),
                pygame.image.load(path + 'player13.png').convert_alpha()],
            enums.PS_WALK_RIGHT: [
                pygame.image.load(path + 'player14.png').convert_alpha(),
                pygame.image.load(path + 'player12.png').convert_alpha(),
                pygame.image.load(path + 'player15.png').convert_alpha(),
                pygame.image.load(path + 'player12.png').convert_alpha()],
        }
            

    # Load sounds for the player
    def load_sounds(self):
        sound_path = 'sounds/fx/'
        self.sfx_shot = pygame.mixer.Sound(sound_path + 'sfx_shot.wav')
        self.sfx_shot.set_volume(0.7)
        self.sfx_no_ammo = pygame.mixer.Sound(sound_path + 'sfx_no_ammo.wav')
        self.sfx_no_ammo.set_volume(0.8)
        self.sfx_death = pygame.mixer.Sound(sound_path + 'sfx_death.wav')  # Touched by an enemy
        self.sfx_flag = pygame.mixer.Sound(sound_path + "sfx_shot.wav")


    # common code for a shot to be fired
    def fire(self):
        if self.ammo > 0:       
            if not self.game.groups[enums.SG_SHOT].sprite: # no shots on screen
                # direction of the shot
                dir_vectors = {
                    enums.D_UP: pygame.math.Vector2(0, -2),
                    enums.D_DOWN: pygame.math.Vector2(0, 2),
                    enums.D_LEFT: pygame.math.Vector2(-2, 0),
                    enums.D_RIGHT: pygame.math.Vector2(2, 0) }
                vector = dir_vectors.get(self.look_at, pygame.math.Vector2(0, -2)) # UP by default
                # shot creation
                shot = Shot(self.rect, self.game.srf_map.get_rect(), vector)
                self.game.groups[enums.SG_SHOT].add(shot)
                self.game.groups[enums.SG_ALL].add(shot)
                self.sfx_shot.play()
                self.ammo -= 1
                self.scoreboard.invalidate()
        else: # no bullets
            self.sfx_no_ammo.play()


    # common code for placing a flag
    def place_flag(self):
        if self.game.remaining_flags > 0:
            offsets = {
                enums.D_UP: (0, -1), enums.D_DOWN: (0, 1),
                enums.D_LEFT: (-1, 0), enums.D_RIGHT: (1, 0) }
            # places the flag in front of where the player is facing
            offset_x, offset_y = offsets.get(self.look_at, (0, 0))  
            x = (self.rect.x // constants.TILE_SIZE) + offset_x
            y = (self.rect.y // constants.TILE_SIZE) + offset_y
            # if there is no flag on the tile
            if self.map.map_data['mines'][y][x] != enums.MD_FLAG:
                # if there is a mine in the marked tile
                if self.map.map_data['mines'][y][x] == enums.MD_MINE:
                    self.game.remaining_mines -= 1
                self.map.map_data['mines'][y][x] = enums.MD_FLAG # place the flag
                self.sfx_flag.play()
                self.game.remaining_flags -= 1
                self.scoreboard.invalidate()
        else: # no flags
            self.sfx_no_ammo.play()


    # keyboard/mouse/joystick keystroke input
    def get_input(self): 
        def update_steps():
            # distance travelled control
            if self.steps >= 0: 
                self.steps += 1 # continue walking
            # if it exceeds the tile size...
            if self.steps >= constants.TILE_SIZE-1: 
                self.steps = -1 # it stops

        if self.game.joystick is not None: # manages the joystick/joypad/gamepad
            # press fire buttons
            if self.game.joystick.get_button(0) or self.game.joystick.get_button(1):
                self.fire()
            # press flag buttons
            if self.game.joystick.get_button(2) or self.game.joystick.get_button(3):
                self.place_flag()

            if self.steps < 0: # if it is not moving
                # obtains the possible movement of the axes. A value greater than +-0.5 
                # is considered as intentional movement. The values obtained range from -1 to 1.
                axis_x = self.game.joystick.get_axis(0)
                axis_y = self.game.joystick.get_axis(1)
                # eliminates false movements
                def eliminate_false_movements(value):
                    return value if abs(value) >= 0.1 else 0.0
                axis_x = eliminate_false_movements(axis_x)
                axis_y = eliminate_false_movements(axis_y)
                # press up
                if axis_y < -0.5:
                    self.direction.update(0, -1)
                    self.look_at = enums.D_UP
                    self.steps += 1
                    return
                # press down
                elif axis_y > 0.5:
                    self.direction.update(0, 1)
                    self.look_at = enums.D_DOWN
                    self.steps += 1
                    return
                # press left
                elif axis_x < -0.5:
                    self.direction.update(-1, 0)
                    self.look_at = enums.D_LEFT
                    self.steps += 1
                    return
                # press right
                elif axis_x > 0.5:
                    self.direction.update(1, 0)
                    self.look_at = enums.D_RIGHT
                    self.steps += 1
                    return
                # without movement
                else:
                    self.direction.update(0, 0)

        else: # manages keystrokes
            key_state = pygame.key.get_pressed()
            if self.steps < 0: # if it is not moving
                # press up
                if key_state[self.game.config.up_key]:
                    self.direction.update(0, -1)
                    self.look_at = enums.D_UP
                    self.steps += 1
                    return
                # press down
                elif key_state[self.game.config.down_key]:
                    self.direction.update(0, 1)
                    self.look_at = enums.D_DOWN
                    self.steps += 1
                    return
                # press left
                elif key_state[self.game.config.left_key]:
                    self.direction.update(-1, 0)
                    self.look_at = enums.D_LEFT
                    self.steps += 1
                    return
                # press right
                elif key_state[self.game.config.right_key]:
                    self.direction.update(1, 0)
                    self.look_at = enums.D_RIGHT
                    self.steps += 1
                    return
                # without movement
                else:
                    self.direction.update(0, 0)

                #=================================================================
                # BETA trick
                #if key_state[pygame.K_KP_PLUS] or key_state[pygame.K_PLUS]:
                #    if self.lives < 99: 
                #        self.lives += 1
                #        self.scoreboard.invalidate() 
                # ================================================================          

        # distance travelled control
        update_steps()


    # player status according to movement
    def get_state(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.state = self.look_at
        elif self.direction.y < 0:  self.state = enums.PS_WALK_UP
        elif self.direction.y > 0:  self.state = enums.PS_WALK_DOWN
        elif self.direction.x > 0:  self.state = enums.PS_WALK_RIGHT
        elif self.direction.x < 0:  self.state = enums.PS_WALK_LEFT


    # gets the new rect after applying the movement and check for collision
    def move(self, axis):
        if axis == enums.CA_HORIZONTAL:
            temp_rect = pygame.Rect((self.rect.x + self.direction.x * self.speed, self.rect.y),
                                    (constants.TILE_SIZE, constants.TILE_SIZE))
            temp_pos = self.rect.x
        else: # vertical
            temp_rect = pygame.Rect((self.rect.x, self.rect.y + self.direction.y * self.speed),
                                    (constants.TILE_SIZE, constants.TILE_SIZE))
            temp_pos = self.rect.y

        collision = False
        # it is necessary to check all obstacle tiles.
        for tileRect, behaviour in self.map.map_data['tilemap_info']:
            if tileRect.colliderect(temp_rect):
                if behaviour == enums.TB_OBSTACLE: collision = True
                break
        # Apply the new position if no collision occurs
        if not collision:
            if axis == enums.CA_HORIZONTAL:
                self.rect.x = temp_pos + self.direction.x * self.speed
            else: # vertical
                self.rect.y = temp_pos + self.direction.y * self.speed
            if self.steps < 0:
                self.map.reveal_tile(self.rect.y // constants.TILE_SIZE, self.rect.x // constants.TILE_SIZE)


    def horizontal_mov(self):
        self.move(enums.CA_HORIZONTAL)


    def vertical_mov(self):
        self.move(enums.CA_VERTICAL)


    def animate(self):
        # invincible effect (player blinks)
        def handle_invincibility_effect():
            if self.invincible:
                if (self.game.loop_counter >> 3) & 1 == 0: # % 8
                    self.image.set_alpha(0) # visible
                else: 
                    self.image.set_alpha(255) # no visible
            else:
                self.image.set_alpha(255)
        # animation
        if (self.state <= enums.PS_IDLE_RIGHT): # breathing
            self.animation_speed = constants.ANIM_SPEED_IDLE # slower
        else: # walking
            self.animation_speed = constants.ANIM_SPEED_WALK
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0 # reset the timer
            self.frame_index += 1 # next frame
        # exceeded the number of frames?
        if self.frame_index > len(self.image_list[self.state]) - 1:
            self.frame_index = 0 # reset the frame number
        # assigns image according to frame, status and direction
        self.image = self.image_list[self.state][self.frame_index]
        # invincible effect (player blinks)
        handle_invincibility_effect()


    # subtracts one life and applies temporary invincibility
    def loses_life(self, value):
        if not self.invincible:
            self.energy -= value
            self.sfx_death.play()
            if self.energy >= 0:
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
        if self.direction.x != 0: self.horizontal_mov()
        if self.direction.y != 0: self.vertical_mov()
        self.animate()
        self.check_timer()