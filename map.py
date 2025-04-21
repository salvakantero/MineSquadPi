
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
        self.number = 0 # current map
        self.last = -1 # last map loaded
        self.map_data = {} # all the information needed to build the map
        self.stage_name1 = ("El Alamein", "D-Day", "Battle of the Bulge")
        self.stage_name2 = ("NORTH AFRICA, OCTOBER 1942", 
                            "NORMANDY, JUNE 1944", 
                            "THE ARDENNES, JANUARY 1945")        


    # does everything necessary to change the map and add enemies and hotspots.
    def change(self, player, scoreboard):
        # sets the new map as the current one
        self.last = self.number
        # load the wallpaper if necessary
        if self.game.config.data['screen_mode'] == enums.SM_X720: # 16:9
            self.game.set_background(self.number)
            self.game.screen.blit(self.game.img_background, (0,0))
        # load the new map
        self.load()
        # save the new background (empty of sprites)
        self.game.srf_map_bk.blit(self.game.srf_map, (0,0))
        # refresh the scoreboard area
        scoreboard.reset(self.number)
        scoreboard.invalidate()
        # reset the sprite groups  
        for group in self.game.groups: group.empty()
        # removes any possible floating text
        self.game.floating_text.y = 0
        # add the player  
        self.game.groups[enums.SG_ALL].add(player)
        self.mark_tile(constants.PLAYER_Y_INI // constants.TILE_SIZE, 
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
        
        # rects and behaviours of each tile (to fill in later)
        data['rects'] = []
        data['behaviours'] = []
        # randomly places mines on the map
        data['mines'] = self.generate_mines(data['data'])
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
                # generates the list of rects and behaviour of the current map
                # from T16.png to T35.png: blocking tiles (OBSTACLE)
                # from T70.png to T75.png: tiles that kill (KILLER)
                tn = self.get_tile_number(t['image'])
                behaviour = enums.TB_NO_ACTION
                if tn >= 16 and tn <= 35:   behaviour = enums.TB_OBSTACLE
                elif tn >= 70 and tn <= 75: behaviour = enums.TB_KILLER
                elif data['mines'][y][x] == enums.MD_MINE: behaviour = enums.TB_MINE
                # is only added to the list if there is an active behaviour
                if behaviour != enums.TB_NO_ACTION:
                    data['rects'].append(tileRect)
                    data['behaviours'].append(behaviour)
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
        mine_data = [[enums.MD_FREE] * constants.MAP_TILE_SIZE[0] 
                     for _ in range(constants.MAP_TILE_SIZE[1])]
        # choose random mine positions among the passable tiles
        mines = random.sample(available_tiles, constants.NUM_MINES[self.number])
        for mine in mines:
            row, col = mine
            mine_data[row][col] = enums.MD_MINE # mark the mine
            # Increases the counter of adjacent tiles.
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < constants.MAP_TILE_SIZE[1] \
                    and 0 <= j < constants.MAP_TILE_SIZE[0] \
                    and mine_data[i][j] != enums.MD_MINE:
                        mine_data[i][j] += 1
        return mine_data


    def draw_mine_data(self):
        tilemap = self.map_data['data'] # list of tiles that make up the map
        for row_index, row in enumerate(self.map_data['mines']):
            for col_index, value in enumerate(row):
                if value > enums.MD_FREE \
                and self.map_data['marks'][row_index][col_index] \
                and tilemap[row_index][col_index] < 15:
                    if value == enums.MD_FLAG: # mine deactivated
                        x = (col_index * constants.TILE_SIZE)
                        y = (row_index * constants.TILE_SIZE)
                        self.game.srf_map.blit(self.game.flag_image, (x,y))
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
