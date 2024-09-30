
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


    # update the data (only if it has been invalidated)
    def update(self, player):
        if self.needs_updating:
            # player data
            self.draw_energy_bar(player.energy)
            self.clear_zone(89)
            self.shaded_text(player.ammo, 91, 6)
            self.shaded_text('\'' + str(constants.MAX_AMMO), 107, 6) # ' = /
            self.clear_zone(147)
            self.shaded_text(self.game.remaining_flags, 149, 6)
            self.clear_zone(183)
            self.shaded_text(self.game.remaining_mines, 185, 6)
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


    # draws the entire scoreboard
    def reset(self, map_number):
        # gets the stage number
        if map_number != 0:
            self.stage_number = (map_number - 1) // 4
        # delete the entire scoreboard
        self.game.srf_sboard.fill(self.back_colour[self.stage_number])
        # draw icons
        self.game.srf_sboard.blit(self.energy_icon, (2, 2))
        self.game.srf_sboard.blit(self.game.hotspot_images[enums.AMMO], (70, 2))
        self.game.srf_sboard.blit(self.game.flag_image, (130, 2))
        self.game.srf_sboard.blit(self.landmine_image, (165, 2))


    # 16-position multi-coloured energy bar
    def draw_energy_bar(self, energy):
        x, y = 20, 7
        bar_units = 15
        bar_unit_width, bar_unit_height = 2, 10
        bar_unit_spacing = 1

        # draw as many units as the player has energy
        for i in range(bar_units):
            # block colours: 4 reds, 4 yellows, the rest green
            colors = [constants.PALETTE['RED1']] * 4 + \
                    [constants.PALETTE['YELLOW1']] * 4 + \
                    [constants.PALETTE['GREEN1']] * 7
            # draws the bar units
            rect_x = x + i * (bar_unit_width + bar_unit_spacing)
            color = colors[i] if i < energy else constants.PALETTE['BLACK0']
            pygame.draw.rect(self.game.srf_sboard, color, 
                             (rect_x, y, bar_unit_width, bar_unit_height))
            
            
    # forces the redrawing of the data
    def invalidate(self):
        self.needs_updating = True


    # clean the previous data
    def clear_zone(self, x):
        pygame.draw.rect(self.game.srf_sboard, self.back_colour[self.stage_number], ((x, 4),(13, 12)))


    # draws a text with its shadow
    def shaded_text(self, data, x, y):       
        self.game.fonts[enums.L_B_BLACK].render(
            str(data).rjust(2, '0'), self.game.srf_sboard, (x, y))  # shadow
        self.game.fonts[enums.L_F_WHITE].render(
            str(data).rjust(2, '0'), self.game.srf_sboard, (x-2, y-2))