
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
        self.game = game
        self.needs_updating = False # redrawing of the data if True
        # icons
        self.energy_icon = pygame.image.load('images/sprites/player/0/player0.png').convert_alpha()
        self.landmine_image = pygame.image.load('images/sprites/landmine.png').convert_alpha()
        # dark colour for each level: red, blue, green, gray
        self.back_colour = ((100,10,10), (10,10,100), (10,100,10), (100,100,100))
        self.stage_number = 0

    # draws a text with its shadow
    def shaded_text(self, data, x, y):       
        self.game.fonts[enums.L_B_BLACK].render(
            str(data).rjust(2, '0'), self.game.srf_sboard, (x, y))  # shadow
        self.game.fonts[enums.L_F_WHITE].render(
            str(data).rjust(2, '0'), self.game.srf_sboard, (x-2, y-2))


    # draws the entire scoreboard
    def reset(self, map_number):
        # gets the stage number
        if map_number > 11: self.stage_number = 3
        elif map_number > 7: self.stage_number = 2
        elif map_number > 3: self.stage_number = 1 
        # delete the entire scoreboard
        self.game.srf_sboard.fill(self.back_colour[self.stage_number])
        # draw icons
        self.game.srf_sboard.blit(self.energy_icon, (0, 2))
        self.game.srf_sboard.blit(self.game.hotspot_images[enums.AMMO], (70, 2))
        self.game.srf_sboard.blit(self.game.flag_image, (130, 2))
        self.game.srf_sboard.blit(self.landmine_image, (165, 2))


    # forces the redrawing of the data
    def invalidate(self):
        self.needs_updating = True


    # clean the previous data
    def clear_zone(self, x):
        pygame.draw.rect(self.game.srf_sboard, self.back_colour[self.stage_number], ((x, 4),(13, 12)))


    # update the data (only if it has been invalidated)
    def update(self, player):
        if self.needs_updating:
            # player data
            self.clear_zone(18)
            self.shaded_text(player.energy, 20, 6)
            self.clear_zone(88)
            self.shaded_text(player.ammo, 90, 6)
            self.shaded_text('\'' + str(constants.MAX_AMMO), 106, 6) # ' = /
            self.clear_zone(146)
            self.shaded_text(self.game.remaining_flags, 148, 6)
            self.clear_zone(182)
            self.shaded_text(self.game.remaining_mines, 184, 6)
            self.needs_updating = False
                       
            x = 204
            y = 3
            # show score
            text = 'SC:' + str(player.score).rjust(6, '0')
            self.game.fonts[enums.S_B_BROWN].render(
                text, self.game.srf_sboard, (x+1, y+1)) # shadow
            self.game.fonts[enums.S_F_BROWN].render(
                text, self.game.srf_sboard, (x, y))
            # show high score
            y = 11
            hi = self.game.high_scores[0][2]
            score = hi if hi > player.score else player.score
            text_2 = 'HI:' + str(score).rjust(6, '0')
            self.game.fonts[enums.S_B_BROWN].render(
                text_2, self.game.srf_sboard, (x+1, y+1)) # shadow
            self.game.fonts[enums.S_F_BROWN].render(
                text_2, self.game.srf_sboard, (x, y))