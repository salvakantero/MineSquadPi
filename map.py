
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
        self.number = 0 # current map (0-8)
        self.stage = 0 # current stage (0-2)
        self.last = -1 # last map loaded
        self.map_data = {} # all the information needed to build the map
        self.tile_images = {} # dictionary for storing tile images
        self._tiles_by_id = {}  # cache for quick ID searches        
        self.stage_name1 = ("El Alamein", "D-Day", "Battle of the Bulge")
        self.stage_name2 = ("EGYPT, OCTOBER 1942", "NORMANDY, JUNE 1944", 
                            "ARDENNES FOREST, JANUARY 1945")        



    # does everything necessary to change the map and add enemies and hotspots.
    def change(self, player):
        # sets the new map as the current one
        self.last = self.number
        # set the stage number, knowing that there are 3 levels per stage
        self.stage = self.number // 3
        # load the wallpaper if necessary
        if self.game.config.data['screen_mode'] == enums.SM_16_9: # 16:9
            self.game.set_background(self.stage)
        # load the new map
        self._load()
        # reset some vars
        self.game.loop_counter = 0
        self.game.floating_text.y = 0
        self.game.loss_sequence = 0
        # reset the sprite groups  
        for group in self.game.sprite_groups: group.empty()
        # player in its starting position
        player.rect = player.image.get_rect(
            topleft = (constants.PLAYER_X_INI, constants.PLAYER_Y_INI))
        # marks the initial tile
        self.mark_tile(int(constants.PLAYER_X_INI // constants.TILE_SIZE), 
                       int(constants.PLAYER_Y_INI // constants.TILE_SIZE))
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



    # loads a map from the json file
    def _load(self):
        # reads the entire contents of the json
        with open('maps/map{}.json'.format(self.number)) as json_data:
            data_read = json.load(json_data)
        # the raw_data is a list of tiles in a 1D array
        raw_data = data_read['layers'][0]['data']
        # converts the list of tiles into an array of the map dimensions
        self.map_data['data'] = [
            raw_data[i:i + constants.MAP_TILE_SIZE[0]]
            for i in range(0, len(raw_data), constants.MAP_TILE_SIZE[0])
        ]
        # loads the tileset data
        tileset_path = 'maps/' + data_read['tilesets'][0]['source'].replace('.tsx', '.json')
        with open(tileset_path) as f:
            tileset = json.load(f)        
        self.map_data['tiles'] = tileset['tiles']
        for tile in self.map_data['tiles']:
            # gets the tile ID and image name
            tile['image'] = os.path.basename(tile['image'])
            tile['id'] += 1            
            # stores the tile in the dictionary by ID
            self._tiles_by_id[tile['id']] = tile            
            # loads the tile image only once and saves it in the dictionary.
            img_path = f"images/tiles/{tile['image']}"
            if tile['image'] not in self.tile_images:
                self.tile_images[tile['image']] = pygame.image.load(img_path).convert()        
        # randomly places mines on the map (generates mines and proximity info)
        self.map_data['mines_info'] = self.generate_mines(self.map_data['data'])
        # tiles trodden by the player (marked as False by default)
        self.map_data['marks'] = [[False] * constants.MAP_TILE_SIZE[0] 
                                for _ in range(constants.MAP_TILE_SIZE[1])]
        self._generate_tile_types()



    def _generate_tile_types(self):
        height, width = constants.MAP_TILE_SIZE[1], constants.MAP_TILE_SIZE[0]
        self.map_data['tile_types'] = [[enums.TT_NO_ACTION] * width for _ in range(height)]        
        for y in range(height):
            for x in range(width):
                tile_id = self.map_data['data'][y][x]
                if tile_id in self._tiles_by_id:
                    tile = self._tiles_by_id[tile_id]
                    tile_num = self._get_tile_number(tile['image'])                    
                    # generates the behaviour of the current tile
                    # from T16.png to T35.png : tiles that block (OBSTACLE)
                    # from T70.png to T75.png : tiles that kill (KILLER)
                    if 16 <= tile_num <= 35: tile_type = enums.TT_OBSTACLE
                    elif 70 <= tile_num <= 75: tile_type = enums.TT_KILLER
                    elif self.map_data['mines_info'][y][x] == enums.MI_MINE: 
                        tile_type = enums.TT_MINE
                    else: tile_type = enums.TT_NO_ACTION                    
                    self.map_data['tile_types'][y][x] = tile_type



    # extracts the tile number from the file name
    def _get_tile_number(self, tile_name):
        return int(tile_name.replace('.png', '').replace('T', ''))  
    


    def draw(self, camera):
        tile_size = constants.TILE_SIZE
        map_width, map_height = constants.MAP_TILE_SIZE
        screen_width, screen_height = constants.SCREEN_MAP_UNSCALED_SIZE
        # calculates the visible columns in the map
        start_col = max(0, camera.x // tile_size)
        end_col = min(map_width, start_col + (screen_width // tile_size) + 2)
        start_row = max(0, camera.y // tile_size)
        end_row = min(map_height, start_row + (screen_height // tile_size) + 2) 
        # goes over the entire visible map
        for y in range(int(start_row), int(end_row)):
            for x in range(int(start_col), int(end_col)):
                # screen coordinates
                screen_x = x * tile_size - camera.x
                screen_y = y * tile_size - camera.y
                # only draws the tile if it is within the visible area
                if (-tile_size <= screen_x <= screen_width and 
                    -tile_size <= screen_y <= screen_height):
                    tile_id = self.map_data['data'][y][x]
                    if tile_id in self._tiles_by_id:
                        tile_data = self._tiles_by_id[tile_id]
                        tile_image = self.tile_images[tile_data['image']]
                        self.game.srf_map.blit(tile_image, (screen_x, screen_y))



    # gets the tile type at a specific tile position
    def get_tile_type(self, x, y):
        if (0 <= x < constants.MAP_TILE_SIZE[0] and 
            0 <= y < constants.MAP_TILE_SIZE[1]):
            return self.map_data['tile_types'][y][x]
        return enums.TT_OBSTACLE  # default to obstacle if out of bounds



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



    def draw_mine_data(self, camera):
        tilemap = self.map_data['data'] # list of tiles that make up the map
        for row_index, row in enumerate(self.map_data['mines_info']):
            for col_index, value in enumerate(row):
                if value > enums.MI_FREE \
                and self.map_data['marks'][row_index][col_index] \
                and tilemap[row_index][col_index] < 15:
                    x = (col_index * constants.TILE_SIZE) - camera.x
                    y = (row_index * constants.TILE_SIZE) - camera.y
                    if value == enums.MI_BEACON: # mine deactivated
                        self.game.srf_map.blit(self.game.beacon_image, (x, y))
                    else: # proximity information
                        x = x + constants.HALF_TILE_SIZE
                        y = y + constants.HALF_TILE_SIZE
                        self.game.fonts[enums.L_B_BLACK].render(
                            str(value), self.game.srf_map, (x-2,y-6))
                        self.game.fonts[enums.L_F_RED].render(
                            str(value), self.game.srf_map, (x-3,y-7))



    def mark_tile(self, x, y):
        # Check bounds
        if 0 <= y < constants.MAP_TILE_SIZE[1] and 0 <= x < constants.MAP_TILE_SIZE[0]:          
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if 0 <= i < constants.MAP_TILE_SIZE[1] \
                    and 0 <= j < constants.MAP_TILE_SIZE[0]:
                        self.map_data['marks'][i][j] = True
