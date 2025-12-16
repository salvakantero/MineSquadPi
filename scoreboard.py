
# ==============================================================================
# .::Scoreboard class::.
# Draws the scoreboard and refreshes its data.
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



class Scoreboard():
    def __init__(self, game):
        self.game = game
        self.needs_updating = False # redrawing of the data if True
        # icons
        self.landmine_image = pygame.image.load(constants.SPR_PATH + 'landmine.png').convert_alpha()
        self.player0_image = pygame.image.load(constants.SPR_PATH + 'player/0/player12.png').convert_alpha()
        self.player1_image = pygame.image.load(constants.SPR_PATH + 'player/1/player12.png').convert_alpha()
        # background dark colour for each level: red, blue, green
        self.back_colour = ((100,10,10), (10,10,120), (10,100,10))
        self.stage_number = 0
        # pre-create energy bar colors (avoid recreation in loop)
        self._energy_bar_colors = (
            [constants.PALETTE['RED1']] * 4 +
            [constants.PALETTE['YELLOW1']] * 4 +
            [constants.PALETTE['GREEN1']] * 6
        )



    # update the data (only if it has been invalidated)
    def update(self, player):
        if self.needs_updating:
            # player data
            self._draw_energy_bar(player)
            self._clear_zone(88, 15)
            self._shaded_text(player.ammo, 90, 6)
            self._shaded_text('\'' + str(constants.MAX_AMMO), 105, 6) # ' = /
            self._clear_zone(147, 15)
            self._shaded_text(self.game.remaining_beacons, 149, 6)
            self._clear_zone(183, 15)
            self._shaded_text(self.game.remaining_mines, 185, 6)
            self.needs_updating = False

            x = 204
            y = 3
            self._clear_zone(x, 34)
            # show score
            text = f"SC:{self.game.score:06d}"
            self.game.fonts[enums.S_B_BROWN].render(text, self.game.srf_sboard, (x+1, y+1)) # shadow
            self.game.fonts[enums.S_F_BROWN].render(text, self.game.srf_sboard, (x, y))
            # show high score
            y = 11
            hi = self.game.high_scores[0][2]
            score = hi if hi > self.game.score else self.game.score
            text = f"HI:{score:06d}"
            self.game.fonts[enums.S_B_BROWN].render(text, self.game.srf_sboard, (x+1, y+1)) # shadow
            self.game.fonts[enums.S_F_BROWN].render(text, self.game.srf_sboard, (x, y))



    # draws the entire scoreboard
    def reset(self, map_number):
        # gets the stage number
        if map_number != 0:
            self.stage_number = map_number // 3
        # delete the entire scoreboard
        self.game.srf_sboard.fill(self.back_colour[self.stage_number])
        # draw icons
        self.game.srf_sboard.blit(self.game.hotspot_images[enums.HS_AMMO], (70, 2))
        self.game.srf_sboard.blit(self.game.beacon_image, (130, 3))
        self.game.srf_sboard.blit(self.landmine_image, (165, 2))
        energy_icon = self.player0_image if self.game.selected_player == enums.PL_BLAZE else self.player1_image
        self.game.srf_sboard.blit(energy_icon, (2, 2))



    # forces the redrawing of the data
    def invalidate(self):
        self.needs_updating = True



    ##### auxiliary functions #####

    # 14-position multi-coloured energy bar
    def _draw_energy_bar(self, player):
        x, y = 20, 7
        bar_unit_width, bar_unit_height = 2, 10
        bar_unit_spacing = 1

        # draw as many units as the player has energy
        for i in range(player.max_energy):
            # draws the bar units using pre-created color array
            rect_x = x + i * (bar_unit_width + bar_unit_spacing)
            color = self._energy_bar_colors[i] if i < player.energy else constants.PALETTE['BLACK0']
            pygame.draw.rect(self.game.srf_sboard, color,
                             (rect_x, y, bar_unit_width, bar_unit_height))
            


    # clean the previous data
    def _clear_zone(self, x, width):
        pygame.draw.rect(self.game.srf_sboard, self.back_colour[self.stage_number], ((x, 3),(width, 15)))



    # draws a text with its shadow
    def _shaded_text(self, data, x, y):
        text = str(data).rjust(2, '0')
        self.game.fonts[enums.L_B_BLACK].render(text, self.game.srf_sboard, (x, y))  # shadow
        self.game.fonts[enums.L_F_WHITE].render(text, self.game.srf_sboard, (x-2, y-2))
