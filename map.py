
# ==============================================================================
# .::Map class::.
# Everything related to the drawing of the tile map.
# This game uses levels made with the "Tiled" program.
# Each screen is a JSON file exported from "Tiled".
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
        self.number = 0 # current map (0-11)
        self.stage = 0 # current stage (0-2)
        self.last = -1 # last map loaded
        self.map_data = {} # all the information needed to build the map
        self.stage_name1 = ("El Alamein", "D-Day", "Battle of the Bulge")
        self.stage_name2 = ("EGYPT, OCTOBER 1942", 
                            "NORMANDY, JUNE 1944", 
                            "ARDENNES FOREST, JANUARY 1945")        


    # does everything necessary to change the map and add enemies and hotspots.
    def change(self, player):
        # sets the new map as the current one
        self.last = self.number
        # set the stage number, knowing that there are 4 levels per stage
        self.stage = self.number // 4
        # load the wallpaper if necessary
        if self.game.config.data['screen_mode'] == enums.SM_X720: # 16:9
            self.game.set_background(self.stage)
        # load the new map
        self.load()
        # save the new background (empty of sprites)
        self.game.srf_map_bk.blit(self.game.srf_map, (0,0))
        # reset some vars
        self.game.loop_counter = 0
        self.game.floating_text.y = 0
        self.game.loss_sequence = 0
        # reset the sprite groups  
        for group in self.game.groups: group.empty()
        # add the player
        self.game.groups[enums.SG_ALL].add(player)
        # player in its starting position
        player.rect = player.image.get_rect(topleft = (
            constants.PLAYER_X_INI, constants.PLAYER_Y_INI))
        # marks the initial tile
        self.mark_tile(constants.PLAYER_Y_INI // constants.TILE_SIZE, 
                       constants.PLAYER_X_INI // constants.TILE_SIZE)
        # sets the available mines and beacons for the map
        self.game.remaining_mines = constants.NUM_MINES[self.number]
        self.game.remaining_beacons = constants.NUM_BEACONS[self.number]
        # # add the hotspot
        # hotspot = constants.HOTSPOT_DATA[self.number]        
        # hotspot_sprite = Hotspot(hotspot, self.game.hotspot_images[hotspot[0]])
        # self.game.groups[enums.SG_ALL].add(hotspot_sprite) # to update/draw it
        # self.game.groups[enums.SG_HOTSPOT].add(hotspot_sprite) # to check for collisions
        # # add enemies to the map reading from 'ENEMIES_DATA' list.
        # # a maximum of three enemies per map
        # # ENEMIES_DATA = (x1, y1, x2, y2, vx, vy, type)
        # for i in range(3):
        #    enemy_data = constants.ENEMIES_DATA[self.number*3 + i]
        #    if enemy_data[6] != enums.EN_NONE:
        #        enemy = Enemy(enemy_data, player.rect, self.game.enemy_images[enemy_data[6]])
        #        self.game.groups[enums.SG_ALL].add(enemy) # to update/draw it


    # loads a map from the json file, and draws it on screen
    def load(self):
        # reads the entire contents of the json
        with open('maps/map{}.json'.format(self.number)) as json_data:
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
        
        # randomly places mines on the map (generates mines and proximity info)
        data['mines_info'] = self.generate_mines(data['data'])

        # tile types; no action, obstacle, killer, mine
        data['tile_types'] = [[enums.TT_NO_ACTION] * constants.MAP_TILE_SIZE[0] 
                            for _ in range(constants.MAP_TILE_SIZE[1])]
        
        # tiles trodden by the player (marked as False by default)
        data['marks'] = [[False] * constants.MAP_TILE_SIZE[0] 
                        for _ in range(constants.MAP_TILE_SIZE[1])]

        # scroll through the map data
        for y in range(0, data['height']):
            for x in range(0, data['width']):
                # gets the tile number from the list
                t = self.find_data(data['tiles'], 'id', data['data'][y][x])
                # draws the selected tile
                tile = pygame.image.load('images/tiles/' + t['image']).convert()
                tileRect = tile.get_rect()
                tileRect.topleft = (x * t['imagewidth'], y * t['imageheight'])   
                self.game.srf_map.blit(tile, tileRect)
                
                # generates the behaviour of the current tile
                # from T16.png to T35.png: blocking tiles (OBSTACLE)
                # from T70.png to T75.png: tiles that kill (KILLER)
                number = self.get_tile_number(t['image'])
                type = enums.TT_NO_ACTION
                if number >= 16 and number <= 35:   
                    type = enums.TT_OBSTACLE
                elif number >= 70 and number <= 75: 
                    type = enums.TT_KILLER
                elif data['mines_info'][y][x] == enums.MI_MINE: 
                    type = enums.TT_MINE
                data['tile_types'][y][x] = type                
        
        # transfer data to the map object
        self.map_data = data


    # function to generate mines on the game map
    def generate_mines(self, tilemap):      
        available_tiles = [] # list of tiles on which to lay mines
        for row_index, row in enumerate(tilemap):
            for col_index, tile in enumerate(row):
                # if number of tile less than 15, is passable
                # we will not use the two rows closest to the player.
                if tile < 15 and row_index < len(tilemap) - 2:
                    available_tiles.append((row_index, col_index))
        # initial mine map with all its values at 0
        mine_data = [[enums.MI_FREE] * constants.MAP_TILE_SIZE[0] 
                    for _ in range(constants.MAP_TILE_SIZE[1])]
        # choose random mine positions among the passable tiles
        mines = random.sample(available_tiles, constants.NUM_MINES[self.number])
        for mine in mines:
            row, col = mine
            mine_data[row][col] = enums.MI_MINE # mark the mine
            # Increases the counter of adjacent tiles.
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < constants.MAP_TILE_SIZE[1] \
                    and 0 <= j < constants.MAP_TILE_SIZE[0] \
                    and mine_data[i][j] != enums.MI_MINE:
                        mine_data[i][j] += 1
        return mine_data


    def get_behaviour_at(self, x, y):
        # Obtiene el comportamiento del tile en las coordenadas x,y
        if 0 <= y < len(self.map_data['tile_types']) and 0 <= x < len(self.map_data['tile_types'][0]):
            return self.map_data['tile_types'][y][x]
        return enums.TT_NO_ACTION


    def get_mine_info_at(self, x, y):
        # Obtiene la información de minas en las coordenadas x,y
        if 0 <= y < len(self.map_data['mines_info']) and 0 <= x < len(self.map_data['mines_info'][0]):
            return self.map_data['mines_info'][y][x]
        return enums.MI_FREE


    def set_behaviour_at(self, x, y, type):
        # Establece el comportamiento en las coordenadas x,y
        if 0 <= y < len(self.map_data['tile_types']) and 0 <= x < len(self.map_data['tile_types'][0]):
            self.map_data['tile_types'][y][x] = type


    def set_mine_info_at(self, x, y, mine_info):
        # Establece la información de minas en las coordenadas x,y
        if 0 <= y < len(self.map_data['mines_info']) and 0 <= x < len(self.map_data['mines_info'][0]):
            self.map_data['mines_info'][y][x] = mine_info


    def draw_mine_data(self):
        tilemap = self.map_data['data'] # list of tiles that make up the map
        for row_index, row in enumerate(self.map_data['mines_info']):
            for col_index, value in enumerate(row):
                if value > enums.MI_FREE \
                and self.map_data['marks'][row_index][col_index] \
                and tilemap[row_index][col_index] < 15:
                    if value == enums.MI_BEACON: # mine deactivated
                        x = (col_index * constants.TILE_SIZE)
                        y = (row_index * constants.TILE_SIZE)
                        self.game.srf_map.blit(self.game.beacon_image, (x,y))
                    else: # proximity information
                        x = (col_index * constants.TILE_SIZE + constants.TILE_SIZE // 2)
                        y = (row_index * constants.TILE_SIZE + constants.TILE_SIZE // 2)
                        self.game.fonts[enums.L_B_BLACK].render(
                            str(value), self.game.srf_map, (x-2,y-6))
                        self.game.fonts[enums.L_F_RED].render(
                            str(value), self.game.srf_map, (x-3,y-7))


    def mark_tile(self, row, col):
        # Check bounds
        if 0 <= row < constants.MAP_TILE_SIZE[1] and 0 <= col < constants.MAP_TILE_SIZE[0]:          
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < constants.MAP_TILE_SIZE[1] \
                    and 0 <= j < constants.MAP_TILE_SIZE[0]:
                        self.map_data['marks'][i][j] = True
                        
 
    # extracts the tile number from the filename
    def get_tile_number(self, tile_name):
        tile_name = tile_name.replace('.png', '')
        tile_name = tile_name.replace('T', '')
        return int(tile_name)
  

    # get a value from a dictionary
    def find_data(self, lst, key, value):
        matches = [d for d in lst if d[key] == value]
        return matches[0] if matches else None
