
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
        self.img_menu = pygame.image.load('images/assets/menu_back.png').convert()
        self.img_blaze = pygame.image.load('images/assets/blaze.png').convert_alpha()
        self.img_piper = pygame.image.load('images/assets/piper.png').convert_alpha()
        self.img_star = pygame.image.load('images/sprites/star.png').convert_alpha()
        self.img_pointer = pygame.image.load('images/sprites/pointer.png').convert_alpha()
        # sounds
        self.sfx_menu_click = pygame.mixer.Sound('sounds/fx/sfx_menu_click.wav')
        self.sfx_menu_select = pygame.mixer.Sound('sounds/fx/sfx_menu_select.wav')

        # page 0: menu options
        # page 1: high scores
        # page 2: Blaze info
        # page 3: Piper info
        # page 4: control info
        # page 5: hotspots info
        # page 6: options
        self.menu_pages = []
        for _ in range(0, 7):
            surface = pygame.Surface(constants.MENU_UNSCALED_SIZE)
            surface.set_colorkey(constants.PALETTE['BLACK0'])
            self.menu_pages.append(surface)   
        self.page_0()
        self.page_1()
        self.page_2()
        self.page_3()
        self.page_4()
        self.page_5()
        

    # draws a text with its shadow
    def shaded_text(self, font_BG, font_FG, text, surface, x, y, offset):
        font_BG.render(text, surface, (x, y))  # shadow
        font_FG.render(text, surface, (x-offset, y-offset))


    # draws the player's characteristics graphically
    def draw_player_info(self, x, player, page):
        # player characteristics
        if player == enums.PL_BLAZE:
            speed = 4
            strength = 4
            age = '23'
            origin = 'Brighton (England)'
        else:
            speed = 5
            strength = 3
            age = '20'
            origin = 'Glasgow (Scotland)'
        # headers
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        self.shaded_text(fb, ff, 'SPEED', self.menu_pages[page], x, 40, 1)
        self.shaded_text(fb, ff, 'STRENGTH', self.menu_pages[page] ,x, 70, 1)
        self.shaded_text(fb, ff, 'AGE', self.menu_pages[page], x, 100, 1) 
        self.shaded_text(fb, ff, 'ORIGIN', self.menu_pages[page], x, 130, 1) 
        # draws the data (using stars)
        for i in range(speed):
            self.menu_pages[page].blit(self.img_star, (x+i*18, 47))
        for i in range(strength):
            self.menu_pages[page].blit(self.img_star, (x+i*18, 77))
        # draws more data (using text)
        self.shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 
                         age, self.menu_pages[page], x, 110, 1)
        self.shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 
                         origin , self.menu_pages[page], x, 140, 1)


    def page_0(self): # main menu options 
        # 16:9 background
        if self.game.config.data['screen_mode'] == enums.SM_X720:
            self.game.set_background(-1) # no level number (menu screen)
            self.game.screen.blit(self.game.img_background, (0,0))  
             
        options = ['Start New Game', 'Continue Game', 'Options', 'Exit']
        x, y = 80, 60
        # draws the options
        for i, option in enumerate(options):
            self.shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 
                             option, self.menu_pages[0], x, y + i*20, 1)            
        self.shaded_text(self.game.fonts[enums.S_B_BROWN], self.game.fonts[enums.S_F_BROWN], 
                        self.tip, self.menu_pages[0], 12, y-55, 1)


    def page_1(self): # high scores
        # header
        x, y = 85, 32
        self.shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN],
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
            self.shaded_text(fb, ff, self.game.high_scores[i][0], self.menu_pages[1], 50, y, 1)
            # dates and scores
            self.shaded_text(fb, ff, self.game.high_scores[i][1] + '    ' + 
                str(self.game.high_scores[i][2]).rjust(6, '0'), self.menu_pages[1], 115, y, 1)
            y += 10


    def page_2(self): # Blaze info        
        self.shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_RED], 
                         'B L A Z E', self.menu_pages[2], 115, 15, 1)
        self.draw_player_info(115, enums.PL_BLAZE, 2)
        self.menu_pages[2].blit(self.img_blaze, (10, 0))


    def page_3(self): # Piper info
        self.shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_RED], 
                         'P I P E R', self.menu_pages[3], 10, 15, 1)
        self.draw_player_info(10, enums.PL_PIPER, 3)
        self.menu_pages[3].blit(self.img_piper, (120, 0))


    def page_4(self): # control info
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        layouts = [ # control index, image pos, description, text pos
            (self.game.control_images[0], (30, 52), 'Classic', (39, 90)),
            (self.game.control_images[1], (95, 52), 'Gamer', (104, 90)),
            (self.game.control_images[2], (160, 52), 'Retro', (170, 90)),
            (self.game.control_images[3], (53, 108), 'Joypad', (70, 146)),
            (self.game.control_images[4], (119, 108), 'Common keys', (131, 146))]
        # header
        self.shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 'Controls', self.menu_pages[4], 90, 27, 1)        
        # images and descriptions
        for image, img_pos, text, text_pos in layouts:
            self.menu_pages[4].blit(image, img_pos)
            self.shaded_text(fb, ff, text, self.menu_pages[4], text_pos[0], text_pos[1], 1)


    def page_5(self): # hotspots
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        hotspots1 = [ # hotspot index, image pos, description, text pos
            (self.game.hotspot_images[enums.HS_LIFE], (40, 60), 'FULL ENERGY', (61, 66)),
            (self.game.hotspot_images[enums.HS_SHIELD], (40, 80), 'INVULNERABLE', (61, 86)),
            (self.game.hotspot_images[enums.HS_AMMO], (40, 100), 'AMMO +10', (61, 106)),
            (self.game.hotspot_images[enums.HS_DISK], (40, 120), 'CHECKPOINT', (61, 126))]
        hotspots2 = [ # hotspot index, image pos, description, text pos
            (self.game.hotspot_images[enums.HS_CANDY], (140, 60), 'CANDY +50', (161, 66)),
            (self.game.hotspot_images[enums.HS_APPLE], (140, 80), 'APPLE +75', (161, 86)),
            (self.game.hotspot_images[enums.HS_CHOCO], (140, 100), 'CHOCOLATE +100', (161, 106)),
            (self.game.hotspot_images[enums.HS_COIN], (140, 120), 'COIN +200', (161, 126))]
        # header
        self.shaded_text(self.game.fonts[enums.L_B_BROWN], self.game.fonts[enums.L_F_BROWN], 'HotSpots', self.menu_pages[5], 95, 27, 1)
        # images and descriptions
        for image, img_pos, text, text_pos in hotspots1:
            self.menu_pages[5].blit(image, img_pos)
            self.shaded_text(fb, ff, text, self.menu_pages[5], text_pos[0], text_pos[1], 1)
        for image, img_pos, text, text_pos in hotspots2:
            self.menu_pages[5].blit(image, img_pos)
            self.shaded_text(fb, ff, text, self.menu_pages[5], text_pos[0], text_pos[1], 1)


    def page_6(self): # options
        # menu options      
        x, y = 60, 60
        fb = self.game.fonts[enums.L_B_BROWN] # brown font for the background
        ff = self.game.fonts[enums.L_F_BROWN] # sand font for the foreground
        fb2 = self.game.fonts[enums.L_B_WHITE] # white font for the background
        ff2 = self.game.fonts[enums.L_F_WHITE] # white font for the foreground

        # screen mode
        if self.game.config.data['screen_mode'] == enums.SM_X600: value = '4:3'
        elif self.game.config.data['screen_mode'] == enums.SM_X720: value = '16:9'
        else: value = 'WINDOW'
        self.shaded_text(fb, ff, 'Screen mode:', self.menu_pages[6], x, y, 1)
        self.shaded_text(fb2, ff2, value, self.menu_pages[6], x+105, y, 1)

        # scanlines filter 
        if self.game.config.data['scanlines']: value = 'ON'
        else: value = 'OFF'
        self.shaded_text(fb, ff, 'Scanlines:', self.menu_pages[6], x, y+20, 1)
        self.shaded_text(fb2, ff2, value, self.menu_pages[6], x+105, y+20, 1)

        # control keys
        if self.game.config.data['control'] == enums.CT_CLASSIC: value = 'CLASSIC' 
        elif self.game.config.data['control'] == enums.CT_GAMER: value = 'GAMER'
        elif self.game.config.data['control'] == enums.CT_RETRO: value = 'RETRO'
        else: value = 'JOYPAD'
        self.shaded_text(fb, ff, 'Control Keys:', self.menu_pages[6], x, y+40, 1)
        self.shaded_text(fb2, ff2, value, self.menu_pages[6], x+105, y+40, 1)

        # exit
        self.shaded_text(fb, ff, 'Exit Options', self.menu_pages[6], x, y+60, 1)
        self.shaded_text(self.game.fonts[enums.S_B_BROWN], self.game.fonts[enums.S_F_BROWN], 
                self.tip, self.menu_pages[6], 12, 5, 1)
        

    def show(self):
        # main theme song
        #pygame.mixer.music.load('sounds/music/mus_menu.ogg')
        #pygame.mixer.music.play()

        # help text
        marquee_help = MarqueeText(
            self.srf_menu, Font('images/fonts/large_font.png', constants.PALETTE['ORANGE2'], True),
            self.srf_menu.get_height() - 26, .8, constants.HELP, 2400)
        # credit text     
        marquee_credits = MarqueeText(
            self.srf_menu, Font('images/fonts/small_font.png', constants.PALETTE['GREEN0'], True),
            self.srf_menu.get_height() - 8, .5, constants.CREDITS, 2100)
    
        # some local variables are initialised
        selected_option = enums.MO_START # option where the cursor is located
        confirmed_option = False # 'True' when a selected menu item is pressed
        menu_page = 0 # page displayed (0 to 5 automatically. 6 = config page)
        page_timer = 0 # number of loops the page remains on screen (up to 500)
        y = -(constants.MENU_UNSCALED_SIZE[1]) # for vertical scrolling of pages

        # empties the buffer of controls
        pygame.event.clear([pygame.KEYDOWN, pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION])

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
                            (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE)) \
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
                        # Options menu
                        elif menu_page == 6 and not confirmed_option:
                            # the cursor down or joystick down has been pressed
                            if selected_option < enums.MO_EXIT_OPTIONS \
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
                    self.srf_menu.blit(self.img_pointer, (56, 56 + (20*selected_option)))
                else: # page 6
                    self.srf_menu.blit(self.img_pointer, (35, -24 + (20*selected_option)))

                # an option was confirmed?
                if confirmed_option:
                    # main menu page
                    if selected_option == enums.MO_START:
                        self.game.new = True
                        return                        
                    elif selected_option == enums.MO_LOAD:
                        self.game.new = False
                        return
                    # config page
                    elif selected_option == enums.MO_OPTIONS:
                        y = -(constants.MENU_UNSCALED_SIZE[1]) # completely off-screen
                        selected_option = enums.MO_SCREEN_MODE # 1st option
                        menu_page = 6
                    elif selected_option == enums.MO_EXIT:
                        self.game.exit()

                    # options menu page
                    elif selected_option == enums.MO_SCREEN_MODE:  # 0 = window, 1 = 4:3, 2 = 16:9
                        self.game.config.data['screen_mode'] = (self.game.config.data['screen_mode'] + 1) % 3
                    elif selected_option == enums.MO_SCANLINES: # 0 = no, 1 = yes
                        self.game.config.data['scanlines'] = (self.game.config.data['scanlines'] + 1) % 2
                    elif selected_option == enums.MO_CONTROL: # 0 = classic, 1 = gamer, 2 = retro, 3 = joypad
                        self.game.config.data['control'] = (self.game.config.data['control'] + 1) % 4
                        self.game.config.apply_controls() # remap the keyboard
                    elif selected_option == enums.MO_EXIT_OPTIONS:
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
