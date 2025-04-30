
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
#game.show_intro()

# Main loop
while True:
    if game.status == enums.GS_OVER: # game not running
        # default wallpaper for the 16:9 screen mode
        if game.config.data['screen_mode'] == enums.SM_X720: # 16:9
            game.set_background(-1)
            game.screen.blit(game.img_background, (0,0))
        # creates and displays the initial menu
        game.show_menu()         
        # new unordered playlist with the 12 available music tracks
        pygame.mixer.music.stop()
        game.jukebox.shuffle()
        # create the player
        player = Player(enums.PL_BLAZE, game, map, scoreboard)
        # reset variables
        map.last = -1 # map before the current map
        game.status = enums.GS_RUNNING
        game.loop_counter = 0
        game.floating_text.y = 0
        game.win_sequence = 0
        game.loss_sequence = 0
        for hotspot in constants.HOTSPOT_DATA:
            hotspot[3] = True # all visible hotspots
        # current map
        if game.new: # start a new game
            map.number = 0
        else: # load the last checkpoint
            game.checkpoint.load() # loading the file
            #assigns the loaded data to the objects
            d = game.checkpoint.data
            map.number = d['map_number']
        game.remaining_mines = constants.NUM_MINES[map.number]
        game.remaining_beacons = constants.NUM_BEACONS[map.number]
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
                # press fire or left mouse button
                elif event.key == game.config.fire_key or pygame.mouse.get_pressed()[0]:
                    player.fire()
                # press beacon or right mouse button
                elif event.key == game.config.beacon_key or pygame.mouse.get_pressed()[2]:
                    player.place_beacon()
        
        # change the map if necessary
        if map.number != map.last:
            map.change(player, scoreboard)
            scoreboard.update(player)
            game.message(map.stage_name1[map.number], 
                         map.stage_name2[map.number] + 
                         '. - LEVEL ' + str(map.number+1), True, False, True)
            pygame.mixer.music.stop()
            game.sfx_game_over.play()
            # wait for a key
            pygame.event.clear(pygame.KEYDOWN)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN: break
                else: continue
                break

        # our player wins the game
        if game.win_sequence > 0:
            game.win(player.score)         
            player.score += 15 # 350x15 = +5250 points
            scoreboard.invalidate()

        # update sprites (player, enemies, hotspots, explosions, etc...)
        game.groups[enums.SG_ALL].update()

        # collision between player and enemies, mines or hotspots      
        game.check_player_collisions(player, scoreboard, map.number, map.map_data)
        # collision between bullets and enemies
        game.check_bullet_collisions(player, scoreboard)

        # game over?
        if player.energy <= 0:
            player.energy = 0
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
            game.jukebox.update()
            
        # check map change using player's coordinates
        # if the player leaves, the map number changes
        #map.check_change(player)

        # TEST ZONE ================================================================================
        game.fonts[enums.S_B_GREEN].render(str(int(game.clock.get_fps())), game.srf_map, (233, 169))
        #game.fonts[enums.S_B_WHITE].render(str(player.state), game.srf_sboard, (100, 25))
        # ==========================================================================================
        
        # increases the loop counter, up to a maximum of 10000 loops
        game.loop_counter = 0 if game.loop_counter == 9999 else game.loop_counter + 1
        game.update_screen()