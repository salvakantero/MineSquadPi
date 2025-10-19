
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
        # optimization cache for draw_mine_data
        self._player_tile_cache = (-1, -1)  # (tile_x, tile_y)
        self._alpha_cache = {}  # {(tile_x, tile_y): alpha_value}
        self._text_surfaces_cache = {}  # {(value, alpha): surface}
        self._tile_size = constants.TILE_SIZE
        self._half_tile_size = constants.HALF_TILE_SIZE
        # pre-create fog surface (avoid creating one per tile per frame)
        self._fog_surface = pygame.Surface((constants.TILE_SIZE, constants.TILE_SIZE), pygame.SRCALPHA)
        self._fog_surface.fill((0, 0, 0, 35))



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
        self.game.floating_text.active = False
        self.game.blast_sequence = 0
        # reset optimization caches
        self._player_tile_cache = (-1, -1)
        self._alpha_cache.clear()
        self._text_surfaces_cache.clear()
        # reset the sprite groups
        for group in self.game.sprite_groups: group.empty()
        # clear explosion pool for new map
        self.game.explosion_pool.clear()
        # player in its starting position
        player.x, player.y = constants.PLAYER_X_INI, constants.PLAYER_Y_INI
        player.target_x, player.target_y = player.x, player.y
        # marks the initial tile
        self.mark_tile(int(constants.PLAYER_X_INI // constants.TILE_SIZE), 
                       int(constants.PLAYER_Y_INI // constants.TILE_SIZE))
        # sets the available mines and beacons for the map
        self.game.remaining_mines = constants.NUM_MINES[self.number]
        self.game.remaining_beacons = constants.NUM_BEACONS[self.number]

        # add the hotspots
        map_hotspots = [hotspot for hotspot in constants.HOTSPOT_DATA if hotspot[1] == self.number]
        for hotspot_data in map_hotspots:
            type = hotspot_data[0] # LIFE, SHIELD, AMMO, CANDY, APPLE, CHOCOLATE, COIN
            hotspot_sprite = Hotspot(type, self.game.hotspot_images[type], self)
            self.game.sprite_groups[enums.SG_HOTSPOT].add(hotspot_sprite)

        # add enemies to the map reading from 'ENEMIES_DATA' list
        map_enemies = [enemy for enemy in constants.ENEMIES_DATA if enemy[0] == self.number]
        for enemy_data in map_enemies:
            enemy = Enemy(enemy_data, player.rect, self.game.enemy_images[enemy_data[1]], self)
            self.game.sprite_groups[enums.SG_ENEMIES].add(enemy)



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
                        # 'fog of war'
                        if (not self.map_data['marks'][y][x]):
                            self.game.srf_map.blit(self._fog_surface, (screen_x, screen_y))



    # gets the tile type at a specific tile position (calculated dynamically)
    def get_tile_type(self, x, y):
        if (0 <= x < constants.MAP_TILE_SIZE[0] and
            0 <= y < constants.MAP_TILE_SIZE[1]):
            # calculate tile type from tile ID and mines_info
            tile_id = self.map_data['data'][y][x]
            if tile_id in self._tiles_by_id:
                tile = self._tiles_by_id[tile_id]
                tile_num = self._get_tile_number(tile['image'])
                # from T0.png to T19.png : tiles that allow movement (PASSABLE)
                # from T20.png to T39.png : tiles that block (OBSTACLE)
                if 20 <= tile_num <= 39:
                    return enums.TT_OBSTACLE
                # from T40.png to T49.png : tiles that kill (KILLER)
                elif 40 <= tile_num <= 49:
                    return enums.TT_KILLER
                # check if it's a mine
                elif self.map_data['mines_info'][y][x] == enums.MI_MINE:
                    return enums.TT_MINE
            return enums.TT_NO_ACTION
        return enums.TT_OBSTACLE  # default to obstacle if out of bounds



    def draw_mine_data(self, camera, player):
        # cache player tile position (calculated once per frame instead of per tile)
        player_tile_x = player.rect.centerx // self._tile_size
        player_tile_y = player.rect.centery // self._tile_size
        
        # update alpha cache only if player moved to different tile
        if (player_tile_x, player_tile_y) != self._player_tile_cache:
            self._update_alpha_cache(player_tile_x, player_tile_y)
        
        # cache frequently accessed data structures
        mines_info = self.map_data['mines_info']
        marks = self.map_data['marks']
        tilemap = self.map_data['data']
        map_surface = self.game.srf_map
        beacon_image = self.game.beacon_image
        beacon2_image = self.game.beacon2_image
        
        # optimized main loop
        for row_index, row in enumerate(mines_info):
            for col_index, value in enumerate(row):
                if (value > enums.MI_FREE and 
                    marks[row_index][col_index] and 
                    # if number of tile less than 7, is passable (json map file)
                    tilemap[row_index][col_index] < 7):
                    
                    screen_x = (col_index * self._tile_size) - camera.x
                    screen_y = (row_index * self._tile_size) - camera.y
                    
                    # draw the beacon if the mine is deactivated
                    if value == enums.MI_BEACON:
                        map_surface.blit(beacon_image, (screen_x, screen_y))
                    # draw the red flag for incorrect beacon
                    elif value == enums.MI_BEACON2:
                        map_surface.blit(beacon2_image, (screen_x, screen_y))
                    # draw the proximity number if the mine is active
                    else:
                        # get pre-calculated alpha value
                        alpha = self._alpha_cache[(col_index, row_index)]
                        text_x = screen_x + self._half_tile_size
                        text_y = screen_y + self._half_tile_size
                        
                        if alpha < 255:
                            # use cached surface with transparency
                            text_surface = self._get_text_surface(value, alpha)
                            map_surface.blit(text_surface, (screen_x, screen_y))
                        else:
                            # direct rendering for full opacity (fastest path)
                            self.game.fonts[enums.L_B_BLACK].render(str(value), map_surface, (text_x-2, text_y-6))
                            self.game.fonts[enums.L_F_RED].render(str(value), map_surface, (text_x-3, text_y-7))



    def mark_tile(self, x, y):
        # Check bounds
        if 0 <= y < constants.MAP_TILE_SIZE[1] and 0 <= x < constants.MAP_TILE_SIZE[0]:          
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if 0 <= i < constants.MAP_TILE_SIZE[1] \
                    and 0 <= j < constants.MAP_TILE_SIZE[0]:
                        self.map_data['marks'][i][j] = True



    ##### auxiliary functions #####

    # updates alpha cache when player position changes
    def _update_alpha_cache(self, player_tile_x, player_tile_y):
        self._alpha_cache.clear()
        # pre-calculate alpha values for all potentially visible tiles
        for row_index in range(constants.MAP_TILE_SIZE[1]):
            for col_index in range(constants.MAP_TILE_SIZE[0]):
                distance = max(abs(col_index - player_tile_x), abs(row_index - player_tile_y))
                if distance > 1:
                    alpha = max(20, 255 - (distance - 1) * 50)
                else:
                    alpha = 255
                self._alpha_cache[(col_index, row_index)] = alpha
        self._player_tile_cache = (player_tile_x, player_tile_y)



    # gets or creates a cached surface for text rendering
    def _get_text_surface(self, value, alpha):
        cache_key = (value, alpha)
        if cache_key not in self._text_surfaces_cache:
            surface = pygame.Surface((self._tile_size, self._tile_size), pygame.SRCALPHA)
            self.game.fonts[enums.L_B_BLACK].render(str(value), surface, (self._half_tile_size-2, self._half_tile_size-6))
            self.game.fonts[enums.L_F_RED].render(str(value), surface, (self._half_tile_size-3, self._half_tile_size-7))
            if alpha < 255:
                surface.set_alpha(alpha)
            self._text_surfaces_cache[cache_key] = surface
        return self._text_surfaces_cache[cache_key]



    # loads a map from the json file
    def _load(self):
        # reads the entire contents of the json
        with open(f'maps/map{self.number}.json') as json_data:
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
        self.map_data['mines_info'] = self._generate_mines(self.map_data['data'])
        # tiles trodden by the player (marked as False by default)
        self.map_data['marks'] = [[False] * constants.MAP_TILE_SIZE[0]
                                for _ in range(constants.MAP_TILE_SIZE[1])]




    # extracts the tile number from the file name
    def _get_tile_number(self, tile_name):
        return int(tile_name.replace('.png', '').replace('T', ''))  
    


    # function to generate mines on the game map
    def _generate_mines(self, tilemap):      
        available_tiles = [] # list of tiles on which to lay mines
        for row_index, row in enumerate(tilemap):
            for col_index, tile in enumerate(row):
                # if number of tile less than 7, is passable (json map file)
                # we will not use the two rows closest to the player.
                if tile < 7 and row_index < len(tilemap) - 2:
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
