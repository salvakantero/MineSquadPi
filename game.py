
# ==============================================================================
# .::Game class::.
# One class to rule them all
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
import random
import sys
import constants
import enums
import os
import pickle
from datetime import date
from config import Configuration
from font import Font
from explosion import ExplosionPool
from floatingtext import FloatingText
from hotspot import Hotspot



class Game():
    def __init__(self):
        self.clock = pygame.time.Clock() # game clock for FPS and timers
        self.config = Configuration() # read the configuration file to apply the personal settings
        self.config.load()
        self.loss_sequence = 0 # animated sequence on losing (if > 0)
        self.remaining_beacons = 0 # available beacons
        self.remaining_mines = 0 # mines left (to be deactivated)
        self.score = 0 # current game score
        self.status = enums.GS_OVER # start from menus
        self.music_status = enums.MS_UNMUTED # Music!
        # area covered by the menu
        self.srf_menu = pygame.Surface(constants.MENU_UNSCALED_SIZE)
        # area covered by the map
        self.srf_map = pygame.Surface(constants.SCREEN_MAP_UNSCALED_SIZE)
        # area covered by the scoreboard
        self.srf_sboard = pygame.Surface(constants.SBOARD_UNSCALED_SIZE)
        # player selected BLAZE/PIPER
        self.selected_player = enums.PL_BLAZE
        # default difficulty
        self.selected_difficulty = enums.DF_NORMAL
        # sprite control groups (for update and collision detection)
        self.sprite_groups = [
            pygame.sprite.Group(),          # [0] explosions
            pygame.sprite.Group(),          # [1] enemies
            pygame.sprite.Group(),          # [2] hotspots
            pygame.sprite.GroupSingle()]    # [3] shot
        # display mode and margins (default values)
        self.v_margin = constants.V_MARGIN
        self.h_margin = constants.H_MARGIN
        self.win_size = constants.WIN_SIZE
        # main surface
        self.screen = pygame.display.set_mode(self.win_size, 0, 32)
        # change the resolution and display type according to the settings
        self.apply_display_settings()

        # The following image lists are created here, not in their corresponding classes, 
        # to avoid loading from disk during gameplay.
        self.beacon_image = self._load_image(constants.SPR_PATH + 'beacon.png')

        # enemies
        enem_path = constants.SPR_PATH + 'enemies/'
        self.enemy_images = {
            # stage 1
            enums.EN_SCORPION: [
                self._load_image(enem_path + 'scorpion_0.png'),
                self._load_image(enem_path + 'scorpion_1.png')],
            enums.EN_SNAKE: [
                self._load_image(enem_path + 'snake_0.png'),
                self._load_image(enem_path + 'snake_1.png')],
            enums.EN_SOLDIER0: [
                self._load_image(enem_path + 'soldier0_0.png'),
                self._load_image(enem_path + 'soldier0_1.png')],
            # stage 2
            enums.EN_PROJECTILE: [
                self._load_image(enem_path + 'projectile_0.png'),
                self._load_image(enem_path + 'projectile_1.png')],
            enums.EN_CRAB: [
                self._load_image(enem_path + 'crab_0.png'),
                self._load_image(enem_path + 'crab_1.png')],
            enums.EN_SOLDIER1: [
                self._load_image(enem_path + 'soldier1_0.png'),
                self._load_image(enem_path + 'soldier1_1.png')],
            # stage 3
            enums.EN_SKIER: [
                self._load_image(enem_path + 'skier_0.png'),
                self._load_image(enem_path + 'skier_1.png')],
            enums.EN_BOAR: [
                self._load_image(enem_path + 'boar_0.png'),
                self._load_image(enem_path + 'boar_1.png')],
            enums.EN_SOLDIER2: [
                self._load_image(enem_path + 'soldier2_0.png'),
                self._load_image(enem_path + 'soldier2_1.png')]                               
        }
        self.hotspot_images = {
            enums.HS_LIFE: self._load_image(constants.SPR_PATH + 'hotspot0.png'),
            enums.HS_SHIELD: self._load_image(constants.SPR_PATH + 'hotspot1.png'),
            enums.HS_AMMO: self._load_image(constants.SPR_PATH + 'hotspot2.png'),
            enums.HS_CANDY: self._load_image(constants.SPR_PATH + 'hotspot3.png'),
            enums.HS_APPLE: self._load_image(constants.SPR_PATH + 'hotspot4.png'),
            enums.HS_CHOCO: self._load_image(constants.SPR_PATH + 'hotspot5.png'),
            enums.HS_COIN: self._load_image(constants.SPR_PATH + 'hotspot6.png')}
        self.control_images = {
            enums.CT_CLASSIC: self._load_image(constants.ASS_PATH + 'classic.png'),
            enums.CT_GAMER: self._load_image(constants.ASS_PATH + 'gamer.png'),
            enums.CT_RETRO: self._load_image(constants.ASS_PATH + 'retro.png'),
            enums.CT_JOYSTICK: self._load_image(constants.ASS_PATH + 'joypad.png'),
            enums.CT_COMMON: self._load_image(constants.ASS_PATH + 'common.png')
        }
        blast_path = constants.SPR_PATH
        self.blast_images = {
            0: [ # explosion 1: enemies
                self._load_image(blast_path + 'blast0.png'),
                self._load_image(blast_path + 'blast1.png'),
                self._load_image(blast_path + 'blast2.png'),
                self._load_image(blast_path + 'blast3.png'),
                self._load_image(blast_path + 'blast4.png'),
                self._load_image(blast_path + 'blast5.png'),
                self._load_image(blast_path + 'blast6.png')],
            1: [ # explosion 2: mines
                self._load_image(blast_path + 'blast7.png'),
                self._load_image(blast_path + 'blast8.png'),
                self._load_image(blast_path + 'blast9.png'),
                self._load_image(blast_path + 'blast10.png'),
                self._load_image(blast_path + 'blast4.png'),
                self._load_image(blast_path + 'blast5.png'),
                self._load_image(blast_path + 'blast6.png')],
            2: [ # magic halo for hotspots
                self._load_image(blast_path + 'blast12.png'),
                self._load_image(blast_path + 'blast11.png'),
                self._load_image(blast_path + 'blast12.png')]}        
        # sound effects
        self.sfx_message = pygame.mixer.Sound(constants.FX_PATH + 'sfx_message.wav')
        self.sfx_click = pygame.mixer.Sound(constants.FX_PATH + 'sfx_menu_click.wav')
        self.sfx_respawn = pygame.mixer.Sound(constants.FX_PATH + 'sfx_respawn.wav')
        self.sfx_hit = pygame.mixer.Sound(constants.FX_PATH + 'sfx_hit.wav')
        self.sfx_blast = {
            0: pygame.mixer.Sound(constants.FX_PATH + 'sfx_blast0.wav'),
            1: pygame.mixer.Sound(constants.FX_PATH + 'sfx_blast1.wav'),
            2: pygame.mixer.Sound(constants.FX_PATH + 'sfx_blast2.wav'),
            3: pygame.mixer.Sound(constants.FX_PATH + 'sfx_blast3.wav')}
        self.sfx_hotspot = {
            enums.HS_LIFE: pygame.mixer.Sound(constants.FX_PATH + 'sfx_life.wav'),
            enums.HS_SHIELD: pygame.mixer.Sound(constants.FX_PATH + 'sfx_shield.wav'),
            enums.HS_AMMO: pygame.mixer.Sound(constants.FX_PATH + 'sfx_ammo.wav'),
            enums.HS_CANDY: pygame.mixer.Sound(constants.FX_PATH + 'sfx_candy.wav'),
            enums.HS_APPLE: pygame.mixer.Sound(constants.FX_PATH + 'sfx_apple.wav'),
            enums.HS_CHOCO: pygame.mixer.Sound(constants.FX_PATH + 'sfx_choco.wav'),
            enums.HS_COIN: pygame.mixer.Sound(constants.FX_PATH + 'sfx_coin.wav')}
        # cache sound effects tuple for better performance
        self._blast_sfx_tuple = tuple(self.sfx_blast.values())
        # modify the XY position of the map on the screen to create 
        # a shaking effect for a given number of frames (explosions)
        self.shake = [0, 0]
        self.shake_timer = 0
        # high scores table
        self.high_scores = []
        self._load_high_scores()
        # create a joystick/joypad/gamepad object
        self.joystick = self.config.prepare_joystick()

        # common fonts. S = small L = large F = foreground B = background
        self.fonts = {
            # small fonts
            enums.S_F_BROWN: Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['SAND1'], True),
            enums.S_B_BROWN: Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['BROWN1'], True),
            enums.S_F_WHITE: Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['GRAY2'], True),
            enums.S_B_WHITE: Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['DARK_GRAY1'], False),
            enums.S_F_GREEN: Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['GREEN0'], True),
            enums.S_B_GREEN: Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['DARK_GREEN0'], True),
            #large fonts
            enums.L_F_WHITE: Font(constants.FNT_PATH + 'large_font.png', constants.PALETTE['WHITE2'], True),
            enums.L_B_WHITE: Font(constants.FNT_PATH + 'large_font.png', constants.PALETTE['DARK_GRAY1'], True),
            enums.L_F_RED:   Font(constants.FNT_PATH + 'large_font.png', constants.PALETTE['RED0'], True),
            enums.L_B_BLACK: Font(constants.FNT_PATH + 'large_font.png', constants.PALETTE['BLACK1'], True),
            enums.L_F_BROWN: Font(constants.FNT_PATH + 'large_font.png', constants.PALETTE['ORANGE0'], True),
            enums.L_B_BROWN: Font(constants.FNT_PATH + 'large_font.png', constants.PALETTE['BROWN0'], False)}
        
        # create floating texts
        self.floating_text = FloatingText(self.srf_map)
        
        # create explosion pool
        self.explosion_pool = ExplosionPool(pool_size=10)
        
        # pre-calculate enemy scores
        self._enemy_scores = {
            enums.EN_SCORPION: ('+25', 25),
            enums.EN_SNAKE: ('+50', 50),
            enums.EN_SOLDIER0: ('+75', 75)
        }

        # cache scanline values to avoid recalculation
        self._scanline_cache = None
        


    # clear the input buffer (keyboard and joystick)
    def clear_input_buffer(self):
        pygame.event.clear()
        if self.joystick is not None:
            # wait until all buttons are released
            while any(self.joystick.get_button(i) 
                      for i in range(self.joystick.get_numbuttons())):
                pygame.event.pump()



    # wait for a key to be pressed
    def wait_for_key(self):
        self.clear_input_buffer()
        while True:
            # joypad buttons
            if self.joystick is not None:
                if any(self.joystick.get_button(i) 
                       for i in range(self.joystick.get_numbuttons())):
                    self.clear_input_buffer()
                    break
            # keyboard keys
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.exit()
                elif event.type == pygame.KEYDOWN:
                    self.clear_input_buffer() 
                    break
            else: continue
            break



    # create a window or full-screen environment
    def apply_display_settings(self):
        if self.config.data['screen_mode'] == enums.SM_4_3: # 4:3
            self._apply_screen_mode_4_3()
        elif self.config.data['screen_mode'] == enums.SM_16_9: # 16:9
            self._apply_screen_mode_16_9()
        else:
            self._apply_windowed_mode()
        # invalidate scanline cache after display change
        self._scanline_cache = None        



    # new high score??
    def update_high_score_table(self, player_score):
        if player_score > self.high_scores[7][2]:
            self.high_scores.append([self._get_player_name(), str(date.today()), player_score])
            self.high_scores.sort(reverse=True, key=lambda x: x[2])
            self.high_scores.pop() # remove last score (8 scores remain)
            # save the high scores table
            with open('scores.dat', "wb") as f:
                pickle.dump(self.high_scores, f)



    # exit to the operating system
    def exit(self):
        pygame.quit()
        sys.exit()



    # draw scanlines
    def apply_scanlines(self):
        # use cached values if available
        if self._scanline_cache is None:
            x = self.win_size[0] - self.h_margin - 1
            if self.config.data['screen_mode'] is not enums.SM_WINDOW:
                height = self.win_size[1] - self.v_margin
            else: # windowed mode: fixed bottom margin of 26 pixels
                height = self.win_size[1] - 26
            self._scanline_cache = (x, height)
        else:
            x, height = self._scanline_cache

        y = self.v_margin
        while y < height:
            # every 3 lines draw an almost black line
            pygame.draw.line(self.screen, (10, 10, 10), (self.h_margin, y), (x, y))
            y += 3            
    


    # dump and scale surfaces to the screen
    def update_screen(self):
        if self.status == enums.GS_OVER:
            # scale the menu
            self.screen.blit(pygame.transform.scale(
                self.srf_menu, constants.MENU_SCALED_SIZE),
                (self.h_margin, self.v_margin))
        else:
            # scale the scoreboard
            self.screen.blit(pygame.transform.scale(
                self.srf_sboard, constants.SBOARD_SCALED_SIZE), 
                (self.h_margin, self.v_margin))
                        
            # shake the surface of the map if it has been requested
            offset = [0,0]
            if self.shake_timer > 0:
                if self.shake_timer == 1: # last frame shaken
                    # it's necessary to clean the edges of the map after shaking
                    if self.config.data['screen_mode'] == enums.SM_16_9: # 16:9 fullscreen
                        self.screen.blit(self.img_background, (0,0))
                    else: # 4:3 fullscreen or windowed mode
                        self.screen.fill(constants.PALETTE['BLACK0'])
                else:
                    offset[0] = random.randint(-self.shake[0], self.shake[0])
                    offset[1] = random.randint(-self.shake[1], self.shake[1])
                self.shake_timer -= 1
            
            # scale the map
            self.screen.blit(pygame.transform.scale(
                self.srf_map, constants.SCREEN_MAP_SCALED_SIZE), (self.h_margin + offset[0], 
                constants.SBOARD_SCALED_SIZE[1] + self.v_margin + offset[1]))
        
        if self.config.data['scanlines']: self.apply_scanlines()
        pygame.display.flip() # refresh the screen
        self.clock.tick(60) # 60 FPS



    # display a message, darkening the screen
    def message(self, msg1, msg2, darken, muted, opaque, control_info):
        # obscure the surface of the map
        if darken:
            self.srf_map.set_alpha(115)
            self.update_screen()
        # save a copy of the darkened screen
        aux_surf = pygame.Surface((constants.SCREEN_MAP_UNSCALED_SIZE), pygame.SRCALPHA)    
        aux_surf.blit(self.srf_map, (0,0))
        # draw the light message on the dark background
        height = 36
        # calculate the width of the box
        message1_len = len(msg1) * 7 # approximate length of text 1 in pixels
        message2_len = len(msg2) * 4 # approximate length of text 2 in pixels
        # width = length of the longest text + margin
        width = max(message1_len, message2_len) + 30
        # extra width and height with control info
        if control_info:
            width = max(width, 160)
            height = height + 50
        # calculate the position of the box
        x = (constants.SCREEN_MAP_UNSCALED_SIZE[0]//2) - (width//2)
        y = (constants.SCREEN_MAP_UNSCALED_SIZE[1]//2) - (height//2)
        # blackest window
        opacity = 195
        if opaque:
            opacity = 255
        pygame.draw.rect(aux_surf, (0, 0, 0, opacity),(x, y, width, height))
        # draw the text centred inside the window (Y positions are fixed)
        # line 1
        text_x = (x + (width//2)) - (message1_len//2)
        text_y = y + 5
        self.fonts[enums.L_B_WHITE].render(msg1, aux_surf, (text_x, text_y))
        self.fonts[enums.L_F_WHITE].render(msg1, aux_surf, (text_x - 1, text_y - 1))
        # line 2
        text_x = (x + (width//2)) - (message2_len//2)
        text_y = y + 25
        self.fonts[enums.S_B_GREEN].render(msg2, aux_surf, (text_x, text_y))
        self.fonts[enums.S_F_GREEN].render(msg2, aux_surf, (text_x - 1, text_y - 1))
        # control images
        if control_info:
            aux_surf.blit(self.control_images[self.config.data['control']], (x + 15, y + 45))
            aux_surf.blit(self.control_images[4], (x + width - 85, y + 39))
        # return the copy with the message on the map surface and redraw it.
        self.srf_map.blit(aux_surf, (0,0))
        self.srf_map.set_alpha(None)
        self.update_screen()
        if muted: self.sfx_click.play()
        else: self.sfx_message.play()



    # display a message to confirm exit
    def confirm_exit(self):
        self.message('Leave the current game?', 'ESC TO EXIT. ANY OTHER KEY TO CONTINUE', True, False, False, False)
        pygame.event.clear(pygame.KEYDOWN)
        while True:
            for event in pygame.event.get():
                # exit when clicking the X button on the window
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:                    
                        return True # back to menu
                    return False # continue game



    # display a 'game over' message and wait
    def over(self):
        self.shake_timer = 1 # clean the edges 
        self.message('G a m e  O v e r', 'PRESS ANY KEY', True, True, False, False)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load(constants.MUS_PATH + 'mus_game_over.ogg')
        pygame.mixer.music.play()
        self.wait_for_key() # back to menu



    # our player wins the game. End sequence
    def win(self):
        self.message('CONGRATULATIONS!!', 'You achieved all the goals!', True, True, False, False)
        # main theme song again
        pygame.mixer.music.load(constants.MUS_PATH + 'mus_menu.ogg')
        pygame.mixer.music.play()
        self.wait_for_key()
        self.update_high_score_table(self.score)
        self.status = enums.GS_OVER
        return                    
            


    # collisions between the player and mines, killer tiles, enemies and hotspots
    def check_player_collisions(self, player, scoreboard, map_number, map_data):
        # player and killer tiles or mines
        # convert player position to tile coordinates
        tile_x = int(player.x // constants.TILE_SIZE)
        tile_y = int(player.y // constants.TILE_SIZE)    
        # check bounds and get tile type
        if (0 <= tile_x < constants.MAP_TILE_SIZE[0] and 
            0 <= tile_y < constants.MAP_TILE_SIZE[1]):            
            tile_type = map_data['tile_types'][tile_y][tile_x]
            if tile_type == enums.TT_MINE:
                # eliminate the mine
                map_data['tile_types'][tile_y][tile_x] = enums.TT_NO_ACTION
                # shake the map
                self.shake = [10, 6]
                self.shake_timer = 14
                # create an explosion at tile center
                tile_size = constants.TILE_SIZE
                blast_x = (tile_x * tile_size) + constants.HALF_TILE_SIZE
                blast_y = (tile_y * tile_size) + constants.TILE_CENTER_OFFSET
                blast = self.explosion_pool.get_explosion([blast_x, blast_y], self.blast_images[1])
                self.sprite_groups[enums.SG_BLASTS].add(blast)
                random.choice(self._blast_sfx_tuple).play()
                player.invincible = False
                player.loses_energy(7, play_sound=False)
                self.remaining_mines -= 1
                self.loss_sequence = 70 # allows to end the animation of the explosion
                scoreboard.invalidate()
                return
            elif tile_type == enums.TT_KILLER:
                player.loses_energy(1)
                scoreboard.invalidate()
                return
    
            # player and enemies
            if not player.invincible:
                # filter only alive enemies for collisions
                alive_enemies = [e for e in self.sprite_groups[enums.SG_ENEMIES] if not e.is_dead]
                for enemy in alive_enemies:
                    if pygame.sprite.collide_rect_ratio(0.60)(player, enemy):
                        player.loses_energy(2)
                        scoreboard.invalidate() # redraws the scoreboard
                        return     
           
        # player and hotspot
        collided_hotspots = pygame.sprite.spritecollide(
            player, self.sprite_groups[enums.SG_HOTSPOT], False, pygame.sprite.collide_rect_ratio(0.60))

        if collided_hotspots:
            hotspot = collided_hotspots[0]  # Solo el primero, que será el único

            # shake the map (just a little)
            self.shake = [4, 4]
            self.shake_timer = 4

            # create a magic halo
            blast = self.explosion_pool.get_explosion(hotspot.rect.center, self.blast_images[2])
            self.sprite_groups[enums.SG_BLASTS].add(blast)                
            self.sfx_hotspot[hotspot.type].play()
            
            # manage the object according to the type
            ftext = '' # floating text
            # power-ups
            if hotspot.type == enums.HS_LIFE:
                ftext = 'Full Energy'
                player.energy, _ = player.set_player_attributes()
            elif hotspot.type == enums.HS_SHIELD:
                ftext = 'Shield'
                player.invincible = True
                player.timer_from = pygame.time.get_ticks()         
            elif hotspot.type == enums.HS_AMMO:
                player.ammo = min(player.ammo + constants.AMMO_ROUND, constants.MAX_AMMO)
                ftext = 'Ammo +10'
            # gifts
            elif hotspot.type == enums.HS_CANDY:
                ftext = '+50'
                self.score += 50
            elif hotspot.type == enums.HS_APPLE:
                ftext = '+75'
                self.score += 75                    
            elif hotspot.type == enums.HS_CHOCO:
                ftext = '+100'
                self.score += 100
            elif hotspot.type == enums.HS_COIN:
                ftext = '+200'
                self.score += 200

            scoreboard.invalidate()
            self.floating_text.show(ftext, 
                hotspot.tile_x * constants.TILE_SIZE, 
                hotspot.tile_y * constants.TILE_SIZE)
            
            hotspot.kill() # remove the collided hotspot                                    
            return



    def check_bullet_collisions(self, player, scoreboard):
        # bullets and enemies
        shot_sprite = self.sprite_groups[enums.SG_SHOT].sprite
        if shot_sprite is not None:  # still shot in progress
            enemies_group = self.sprite_groups[enums.SG_ENEMIES]
            collided_enemies = pygame.sprite.spritecollide(shot_sprite, enemies_group, False)

            # filter only alive enemies
            alive_collided = [e for e in collided_enemies if not e.is_dead]

            if alive_collided:  # collision detected
                enemy = alive_collided[0]  # get first collided enemy
                enemy.health -= 1

                # optimized scoring system using pre-calculated values
                if enemy.type in self._enemy_scores:
                    ftext, score = self._enemy_scores[enemy.type]
                    self.score += score
                    self.floating_text.show(ftext, enemy.rect.x, enemy.rect.y)

                shot_sprite.kill()  # remove the bullet

                # if it's the last life, the enemy dies
                if enemy.health == 0:
                    # shake the map only when enemy dies
                    self.shake = [10, 6]
                    self.shake_timer = 14

                    blast = self.explosion_pool.get_explosion(enemy.rect.center, self.blast_images[0])
                    self.sprite_groups[enums.SG_BLASTS].add(blast)
                    # use pre-computed sound effects tuple
                    random.choice(self._blast_sfx_tuple).play()
                    # mark as dead instead of permanently removing
                    enemy.mark_as_dead()
                else:
                    self.sfx_hit.play()

                # redraw the scoreboard
                scoreboard.invalidate()



    # regenerate the hotspot to score (if needed)
    def regenerate_hotspot(self, tile_types):
        has_score_hotspot = any(
            hotspot.type >= enums.HS_CANDY
                for hotspot in self.sprite_groups[enums.SG_HOTSPOT])
        if not has_score_hotspot:
            # inverse probabilities: lower value = higher probability
            weights = [40, 30, 20, 10]  # CANDY(40%), APPLE(30%), CHOCO(20%), COIN(10%)
            type = random.choices([enums.HS_CANDY, enums.HS_APPLE, enums.HS_CHOCO, enums.HS_COIN],
                                  weights=weights)[0]
            new_hotspot = Hotspot(type, self.hotspot_images[type], tile_types)
            self.sprite_groups[enums.SG_HOTSPOT].add(new_hotspot)



    # check and respawn dead enemies after delay
    def check_enemy_respawn(self, camera):
        current_time = pygame.time.get_ticks()
        for enemy in self.sprite_groups[enums.SG_ENEMIES]:
            if enemy.is_dead:
                # check if respawn time has elapsed
                if current_time - enemy.death_time >= enemy.respawn_delay:
                    # only respawn if player is not too close
                    if not enemy.is_player_near_respawn():
                        # calculate respawn position once
                        spawn_x = enemy.original_data[3] * constants.TILE_SIZE
                        spawn_y = enemy.original_data[4] * constants.TILE_SIZE
                        respawn_center = (spawn_x + constants.HALF_TILE_SIZE, spawn_y + constants.HALF_TILE_SIZE)

                        # create a temporary rect at respawn position to check visibility
                        temp_rect = pygame.Rect(spawn_x, spawn_y, enemy.rect.width, enemy.rect.height)
                        is_spawn_visible = (
                            temp_rect.right > camera.x and
                            temp_rect.left < camera.x + constants.SCREEN_MAP_UNSCALED_SIZE[0] and
                            temp_rect.bottom > camera.y and
                            temp_rect.top < camera.y + constants.SCREEN_MAP_UNSCALED_SIZE[1])

                        # only show blast and play FX if the spawn is visible on screen
                        if is_spawn_visible:
                            blast = self.explosion_pool.get_explosion(respawn_center, self.blast_images[2])
                            self.sprite_groups[enums.SG_BLASTS].add(blast)
                            self.sfx_respawn.play()

                        # respawn the enemy (always, regardless of visibility)
                        enemy.respawn()



    def set_background(self, map_number):
        if map_number >= 6: # Ardennes
            self.img_background =  pygame.image.load(constants.ASS_PATH + 'wp2.png').convert()
        elif map_number >= 3: # Normandy
            self.img_background =  pygame.image.load(constants.ASS_PATH + 'wp1.png').convert()
        elif map_number >= 0: # North Africa
            self.img_background =  pygame.image.load(constants.ASS_PATH + 'wp0.png').convert()
        else: # menu
            self.img_background =  pygame.image.load(constants.ASS_PATH + 'wp3.png').convert()
        # apply
        screen_size = self.screen.get_size()
        self.img_background = pygame.transform.scale(self.img_background, screen_size)
        self.screen.blit(self.img_background, (0,0))



    ##### auxiliary functions #####

    # helper function to load and convert images
    def _load_image(self, path):
        return pygame.image.load(path).convert_alpha()



    # windowed mode, generate a main window with title, icon, and 32-bit colour
    def _apply_windowed_mode(self):        
        # default margins
        self.v_margin = constants.V_MARGIN
        self.h_margin = constants.H_MARGIN
        # create the window
        self.win_size = constants.WIN_SIZE
        self.screen = pygame.display.set_mode(self.win_size, 0, 32)
        pygame.display.set_caption('.:: Mine Squad Pi ::.')
        icon = pygame.image.load('minesquad.png').convert_alpha()
        pygame.display.set_icon(icon)



    # 4:3 screen modes
    def _apply_screen_mode_4_3(self):   
        res_4_3 = [                        
            (800, 600),    # SVGA
            (1024, 768),   # XGA
            (1152, 864),   # XGA+
            (1280, 960),   # SXGA
            (1600, 1200),  # UXGA
        ]
        for res in res_4_3:
            if res in pygame.display.list_modes():
                self.win_size = res[0], res[1]
                self.v_margin = (self.win_size[1] - constants.MENU_SCALED_SIZE[1]) // 2
                self.h_margin = (self.win_size[0] - constants.MENU_SCALED_SIZE[0]) // 2                  
                self.screen = pygame.display.set_mode(self.win_size, pygame.FULLSCREEN, 32)
                return
        # screen resolution not available
        self.config.data['screen_mode'] = enums.SM_WINDOW
        self._apply_windowed_mode()



    # 16:9 screen modes
    def _apply_screen_mode_16_9(self):
        res_16_9 = [            
            (1280, 720),   # HD/720p
            (1366, 768),   # HD
            (1600, 900),   # HD+
            (1920, 1080),  # Full HD
            (2560, 1440),  # 2K QHD
            (3840, 2160),  # 4K UHD  
        ]
        for res in res_16_9:
            if res in pygame.display.list_modes():
                self.win_size = res[0], res[1]
                self.v_margin = (self.win_size[1] - constants.MENU_SCALED_SIZE[1]) // 2
                self.h_margin = (self.win_size[0] - constants.MENU_SCALED_SIZE[0]) // 2            
                self.screen = pygame.display.set_mode(self.win_size, pygame.FULLSCREEN, 32)
                # menu background image to fill in the black sides
                self.set_background(-1)
                return
        # screen resolution not available
        self.config.data['screen_mode'] = enums.SM_WINDOW
        self._apply_windowed_mode()



    # load the high scores table
    def _load_high_scores(self):
        if os.path.exists('scores.dat'):
            with open('scores.dat', "rb") as f:
                self.high_scores = pickle.load(f)
        else: # default values
            today = str(date.today())
            for _ in range(8):
                self.high_scores.append(['SALVAKANTERO', today, 0])



    # allow the player to enter their name
    def _get_player_name(self):
        self.message('You achieved a high score!', 'Enter your name...', False, False, True, False)
        pygame.event.clear(pygame.KEYDOWN)
        name = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.exit()
                if event.type == pygame.KEYDOWN:
                    # RETURN or ESC has been pressed, end the entry of the name                  
                    if (event.key == pygame.K_ESCAPE or 
                        event.key == pygame.K_RETURN or
                        event.key == pygame.K_KP_ENTER):                    
                        return name.upper()
                    # a key between 0 and Z has been pressed. Add to the name
                    elif (event.key > pygame.K_0 and event.key < pygame.K_z):
                        if len(name) < 12: name += pygame.key.name(event.key)
                    # the space bar has been pressed. Add a space
                    elif  event.key == pygame.K_SPACE:
                        if len(name) < 12: name += ' '
                    # a delete key has been pressed, delete the last character                       
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        name = name[:-1]
                    # draw the current name
                    self.message('You achieved a high score!', name.upper(), False, True, True, False)

