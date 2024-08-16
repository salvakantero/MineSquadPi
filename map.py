
# ==============================================================================
# .::Map class::.
# Everything related to the drawing of the tile map.
# This game uses levels made with the "Tiled" program.
# Each screen is a JSON file exported from "Tiled".
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
import json
import os
import random
import constants
import enums

from hotspot import Hotspot
from enemy import Enemy


class Map():
    def __init__(self, game):
        self.game = game
        self.number = 0 # current map
        self.last = -1 # last map loaded
        self.tilemap_info = [] # list of tile rects and behaviours (except for transparent ones)
        #self.anim_tiles_list = [] # (frame_1, frame_2, x, y, num_frame)
        self.map_data = {} # tiles that make up the map
        self.revealed_tiles = {} # tiles trodden by the player
        self.mine_data = [] # location of the mines on the map


    # loads a map and draws it on screen
    def load(self):
        self.map_data = self.process_map('maps/map{}.json'.format(self.number))
        self.mine_data = self.generate_mines() # randomly places mines on the map.
        self.revealed_tiles = [[False] * constants.MAP_TILE_SIZE[0] 
                               for _ in range(constants.MAP_TILE_SIZE[1])]
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


    # function to generate mines on the game map
    def generate_mines(self):      
        tile_data = self.map_data['data'] # list of tiles that make up the map
        available_tiles = [] # list of tiles on which to lay mines
        for row_index, row in enumerate(tile_data):
            for col_index, tile in enumerate(row):
                # if number of tile less than 15, is passable
                # we will not use the two rows closest to the player.
                if tile < 15 and row_index < len(tile_data) - 2:
                    available_tiles.append((row_index, col_index))
        # initial mine map with all its values at 0
        mine_data = [[0] * constants.MAP_TILE_SIZE[0] for _ in range(constants.MAP_TILE_SIZE[1])]
        # choose random mine positions among the passable tiles
        mines = random.sample(available_tiles, constants.NUM_MINES[self.number])
        for mine in mines:
            row, col = mine
            mine_data[row][col] = -1 # mark the mine
            # Increases the counter of adjacent tiles.
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < constants.MAP_TILE_SIZE[1] \
                    and 0 <= j < constants.MAP_TILE_SIZE[0] \
                    and mine_data[i][j] != -1:
                        mine_data[i][j] += 1
        return mine_data


    # draws the tile map on the screen
    def draw_map(self):
        self.tilemap_info.clear()
        #self.anim_tiles_list.clear()
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
                # from T16.png to T35.png: blocking tiles (OBSTACLE)
                # from T70.png to T75.png: tiles that kill (KILLER)
                tn = self.get_tile_number(t['image'])
                behaviour = enums.NO_ACTION
                if tn >= 16 and tn <= 35:   behaviour = enums.OBSTACLE
                elif tn >= 70 and tn <= 75: behaviour = enums.KILLER
                elif self.mine_data[y][x] == -1: behaviour = enums.KILLER
                # is only added to the list if there is an active behaviour
                if behaviour != enums.NO_ACTION:
                    self.tilemap_info.append((tileRect, behaviour))

                # generates the list of animated tiles of the current map
                # (frame_1, frame_2, x, y, num_frame)
                #if t['image'] in constants.ANIM_TILES.keys():                
                #    self.anim_tiles_list.append(
                #        [tile, pygame.image.load('images/tiles/' 
                #        + constants.ANIM_TILES[t['image']]).convert(), 
                #        tileRect.topleft[0], tileRect.topleft[1], 0])


    def reveal_tile(self, row, col):
        # Check bounds
        if 0 <= row < constants.MAP_TILE_SIZE[1] and 0 <= col < constants.MAP_TILE_SIZE[0]:          
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < constants.MAP_TILE_SIZE[1] and 0 <= j < constants.MAP_TILE_SIZE[0]:
                        if not self.revealed_tiles[i][j]:
                            self.revealed_tiles[i][j] = True


    def draw_mine_data(self):
        tile_data = self.map_data['data'] # list of tiles that make up the map
        for row_index, row in enumerate(self.mine_data):
            for col_index, value in enumerate(row):
                if value > 0 \
                and self.revealed_tiles[row_index][col_index] \
                and tile_data[row_index][col_index] < 15:
                    x = (col_index * constants.TILE_SIZE + constants.TILE_SIZE // 2)
                    y = (row_index * constants.TILE_SIZE + constants.TILE_SIZE // 2)
                    self.game.fonts[enums.L_B_BLACK].render(str(value), self.game.srf_map, (x-2,y-6))
                    self.game.fonts[enums.L_F_RED].render(str(value), self.game.srf_map, (x-3,y-7))

    # select some of the animated tiles on the current map to change the frame
    # and apply to the surface. 
    # anim_tiles_list = (frame_1, frame_2, x, y, num_frame)
    #def animate_tiles(self):
    #    for anim_tile in self.anim_tiles_list: # for each animated tile on the map
    #        if random.randint(0,24) == 0: # 4% chance of changing frame
    #            tile = anim_tile[0+anim_tile[4]] # select image according to frame number
    #            tileRect = tile.get_rect()
    #            tileRect.topleft = (anim_tile[2], anim_tile[3]) # sets the xy position
    #            self.game.srf_map_bk.blit(tile, tileRect) # draws on the background image
    #           # update frame number (0,1)
    #            anim_tile[4] = (anim_tile[4] + 1) % 2


    # checks if the map needs to be changed (depending on the player's XY position)
    #def check_change(self, player):
        # player disappears on the left
        # appearing from the right on the new map
        #if player.rect.x < -(constants.TILE_SIZE-8):
        #    self.number -= 1
        #    player.rect.right = constants.MAP_UNSCALED_SIZE[0]
        # player disappears on the right
        # appearing from the left on the new map
        #elif player.rect.x > constants.MAP_UNSCALED_SIZE[0] - 8:
        #    self.number += 1
        #    player.rect.left = 0
        # player disappears over the top
        # appearing at the bottom of the new map 
        # and jumps again to facilitate the return
        #elif player.rect.y < (-constants.TILE_SIZE):
        #    self.number -= 5
        #    player.rect.bottom = constants.MAP_UNSCALED_SIZE[1]            
        # player disappears from underneath
        #appearing at the top of the new map
        #elif player.rect.y > constants.MAP_UNSCALED_SIZE[1]:
        #    self.number += 5
        #    player.rect.top = 0


    # does everything necessary to change the map and add enemies and hotspots.
    def change(self, player, scoreboard):
        # sets the new map as the current one
        self.last = self.number
        # load the new map
        self.load()
        # save the new background (empty of sprites)
        self.game.srf_map_bk.blit(self.game.srf_map, (0,0))
        # refresh the scoreboard area
        scoreboard.reset()
        scoreboard.map_info(self.number)
        scoreboard.invalidate()
        # reset the sprite groups  
        for group in self.game.groups: group.empty()
        # removes any possible floating text
        self.game.floating_text.y = 0
        # add the player  
        self.game.groups[enums.ALL].add(player)
        self.reveal_tile(constants.PLAYER_Y_INI // constants.TILE_SIZE, 
                         constants.PLAYER_X_INI // constants.TILE_SIZE)

        # add the hotspot (if available)
        #hotspot = constants.HOTSPOT_DATA[self.number]
        #if hotspot[3] == True: # visible/available?           
        #    hotspot_sprite = Hotspot(hotspot, self.game.hotspot_images[hotspot[0]])
        #    self.game.groups[enums.ALL].add(hotspot_sprite) # to update/draw it
        #    self.game.groups[enums.HOTSPOT].add(hotspot_sprite) # to check for collisions

        # add enemies to the map reading from 'ENEMIES_DATA' list.
        # a maximum of three enemies per map
        # ENEMIES_DATA = (x1, y1, x2, y2, vx, vy, type)
        #for i in range(3):
        #    enemy_data = constants.ENEMIES_DATA[self.number*3 + i]
        #    if enemy_data[6] != enums.NONE:
        #        enemy = Enemy(enemy_data, player.rect, self.game.enemy_images[enemy_data[6]])
        #        self.game.groups[enums.ALL].add(enemy) # to update/draw it
        #        self.game.groups[enums.ENEMIES].add(enemy) # to check for collisions               




