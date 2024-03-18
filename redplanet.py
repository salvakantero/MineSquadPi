
# ==============================================================================
# .::Red Planet Pi::. v1.0
# Initialization and main loop
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

import constants
import enums

from game import Game
from map import Map
from scoreboard import Scoreboard
from player import Player


# initialisation
pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

# creates the Game object, container for common variables and functions
game = Game()
# creates the Scoreboard object
scoreboard = Scoreboard(game)
# creates the Map object
map = Map(game)

# shows an intro
game.show_intro()

# Main loop
while True:
    if game.status == enums.OVER: # game not running
        # creates and displays the initial menu
        game.show_menu()         
        # new unordered playlist with the 12 available music tracks
        pygame.mixer.music.stop()
        game.jukebox.shuffle()
        # create the player
        player = Player(game, map, scoreboard)
        # reset variables
        map.last = -1 # map before the current map
        map.scroll = enums.RIGHT
        game.status = enums.RUNNING
        game.floating_text.y = 0
        game.win_secuence = 0
        if game.new:
            for hotspot in constants.HOTSPOT_DATA: hotspot[3] = True # all visible hotspots
            for gate in constants.GATE_DATA.values(): gate[2] = True # all visible doors                        
            map.number = 0 # current map
            scoreboard.game_percent = 0 # percentage of completed gameplay
        else: # load the last checkpoint
            game.checkpoint.load() # loading the file
            #assigns the loaded data to the objects
            d = game.checkpoint.data
            map.number = d['map_number']
            scoreboard.game_percent = d['game_percent']
            player.lives = d['player_lives']
            player.ammo = d['player_ammo']
            player.keys = d['player_keys']
            player.TNT = d['player_TNT']
            player.oxygen = d['player_oxygen']
            player.stacked_TNT = d['player_stacked_TNT']
            player.facing_right = d['player_facing_right']
            player.rect = d['player_rect']
            player.score = d['player_score']
            constants.HOTSPOT_DATA = d['hotspot_data']
            constants.GATE_DATA = d['gate_data']
            player.invincible = True
            player.invincible_time_from = pygame.time.get_ticks()
    else: # game running
        # event management
        for event in pygame.event.get():
            # exit when click on the X in the window
            if event.type == pygame.QUIT:
                game.exit()
            if event.type == pygame.KEYDOWN: # a key is pressed
                # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                     # stops the music when the game is paused
                    if game.music_status == enums.UNMUTED:
                        pygame.mixer.music.pause()
                    if game.confirm_exit():
                        game.status = enums.OVER # go to the main menu
                    else:
                        # restores the music if the game continues
                        if game.music_status == enums.UNMUTED:
                            pygame.mixer.music.unpause()                            
                # mutes the music, or vice versa
                if event.key == game.config.mute_key :
                    game.music_status = enums.UNMUTED if game.music_status == enums.MUTED else enums.MUTED
                    pygame.mixer.music.play() if game.music_status == enums.UNMUTED else pygame.mixer.music.fadeout(1200)
                    
        # change the map if necessary
        if map.number != map.last:
            map.change(player, scoreboard)

        # everything blows up and our player wins the game
        if game.win_secuence > 0:
            game.win(player.score)         
            player.score += 15 # 350x15 = +5250 points
            scoreboard.invalidate()

        # update sprites (player, enemies, hotspots, explosions, etc...)
        game.groups[enums.ALL].update()

        # collision between player and mobile platform, martians, hotspot and gates        
        game.check_player_collisions(player, scoreboard, map.number)
        # collision between bullets and martians or map tiles
        game.check_bullet_collisions(player, scoreboard, map.tilemap_rect_list)

        # game over?
        if player.lives == 0 or player.oxygen < 0:           
            game.over()
            game.update_high_score_table(player.score)
            game.status = enums.OVER
            continue
        
        # change the frame of the animated tiles
        map.animate_tiles()

        # draws the map free of sprites to clean it up
        game.srf_map.blit(game.srf_map_bk, (0,0))
        
        # draws the sprites in their new positions
        game.groups[enums.ALL].draw(game.srf_map)

        # updates the floating text, only if needed (y>0)
        game.floating_text.update()

        # updates the scoreboard, only if needed (needs_updating = True)
        scoreboard.update(player)

        # next track in the playlist if the music has been stopped
        if game.music_status == enums.UNMUTED:
            game.jukebox.update()
            
        # check map change using player's coordinates
        # if the player leaves, the map number changes
        map.check_change(player)

        # TEST ZONE ================================================================================
        #game.fonts[enums.S_F_WHITE].render(str(int(game.clock.get_fps())), game.srf_map, (228, 154))
        # ==========================================================================================

        game.update_screen()
