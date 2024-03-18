
# ==============================================================================
# .::Map class::.
# Everything related to the drawing of the tile map.
# This game uses levels made with the "Tiled" program.
# Each screen is a JSON file exported from "Tiled".
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
import json
import os
import random
import constants
import enums

from hotspot import Hotspot
from gate import Gate
from enemy import Enemy


class Map():
    def __init__(self, game):
        self.game = game
        self.number = 0 # current map
        self.scroll = 0 # scroll direction for map_transition()
        self.last = -1 # last map loaded
        self.tilemap_rect_list = [] # list of tile rects (except for transparent ones)
        self.tilemap_behaviour_list = [] # list of tile behaviours (obstacle, platform, etc.)
        self.anim_tiles_list = [] # (frame_1, frame_2, x, y, num_frame)
        self.map_data = {}
        # to generate the pile of explosives
        self.img_TNT = game.hotspot_images[enums.TNT]


    # loads a map and draws it on screen
    def load(self):
        self.map_data = self.process_map('maps/map{}.json'.format(self.number))
        self.draw_map() # draws the tile map on the screen


    # dump the tiled file into mapdata
    def process_map(self, map_file):
        # reads the entire contents of the json
        with open(map_file) as json_data:
            data_readed = json.load(json_data)
        # gets the map dimensions
        data = {'width': data_readed['width'], 'height': data_readed['height']}
        # gets a list of all tiles
        raw_data = data_readed['layers'][0]['data']
        data['data'] = []
        # divides the list into tile lines, according to the map dimensions
        for x in range(0, data['height']):
            st = x * data['width']
            data['data'].append(raw_data[st: st + data['width']])
        # gets the name of the tile file
        tileset = data_readed['tilesets'][0]['source'].replace('.tsx','.json')
        # gets the data from the tile file
        with open('maps/' + tileset) as json_data:
            t = json.load(json_data)
        # removes the path to each image from the tile file
        data['tiles'] = t['tiles']
        for tile in range(0, len(data['tiles'])):
            path = data['tiles'][tile]['image']
            data['tiles'][tile]['image'] = os.path.basename(path)
            data['tiles'][tile]['id'] = data['tiles'][tile]['id'] + 1
        return data


    # extracts the tile number from the filename
    def get_tile_number(self, tile_name):
        tile_name = tile_name.replace('.png', '')
        tile_name = tile_name.replace('T', '')
        return int(tile_name)
  

    # get a value from a dictionary
    def find_data(self, lst, key, value):
        matches = [d for d in lst if d[key] == value]
        return matches[0] if matches else None


    # draws the tile map on the screen
    def draw_map(self):
        self.tilemap_rect_list.clear()
        self.tilemap_behaviour_list.clear()
        self.anim_tiles_list.clear()
        # scroll through the map data
        for y in range(0, self.map_data['height']):
            for x in range(0, self.map_data['width']):
                # gets the tile number from the list
                t = self.find_data(self.map_data['tiles'], 'id', self.map_data['data'][y][x])
                # draws the selected tile
                tile = pygame.image.load('images/tiles/' + t['image']).convert()
                tileRect = tile.get_rect()
                tileRect.topleft = (x * t['imagewidth'], y * t['imageheight'])   
                self.game.srf_map.blit(tile, tileRect)

                # generates the list of rects and behaviour of the current map
                # from T16.png to T35.png: blocking tiles (OBSTABLE)
                # T40.png: platform tile (PLATFORM)
                # from T70.png to T75.png: tiles that kill (KILLER)
                tn = self.get_tile_number(t['image'])            
                behaviour = enums.NO_ACTION
                if tn >= 16 and tn <= 35:   behaviour = enums.OBSTACLE
                elif tn == 40:              behaviour = enums.PLATFORM_TILE
                elif tn >= 70 and tn <= 75: behaviour = enums.KILLER
                # is only added to the list if there is an active behaviour
                if behaviour != enums.NO_ACTION:
                    self.tilemap_rect_list.append(tileRect)
                    self.tilemap_behaviour_list.append(behaviour)

                # generates the list of animated tiles of the current map
                # (frame_1, frame_2, x, y, num_frame)
                if t['image'] in constants.ANIM_TILES.keys():                
                    self.anim_tiles_list.append(
                        [tile, pygame.image.load('images/tiles/' 
                        + constants.ANIM_TILES[t['image']]).convert(), 
                        tileRect.topleft[0], tileRect.topleft[1], 0])


    # select some of the animated tiles on the current map to change the frame
    # and apply to the surface. 
    # anim_tiles_list = (frame_1, frame_2, x, y, num_frame)
    def animate_tiles(self):
        for anim_tile in self.anim_tiles_list: # for each animated tile on the map
            if random.randint(0,24) == 0: # 4% chance of changing frame
                tile = anim_tile[0+anim_tile[4]] # select image according to frame number
                tileRect = tile.get_rect()
                tileRect.topleft = (anim_tile[2], anim_tile[3]) # sets the xy position
                self.game.srf_map_bk.blit(tile, tileRect) # draws on the background image
                # update frame number (0,1)
                anim_tile[4] = (anim_tile[4] + 1) % 2


    # checks if the map needs to be changed (depending on the player's XY position)
    def check_change(self, player):
        # player disappears on the left
        # appearing from the right on the new map
        if player.rect.x < -(constants.TILE_SIZE-8):
            self.number -= 1
            self.scroll = enums.LEFT
            player.rect.right = constants.MAP_UNSCALED_SIZE[0]
        # player disappears on the right
        # appearing from the left on the new map
        elif player.rect.x > constants.MAP_UNSCALED_SIZE[0] - 8:
            self.number += 1
            self.scroll = enums.RIGHT
            player.rect.left = 0
        # player disappears over the top
        # appearing at the bottom of the new map 
        # and jumps again to facilitate the return
        elif player.rect.y < (-constants.TILE_SIZE):
            self.number -= 5
            self.scroll = enums.UP
            player.rect.bottom = constants.MAP_UNSCALED_SIZE[1]            
            player.direction.y = constants.JUMP_VALUE
        # player disappears from underneath
        #appearing at the top of the new map
        elif player.rect.y > constants.MAP_UNSCALED_SIZE[1]:
            self.number += 5
            self.scroll = enums.DOWN
            player.rect.top = 0


    # does everything necessary to change the map and add enemies and hotspots.
    def change(self, player, scoreboard):
        # sets the new map as the current one
        self.last = self.number
        # load the new map
        self.load()
        # preserves the previous map to make the transition
        if self.game.config.data['map_transition']:
            self.game.srf_map_bk_prev.blit(self.game.srf_map_bk, (0,0))
        # save the new background (empty of sprites)
        self.game.srf_map_bk.blit(self.game.srf_map, (0,0))
        # add the TNT pile if necessary to the background
        if self.number == 44 and player.stacked_TNT:
            self.add_TNT_pile()
        # performs the screen transition
        if self.game.config.data['map_transition']:
            self.transition()
        # refresh the scoreboard area
        scoreboard.reset()
        scoreboard.map_info(self.number)
        scoreboard.map_info_timer = 150 # shows the map info for a few seconds
        scoreboard.invalidate()      
        # reset the sprite groups  
        for group in self.game.groups: group.empty()
        # removes any possible floating text
        self.game.floating_text.y = 0
        # add the player  
        self.game.groups[enums.ALL].add(player)

        # add the hotspot (if available)
        hotspot = constants.HOTSPOT_DATA[self.number]
        if hotspot[3] == True: # visible/available?           
            hotspot_sprite = Hotspot(hotspot, self.game.hotspot_images[hotspot[0]])
            self.game.groups[enums.ALL].add(hotspot_sprite) # to update/draw it
            self.game.groups[enums.HOTSPOT].add(hotspot_sprite) # to check for collisions

        # add a checkpoint at the empty position of the keys
        elif hotspot[0] == enums.KEY:
            if self.game.new: 
                hotspot[0] = enums.CHECKPOINT
                hotspot_sprite = Hotspot(hotspot, self.game.hotspot_images[enums.CHECKPOINT])
                self.game.groups[enums.ALL].add(hotspot_sprite) # to update/draw it
                self.game.groups[enums.HOTSPOT].add(hotspot_sprite) # to check for collisions
                constants.HOTSPOT_DATA[self.number][0] = enums.KEY # restores its original type
            else: # does not re-display the checkpoint just loaded
                self.game.new = True

        # sometimes adds an extra score at the empty position of the TNT
        elif hotspot[0] == enums.TNT:            
            hotspot[0] = random.randint(5,9) # 5 = Burger, 6 = Cake, 7 = Donut, 8-9 = None
            if hotspot[0] < 8:
                hotspot_sprite = Hotspot(hotspot, self.game.hotspot_images[hotspot[0]])
                self.game.groups[enums.ALL].add(hotspot_sprite) # to update/draw it
                self.game.groups[enums.HOTSPOT].add(hotspot_sprite) # to check for collisions
            constants.HOTSPOT_DATA[self.number][0] = enums.TNT # restores its original type

        # add the gate (if there is one visible on the map)
        gate = constants.GATE_DATA.get(self.number)
        if gate != None and gate[2] == True: # visible/available?
            gate_sprite = Gate(gate, self.game.hotspot_images[enums.GATE_TILE])
            self.game.groups[enums.ALL].add(gate_sprite) # to update/draw it
            self.game.groups[enums.GATE].add(gate_sprite) # to check for collisions

        # add enemies (and mobile platforms) to the map reading from 'ENEMIES_DATA' list.
        # a maximum of three enemies per map
        # ENEMIES_DATA = (x1, y1, x2, y2, vx, vy, type)
        for i in range(3):
            enemy_data = constants.ENEMIES_DATA[self.number*3 + i]
            if enemy_data[6] != enums.NONE:
                enemy = Enemy(enemy_data, player.rect, self.game.enemy_images[enemy_data[6]])
                self.game.groups[enums.ALL].add(enemy) # to update/draw it
                # enemy sprite? add to the enemy group
                if enemy_data[6] != enums.PLATFORM_SPR:
                    self.game.groups[enums.ENEMIES].add(enemy) # to check for collisions
                else: # platform sprite? add to the platform group
                    self.game.groups[enums.PLATFORM].add(enemy) # to check for collisions                


    # makes a screen transition between the old map and the new one.
    def transition(self):
        # surfaces to save the old and the new map together
        srf_map_t_h = pygame.Surface((constants.MAP_UNSCALED_SIZE[0]*2, constants.MAP_UNSCALED_SIZE[1]))
        srf_map_t_v = pygame.Surface((constants.MAP_UNSCALED_SIZE[0], constants.MAP_UNSCALED_SIZE[1]*2))

        #  -----------   
        #  | new map |  /|\
        #  -----------   |
        #  | old map |   |
        #  -----------   
        if self.scroll == enums.UP:
            # joins the two maps on a single surface
            srf_map_t_v.blit(self.game.srf_map_bk, (0,0))
            srf_map_t_v.blit(self.game.srf_map_bk_prev, (0, constants.MAP_UNSCALED_SIZE[1]))
            # scrolls the two maps across the screen
            for y in range(-constants.MAP_UNSCALED_SIZE[1], 0, 4):
                self.game.srf_map.blit(srf_map_t_v, (0, y))
                self.game.update_screen()

        #  -----------   
        #  | old map |   |
        #  -----------   |
        #  | new map |  \|/
        #  -----------   
        elif self.scroll == enums.DOWN:
            # joins the two maps on a single surface
            srf_map_t_v.blit(self.game.srf_map_bk_prev, (0,0))
            srf_map_t_v.blit(self.game.srf_map_bk, (0, constants.MAP_UNSCALED_SIZE[1]))
            # scrolls the two maps across the screen
            for y in range(0, -constants.MAP_UNSCALED_SIZE[1], -4):
                self.game.srf_map.blit(srf_map_t_v, (0, y))
                self.game.update_screen()

        #         <-----
        #  ---------------------
        #  | new map | old map |
        #  ---------------------
        elif self.scroll == enums.LEFT:
            # joins the two maps on a single surface
            srf_map_t_h.blit(self.game.srf_map_bk, (0,0))
            srf_map_t_h.blit(self.game.srf_map_bk_prev, (constants.MAP_UNSCALED_SIZE[0], 0))
            # scrolls the two maps across the screen
            for x in range(-constants.MAP_UNSCALED_SIZE[0], 0, 6):
                self.game.srf_map.blit(srf_map_t_h, (x, 0))
                self.game.update_screen()

        #         ----->
        #  ---------------------
        #  | old map | new map |
        #  ---------------------
        else: # right
            # joins the two maps on a single surface
            srf_map_t_h.blit(self.game.srf_map_bk_prev, (0,0))
            srf_map_t_h.blit(self.game.srf_map_bk, (constants.MAP_UNSCALED_SIZE[0], 0))
            # scrolls the two maps across the screen
            for x in range(0, -constants.MAP_UNSCALED_SIZE[0], -6):
                self.game.srf_map.blit(srf_map_t_h, (x, 0))
                self.game.update_screen()


    # add the pile of explosives to the background (5 x 3)
    def add_TNT_pile(self):
        for y in range(80, 97, 8): # y = 80, 88, 96
            for x in range(105, 154, 12): # x = 105, 117, 129, 141, 153
                self.game.srf_map_bk.blit(self.img_TNT, (x,y))



