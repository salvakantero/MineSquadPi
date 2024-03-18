
# ==============================================================================
# .::Game class::.
# One class to rule them all
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
import random
import sys
import constants
import enums
import os
import pickle
from datetime import date
from config import Configuration
from font import Font
from intro import Intro
from menu import Menu
from checkpoint import Checkpoint
from jukebox import Jukebox
from explosion import Explosion
from floatingtext import FloatingText


class Game():
    def __init__(self):
        self.clock = pygame.time.Clock() # game clock for FPS and timers
        self.config = Configuration() # reads the configuration file to apply the personal settings
        self.config.load()
        self.checkpoint = Checkpoint() # creates a checkpoint object to load/record game
        self.new = True # when 'False', load the last checkpoint
        self.win_secuence = 0 # animated sequence on winning (if > 0)
        self.status = enums.OVER # start from menu
        self.music_status = enums.UNMUTED # Music!
        # area covered by the menu
        self.srf_menu = pygame.Surface(constants.MENU_UNSCALED_SIZE)
        # area covered by the map
        self.srf_map = pygame.Surface(constants.MAP_UNSCALED_SIZE)
        # surface to save the generated map without sprites (background for each frame)
        self.srf_map_bk = pygame.Surface(constants.MAP_UNSCALED_SIZE)
        # area covered by the scoreboard
        self.srf_sboard = pygame.Surface(constants.SBOARD_UNSCALED_SIZE)
        # surface to save the previous map (transition effect between screens)
        self.srf_map_bk_prev = pygame.Surface(constants.MAP_UNSCALED_SIZE)
        # sprite control groups (for collision detection)
        self.groups = [
            pygame.sprite.Group(), # all sprites (to display them)
            pygame.sprite.Group(), # enemies
            pygame.sprite.GroupSingle(), # hotspot
            pygame.sprite.GroupSingle(), # gate
            pygame.sprite.GroupSingle(), # mobile platform
            pygame.sprite.GroupSingle(), # dust
            pygame.sprite.GroupSingle()] # shot
        # display mode and margins (default values)
        self.v_margin = constants.V_MARGIN
        self.h_margin = constants.H_MARGIN
        self.win_size = constants.WIN_SIZE
        # main surface
        self.screen = pygame.display.set_mode(self.win_size, 0, 32)
        # wallpaper for the 16:9 fullscreen mode
        self.img_background = pygame.image.load('images/assets/screen_back.png').convert()        
        # change the resolution and type of display according to the settings
        self.apply_display_settings()
        # common fonts. S = small F = foreground B = background
        self.fonts = {
            enums.S_F_GREEN: Font('images/fonts/small_font.png', constants.PALETTE['GREEN'], True),
            enums.S_B_GREEN: Font('images/fonts/small_font.png', constants.PALETTE['DARK_GREEN'], False),
            enums.S_F_WHITE: Font('images/fonts/small_font.png', constants.PALETTE['WHITE'], True),
            enums.S_B_WHITE: Font('images/fonts/small_font.png', constants.PALETTE['DARK_GRAY'], False),
            enums.L_F_WHITE: Font('images/fonts/large_font.png', constants.PALETTE['WHITE'], True),
            enums.L_B_WHITE: Font('images/fonts/large_font.png', constants.PALETTE['DARK_GRAY'], False),
            enums.L_F_SAND: Font('images/fonts/large_font.png', constants.PALETTE['SAND'], True),
            enums.L_B_SAND: Font('images/fonts/large_font.png', constants.PALETTE['BROWN'], False)}
        # create floating texts
        self.floating_text = FloatingText(self.srf_map)
         # playlist with the 12 available tracks
        self.jukebox = Jukebox('sounds/music/', 'mus_ingame_', 12)
        # The following image lists are created here, not in their corresponding classes, 
        # to avoid loading from disk during game play.
        self.enemy_images = {
            # animation sequence of the enemies depending on their type
            enums.INFECTED: [
                pygame.image.load('images/sprites/infected0.png').convert_alpha(),
                pygame.image.load('images/sprites/infected1.png').convert_alpha()],
            enums.PELUSOID: [
                pygame.image.load('images/sprites/pelusoid0.png').convert_alpha(),
                pygame.image.load('images/sprites/pelusoid1.png').convert_alpha()],
            enums.AVIRUS: [
                pygame.image.load('images/sprites/avirus0.png').convert_alpha(),
                pygame.image.load('images/sprites/avirus1.png').convert_alpha()],
            enums.PLATFORM_SPR: [
                pygame.image.load('images/sprites/platform0.png').convert_alpha(),
                pygame.image.load('images/sprites/platform1.png').convert_alpha()],
            enums.FANTY: [
                pygame.image.load('images/sprites/fanty0.png').convert_alpha(),
                pygame.image.load('images/sprites/fanty1.png').convert_alpha()]}
        self.hotspot_images = {
            enums.TNT: pygame.image.load('images/sprites/hotspot0.png').convert_alpha(),
            enums.KEY: pygame.image.load('images/sprites/hotspot1.png').convert_alpha(),
            enums.AMMO: pygame.image.load('images/sprites/hotspot2.png').convert_alpha(),
            enums.OXYGEN: pygame.image.load('images/sprites/hotspot3.png').convert_alpha(),
            enums.CHECKPOINT: pygame.image.load('images/sprites/hotspot4.png').convert_alpha(),
            enums.BURGER: pygame.image.load('images/sprites/hotspot5.png').convert_alpha(),
            enums.CAKE: pygame.image.load('images/sprites/hotspot6.png').convert_alpha(),
            enums.DONUT: pygame.image.load('images/sprites/hotspot7.png').convert_alpha(),
            enums.GATE_TILE: pygame.image.load('images/tiles/T60.png').convert()} 
        self.blast_images = {
            0: [ # explosion 1: on the air
                pygame.image.load('images/sprites/blast0.png').convert_alpha(),
                pygame.image.load('images/sprites/blast1.png').convert_alpha(),
                pygame.image.load('images/sprites/blast2.png').convert_alpha(),
                pygame.image.load('images/sprites/blast3.png').convert_alpha(),
                pygame.image.load('images/sprites/blast4.png').convert_alpha(),
                pygame.image.load('images/sprites/blast5.png').convert_alpha(),                                 
                pygame.image.load('images/sprites/blast6.png').convert_alpha()],
            1: [ # explosion 2: on the ground
                pygame.image.load('images/sprites/blast7.png').convert_alpha(),
                pygame.image.load('images/sprites/blast8.png').convert_alpha(),
                pygame.image.load('images/sprites/blast9.png').convert_alpha(),
                pygame.image.load('images/sprites/blast10.png').convert_alpha(),
                pygame.image.load('images/sprites/blast4.png').convert_alpha(),
                pygame.image.load('images/sprites/blast5.png').convert_alpha(),                                 
                pygame.image.load('images/sprites/blast6.png').convert_alpha()],
            2: [ # explosion 3: magic halo for hotspots
                pygame.image.load('images/sprites/blast11.png').convert_alpha(),
                pygame.image.load('images/sprites/blast12.png').convert_alpha(),
                pygame.image.load('images/sprites/blast13.png').convert_alpha(),
                pygame.image.load('images/sprites/blast14.png').convert_alpha(),
                pygame.image.load('images/sprites/blast15.png').convert_alpha(),
                pygame.image.load('images/sprites/blast16.png').convert_alpha()]}         
        # sound effects
        self.sfx_message = pygame.mixer.Sound('sounds/fx/sfx_message.wav')
        self.sfx_click = pygame.mixer.Sound('sounds/fx/sfx_menu_click.wav') 
        self.sfx_game_over = pygame.mixer.Sound('sounds/fx/sfx_game_over.wav')
        self.sfx_open_door = pygame.mixer.Sound('sounds/fx/sfx_open_door.wav')
        self.sfx_locked_door = pygame.mixer.Sound('sounds/fx/sfx_locked_door.wav')
        self.sfx_enemy_down = {
            enums.INFECTED: pygame.mixer.Sound('sounds/fx/sfx_exp_infected.wav'),
            enums.PELUSOID: pygame.mixer.Sound('sounds/fx/sfx_exp_pelusoid.wav'),
            enums.AVIRUS: pygame.mixer.Sound('sounds/fx/sfx_exp_avirus.wav'),
            enums.FANTY: pygame.mixer.Sound('sounds/fx/sfx_exp_fanty.wav')}
        self.sfx_hotspot = {
            enums.TNT: pygame.mixer.Sound('sounds/fx/sfx_TNT.wav'),
            enums.KEY: pygame.mixer.Sound('sounds/fx/sfx_key.wav'),
            enums.AMMO: pygame.mixer.Sound('sounds/fx/sfx_ammo.wav'),
            enums.OXYGEN: pygame.mixer.Sound('sounds/fx/sfx_oxygen.wav'),
            enums.CHECKPOINT: pygame.mixer.Sound('sounds/fx/sfx_checkpoint.wav'),
            enums.BURGER: pygame.mixer.Sound('sounds/fx/sfx_burger.wav'),
            enums.CAKE: pygame.mixer.Sound('sounds/fx/sfx_cake.wav'),
            enums.DONUT: pygame.mixer.Sound('sounds/fx/sfx_donut.wav')}
        # modifies the XY position of the map on the screen to create 
        # a shaking effect for a given number of frames (explosions, big jumps)
        self.shake = [0, 0]
        self.shake_timer = 0
        # high scores table
        self.high_scores = []
        self.load_high_scores()
        # create a joystick/joypad/gamepad object
        self.joystick = self.config.prepare_joystick()


    # windowed mode, generates a main window with title, icon, and 32-bit colour
    def apply_windowed_mode(self):        
        # default margins
        self.v_margin = constants.V_MARGIN
        self.h_margin = constants.H_MARGIN
        # creates the window
        self.win_size = constants.WIN_SIZE
        self.screen = pygame.display.set_mode(self.win_size, 0, 32)
        pygame.display.set_caption('.:: Red Planet Pi ::.')
        icon = pygame.image.load('images/assets/intro3.png').convert_alpha()
        pygame.display.set_icon(icon)


    # 4:3 (800x600) clear and faaaasssst!
    def apply_full_screen_X600(self):   
        if (800, 600) in pygame.display.list_modes():
            self.win_size = 800, 600
            self.v_margin = 4            
            self.screen = pygame.display.set_mode(self.win_size, pygame.FULLSCREEN, 32)
        else: # full screen at low resolution not available
            self.apply_windowed_mode()


    # 16:9 (1280x720) clear and is still fast!
    def apply_full_screen_X720(self):
        if (1280, 720) in pygame.display.list_modes():
            self.win_size = 1280, 720
            self.v_margin = (self.win_size[1] - constants.MENU_SCALED_SIZE[1]) // 2
            self.h_margin = (self.win_size[0] - constants.MENU_SCALED_SIZE[0]) // 2            
            self.screen = pygame.display.set_mode(self.win_size, pygame.FULLSCREEN, 32)
            # background image to fill in the black sides
            self.screen.blit(self.img_background, (0,0))
        else: # full screen at low resolution not available
            self.apply_windowed_mode()


    # creates a window or full-screen environment 
    def apply_display_settings(self):
        if self.config.data['full_screen'] == enums.X600: # 4:3
            self.apply_full_screen_X600()
        elif self.config.data['full_screen'] == enums.X720: # 16:9
            self.apply_full_screen_X720()
        else:
            self.apply_windowed_mode()         


    # load the high scores table
    def load_high_scores(self):
        if os.path.exists('scores.dat'):
            with open('scores.dat', "rb") as f:
                self.high_scores = pickle.load(f)
        else: # default values
            today = str(date.today())
            for _ in range(8):
                self.high_scores.append(['SALVAKANTERO', today, 0])


    # save the high scores table
    def save_high_scores(self):
        with open('scores.dat', "wb") as f:
            pickle.dump(self.high_scores, f)


    # allows to enter the player's name
    def get_player_name(self):
        self.message('You achieved a high score!', 'Enter your name...', False, False)
        pygame.event.clear(pygame.KEYDOWN)
        name = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # RETURN or ESC has been pressed, ends the entry of the name                  
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:                    
                        return name.upper()
                    # a key between 0 and Z has been pressed. Is added to the name
                    elif (event.key > pygame.K_0 and event.key < pygame.K_z):
                        if len(name) < 12: name += pygame.key.name(event.key)
                    # The space bar has been pressed. A space is added
                    elif  event.key == pygame.K_SPACE:
                        if len(name) < 12: name += ' '
                    # a delete key has been pressed, deletes the last character                       
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        name = name[:-1]
                    # draws the current name
                    self.message('You achieved a high score!', name.upper(), False, True)


    # new high score??
    def update_high_score_table(self, player_score):
        if player_score > self.high_scores[7][2]:
            self.high_scores.append([self.get_player_name(), str(date.today()), player_score])
            self.high_scores.sort(reverse=True, key=lambda x: x[2])
            self.high_scores.pop() # remove last score (8 scores remain)
            self.save_high_scores()


    # exits to the operating system
    def exit(self):
        pygame.quit()
        sys.exit()


    # shows an intro
    def show_intro(self):
        intro = Intro(self)
        intro.play()


    # creates the initial Menu object
    def show_menu(self):
        menu = Menu(self)
        menu.show()


    # draws scanlines
    def apply_scanlines(self):
        x = self.win_size[0]-self.h_margin-1
        y = self.v_margin    
        if self.config.data['full_screen'] is not enums.OFF: 
            height = self.win_size[1]-self.v_margin
        else: # windowed mode: fixed bottom margin of 26 pixels
            height = self.win_size[1]-26
        while y < height:
            # every 3 lines draws an almost black line
            pygame.draw.line(self.screen, (10, 10, 10), (self.h_margin, y), (x, y))
            y += 3            
    

    # dumps and scales surfaces to the screen
    def update_screen(self):
        if self.status == enums.OVER:
            # scale the menu
            self.screen.blit(pygame.transform.scale(
                self.srf_menu, constants.MENU_SCALED_SIZE),
                (self.h_margin, self.v_margin))
        else:
            # scale the scoreboard
            self.screen.blit(pygame.transform.scale(
                self.srf_sboard, constants.SBOARD_SCALED_SIZE), 
                (self.h_margin, self.v_margin))
                        
            # shakes the surface of the map if it has been requested
            offset = [0,0]
            if self.shake_timer > 0:
                if self.shake_timer == 1: # last frame shaken
                    # it's necessary to clean the edges of the map after shaking it
                    if self.config.data['full_screen'] == enums.X720: # 16:9 fullscreen
                        self.screen.blit(self.img_background, (0,0))
                    else: # 4:3 fullscreen or windowed mode
                        self.screen.fill(constants.PALETTE['BLACK'])
                else:
                    offset[0] = random.randint(-self.shake[0], self.shake[0])
                    offset[1] = random.randint(-self.shake[1], self.shake[1])
                self.shake_timer -= 1
            
            # scale the map
            self.screen.blit(pygame.transform.scale(
                self.srf_map, constants.MAP_SCALED_SIZE), (self.h_margin + offset[0], 
                constants.SBOARD_SCALED_SIZE[1] + self.v_margin + offset[1]))
        
        if self.config.data['scanlines']: self.apply_scanlines()
        pygame.display.update() # refreshes the screen
        self.clock.tick(60) # 60 FPS


    # displays a message, darkening the screen
    def message(self, msg1, msg2, darken, muted):
        # obscures the surface of the map
        if darken:
            self.srf_map.set_alpha(120)
            self.update_screen()
        # saves a copy of the darkened screen
        aux_surf = pygame.Surface(constants.MAP_UNSCALED_SIZE)    
        aux_surf.blit(self.srf_map, (0,0))
        # draws the light message on the dark background
        height = 36
        # calculates the width of the box
        message1_len = len(msg1) * 7 # approximate length of text 1 in pixels
        message2_len = len(msg2) * 4 # approximate length of text 2 in pixels
        # width = length of the longest text + margin
        width = max(message1_len, message2_len) + 30
        # calculates the position of the box
        x = (constants.MAP_UNSCALED_SIZE[0]//2) - (width//2)
        y = (constants.MAP_UNSCALED_SIZE[1]//2) - (height//2)
        # black window
        pygame.draw.rect(aux_surf, constants.PALETTE['BLACK'],(x, y, width, height))
        # blue border
        pygame.draw.rect(aux_surf, constants.PALETTE['DARK_BLUE'],(x, y, width, height), 1)
        # draws the text centred inside the window (Y positions are fixed)
        # line 1
        text_x = (x + (width//2)) - (message1_len//2)
        text_y = y + 5
        self.fonts[enums.L_B_WHITE].render(msg1, aux_surf, (text_x, text_y))
        self.fonts[enums.L_F_WHITE].render(msg1, aux_surf, (text_x - 2, text_y - 2))
        # line 2
        text_x = (x + (width//2)) - (message2_len//2)
        text_y = y + 25
        self.fonts[enums.S_B_GREEN].render(msg2, aux_surf, (text_x, text_y))
        self.fonts[enums.S_F_GREEN].render(msg2, aux_surf, (text_x - 1, text_y - 1))
        # return the copy with the message on the map surface and redraw it.
        self.srf_map.blit(aux_surf, (0,0))
        self.srf_map.set_alpha(None)
        self.update_screen() 
        if muted: self.sfx_click.play()
        else: self.sfx_message.play()


    # displays a message to confirm exit
    def confirm_exit(self):
        self.message('Leave the current game?', 'ESC TO EXIT. ANY OTHER KEY TO CONTINUE', True, False)
        pygame.event.clear(pygame.KEYDOWN)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:                    
                        return True # back to menu
                    return False # continue game


    # displays a 'game over' message and waits
    def over(self):
        self.shake_timer = 1 # clean the edges 
        self.message('G a m e  O v e r', 'PRESS ANY KEY', True, True)
        pygame.mixer.music.stop()
        self.sfx_game_over.play()
        pygame.event.clear(pygame.KEYDOWN)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:                  
                    return # back to menu


    # everything blows up and our player wins the game
    def win(self, score):
        sounds = [enums.INFECTED, enums.PELUSOID, enums.AVIRUS, enums.FANTY]
        # first frame (from 350 to 1)...
        if self.win_secuence == 350:
            # eliminate the remaining enemies
            for enemy in self.groups[enums.ENEMIES]:
                enemy.kill()
                blast = Explosion([enemy.rect.centerx, enemy.rect.centery], self.blast_images[0])              
                self.groups[enums.ALL].add(blast)                    
                self.sfx_enemy_down[1].play()                
                self.shake = [10, 6] # shake the map
                self.shake_timer = 14            
        # intermediate frames. Generates multiple random explosions
        elif self.win_secuence % random.randint(2, 8) == 0:
            blast = Explosion((random.randint(30, constants.MAP_UNSCALED_SIZE[0]-10), 
                random.randint(10, constants.MAP_UNSCALED_SIZE[0]-10)), self.blast_images[0])              
            self.groups[enums.ALL].add(blast)                    
            self.sfx_enemy_down[random.choice(sounds)].play()            
            self.shake = [10, 6] # shake the map
            self.shake_timer = 14
        # last frame!
        elif self.win_secuence == 1:
            self.shake_timer = 1 # clean the edges
            self.message('CONGRATULATIONS!!', 'You achieved all the goals!', True, True)
            # main theme song again
            pygame.mixer.music.load('sounds/music/mus_menu.ogg')
            pygame.mixer.music.play()
            # wait for a key
            pygame.event.clear(pygame.KEYDOWN)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit()
                    if event.type == pygame.KEYDOWN:                  
                        self.update_high_score_table(score)
                        self.status = enums.OVER
                        return # back to the main menu                       
        self.win_secuence -= 1 # next frame


    # collisions between the player and mobile platforms, enemies, hotspots and gates
    def check_player_collisions(self, player, scoreboard, map_number):
        # player and mobile platform
        if self.groups[enums.PLATFORM].sprite is not None: # there is a platform on the map
            if pygame.sprite.spritecollide(player, self.groups[enums.PLATFORM], False, pygame.sprite.collide_rect_ratio(1.15)):
                platform = self.groups[enums.PLATFORM].sprite                
                # the player is above the platform?
                if player.rect.bottom - 2 < platform.rect.top:               
                    player.rect.bottom = platform.rect.top
                    # stops the fall
                    player.direction.y = 0                    
                    player.on_ground = True                                        
                    # horizontal platform?
                    if platform.vy == 0:
                        # if the movement keys are not pressed
                        # takes the movement of the platform
                        key_state = pygame.key.get_pressed()
                        if not key_state[self.config.left_key] and not key_state[self.config.right_key]:
                            player.rect.x += platform.vx
        # player and martians
        if not player.invincible:
            if pygame.sprite.spritecollide(player, self.groups[enums.ENEMIES], False, pygame.sprite.collide_rect_ratio(0.60)):
                player.loses_life()        
                scoreboard.invalidate() # redraws the scoreboard
                return        
        # player and hotspot
        if self.groups[enums.HOTSPOT].sprite is not None:
            if player.rect.colliderect(self.groups[enums.HOTSPOT].sprite):
                save_game = False
                hotspot = self.groups[enums.HOTSPOT].sprite
                # shake the map (just a little)
                self.shake = [4, 4]
                self.shake_timer = 4
                # creates a magic halo
                blast = Explosion(hotspot.rect.center, self.blast_images[2])
                self.groups[enums.ALL].add(blast)                
                self.sfx_hotspot[hotspot.type].play()
                # manages the object according to the type
                if hotspot.type == enums.TNT:
                    player.TNT += 1
                    scoreboard.game_percent += 3
                    self.floating_text.text = '+50 ' + str(player.TNT) + '/15'
                    player.score += 50
                elif hotspot.type == enums.KEY:
                    player.keys += 1
                    scoreboard.game_percent += 2
                    self.floating_text.text = '+125'
                    player.score += 125
                elif hotspot.type == enums.AMMO:
                    player.ammo = min(player.ammo + constants.AMMO_ROUND, constants.MAX_AMMO)
                    self.floating_text.text = '+75'
                    player.score += 75
                elif hotspot.type == enums.OXYGEN:
                    player.oxygen = constants.MAX_OXYGEN
                    self.floating_text.text = '+100'
                    player.score += 100
                elif hotspot.type == enums.BURGER:
                    self.floating_text.text = '+500'
                    player.score += 500
                elif hotspot.type == enums.CAKE:
                    self.floating_text.text = '+350'
                    player.score += 350
                elif hotspot.type == enums.DONUT:
                    self.floating_text.text = '+200'
                    player.score += 200                                        
                elif hotspot.type == enums.CHECKPOINT:                    
                    self.floating_text.text = 'Checkpoint'                    
                    self.checkpoint.data = {
                        'map_number' : map_number,
                        'game_percent' : scoreboard.game_percent,
                        'player_lives' : player.lives,
                        'player_ammo' : player.ammo,
                        'player_keys' : player.keys,
                        'player_TNT' : player.TNT,
                        'player_oxygen' : player.oxygen,
                        'player_stacked_TNT' : player.stacked_TNT,
                        'player_facing_right' : player.facing_right,
                        'player_rect' : player.rect,
                        'player_score' : player.score,
                        'hotspot_data' : constants.HOTSPOT_DATA,
                        'gate_data' : constants.GATE_DATA }
                    self.checkpoint.save() 

                scoreboard.invalidate()
                self.floating_text.x = hotspot.x*constants.TILE_SIZE
                self.floating_text.y = hotspot.y*constants.TILE_SIZE
                self.floating_text.speed = 0
                # removes objects
                self.groups[enums.HOTSPOT].sprite.kill()
                constants.HOTSPOT_DATA[map_number][3] = False # not visible            
                return
        # player and gates
        if self.groups[enums.GATE].sprite is not None: # # there is a door on the map
            if player.rect.colliderect(self.groups[enums.GATE].sprite):        
                if player.keys > 0: # player has a key
                    player.keys -= 1
                    self.sfx_open_door.play()
                    # creates a magic halo
                    blast = Explosion(self.groups[enums.GATE].sprite.rect.center, self.blast_images[2])
                    self.groups[enums.ALL].add(blast)
                    # deletes the door
                    self.groups[enums.GATE].sprite.kill()                    
                    constants.GATE_DATA[map_number][2] = False # not visible
                    # increases the percentage of game play
                    scoreboard.game_percent += 3
                    scoreboard.invalidate()
                    # increases the score
                    player.score += 150
                    self.floating_text.text = '+150'
                    self.floating_text.speed = 0
                    self.floating_text.x = player.rect.x
                    self.floating_text.y = player.rect.y
                else: # no key
                    self.sfx_locked_door.play()
                    # shake the map (just a little in X)
                    self.shake = [4, 0]
                    self.shake_timer = 4
                    # bounces the player
                    if player.facing_right: player.rect.x -= 5
                    else: player.rect.x += 5


    def check_bullet_collisions(self, player, scoreboard, tilemap_rect_list):  
        # bullets and map tiles
        if self.groups[enums.SHOT].sprite is not None: # shot in progress
            bullet_rect = self.groups[enums.SHOT].sprite.rect
            for tile in tilemap_rect_list:
                if tile.colliderect(bullet_rect):
                    self.groups[enums.SHOT].sprite.kill()
                    break                                      
        # bullets and martians
        if self.groups[enums.SHOT].sprite is not None: # still shot in progress
            for enemy in self.groups[enums.ENEMIES]:
                if enemy.rect.colliderect(self.groups[enums.SHOT].sprite):        
                    # shake the map
                    self.shake = [10, 6]
                    self.shake_timer = 14
                    # creates an explosion and assigns a score according to the type of enemy
                    if enemy.type == enums.INFECTED:
                        blast = Explosion([enemy.rect.centerx, enemy.rect.centery-4], self.blast_images[1])
                        self.floating_text.text = '+25'
                        player.score += 25
                    else: # flying enemies
                        blast = Explosion(enemy.rect.center, self.blast_images[0])
                        if enemy.type == enums.AVIRUS: 
                            self.floating_text.text = '+50'
                            player.score += 50
                        elif enemy.type == enums.PELUSOID: 
                            self.floating_text.text = '+75'
                            player.score += 75
                        else: # fanty
                            self.floating_text.text = '+100'
                            player.score += 100
                    self.groups[enums.ALL].add(blast)                    
                    self.sfx_enemy_down[enemy.type].play()
                    # floating text position
                    self.floating_text.x = enemy.rect.x
                    self.floating_text.y = enemy.rect.y
                    self.floating_text.speed = 0
                    # removes objects
                    enemy.kill()
                    self.groups[enums.SHOT].sprite.kill()
                    # redraws the scoreboard
                    scoreboard.invalidate()
                    break
