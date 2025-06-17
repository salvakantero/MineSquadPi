
# ==============================================================================
# .::Intro class::.
# An animation with graphics and sound as an introduction to the game
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


class Intro():
    def __init__(self, game):
        self.game = game
        self.srf_intro = game.srf_menu
        # images
        self.img_logo = pygame.image.load('images/assets/logo.png').convert() # PlayOnRetro logo  
        self.img_intro = pygame.image.load('images/assets/intro.png').convert() # background
        # sounds
        self.sfx_logo = pygame.mixer.Sound('sounds/fx/sfx_logo.wav') # PlayOnRetro logo sfx
        # auxiliary surface for fading and flashing visual effects
        self.srf_aux = pygame.Surface(constants.MENU_UNSCALED_SIZE, pygame.SRCALPHA)


    def fades_surface(self, target_surf, aux_surf, opacity, delay):
        aux_surf.set_alpha(0) # totally transparent    
        for z in range(opacity):
            aux_surf.set_alpha(z) # opacity is being applied
            target_surf.blit(aux_surf, (0,0)) # the two surfaces come together to be drawn
            self.game.update_screen() # draw target_surf
            if self.wait_with_skip(delay): return True
        return False


    # wait for a duration while checking for skip keys
    def wait_with_skip(self, milliseconds):        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < milliseconds:
            # check for skip keys
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: return True
                elif event.type == pygame.QUIT: self.game.exit()
            pygame.time.delay(10)  # reduce CPU usage
        return False


    def play(self):
        if self.wait_with_skip(500): return True

        # PlayOnRetro logo
        # fade in
        self.srf_intro.fill(constants.PALETTE['BLACK0']) # black background
        self.srf_aux.blit(self.img_logo, (0, 0))
        if self.fades_surface(self.srf_intro, self.srf_aux, 45, 12): return True
        self.sfx_logo.play()
        if self.wait_with_skip(1500): return True
        # fade out
        self.srf_aux.fill(constants.PALETTE['BLACK0']) # black background
        if self.fades_surface(self.srf_intro, self.srf_aux, 45, 12): return True

        # MineSquad logo
        # fade in
        self.srf_intro.fill(constants.PALETTE['BLACK0'])
        self.srf_aux.blit(self.img_intro, (0, 0))
        if self.fades_surface(self.srf_intro, self.srf_aux, 45, 60): return True
        # pause for recreation. Waooouuu!
        if self.wait_with_skip(1500): return True

