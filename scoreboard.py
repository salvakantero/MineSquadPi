
# ==============================================================================
# .::Scoreboard class::.
# Draws the scoreboard and refreshes its data.
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
import constants
import enums


class Scoreboard():
    def __init__(self, game):
        self.srf_sboard = game.srf_sboard
        self.fonts = game.fonts
        self.hi = game.high_scores[0][2]
        self.needs_updating = False # redrawing of the data if True
        # icons
        self.energy_icon = pygame.image.load(
            'images/sprites/player/0/player0.png').convert()
        self.hotspot_images = game.hotspot_images


    # draws the name of the map and other data
    def map_info(self, map_number):
        # print map number
        x = constants.SBOARD_UNSCALED_SIZE[0] - 55
        y = 22
        text_1 = 'SCREEN.....' + str(map_number+1).rjust(2, '0') + '/20'        
        self.fonts[enums.S_B_BROWN].render(text_1, self.srf_sboard, (x+1, y+1)) # shadow
        self.fonts[enums.S_F_BROWN].render(text_1, self.srf_sboard, (x, y))


    # draws a text with its shadow
    def shaded_text(self, data, x, y):       
        self.fonts[enums.L_B_WHITE].render(str(data).rjust(2, '0'), self.srf_sboard, (x, y))  # shadow
        self.fonts[enums.L_F_WHITE].render(str(data).rjust(2, '0'), self.srf_sboard, (x-2, y-2))


    # draws the entire scoreboard
    def reset(self):
        # delete the entire scoreboard
        self.srf_sboard.fill((0,0,0))
        # icons
        self.srf_sboard.blit(self.energy_icon, (0, 2))
        self.srf_sboard.blit(self.hotspot_images[enums.AMMO], (82, 2))
        #self.srf_sboard.blit(self.hotspot_images[enums.XRAY], (145, 2))
        #self.srf_sboard.blit(self.hotspot_images[enums.SHIELD], (186, 2))
        # fixed texts
        self.shaded_text('\'' + str(constants.MAX_AMMO), 116, 6) # ' = /
        self.shaded_text('\'15', 220, 6)


    # forces the redrawing of the data
    def invalidate(self):
        self.needs_updating = True


    # clean the previous data
    def clear_zone(self, x):
        pygame.draw.rect(self.srf_sboard, constants.PALETTE['BLACK0'], ((x, 4),(13, 12)))


    # update the data (only if it has been invalidated)
    def update(self, player):
        if self.needs_updating:
            # player data
            self.clear_zone(18)
            self.shaded_text(player.energy, 20, 6)
            self.clear_zone(100)
            self.shaded_text(player.ammo, 102, 6)
            self.needs_updating = False
                       
            x = 0
            y = 22
            # clears the above content
            pygame.draw.rect(self.srf_sboard, constants.PALETTE['BLACK0'], ((185, y),(54, 15)))
            # show score
            text = 'SCORE: ' + str(player.score).rjust(6, '0')
            self.fonts[enums.S_B_BROWN].render(text, self.srf_sboard, (x+1, y+1)) # shadow
            self.fonts[enums.S_F_BROWN].render(text, self.srf_sboard, (x, y))
            # show high score
            y = 30
            score = self.hi if self.hi > player.score else player.score
            text_2 = 'HIGH: ' + str(score).rjust(6, '0')
            self.fonts[enums.S_B_BROWN].render(text_2, self.srf_sboard, (x+5, y+1)) # shadow
            self.fonts[enums.S_F_BROWN].render(text_2, self.srf_sboard, (x+4, y))
