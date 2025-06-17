
# ==============================================================================
# .::Mine Squad Pi::. v1.0
# Initialization and main loop
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
import random

from game import Game
from map import Map
from scoreboard import Scoreboard
from intro import Intro
from menu import Menu
from player import Player
from jukebox import Jukebox


# initialisation
pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

game = Game() # common variables and functions
scoreboard = Scoreboard(game)
map = Map(game)
intro = Intro(game)
menu = Menu(game)
# playlist with the 12 available tracks
jukebox = Jukebox('sounds/music/', 'mus_ingame_', 12)

#intro.play() # shows an intro

# Main loop
while True:
    if game.status == enums.GS_OVER: # game not running (menu)
        menu.show() # displays the main menu   
        # new unordered playlist with the 12 available music tracks
        pygame.mixer.music.stop()
        jukebox.shuffle()
        # create the player
        player = Player(enums.PL_BLAZE, game, map, scoreboard)
        # reset some variables
        map.last = -1
        game.remaining_mines = -1
        game.status = enums.GS_RUNNING
        for hotspot in constants.HOTSPOT_DATA:
            hotspot[3] = True # used hotspots available again
        # current map
        if game.new: # start a new game
            map.number = 0
        else: # load the last checkpoint
            game.checkpoint.load() # loading the file
            #assigns the loaded data to the objects
            d = game.checkpoint.data
            map.number = d['map_number']
    else: # game running
        # event management
        for event in pygame.event.get():
            # exit when click on the X in the window
            if event.type == pygame.QUIT:
                game.exit()
            elif event.type == pygame.KEYDOWN: # a key is pressed
                # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                     # stops the music when the game is paused
                    if game.music_status == enums.MS_UNMUTED:
                        pygame.mixer.music.pause()
                    if game.confirm_exit():
                        game.status = enums.GS_OVER # go to the main menu
                    else:
                        # restores the music if the game continues
                        if game.music_status == enums.MS_UNMUTED:
                            pygame.mixer.music.unpause()                            
                # mutes the music, or vice versa               
                elif event.key == game.config.mute_key:
                    if game.music_status == enums.MS_MUTED:
                        game.music_status = enums.MS_UNMUTED
                        pygame.mixer.music.play()
                    else:
                        game.music_status = enums.MS_MUTED
                        pygame.mixer.music.fadeout(1200)
                # press fire
                elif event.key == game.config.fire_key:
                    player.fire()
                # press beacon
                elif event.key == game.config.beacon_key:
                    player.place_beacon()
            # mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 = left click (fire)
                    player.fire()
                elif event.button == 3:  # 3 = right click (beacon)
                    player.place_beacon()

        # check map completion (12 levels from 0 to 11)
        if game.remaining_mines == 0:
            if map.number < 11:
                # show a random end-of-level message
                title, message = random.choice(constants.END_LEVEL_MESSAGES)
                game.message(title, message, True, False, False, False)
                pygame.mixer.music.stop()
                #game.sfx_game_over.play()
                game.wait_for_key()
                map.number += 1 
            else: game.win()                    
        # change the map if necessary
        if map.number != map.last:
            map.change(player)
            scoreboard.reset(map.number)
            scoreboard.invalidate()
            scoreboard.update(player)
            game.message(map.stage_name1[map.stage], 
                         map.stage_name2[map.stage] + 
                         '. - LEVEL ' + str(map.number+1), True, False, False, True)
            pygame.mixer.music.stop()
            #game.sfx_game_over.play()
            game.wait_for_key()

        # update sprites (player, enemies, hotspots, explosions, etc...)
        game.groups[enums.SG_ALL].update()

        # collision between player and enemies, mines or hotspots      
        game.check_player_collisions(player, scoreboard, map.number, map.map_data)
        # collision between bullets and enemies
        game.check_bullet_collisions(player, scoreboard)

        # game over?
        if player.energy <= 0 or (game.remaining_beacons == 0 and game.remaining_mines > 0):
            if player.energy < 0: player.energy = 0
            if game.loss_sequence == 0: # blast animation completed                           
                game.over()
                game.update_high_score_table(player.score)
                game.status = enums.GS_OVER
                continue
            else: # blast animation in progress
                game.loss_sequence -= 1

        # draws the map free of sprites to clean it up
        game.srf_map.blit(game.srf_map_bk, (0,0))

        # draws the location of the mines
        map.draw_mine_data()
        
        # draws the sprites in their new positions
        game.groups[enums.SG_ALL].draw(game.srf_map)

        # updates the floating text, only if needed (y>0)
        game.floating_text.update()

        # updates the scoreboard, only if needed (needs_updating = True)
        scoreboard.update(player)

        # next track in the playlist if the music has been stopped
        if game.music_status == enums.MS_UNMUTED:
            jukebox.update()

        # TEST ZONE ================================================================================
        game.fonts[enums.S_B_GREEN].render(str(int(game.clock.get_fps())), game.srf_map, (232, 169))
        #game.fonts[enums.S_B_WHITE].render(str(player.state), game.srf_sboard, (100, 25))
        # ==========================================================================================
        
        # increases the loop counter, up to a maximum of 10000 loops
        game.loop_counter = 0 if game.loop_counter == 9999 else game.loop_counter + 1
        game.update_screen()