
# ==============================================================================
# .::Menu class::.
# Initial menu and additional information displayed on sliding pages
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

from font import Font
from marqueetext import MarqueeText



class Menu():
    def __init__(self, game):
        self.game = game        
        self.srf_menu = game.srf_menu # surface
        self.tip = 'Use mouse, joypad, or cursors and SPACE/ENTER to select'        
        # images
        self.img_menu = pygame.image.load(constants.ASS_PATH + 'menu_back.png').convert()
        self.img_piper_flipped = pygame.transform.flip(self.game.img_piper, True, False)
        self.img_star = pygame.image.load(constants.SPR_PATH + 'star.png').convert_alpha()
        self.img_pointer = pygame.image.load(constants.SPR_PATH + 'pointer.png').convert_alpha()
        # sounds
        self.sfx_menu_click = pygame.mixer.Sound(constants.FX_PATH + 'sfx_menu_click.wav')
        self.sfx_menu_select = pygame.mixer.Sound(constants.FX_PATH + 'sfx_menu_select.wav')

        # pre-create fonts for marquee (avoid recreation on each show())
        self._marquee_help_font = Font(constants.FNT_PATH + 'large_font.png', constants.PALETTE['ORANGE2'], True)
        self._marquee_credits_font = Font(constants.FNT_PATH + 'small_font.png', constants.PALETTE['GREEN0'], True)

        # page 0: menu options
        # page 1: high scores
        # page 2: Blaze info
        # page 3: Piper info
        # page 4: control info
        # page 5: hotspots info
        # page 6: settings
        # page 7: player selection
        # page 8: difficulty selection
        self.menu_pages = []
        for _ in range(0, 9):
            surface = pygame.Surface(constants.MENU_UNSCALED_SIZE)
            surface.set_colorkey(constants.PALETTE['BLACK0'])
            self.menu_pages.append(surface)  
        # preload static pages 
        self.page_0()
        self.page_2()
        self.page_3()
        self.page_4()
        self.page_5()        
        self.page_7()
        self.page_8()



    def page_0(self): # main menu options      
        options = ['Start Game', 'Settings', 'Exit']
        x, y = 90, 70
        # draws the options
        for i, option in enumerate(options):
            self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 
                             option, self.menu_pages[0], x, y + i*20, 1)            
        self._shaded_text(self.game.fonts[enums.S_B_BROWN], self.game.fonts[enums.S_F_BROWN], 
                        self.tip, self.menu_pages[0], 12, y-55, 1)



    def page_1(self): # high scores
        self.menu_pages[1].fill(constants.PALETTE['BLACK0']) # black background
        # header
        x, y = 85, 32
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN],
                         'High Scores', self.menu_pages[1], x, y, 1)                
        y = 60
        for i in range(8):
            if i % 2 == 0: # even index
                fb = self.game.fonts[enums.S_B_WHITE] # small gray font for the background
                ff = self.game.fonts[enums.S_F_WHITE] # small white font for the foreground
            else: # odd index 
                fb = self.game.fonts[enums.S_B_BROWN] # small dark green font for the background
                ff = self.game.fonts[enums.S_F_BROWN] # small green font for the foreground
            # names
            self._shaded_text(fb, ff, self.game.high_scores[i][0], self.menu_pages[1], 50, y, 1)
            # dates and scores
            self._shaded_text(fb, ff, self.game.high_scores[i][1] + '    ' + 
                str(self.game.high_scores[i][2]).rjust(6, '0'), self.menu_pages[1], 115, y, 1)
            y += 10



    def page_2(self): # Blaze info        
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_RED], 
                         'B L A Z E', self.menu_pages[2], 115, 30, 1)
        self._draw_player_info(115, enums.PL_BLAZE, 2)
        self.menu_pages[2].blit(self.game.img_blaze, (10, 0))



    def page_3(self): # Piper info
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_RED], 
                         'P I P E R', self.menu_pages[3], 10, 30, 1)
        self._draw_player_info(10, enums.PL_PIPER, 3)
        self.menu_pages[3].blit(self.game.img_piper, (120, 0))



    def page_4(self): # control info
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        layouts = [ # control index, image pos, description, text pos
            (self.game.control_images[0], (30, 52), 'Classic', (39, 90)),
            (self.game.control_images[1], (95, 52), 'Gamer', (104, 90)),
            (self.game.control_images[2], (160, 52), 'Retro', (170, 90)),
            (self.game.control_images[3], (53, 110), 'Joypad', (70, 149)),
            (self.game.control_images[4], (119, 101), 'Common keys', (131, 149))]
        # header
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 'Controls', self.menu_pages[4], 90, 27, 1)        
        # images and descriptions
        for image, img_pos, text, text_pos in layouts:
            self.menu_pages[4].blit(image, img_pos)
            self._shaded_text(fb, ff, text, self.menu_pages[4], text_pos[0], text_pos[1], 1)



    def page_5(self): # hotspots
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        hotspots1 = [ # hotspot index, image pos, description, text pos
            (self.game.hotspot_images[enums.HS_LIFE], (40, 60), 'FULL ENERGY', (61, 66)),
            (self.game.hotspot_images[enums.HS_SHIELD], (40, 80), 'INVULNERABLE', (61, 86)),
            (self.game.hotspot_images[enums.HS_AMMO], (40, 100), 'AMMO +10', (61, 106)),
            (self.game.hotspot_images[enums.HS_BEACON], (40, 120), 'BEACONS +5', (61, 126))]
        hotspots2 = [ # hotspot index, image pos, description, text pos
            (self.game.hotspot_images[enums.HS_CANDY], (140, 60), 'CANDY +50', (161, 66)),
            (self.game.hotspot_images[enums.HS_APPLE], (140, 80), 'APPLE +75', (161, 86)),
            (self.game.hotspot_images[enums.HS_CHOCO], (140, 100), 'CHOCOLATE +100', (161, 106)),
            (self.game.hotspot_images[enums.HS_COIN], (140, 120), 'COIN +200', (161, 126))]
        # header
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 'HotSpots', self.menu_pages[5], 95, 27, 1)
        # images and descriptions
        for image, img_pos, text, text_pos in hotspots1:
            self.menu_pages[5].blit(image, img_pos)
            self._shaded_text(fb, ff, text, self.menu_pages[5], text_pos[0], text_pos[1], 1)
        for image, img_pos, text, text_pos in hotspots2:
            self.menu_pages[5].blit(image, img_pos)
            self._shaded_text(fb, ff, text, self.menu_pages[5], text_pos[0], text_pos[1], 1)



    def page_6(self): # settings 
        x, y = 60, 60
        fb = self.game.fonts[enums.L_B_BROWN] # brown font for the background
        ff = self.game.fonts[enums.L_F_BROWN] # sand font for the foreground
        fb2 = self.game.fonts[enums.L_B_WHITE] # white font for the background
        ff2 = self.game.fonts[enums.L_F_WHITE] # white font for the foreground

        # screen mode
        if self.game.config.data['screen_mode'] == enums.SM_4_3: value = '4:3'
        elif self.game.config.data['screen_mode'] == enums.SM_16_9: value = '16:9'
        else: value = 'WINDOW'
        self._shaded_text(fb, ff, 'Screen mode:', self.menu_pages[6], x, y, 1)
        self._shaded_text(fb2, ff2, value, self.menu_pages[6], x+105, y, 1)

        # scanlines filter 
        if self.game.config.data['scanlines']: value = 'ON'
        else: value = 'OFF'
        self._shaded_text(fb, ff, 'Scanlines:', self.menu_pages[6], x, y+20, 1)
        self._shaded_text(fb2, ff2, value, self.menu_pages[6], x+105, y+20, 1)

        # control keys
        if self.game.config.data['control'] == enums.CT_CLASSIC: value = 'CLASSIC' 
        elif self.game.config.data['control'] == enums.CT_GAMER: value = 'GAMER'
        elif self.game.config.data['control'] == enums.CT_RETRO: value = 'RETRO'
        else: value = 'JOYPAD'
        self._shaded_text(fb, ff, 'Control Keys:', self.menu_pages[6], x, y+40, 1)
        self._shaded_text(fb2, ff2, value, self.menu_pages[6], x+105, y+40, 1)

        # exit
        self._shaded_text(fb, ff, 'Exit Options', self.menu_pages[6], x, y+60, 1)
        self._shaded_text(self.game.fonts[enums.S_B_BROWN], self.game.fonts[enums.S_F_BROWN], 
                self.tip, self.menu_pages[6], 12, 5, 1)



    def page_7(self):  # player selection
        # title
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], 
                        self.game.fonts[enums.L_F_BROWN], 
                        'Select Player', self.menu_pages[7], 80, 1, 1)
        # instructions
        self._shaded_text(self.game.fonts[enums.S_B_BROWN], 
                        self.game.fonts[enums.S_F_BROWN], 
                        'Use mouse, joypad, or cursors and SPACE/ENTER to select', 
                        self.menu_pages[7], 12, 22, 1)                        
        # Blaze info (left side)
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], 
                        self.game.fonts[enums.L_F_RED], 
                        'B L A Z E', self.menu_pages[7], 27, 36, 1)
        self.menu_pages[7].blit(self.game.img_blaze, (15, 60)) 
        # Piper info (right side)
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], 
                        self.game.fonts[enums.L_F_RED], 
                        'P I P E R', self.menu_pages[7], 152, 36, 1)
        self.menu_pages[7].blit(self.img_piper_flipped, (129, 60))      



    def page_8(self):  # difficulty selection
        # title
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 
                        'Select Difficulty', self.menu_pages[8], 68, 1, 1)
        # instructions
        self._shaded_text(self.game.fonts[enums.S_B_BROWN], self.game.fonts[enums.S_F_BROWN], 
                        'Use mouse, joypad, or cursors and SPACE/ENTER to select', 
                        self.menu_pages[8], 12, 22, 1)
        # easy difficulty (left)
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_RED], 
                        'EASY', self.menu_pages[8], 32, 45, 1)        
        # normal difficulty (center)
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_RED], 
                        'NORMAL', self.menu_pages[8], 100, 45, 1)
        # hard difficulty (right)  
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_RED], 
                        'HARD', self.menu_pages[8], 182, 45, 1)



    # allows you to choose between Blaze and Piper
    def select_player(self):
        selected_player = enums.PL_BLAZE  # player 1 BLAZE by default
        confirmed = False

        self.game.clear_input_buffer()        
        while not confirmed:
            self.srf_menu.blit(self.img_menu, (0, 0))
            self.srf_menu.blit(self.menu_pages[7], (0, 0))            
            # draw a selection box according to the chosen player
            if selected_player == enums.PL_BLAZE:
                self._draw_selection_box(self.srf_menu, 2, 54, 114, 142)
            else:  # PL_PIPER
                self._draw_selection_box(self.srf_menu, 124, 54, 114, 142)            
            # event management
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:                       
                        return None  # cancel, return to main menu         
                    elif event.key == pygame.K_LEFT:
                        if selected_player == enums.PL_PIPER:
                            selected_player = enums.PL_BLAZE
                            self.sfx_menu_click.play()                    
                    elif event.key == pygame.K_RIGHT:
                        if selected_player == enums.PL_BLAZE:
                            selected_player = enums.PL_PIPER
                            self.sfx_menu_click.play()                    
                    elif (event.key == pygame.K_RETURN or 
                        event.key == pygame.K_KP_ENTER or 
                        event.key == pygame.K_SPACE):
                        self.sfx_menu_select.play()
                        confirmed = True                
                # joystick/gamepad
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.sfx_menu_select.play()
                    confirmed = True                
                elif event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:  # horizontal axis
                        if event.value < -0.5 and selected_player == enums.PL_PIPER: # left
                            selected_player = enums.PL_BLAZE
                            self.sfx_menu_click.play()
                        elif event.value > 0.5 and selected_player == enums.PL_BLAZE: # right
                            selected_player = enums.PL_PIPER
                            self.sfx_menu_click.play()
            self.game.update_screen()
        
        return selected_player



    def select_difficulty(self):
        selected_difficulty = enums.DF_NORMAL  # balanced difficulty by default
        confirmed = False
        speed, strength = 4, 4
        previous_difficulty = None  # track changes to avoid unnecessary redraws

        self.game.clear_input_buffer()
        while not confirmed:
            self.srf_menu.blit(self.img_menu, (0, 0))

            # only recreate surface when difficulty changes
            if previous_difficulty != selected_difficulty:
                self.menu_pages[8] = pygame.Surface(constants.MENU_UNSCALED_SIZE)
                self.menu_pages[8].set_colorkey(constants.PALETTE['BLACK0'])
                self.page_8()  # redraw the base content
                previous_difficulty = selected_difficulty

            self.srf_menu.blit(self.menu_pages[8], (0, 0))                        
            # draw selection boxes according to the chosen difficulty
            if selected_difficulty == enums.DF_EASY:
                self._draw_selection_box(self.srf_menu, 15, 35, 60, 30)
                speed, strength = 3, 5                           
            elif selected_difficulty == enums.DF_NORMAL:
                self._draw_selection_box(self.srf_menu, 90, 35, 60, 30)
                speed, strength = 4, 4
            else:  # DF_HARD
                self._draw_selection_box(self.srf_menu, 165, 35, 60, 30)
                speed, strength = 5, 3                            

            if self.game.selected_player == enums.PL_BLAZE:
                self.srf_menu.blit(self.game.img_blaze, (125, 75))
            else:  # PL_PIPER
                self.srf_menu.blit(self.game.img_piper, (125, 75))
            # stars
            x, y = 30, 120
            fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
            self._shaded_text(fb, ff, 'SPEED', self.srf_menu, x, y, 1)
            self._shaded_text(fb, ff, 'STRENGTH', self.srf_menu, x, y+30, 1)        
            for i in range(speed):
                self.srf_menu.blit(self.img_star, (x+i*18, y+6))
            for i in range(strength):
                self.srf_menu.blit(self.img_star, (x+i*18, y+36))        

            # event management
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:                       
                        return None  # cancel, return to player selection         
                    elif event.key == pygame.K_LEFT:
                        if selected_difficulty == enums.DF_NORMAL:
                            selected_difficulty = enums.DF_EASY
                            self.sfx_menu_click.play()
                        elif selected_difficulty == enums.DF_HARD:
                            selected_difficulty = enums.DF_NORMAL
                            self.sfx_menu_click.play()
                    elif event.key == pygame.K_RIGHT:
                        if selected_difficulty == enums.DF_EASY:
                            selected_difficulty = enums.DF_NORMAL
                            self.sfx_menu_click.play()
                        elif selected_difficulty == enums.DF_NORMAL:
                            selected_difficulty = enums.DF_HARD
                            self.sfx_menu_click.play()
                    elif (event.key == pygame.K_RETURN or 
                        event.key == pygame.K_KP_ENTER or 
                        event.key == pygame.K_SPACE):
                        self.sfx_menu_select.play()
                        confirmed = True                
                # joystick/gamepad
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.sfx_menu_select.play()
                    confirmed = True                
                elif event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:  # horizontal axis
                        if event.value < -0.5: # left
                            if selected_difficulty == enums.DF_NORMAL:
                                selected_difficulty = enums.DF_EASY
                                self.sfx_menu_click.play()
                            elif selected_difficulty == enums.DF_HARD:
                                selected_difficulty = enums.DF_NORMAL
                                self.sfx_menu_click.play()
                        elif event.value > 0.5: # right
                            if selected_difficulty == enums.DF_EASY:
                                selected_difficulty = enums.DF_NORMAL
                                self.sfx_menu_click.play()
                            elif selected_difficulty == enums.DF_NORMAL:
                                selected_difficulty = enums.DF_HARD
                                self.sfx_menu_click.play()
            self.game.update_screen()
        
        return selected_difficulty
        


    def show(self):
        # main theme song
        pygame.mixer.music.load(constants.MUS_PATH + 'mus_menu.ogg')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

        # default wallpaper for the 16:9 screen mode
        if self.game.config.data['screen_mode'] == enums.SM_16_9: # 16:9
            self.game.set_background(-1) # no level number (menu screen)

        # help text (using pre-created fonts)
        marquee_help = MarqueeText(
            self.srf_menu, self._marquee_help_font,
            self.srf_menu.get_height() - 26, .8, constants.HELP, 2000)
        # credit text (using pre-created fonts)
        marquee_credits = MarqueeText(
            self.srf_menu, self._marquee_credits_font,
            self.srf_menu.get_height() - 8, .5, constants.CREDITS, 2100)
    
        # some local variables are initialised
        selected_option = enums.MO_START # option where the cursor is located
        confirmed_option = False # 'True' when a selected menu item is pressed
        menu_page = 0 # page displayed (0 to 5 automatically. 6 = config page)
        page_timer = 0 # number of loops the page remains on screen (up to 500)
        y = -(constants.MENU_UNSCALED_SIZE[1]) # for vertical scrolling of pages
        # refresh the high scores page
        self.page_1()
        # clears the input buffer (keyboard and joystick)
        self.game.clear_input_buffer()

        # ========================= main menu loop =========================        
        while True:
            page_timer += 1

            # draws the background image
            self.srf_menu.blit(self.img_menu, (0,0))

            # ====== transition of menu pages from top to bottom, and back again ======
            if page_timer >= 500: # time exceeded?
                menu_page += 1 # change the page
                if menu_page > 5: menu_page = 0 # back to the main page
                page_timer = 0 # and reset the timer
                y = -(constants.MENU_UNSCALED_SIZE[1]) # again in the upper margin
                selected_option = enums.MO_START
            elif page_timer >= 470: # time almost exceeded?
                y -= 6 # scrolls the page up (is disappearing)
            elif y < 0: # as long as the page does not reach the upper margin
                y += 6 # scrolls the page up (is appearing)           
            # draw one of the 6 menu pages
            self.srf_menu.blit(self.menu_pages[menu_page], (0, y))

            # ====================== keyboard/gamepad management =======================
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # X button in the main window
                    self.game.exit()
                # a key or button has been pressed
                elif (event.type == pygame.KEYDOWN or 
                      event.type == pygame.JOYBUTTONDOWN or 
                      event.type == pygame.JOYAXISMOTION) and y == 0:
                    # active pages
                    if menu_page == 0 or menu_page == 6:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                            if menu_page == 0: self.game.exit() # exits the application completely
                            else: # on page 6, return to page 0
                                menu_page = 0
                                selected_option = enums.MO_START # 1st option
                                break
                        # the selected option is accepted by pressing ENTER or SPACE or any joystick button
                        if (event.type == pygame.KEYDOWN and 
                            (event.key == pygame.K_RETURN or
                            event.key == pygame.K_KP_ENTER or 
                            event.key == pygame.K_SPACE)) \
                            or event.type == pygame.JOYBUTTONDOWN:
                            self.sfx_menu_select.play()
                            confirmed_option = True
                        # Main menu?
                        elif menu_page == 0 and not confirmed_option:                            
                            # the cursor down or joystick down has been pressed
                            if selected_option < enums.MO_EXIT \
                            and ((event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) \
                            or (event.type == pygame.JOYAXISMOTION and event.axis == 1 and event.value > 0.5)):
                                selected_option += 1
                                self.sfx_menu_click.play()
                                page_timer = 0
                            # the cursor up or joystick up has been pressed
                            elif selected_option > enums.MO_START \
                            and ((event.type == pygame.KEYDOWN and event.key == pygame.K_UP) \
                            or (event.type == pygame.JOYAXISMOTION and event.axis == 1 and event.value < -0.5)):
                                selected_option -= 1
                                self.sfx_menu_click.play()
                                page_timer = 0
                        # Settings menu
                        elif menu_page == 6 and not confirmed_option:
                            # the cursor down or joystick down has been pressed
                            if selected_option < enums.MO_EXIT_SETTINGS \
                            and ((event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) \
                            or (event.type == pygame.JOYAXISMOTION and event.axis == 1 and event.value > 0.5)):
                                selected_option += 1
                                self.sfx_menu_click.play()
                                page_timer = 0
                            # the cursor up or joystick up has been pressed
                            elif selected_option > enums.MO_SCREEN_MODE \
                            and ((event.type == pygame.KEYDOWN and event.key == pygame.K_UP) \
                            or (event.type == pygame.JOYAXISMOTION and event.axis == 1 and event.value < -0.5)):
                                selected_option -= 1
                                self.sfx_menu_click.play()
                                page_timer = 0                             
                    # pressing any key on a passive page (info), returns to the main menu
                    else:
                        menu_page = 0
                        page_timer = 0
            
            # =================== management of active pages ===================
            if (menu_page == 0 or menu_page == 6) and y == 0:
                # shows the cursor next to the selected option
                if menu_page == 0:
                    self.srf_menu.blit(self.img_pointer, (66, 66 + (20*selected_option)))
                else: # page 6
                    self.srf_menu.blit(self.img_pointer, (35, -4 + (20*selected_option)))

                # an option was confirmed?
                if confirmed_option:
                    # main menu page
                    if selected_option == enums.MO_START:
                        # player selection
                        selected_player = self.select_player()
                        if selected_player is not None: # not cancelled
                            self.game.selected_player = selected_player
                            # difficulty selection
                            selected_difficulty = self.select_difficulty()
                            if selected_difficulty is not None: # not cancelled
                                self.game.selected_difficulty = selected_difficulty
                                return
                        confirmed_option = False
                        page_timer = 0
                    # config page
                    elif selected_option == enums.MO_SETTINGS:
                        y = -(constants.MENU_UNSCALED_SIZE[1]) # completely off-screen
                        selected_option = enums.MO_SCREEN_MODE # 1st option
                        menu_page = 6
                    elif selected_option == enums.MO_EXIT:
                        self.game.exit()
                    # options menu page
                    elif selected_option == enums.MO_SCREEN_MODE:  # 0 = window, 1 = 4:3, 2 = 16:9
                        if self.game.config.OS == 'Windows':
                            self.game.config.data['screen_mode'] = (self.game.config.data['screen_mode'] + 1) % 3
                    elif selected_option == enums.MO_SCANLINES: # 0 = no, 1 = yes
                        self.game.config.data['scanlines'] = (self.game.config.data['scanlines'] + 1) % 2
                    elif selected_option == enums.MO_CONTROL: # 0 = classic, 1 = gamer, 2 = retro, 3 = joypad
                        self.game.config.data['control'] = (self.game.config.data['control'] + 1) % 4
                        self.game.config.apply_controls() # remap the keyboard
                    elif selected_option == enums.MO_EXIT_SETTINGS:
                        y = -(constants.MENU_UNSCALED_SIZE[1]) # completely off-screen
                        selected_option = enums.MO_START # 1st option
                        menu_page = 0                        

                    # common values for pages 1 and 6
                    confirmed_option = False
                    page_timer = 0

                    if menu_page == 6:
                        # create joystick/joypad/gamepad object (if it exists)
                        self.game.joystick = self.game.config.prepare_joystick()                        
                        # saves and apply possible changes to the configuration
                        self.game.apply_display_settings()
                        self.game.config.save()                       
                        # refresh the page with the new data
                        self.menu_pages[6] = pygame.Surface(constants.MENU_UNSCALED_SIZE)
                        self.menu_pages[6].set_colorkey(constants.PALETTE['BLACK0'])
                        self.page_6()

            # draws the texts of the marquee in their new position
            marquee_help.update()
            marquee_credits.update()  

            self.game.update_screen()
            # next loop...



    ##### auxiliary functions #####

    # draws a text with its shadow
    def _shaded_text(self, font_BG, font_FG, text, surface, x, y, offset):
        font_BG.render(text, surface, (x, y))  # shadow
        font_FG.render(text, surface, (x-offset, y-offset))



    # draws the player's characteristics graphically
    def _draw_player_info(self, x, player, page):
        # player characteristics
        if player == enums.PL_BLAZE:
            rank = 'Sergeant'
            age = '23'
            origin = 'Brighton (England)'
        else:
            rank = 'Corporal'
            age = '20'
            origin = 'Glasgow (Scotland)'
        # headers
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        self._shaded_text(fb, ff, 'RANK', self.menu_pages[page], x, 65, 1)
        self._shaded_text(fb, ff, 'AGE', self.menu_pages[page], x, 95, 1) 
        self._shaded_text(fb, ff, 'ORIGIN', self.menu_pages[page], x, 125, 1)
        # data
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 
                         rank, self.menu_pages[page], x, 75, 1)
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 
                         age, self.menu_pages[page], x, 105, 1)
        self._shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 
                         origin , self.menu_pages[page], x, 135, 1)     



    # draw a box to mark the selected player
    def _draw_selection_box(self, surface, x, y, width, height):
        pygame.draw.rect(surface, constants.PALETTE['WHITE2'], 
                         (x-2, y-2, width+4, height+4), 2, border_radius=10)

