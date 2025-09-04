
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
from camera import Camera
from map import Map
from scoreboard import Scoreboard
from intro import Intro
from menu import Menu
from player import Player
from jukebox import Jukebox

# cache constants for better performance
MAX_LEVEL = 8
LOSS_SEQUENCE_DURATION = 70


# initialisation
pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

game = Game()
camera = Camera()
scoreboard = Scoreboard(game)
map = Map(game)
intro = Intro(game)
menu = Menu(game)
# playlist with the X available tracks
jukebox = Jukebox(constants.MUS_PATH, 'mus_ingame_', 10)

intro.play() # display the intro sequence

# Main loop
while True:
    if game.status == enums.GS_OVER: # game not running (menu)
        menu.show() # display the main menu   
        # create new unordered playlist with the 12 available music tracks
        pygame.mixer.music.stop()
        jukebox.shuffle()
        # create the player
        player = Player(game, map, scoreboard)
        # reset some variables
        map.last = -1
        game.remaining_mines = -1
        game.status = enums.GS_RUNNING
        map.number = 0
    else: # game running
        # event management
        for event in pygame.event.get():
            # exit when clicking the X button on the window
            if event.type == pygame.QUIT:
                game.exit()
            elif event.type == pygame.KEYDOWN: # a key has been pressed
                # exit by pressing the ESC key
                if event.key == pygame.K_ESCAPE:
                     # stop the music when the game is paused
                    if game.music_status == enums.MS_UNMUTED:
                        pygame.mixer.music.pause()
                    if game.confirm_exit():
                        game.status = enums.GS_OVER # return to the main menu
                    else:
                        # restore the music if the game continues
                        if game.music_status == enums.MS_UNMUTED:
                            pygame.mixer.music.unpause()                            
                # mute the music, or vice versa               
                elif event.key == game.config.mute_key:
                    if game.music_status == enums.MS_MUTED:
                        game.music_status = enums.MS_UNMUTED
                        pygame.mixer.music.play()
                    else:
                        game.music_status = enums.MS_MUTED
                        pygame.mixer.music.fadeout(1200)
                # handle fire and beacon keys
                elif event.key == game.config.fire_key:
                    player.fire()
                elif event.key in (game.config.beacon_key, game.config.beacon_key2):
                    player.place_beacon()
            # mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 = left click (fire)
                    player.fire()
                elif event.button == 3:  # 3 = right click (beacon)
                    player.place_beacon()
                                       
        # change the map if necessary
        if map.number != map.last:
            map.change(player)
            map.draw(camera) # draw the new map
            scoreboard.reset(map.number)
            scoreboard.invalidate()
            scoreboard.update(player)
            game.message(map.stage_name1[map.stage], 
                         map.stage_name2[map.stage] + 
                         '. - LEVEL ' + str(map.number+1), True, False, False, True)
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(constants.MUS_PATH + 'mus_new_level.ogg')
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
            game.wait_for_key()
            pygame.mixer.music.stop()

        ##########
        # UPDATE #
        ##########
        player.update() # update the player position and state   
        camera.update(player.x, player.y) # update camera position based on player    
        
        # cache frequently accessed objects for better performance
        sprite_groups = game.sprite_groups  # cache reference
        enemies = sprite_groups[enums.SG_ENEMIES]
        hotspots = sprite_groups[enums.SG_HOTSPOT]
        shots = sprite_groups[enums.SG_SHOT]
        blasts = sprite_groups[enums.SG_BLASTS]
        map_surface = game.srf_map
        
        # enemies, hotspots, blasts, shots
        for enemy in enemies: enemy.update()
        for hotspot in hotspots: hotspot.update(camera)
        for shot in shots: shot.update(camera)
        blasts.update() # use native pygame group update (no parameters needed)
        game.floating_text.update(camera)
        # update explosion pool to recycle finished explosions
        game.explosion_pool.update()

        ########
        # DRAW #
        ########       
        map.draw(camera) # visible map area, free of sprites and marks (15x11 tiles)        
        map.draw_mine_data(camera, player) # draw the location of the mines                     
        player.draw(camera) # draw the player
        # enemies, hotspots, blasts, shots
        for enemy in enemies: enemy.draw(map_surface, camera)
        for hotspot in hotspots: hotspot.draw(map_surface, camera)
        for shot in shots: shot.draw(map_surface, camera)
        for blast in blasts: blast.draw(map_surface, camera)
        game.floating_text.draw(camera)

        # collision between player and enemies, mines or hotspots      
        game.check_player_collisions(player, scoreboard, map.number, map.map_data)
        # collision between bullets and enemies
        game.check_bullet_collisions(player, scoreboard)        
        
        # regenerate the hotspot to score (if needed)
        game.regenerate_hotspot(map.map_data['tile_types'])

        # update the scoreboard (if needed, needs_updating = True)
        scoreboard.update(player)

        # next track in the playlist if the music has been stopped
        if game.music_status == enums.MS_UNMUTED:
            jukebox.update()

        # check map completion (9 levels from 0 to 8)
        if game.remaining_mines == 0:
            if map.number < MAX_LEVEL:
                game.update_screen()
                # show a random end-of-level message
                title, message = random.choice(constants.END_LEVEL_MESSAGES)
                game.message(title, message, True, False, False, False)
                pygame.mixer.music.load(constants.MUS_PATH + 'mus_new_level.ogg')
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                game.wait_for_key()
                map.number += 1 
            else: game.win()

        # game over?
        if player.energy <= 0 or (game.remaining_beacons == 0 and game.remaining_mines > 0):
            if player.energy < 0: 
                player.energy = 0
            if game.loss_sequence == 0: # blast animation completed                           
                game.over()
                game.update_high_score_table(game.score)
                game.status = enums.GS_OVER
                continue
            # blast animation in progress
            game.loss_sequence -= 1

        # TEST ZONE ================================================================================
        game.fonts[enums.S_B_GREEN].render(str(int(game.clock.get_fps())), game.srf_map, (228, 169))
        #game.fonts[enums.S_B_WHITE].render(str(player.state), game.srf_sboard, (100, 25))
        # ==========================================================================================
        
        # increment the loop counter, up to a maximum of 10000 loops
        game.loop_counter = 0 if game.loop_counter == 9999 else game.loop_counter + 1
        game.update_screen()