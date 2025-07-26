
# ==============================================================================
# .::Player class::.
# Create the main sprite and manage keyboard/mouse/joystick control, 
# movement and animation according to its state.
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
import pygame.joystick
import constants
import enums
from shot import Shot



class Player(pygame.sprite.Sprite):
    def __init__(self, who_is, game, map, scoreboard):
        super().__init__()
        # Blaze = 0, Piper = 1
        self.who_is = who_is
        self.energy, self.speed = self._set_player_attributes()
        self.ammo = 10 # ammunition collected
        # initialize player position
        # starts at the centre of the map, 1/4 from the left and at the bottom
        self.x, self.y = constants.PLAYER_X_INI, constants.PLAYER_Y_INI
        # movement
        self.direction = pygame.math.Vector2(0.0, 0.0) # direction of movement
        self.steps = -1 # check that the distance does not exceed the size of the tile.
        # player state
        self.state = enums.PS_IDLE_UP # to know the animation to be applied
        self.look_at = enums.DI_UP # where the player looks
        # turning state
        self.is_turning = False # if 'True' apply a pause before movement
        self.turn_timer = 0 # time before applying movement if it rotates
        self.last_key_pressed = None # check that the key is still pressed
        #animation
        self.frame_index = 0 # frame number
        self.animation_timer = 0 # timer to change frame
        self.animation_speed = constants.ANIM_SPEED_IDLE # frame dwell time
        # images
        self._load_player_images(self.who_is)
        self.image = self.image_list[self.state][0] # 1st frame of the animation
        # invincibility
        self.invincible = False # invincible after losing a life or take a shield
        self.timer_from = 0 # tick number when the shield effect begins
        self.timer_to = constants.TIME_REMAINING # time of shield (20 secs.)        
        # FX sounds
        self.sfx_shot1 = pygame.mixer.Sound(constants.FX_PATH + 'sfx_shot1.wav')
        self.sfx_no_ammo = pygame.mixer.Sound(constants.FX_PATH + 'sfx_no_ammo.wav')
        self.sfx_death = pygame.mixer.Sound(constants.FX_PATH + 'sfx_death.wav')
        self.sfx_beacon = pygame.mixer.Sound(constants.FX_PATH + 'sfx_beacon.wav')
        self.sfx_blocked = pygame.mixer.Sound(constants.FX_PATH + 'sfx_locked.wav')
        self.sfx_blocked.set_volume(0.2)
        # objects and others
        self.game = game
        self.map = map
        self.scoreboard = scoreboard
        # cache frequently used values
        self._direction_mappings = {
            pygame.K_UP: (enums.DI_UP, pygame.math.Vector2(0, -1)),
            pygame.K_DOWN: (enums.DI_DOWN, pygame.math.Vector2(0, 1)),
            pygame.K_LEFT: (enums.DI_LEFT, pygame.math.Vector2(-1, 0)),
            pygame.K_RIGHT: (enums.DI_RIGHT, pygame.math.Vector2(1, 0))
        }
        self._state_mappings = {
            enums.DI_UP: (enums.PS_IDLE_UP, enums.PS_WALK_UP),
            enums.DI_DOWN: (enums.PS_IDLE_DOWN, enums.PS_WALK_DOWN),
            enums.DI_LEFT: (enums.PS_IDLE_LEFT, enums.PS_WALK_LEFT),
            enums.DI_RIGHT: (enums.PS_IDLE_RIGHT, enums.PS_WALK_RIGHT)
        }



    # set energy and speed based on player type
    def _set_player_attributes(self):        # ENERGY  SPEED
        if self.who_is == enums.PL_PIPER:   return 10, 2
        else:                               return 14, 1



    # Load player images for animations
    def _load_player_images(self, who_is):
        base_path = constants.SPR_PATH + 'player/' + str(who_is) + '/'        
        image_files = {
            enums.PS_IDLE_UP: ['player0.png', 'player1.png'],
            enums.PS_WALK_UP: ['player2.png', 'player1.png', 'player3.png', 'player1.png'],
            enums.PS_IDLE_DOWN: ['player4.png', 'player5.png'],
            enums.PS_WALK_DOWN: ['player6.png', 'player5.png', 'player7.png', 'player5.png'],
            enums.PS_IDLE_LEFT: ['player8.png', 'player9.png'],
            enums.PS_WALK_LEFT: ['player10.png', 'player9.png', 'player11.png', 'player9.png'],
            enums.PS_IDLE_RIGHT: ['player12.png', 'player13.png'],
            enums.PS_WALK_RIGHT: ['player14.png', 'player13.png', 'player15.png', 'player13.png'],
        }        
        self.image_list = {}
        for state, files in image_files.items():
            self.image_list[state] = [pygame.image.load(f"{base_path}{filename}").convert_alpha()
                for filename in files]



    # common code for a shot to be fired
    def fire(self):
        pass
        # if self.ammo > 0:       
        #     if not self.game.groups[enums.SG_SHOT].sprite: # no shots on screen
        #         # direction of the shot
        #         dir_vectors = {
        #             enums.DI_UP: pygame.math.Vector2(0, -2),
        #             enums.DI_DOWN: pygame.math.Vector2(0, 2),
        #             enums.DI_LEFT: pygame.math.Vector2(-2, 0),
        #             enums.DI_RIGHT: pygame.math.Vector2(2, 0) }
        #         vector = dir_vectors.get(self.look_at, pygame.math.Vector2(0, -2)) # UP by default
        #         # shot creation
        #         shot = Shot(self.rect, self.game.srf_map.get_rect(), vector)
        #         self.game.groups[enums.SG_SHOT].add(shot)
        #         self.game.groups[enums.SG_ALL].add(shot)
        #         self.sfx_shot1.play()
        #         self.ammo -= 1
        #         self.scoreboard.invalidate()
        # else: # no bullets
        #     self.sfx_no_ammo.play()



    # common code for placing a flag/beacon
    def place_beacon(self):
        pass
        # offsets = {
        #     enums.DI_UP: (0, -1), enums.DI_DOWN: (0, 1),
        #     enums.DI_LEFT: (-1, 0), enums.DI_RIGHT: (1, 0) 
        # }        
        # # places the beacon in front of where the player is facing
        # offset_x, offset_y = offsets.get(self.look_at, (0, 0))
        # x = (self.rect.x // constants.TILE_SIZE) + offset_x
        # y = (self.rect.y // constants.TILE_SIZE) + offset_y
        
        # # Verificar límites del mapa
        # if (0 <= x < constants.MAP_TILE_SIZE[0] and 0 <= y < constants.MAP_TILE_SIZE[1]):
        #     # if there is no beacon on the tile
        #     if self.map.map_data['tile_types'][y][x] != enums.TT_OBSTACLE and \
        #        self.map.map_data['mines_info'][y][x] != enums.MI_BEACON:
        #         # if there is a mine in the marked tile
        #         if self.map.map_data['mines_info'][y][x] == enums.MI_MINE:
        #             self.game.remaining_mines -= 1                    
        #             self.score += 125
        #             self.game.floating_text.text = '+125'
        #             self.game.floating_text.x = self.rect.x
        #             self.game.floating_text.y = self.rect.y
        #             self.game.floating_text.speed = 0
        #             # if there is a mine on the tile, remove it                       
        #             if self.map.map_data['tile_types'][y][x] == enums.TT_MINE:
        #                 self.map.map_data['tile_types'][y][x] = enums.TT_NO_ACTION
        #         # place the beacon
        #         self.map.map_data['mines_info'][y][x] = enums.MI_BEACON
        #         self.sfx_beacon.play()
        #         self.game.remaining_beacons -= 1
        #         self.scoreboard.invalidate()
        #     else: # if there is a beacon on the tile                
        #         self.sfx_no_ammo.play()
        # else: # Tile fuera de los límites del mapa            
        #     self.sfx_no_ammo.play()



    # keyboard/mouse/joystick keystroke input
    def get_input(self): 
        # distance travelled control
        if self.steps >= 0: 
            self.steps += 1 # continue walking
            # if it exceeds the tile size...
            if self.steps >= constants.TILE_SIZE-1: 
                self.steps = -1 # it stops
            return    
        # if the player is turning, handle the waiting time
        if self.is_turning:
            self._handle_turning()
            return        
        # if the player is not turning, check for movement input
        self._handle_movement_input()

        # if self.game.joystick is not None: # manages the joystick/joypad/gamepad
        #     # eliminates false movements
        #     def eliminate_false_movements(value):
        #         return value if abs(value) >= 0.1 else 0.0
            
        #     # press fire buttons
        #     if self.game.joystick.get_button(0) or self.game.joystick.get_button(1):
        #         self.fire()
        #     # press beacon buttons
        #     if self.game.joystick.get_button(2) or self.game.joystick.get_button(3):
        #         self.place_beacon()

        #     if self.steps < 0: # if it is not moving
        #         # obtains the possible movement of the axes. A value greater than +-0.5 
        #         # is considered as intentional movement. The values obtained range from -1 to 1.
        #         axis_x = self.game.joystick.get_axis(0)
        #         axis_y = self.game.joystick.get_axis(1)
        #         axis_x = eliminate_false_movements(axis_x)
        #         axis_y = eliminate_false_movements(axis_y)

        #         # determine new direction
        #         new_look_at = None                
        #         if axis_y < -0.5: new_look_at = enums.DI_UP
        #         elif axis_y > 0.5: new_look_at = enums.DI_DOWN
        #         elif axis_x < -0.5: new_look_at = enums.DI_LEFT
        #         elif axis_x > 0.5: new_look_at = enums.DI_RIGHT

        #         # if there is change of direction
        #         if new_look_at is not None and new_look_at != self.look_at:
        #             self.look_at = new_look_at
        #             self.direction.update(0, 0)  # stop movement
        #             self.turn_timer = pygame.time.get_ticks()
        #             self.is_turning = True
        #             return # exit to wait for delay
                
        #         # if in turning mode and sufficient time has elapsed
        #         if self.is_turning:
        #             current_time = pygame.time.get_ticks()
        #              # waiting time (120ms)
        #             if current_time - self.turn_timer > 120:
        #                 self.is_turning = False
        #                 # move only if the joystick holds direction
        #                 if ( (new_look_at == enums.DI_UP and axis_y < -0.5) or
        #                     (new_look_at == enums.DI_DOWN and axis_y > 0.5) or
        #                     (new_look_at == enums.DI_LEFT and axis_x < -0.5) or
        #                     (new_look_at == enums.DI_RIGHT and axis_x > 0.5) ):
        #                     if new_look_at == enums.DI_UP: self.direction.update(0, -1)
        #                     elif new_look_at == enums.DI_DOWN: self.direction.update(0, 1)
        #                     elif new_look_at == enums.DI_LEFT: self.direction.update(-1, 0)
        #                     elif new_look_at == enums.DI_RIGHT: self.direction.update(1, 0)
        #                     self.steps += 1
        #             return

        #         # immediate movement if not turning
        #         if new_look_at is not None:
        #             if new_look_at == enums.DI_UP: self.direction.update(0, -1)
        #             elif new_look_at == enums.DI_DOWN: self.direction.update(0, 1)
        #             elif new_look_at == enums.DI_LEFT: self.direction.update(-1, 0)
        #             elif new_look_at == enums.DI_RIGHT: self.direction.update(1, 0)
        #             self.steps += 1
        #             return
        #         else:  # no movement
        #             self.direction.update(0, 0)

            #=================================================================
            # BETA trick
            #if key_state[pygame.K_KP_PLUS] or key_state[pygame.K_PLUS]:
            #    if self.lives < 99: 
            #        self.lives += 1
            #        self.scoreboard.invalidate() 
            # ================================================================          



    def _handle_turning(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.turn_timer > 120: # waiting time (120ms)
            self.is_turning = False
            # verifies if the last key pressed is still held down
            # (we only move forward if the key is still pressed)
            key_state = pygame.key.get_pressed()
            if (self.last_key_pressed and 
                key_state[self.last_key_pressed] and 
                self.last_key_pressed in self._direction_mappings):
                _, direction_vector = self._direction_mappings[self.last_key_pressed]
                self.direction.update(direction_vector)
                self.steps = 0



    def _handle_movement_input(self):
        key_state = pygame.key.get_pressed()
        previous_look_at = self.look_at
        # check which key is pressed
        pressed_key = None
        for key in self._direction_mappings:
            if key_state[key]:
                pressed_key = key
                break
        # if no key is pressed, stop the player
        if not pressed_key:
            self.direction.update(0, 0)
            return
        # update the direction and look_at based on the pressed key
        self.look_at, direction_vector = self._direction_mappings[pressed_key]
        self.last_key_pressed = pressed_key
        # if the direction has changed, reset the steps and start turning
        if previous_look_at != self.look_at:
            self.direction.update(0, 0)
            self.turn_timer = pygame.time.get_ticks()
            self.is_turning = True
        else: # if the direction is the same, update the movement vector
            self.direction.update(direction_vector)
            self.steps = 0



    # determines the player's state based on movement
    def get_state(self):
        is_moving = self.direction.x != 0 or self.direction.y != 0
        if self.look_at in self._state_mappings:
            idle_state, walk_state = self._state_mappings[self.look_at]
            self.state = walk_state if is_moving else idle_state          



    # moves the player in the specified axis
    def move(self, axis):
        collision = True
        if axis == enums.CA_HORIZONTAL:
            new_x = self.x + self.direction.x * self.speed
            temp_rect = pygame.Rect(new_x, self.y, constants.TILE_SIZE, constants.TILE_SIZE)
            # check for horizontal collisions
            if not self._check_collision(temp_rect, enums.CA_HORIZONTAL):
                self.x = new_x
                collision = False
        else: # vertical movement
            new_y = self.y + self.direction.y * self.speed
            temp_rect = pygame.Rect(self.x, new_y, constants.TILE_SIZE, constants.TILE_SIZE)
            # verify if the new position is within the map boundaries
            if (temp_rect.top < 0 or temp_rect.bottom > constants.MAP_TILE_SIZE[1] * constants.TILE_SIZE):
                return
            # check for vertical collisions
            if not self._check_collision(temp_rect, enums.CA_VERTICAL):
                self.y = new_y
                collision = False
        if collision: # sounds when the player hits a block
            if self.sfx_blocked.get_num_channels() == 0:
                self.sfx_blocked.play()
        elif self.steps < 0: # mark the tile as visited
            self.map.mark_tile(self.y // constants.TILE_SIZE, self.x // constants.TILE_SIZE)



    # checks for collisions with obstacle tiles
    def _check_collision(self, rect, axis):
        if axis == enums.CA_HORIZONTAL:
            if self.look_at == enums.DI_RIGHT:
                tile_x = (rect.right - 1) // constants.TILE_SIZE
            else:
                tile_x = rect.left // constants.TILE_SIZE
            tile_y = rect.y // constants.TILE_SIZE
        else:  # vertical
            tile_x = rect.x // constants.TILE_SIZE
            if self.look_at == enums.DI_DOWN:
                tile_y = (rect.bottom - 1) // constants.TILE_SIZE
            else:
                tile_y = rect.top // constants.TILE_SIZE
        # returns True if the tile is an obstacle
        return self.map.get_tile_type(tile_x, tile_y) == enums.TT_OBSTACLE
    


    # animates the player sprite based on the current state
    def animate(self):
        self.animation_speed = (constants.ANIM_SPEED_IDLE 
                              if self.state <= enums.PS_IDLE_RIGHT 
                              else constants.ANIM_SPEED_WALK)
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1 # next frame
        # exceeded the number of frames?
        if self.frame_index >= len(self.image_list[self.state]):
            self.frame_index = 0 # reset the frame number
        # assigns the image according to frame, status and direction    
        self.image = self.image_list[self.state][self.frame_index]
        # invincible effect (player blinks)
        self._handle_invincibility_effect()



    # invincible effect (player blinks)
    def _handle_invincibility_effect(self):
        if self.invincible:
            if (self.game.loop_counter >> 3) & 1 == 0: # % 8
                self.image.set_alpha(0) # visible
            else: 
                self.image.set_alpha(255) # no visible
        else:
            self.image.set_alpha(255)



    # subtracts one energy unit and applies temporary invincibility
    def loses_energy(self, value):
        pass
        # if not self.invincible:
        #     self.energy -= value
        #     if self.sfx_death.get_num_channels() == 0:
        #         self.sfx_death.play()
        #     if self.energy >= 0:
        #         self.invincible = True
        #         self.timer_from = pygame.time.get_ticks()
        #         self.timer_from -= (constants.TIME_REMAINING - 3000)  # 3 secs.



    # updates the player position and state
    def update(self):
        self.get_input()
        self.get_state()
        if self.direction.x != 0: self.move(enums.CA_HORIZONTAL)
        if self.direction.y != 0: self.move(enums.CA_VERTICAL)
        self.animate()
        self._check_timer()



    # controls the hotspot time
    def _check_timer(self):
        if self.invincible:
            if (pygame.time.get_ticks() - self.timer_from) >= self.timer_to:
                self.invincible = False



    # draws the player on the screen
    def draw(self, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        self.game.srf_map.blit(self.image, (screen_x, screen_y))