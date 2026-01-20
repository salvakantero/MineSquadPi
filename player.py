# ==============================================================================
# .::Player class::.
# Create the main sprite and manage keyboard/mouse/joystick control, 
# movement and animation according to its state.
# ==============================================================================
#
#  This file is part of "Mine Squad Pi". Copyright (C) 2026 @salvakantero
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

from shot import Shot



class Player(pygame.sprite.Sprite):
    def __init__(self, game, map, scoreboard):
        super().__init__()
        # initialize player position
        # start at the centre of the map, 1/4 from the left and at the bottom
        self.x, self.y = constants.PLAYER_X_INI, constants.PLAYER_Y_INI
        # movement
        self.direction = pygame.math.Vector2(0.0, 0.0) # direction of movement
        self.target_x = self.x
        self.target_y = self.y
        self.move_progress = 0
        self.is_moving_to_target = False
        # player state
        self.state = enums.PS_IDLE_UP # to know the animation to be applied
        self.look_at = enums.DI_UP # where the player looks
        self.turn_time = 0 # timestamp when player changed direction
        #animation
        self.frame_index = 0 # frame number
        self.animation_timer = 0 # timer to change frame
        self.animation_speed = constants.ANIM_SPEED_IDLE # frame dwell time
        # images
        self._load_player_images(game.selected_player)
        self.image = self.image_list[self.state][0] # 1st frame of the animation
        self.rect = pygame.Rect(self.x, self.y, constants.TILE_SIZE, constants.TILE_SIZE)
        # invincibility
        self.invincible = False # invincible after losing a life or take a shield
        self.timer_from = 0 # tick number when the shield effect begins
        self.timer_to = constants.TIME_REMAINING # time of shield (40 secs.)        
        # FX sounds
        self.sfx_shot1 = pygame.mixer.Sound(constants.FX_PATH + 'sfx_shot1.wav')
        self.sfx_no_ammo = pygame.mixer.Sound(constants.FX_PATH + 'sfx_no_ammo.wav')
        self.sfx_no_ammo.set_volume(0.6)
        self.sfx_beacon = pygame.mixer.Sound(constants.FX_PATH + 'sfx_beacon.wav')
        self.sfx_beacon.set_volume(0.6)
        self.sfx_beacon_error = pygame.mixer.Sound(constants.FX_PATH + 'sfx_beacon_error.wav')
        self.sfx_blocked = pygame.mixer.Sound(constants.FX_PATH + 'sfx_blocked.wav')
        self.sfx_blocked.set_volume(0.7)
        # objects and others
        self.game = game
        self.map = map
        self.scoreboard = scoreboard
        # attributes
        self.energy, self.move_time = self.set_player_attributes()
        self.max_energy = self.energy
        self.ammo = 10
        # cache frequently used values
        self._direction_mappings = {
            game.config.up_key: (enums.DI_UP, pygame.math.Vector2(0, -1)),
            game.config.down_key: (enums.DI_DOWN, pygame.math.Vector2(0, 1)),
            game.config.left_key: (enums.DI_LEFT, pygame.math.Vector2(-1, 0)),
            game.config.right_key: (enums.DI_RIGHT, pygame.math.Vector2(1, 0))            
        }
        self._state_mappings = {
            enums.DI_UP: (enums.PS_IDLE_UP, enums.PS_WALK_UP),
            enums.DI_DOWN: (enums.PS_IDLE_DOWN, enums.PS_WALK_DOWN),
            enums.DI_LEFT: (enums.PS_IDLE_LEFT, enums.PS_WALK_LEFT),
            enums.DI_RIGHT: (enums.PS_IDLE_RIGHT, enums.PS_WALK_RIGHT)
        }
        # cache frequently used constants for performance
        self._tile_size = constants.TILE_SIZE
        self._half_tile_size = constants.HALF_TILE_SIZE
        self._map_height_pixels = constants.MAP_TILE_SIZE[1] * constants.TILE_SIZE
        # cache current tile position to avoid repeated calculations
        self._current_tile_x = -1
        self._current_tile_y = -1



    # set energy and move_time based on player type
    def set_player_attributes(self):
        # define stats based on difficulty level, independent of the character.
        # Format: (energy, move_time) - Lower move_time is faster.
        difficulty_stats = {
            enums.DF_EASY:   (14, 30),  # Easy: More energy, slower movement
            enums.DF_NORMAL: (12, 26),  # Normal: Balanced energy and speed
            enums.DF_HARD:   (10, 22)    # Hard: Less energy, faster movement
        }
        # return the tuple (energy, move_time) for the selected difficulty
        return difficulty_stats.get(self.game.selected_difficulty, (12, 26))



    # code for a shot to be fired
    def fire(self):
        if self.ammo > 0:       
            if not self.game.sprite_groups[enums.SG_SHOT].sprite: # no shots on screen
                # direction of the shot
                dir_vectors = {
                    enums.DI_UP: pygame.math.Vector2(0, -2),
                    enums.DI_DOWN: pygame.math.Vector2(0, 2),
                    enums.DI_LEFT: pygame.math.Vector2(-2, 0),
                    enums.DI_RIGHT: pygame.math.Vector2(2, 0) }
                vector = dir_vectors.get(self.look_at, pygame.math.Vector2(0, -2)) # UP by default
                # shot creation
                shot = Shot(self.x, self.y, vector, self.game.srf_map)
                self.game.sprite_groups[enums.SG_SHOT].add(shot)
                self.sfx_shot1.play()
                self.ammo -= 1
                self.scoreboard.invalidate()
        else: # no bullets
            self.sfx_no_ammo.play()
        # clears the input buffer (keyboard and joystick)
        self.game.clear_input_buffer()



    # code for placing a flag/beacon
    def place_beacon(self, from_keyboard=True):
        offsets = {
            enums.DI_UP: (0, -1), enums.DI_DOWN: (0, 1),
            enums.DI_LEFT: (-1, 0), enums.DI_RIGHT: (1, 0)
        }
        # places the beacon in front of where the player is facing
        offset_x, offset_y = offsets.get(self.look_at, (0, 0))
        # use cached tile size for better performance
        player_tile_x = int(self.x // self._tile_size)
        player_tile_y = int(self.y // self._tile_size)
        x = player_tile_x + offset_x
        y = player_tile_y + offset_y        
        # check map boundaries
        if (0 <= x < constants.MAP_TILE_SIZE[0] and 0 <= y < constants.MAP_TILE_SIZE[1]):
            # if there is no beacon on the tile
            if self.map.get_tile_type(x, y) != enums.TT_OBSTACLE and \
               self.map.map_data['mines_info'][y][x] < enums.MI_BEACON:
                # if there is a mine in the marked tile
                if self.map.get_tile_type(x, y) == enums.TT_MINE:
                    self.sfx_beacon.play()
                    if from_keyboard:
                        self.game.keyboard_rgb.effect_beacon()
                    else:
                        self.game.keyboard_rgb.effect_beacon_alt()
                    self.game.remaining_mines -= 1
                    self.game.score += 125
                    self.game.floating_text.show('+125',
                        x * self._tile_size, y * self._tile_size)
                    # place the green beacon
                    self.map.map_data['mines_info'][y][x] = enums.MI_BEACON
                else:
                    self.sfx_beacon_error.play()
                    # place the red beacon for incorrect placement
                    self.map.map_data['mines_info'][y][x] = enums.MI_BEACON2
                self.game.remaining_beacons -= 1
                self.scoreboard.invalidate()
            else: # if there is a beacon on the tile
                self.sfx_no_ammo.play()
        else: # out of the map
            self.sfx_no_ammo.play()
        # clears the input buffer (keyboard and joystick)
        self.game.clear_input_buffer()



    # subtracts one energy unit and applies temporary invincibility
    def loses_energy(self, value):
        if not self.invincible:
            self.energy -= value
            if self.energy >= 0:
                self.invincible = True
                self.timer_from = pygame.time.get_ticks()
                self.timer_from -= (constants.TIME_REMAINING - 3000)  # 3 secs.



    # moves the player in the specified axis
    def move(self, axis):
        if self.is_moving_to_target:
            return  # already in progress, waiting to complete
        
        # calculate new target position using cached tile size
        if axis == enums.CA_HORIZONTAL:
            new_target_x = self.target_x + (self._tile_size if self.direction.x > 0 else -self._tile_size)
            temp_rect = pygame.Rect(new_target_x, self.target_y, self._tile_size, self._tile_size)
            
            if not self._check_collision(temp_rect, axis):
                self.target_x = new_target_x
                self.is_moving_to_target = True
                self.move_progress = 0
            else:
                if self.sfx_blocked.get_num_channels() == 0:
                    self.sfx_blocked.play()        
        else:  # vertical
            new_target_y = self.target_y + (self._tile_size if self.direction.y > 0 else -self._tile_size)
            temp_rect = pygame.Rect(self.target_x, new_target_y, self._tile_size, self._tile_size)
            
            # verify map boundaries using cached map height
            if (temp_rect.top < 0 or temp_rect.bottom > self._map_height_pixels):
                if self.sfx_blocked.get_num_channels() == 0:
                    self.sfx_blocked.play()
                return
                
            if not self._check_collision(temp_rect, axis):
                self.target_y = new_target_y
                self.is_moving_to_target = True
                self.move_progress = 0
            else:
                if self.sfx_blocked.get_num_channels() == 0:
                    self.sfx_blocked.play()



    # update the smooth movement towards the target
    def update_movement(self):
        if self.is_moving_to_target:
            self.move_progress += 1            
            # calculate interpolated position
            progress_ratio = self.move_progress / self.move_time
            if progress_ratio >= 1.0:
                # movement completed
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving_to_target = False
                # update tile position only when movement is complete
                if self._update_tile_position():
                    self.map.mark_tile(self._current_tile_x, self._current_tile_y)
            else:
                # calculate position between origin and destination using cached tile size
                if self.direction.x > 0:
                    start_x = self.target_x - self._tile_size
                elif self.direction.x < 0:
                    start_x = self.target_x + self._tile_size
                else:
                    start_x = self.target_x
                if self.direction.y > 0:
                    start_y = self.target_y - self._tile_size
                elif self.direction.y < 0:
                    start_y = self.target_y + self._tile_size
                else:
                    start_y = self.target_y
                
                self.x = start_x + (self.target_x - start_x) * progress_ratio
                self.y = start_y + (self.target_y - start_y) * progress_ratio
            
            self.rect.x = self.x
            self.rect.y = self.y



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



    # updates the player position and state
    def update(self):
        self._get_input()
        self._get_state()        
        # only process movement if not already in motion
        if not self.is_moving_to_target:
            if self.direction.x != 0:   self.move(enums.CA_HORIZONTAL)
            elif self.direction.y != 0: self.move(enums.CA_VERTICAL)        
        self.update_movement()        
        self.animate()
        self._check_timer()



    # draws the player on the screen
    def draw(self, camera):
        if self.energy > 0: # alive and kicking
            screen_x = self.x - camera.x
            screen_y = self.y - camera.y
            self.game.srf_map.blit(self.image, (screen_x, screen_y))



    ##### auxiliary functions #####
    
    # load player images for animations
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



    #apply deadzone to joystick axis to eliminate drift
    @staticmethod
    def _apply_deadzone(value, threshold=0.1):        
        return value if abs(value) >= threshold else 0.0



    def _get_joystick_direction(self):
        if self.game.joystick is None:
            return None, pygame.math.Vector2(0, 0)
        # apply dead zone for joystick movement
        axis_x = self._apply_deadzone(self.game.joystick.get_axis(0))
        axis_y = self._apply_deadzone(self.game.joystick.get_axis(1))
        # determine direction based on axis values
        if axis_y < -0.5:   return enums.DI_UP, pygame.math.Vector2(0, -1)
        elif axis_y > 0.5:  return enums.DI_DOWN, pygame.math.Vector2(0, 1)
        elif axis_x < -0.5: return enums.DI_LEFT, pygame.math.Vector2(-1, 0)
        elif axis_x > 0.5:  return enums.DI_RIGHT, pygame.math.Vector2(1, 0)
        return None, pygame.math.Vector2(0, 0)



    # keyboard/mouse/joystick keystroke input
    def _get_input(self):
        # don't allow direction changes while moving to a target
        if self.is_moving_to_target:
            return
        # joystick buttons
        if self.game.joystick is not None:
            if self.game.joystick.get_button(0) or self.game.joystick.get_button(1):
                self.fire()
            if self.game.joystick.get_button(2) or self.game.joystick.get_button(3):
                self.place_beacon(from_keyboard=False)
        # keyboard keys
        key_state = pygame.key.get_pressed()
        pressed_key = next((k for k in self._direction_mappings if key_state[k]), None)
        if pressed_key:
            look_at, direction_vector = self._direction_mappings[pressed_key]
            from_joystick = False
        else:
            # check joystick direction if no key is pressed
            look_at, direction_vector = self._get_joystick_direction()
            from_joystick = True
        # no input detected
        if look_at is None:
            self.direction.update(0, 0)
            return
        # if direction changed, only turn (don't move yet)
        if look_at != self.look_at:
            self.look_at = look_at
            self.direction.update(0, 0)
            self.turn_time = pygame.time.get_ticks()
            return
        # wait after turning before allowing movement (longer for joystick)
        wait_time = 225 if from_joystick else 125
        if pygame.time.get_ticks() - self.turn_time < wait_time:
            return
        # update direction to start moving
        self.direction.update(direction_vector)



    # update cached tile position when player moves
    def _update_tile_position(self):
        new_tile_x = int(self.x // self._tile_size)
        new_tile_y = int(self.y // self._tile_size)
        if new_tile_x != self._current_tile_x or new_tile_y != self._current_tile_y:
            self._current_tile_x = new_tile_x
            self._current_tile_y = new_tile_y
            return True  # position changed
        return False  # position unchanged



    # determines the player's state based on movement
    def _get_state(self):
        is_moving = self.direction.x != 0 or self.direction.y != 0
        if self.look_at in self._state_mappings:
            idle_state, walk_state = self._state_mappings[self.look_at]
            self.state = walk_state if is_moving else idle_state          



    # controls the shield time
    def _check_timer(self):
        if self.invincible:
            if (pygame.time.get_ticks() - self.timer_from) >= self.timer_to:
                self.invincible = False



    # checks for collisions with obstacle tiles
    def _check_collision(self, rect, axis):
        # use cached tile size for better performance
        if axis == enums.CA_HORIZONTAL:
            if self.look_at == enums.DI_RIGHT:
                tile_x = (rect.right - 1) // self._tile_size
            else:
                tile_x = rect.left // self._tile_size
            tile_y = rect.y // self._tile_size
        else:  # vertical
            tile_x = rect.x // self._tile_size
            if self.look_at == enums.DI_DOWN:
                tile_y = (rect.bottom - 1) // self._tile_size
            else:
                tile_y = rect.top // self._tile_size
        # returns True if the tile is an obstacle
        return self.map.get_tile_type(tile_x, tile_y) == enums.TT_OBSTACLE
    


    # invincible effect (player blinks)
    def _handle_invincibility_effect(self):
        if self.invincible:
            # use elapsed time since invincibility began
            elapsed_time = pygame.time.get_ticks() - self.timer_from
            # blink every 133ms (equivalent to 8 frames at 60fps)
            if (elapsed_time // 133) & 1 == 0:
                self.image.set_alpha(128)  # semi-transparent
            else: 
                self.image.set_alpha(255)  # fully visible
        else:
            self.image.set_alpha(255)