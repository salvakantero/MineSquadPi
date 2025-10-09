
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
    # class constants
    INITIAL_WAIT = 500
    LOGO_FADE_OPACITY = 45
    LOGO_FADE_DELAY = 12
    INTRO_FADE_DELAY = 60
    PAUSE_DURATION = 1500
    POLL_DELAY = 10

    def __init__(self, game):
        self.game = game
        self.srf_intro = game.srf_menu
        # cache frequently used color
        self._black = constants.PALETTE['BLACK0']
        # PlayOnRetro logo
        self.img_logo = pygame.image.load(constants.ASS_PATH + 'logo.png').convert()
        self.sfx_logo = pygame.mixer.Sound(constants.FX_PATH + 'sfx_logo.wav')
        # MineSquad logo
        self.img_intro = pygame.image.load(constants.ASS_PATH + 'intro.png').convert()
        # auxiliary surface for fading and flashing visual effects
        self.srf_aux = pygame.Surface(constants.MENU_UNSCALED_SIZE, pygame.SRCALPHA)



    def play(self):
        if self._wait_with_skip(self.INITIAL_WAIT): return True

        # PlayOnRetro logo
        # fade in
        self.srf_intro.fill(self._black)
        self.srf_aux.blit(self.img_logo, (0, 0))
        if self._fades_surface(self.srf_intro, self.srf_aux, self.LOGO_FADE_OPACITY, self.LOGO_FADE_DELAY): return True
        self.sfx_logo.play()
        if self._wait_with_skip(self.PAUSE_DURATION): return True
        # fade out
        self.srf_aux.fill(self._black)
        if self._fades_surface(self.srf_intro, self.srf_aux, self.LOGO_FADE_OPACITY, self.LOGO_FADE_DELAY): return True

        # MineSquad logo
        # fade in
        self.srf_intro.fill(self._black)
        self.srf_aux.blit(self.img_intro, (0, 0))
        if self._fades_surface(self.srf_intro, self.srf_aux, self.LOGO_FADE_OPACITY, self.INTRO_FADE_DELAY): return True
        # pause for recreation. Waooouuu!
        if self._wait_with_skip(self.PAUSE_DURATION): return True



    ##### auxiliary functions #####

    def _fades_surface(self, target_surf, aux_surf, opacity, delay):
        aux_surf.set_alpha(0) # totally transparent    
        for z in range(opacity):
            aux_surf.set_alpha(z) # opacity is being applied
            target_surf.blit(aux_surf, (0,0)) # the two surfaces come together to be drawn
            self.game.update_screen() # draw target_surf
            if self._wait_with_skip(delay): return True
        return False



    # wait for a duration while checking for skip keys
    def _wait_with_skip(self, milliseconds):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < milliseconds:
            # check for skip keys
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: return True
                elif event.type == pygame.QUIT: self.game.exit()
            pygame.time.delay(self.POLL_DELAY)  # reduce CPU usage
        return False    