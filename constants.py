
# ==============================================================================
# .::Constants::.
# Values that do not change are named to clarify the source code.
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

import enums

# game screen
WIN_SIZE = 800, 640 # main window size (windowed mode)
MENU_SCALED_SIZE = 720, 594 # menu size scaled x3 (windowed mode)
SCREEN_MAP_SCALED_SIZE = 720, 528 # map size on screen scaled x3 (windowed mode)
SBOARD_SCALED_SIZE = 720, 66 # scoreboard size scaled x3 (windowed mode)
MENU_UNSCALED_SIZE = 240, 198 # menu size (unscaled)
SCREEN_MAP_UNSCALED_SIZE = 240, 176 # map size on screen (unscaled)
SBOARD_UNSCALED_SIZE = 240, 22 # scoreboard size (unscaled)
TILE_SIZE = 16 # size of each tile in pixels (square, 16*16)
HALF_TILE_SIZE = TILE_SIZE // 2 # half size of each tile in pixels
TILE_CENTER_OFFSET = 4  # pre-calculated for blast positioning
MAP_TILE_SIZE = 30, 40 # map size in tiles (width, height)
MAP_PIXEL_SIZE = MAP_TILE_SIZE[0] * TILE_SIZE, MAP_TILE_SIZE[1] * TILE_SIZE # map size in pixels
H_MARGIN = 40 # horizontal distance between the edge and the playing area (windowed mode)
V_MARGIN = 20 # vertical distance between the edge and the playing area (windowed mode)

NUM_MINES =   25, 30, 35, 40, 45, 50, 55, 60, 65 # number of mines per map
NUM_BEACONS = 30, 35, 40, 45, 50, 55, 60, 65, 70 # number of flags/beacons per map

# player
TIME_REMAINING = 40000 # remaining shield time (approximately 40 seconds)
MAX_AMMO = 20 # maximum number of bullets
AMMO_ROUND = 10 # bullets per reload
ANIM_SPEED_IDLE = 16 # loops between each frame change
ANIM_SPEED_WALK = 6 # loops between each frame change in walking state
# XY starting position
PLAYER_X_INI = int(MAP_TILE_SIZE[0] // 4) * TILE_SIZE
PLAYER_Y_INI = (MAP_TILE_SIZE[1] - 1) * TILE_SIZE

# enemies
# Base pause durations (will decrease based on stage)
def get_random_enemy_pause_duration(stage):
    base_durations = [30, 27, 24]  # stage 1, 2, 3
    return base_durations[min(stage, 2)]

def get_chaser_enemy_pause_duration(stage):
    base_durations = [60, 55, 50]  # stage 1, 2, 3
    return base_durations[min(stage, 2)]

CHASER_ACTIVATION_RANGE = 5  # the enemy activates when the player is X tiles or less away
ENEMY_RESPAWN_TIME = 15000  # time in milliseconds before enemy respawns (10 seconds)
ENEMY_RESPAWN_SAFE_DISTANCE = 5  # minimum distance in tiles between player and enemy respawn position
# SCORPION, SNAKE, SOLDIER1, PROJECTILE, CRAB, SOLDIER2, SKIER, WILDBOAR, SOLDIER3
ENEMY_LIFE = 1, 1, 2, 1, 2, 3, 2, 3, 3

# enemies per map (map, type, movement, tile_x1, tile_y1, tile_x2, tile_y2)
ENEMIES_DATA = [
    #-----------STAGE 1-------------
    #
    # types:    0) SCORPION 
    #           1) SNAKE 
    #           2) SOLDIER0
    # 0 ---------------------------------------------------------------
    (0, enums.EN_SCORPION, enums.EM_HORIZONTAL, 2, 35, 13, 35),
    (0, enums.EN_SCORPION, enums.EM_VERTICAL, 23, 4, 23, 38),
    (0, enums.EN_SNAKE, enums.EM_RANDOM, 26, 16, 0, 0),
    (0, enums.EN_SNAKE, enums.EM_RANDOM, 10, 8, 0, 0),
    # 1 ---------------------------------------------------------------
    (1, enums.EN_SCORPION, enums.EM_VERTICAL, 9, 1, 9, 38),
    (1, enums.EN_SCORPION, enums.EM_VERTICAL, 21, 1, 21, 37),
    (1, enums.EN_SNAKE, enums.EM_RANDOM, 22, 36, 0, 0),
    (1, enums.EN_SNAKE, enums.EM_RANDOM, 23, 22, 0, 0),
    (1, enums.EN_SNAKE, enums.EM_RANDOM, 14, 3, 0, 0),
    (1, enums.EN_SNAKE, enums.EM_RANDOM, 5, 20, 0, 0),
    (1, enums.EN_SOLDIER0, enums.EM_CHASER, 15, 12, 0, 0),
    (1, enums.EN_SOLDIER0, enums.EM_CHASER, 15, 25, 0, 0),
    # 2 ---------------------------------------------------------------
    (2, enums.EN_SCORPION, enums.EM_HORIZONTAL, 2, 35, 12, 35),
    (2, enums.EN_SCORPION, enums.EM_HORIZONTAL, 1, 29, 8, 29),
    (2, enums.EN_SCORPION, enums.EM_HORIZONTAL, 19, 18, 28, 18),
    (2, enums.EN_SCORPION, enums.EM_HORIZONTAL, 4, 9, 9, 9),
    (2, enums.EN_SNAKE, enums.EM_RANDOM, 20, 31, 0, 0),
    (2, enums.EN_SNAKE, enums.EM_RANDOM, 11, 20, 0, 0),
    (2, enums.EN_SNAKE, enums.EM_RANDOM, 22, 5, 0, 0),
    (2, enums.EN_SOLDIER0, enums.EM_CHASER, 24, 18, 0, 0),
    (2, enums.EN_SOLDIER0, enums.EM_CHASER, 12, 4, 0, 0),

    #-----------STAGE 2-------------
    #
    # types:    3) PROJECTILE
    #           4) CRAB
    #           5) SOLDIER1
    # 3 ---------------------------------------------------------------
    (3, enums.EN_PROJECTILE, enums.EM_HORIZONTAL_LOOP, -1, 11, 30, 11),
    (3, enums.EN_PROJECTILE, enums.EM_HORIZONTAL_LOOP, -1, 32, 30, 32),
    (3, enums.EN_CRAB, enums.EM_RANDOM, 18, 36, 0, 0),
    (3, enums.EN_CRAB, enums.EM_RANDOM, 7, 18, 0, 0),
    (3, enums.EN_CRAB, enums.EM_RANDOM, 24, 21, 0, 0),
    (3, enums.EN_CRAB, enums.EM_RANDOM, 12, 3, 0, 0),
    # 4 ---------------------------------------------------------------
    (4, enums.EN_PROJECTILE, enums.EM_HORIZONTAL_LOOP, -1, 14, 30, 10),
    (4, enums.EN_PROJECTILE, enums.EM_HORIZONTAL_LOOP, -1, 24, 30, 10),
    (4, enums.EN_PROJECTILE, enums.EM_HORIZONTAL_LOOP, -1, 35, 30, 32),
    (4, enums.EN_CRAB, enums.EM_RANDOM, 22, 36, 0, 0),
    (4, enums.EN_CRAB, enums.EM_RANDOM, 23, 22, 0, 0),
    (4, enums.EN_CRAB, enums.EM_RANDOM, 14, 3, 0, 0),
    (4, enums.EN_CRAB, enums.EM_RANDOM, 1, 20, 0, 0),
    (4, enums.EN_CRAB, enums.EM_RANDOM, 1, 1, 0, 0),
    (4, enums.EN_SOLDIER1, enums.EM_CHASER, 15, 12, 0, 0),
    (4, enums.EN_SOLDIER1, enums.EM_CHASER, 15, 25, 0, 0),
    # 5 ---------------------------------------------------------------
    (5, enums.EN_PROJECTILE, enums.EM_HORIZONTAL_LOOP, -1, 11, 30, 11),
    (5, enums.EN_PROJECTILE, enums.EM_HORIZONTAL_LOOP, -1, 24, 30, 24),
    (5, enums.EN_PROJECTILE, enums.EM_HORIZONTAL_LOOP, -1, 37, 30, 37),
    (5, enums.EN_CRAB, enums.EM_RANDOM, 16, 32, 0, 0),
    (5, enums.EN_CRAB, enums.EM_RANDOM, 18, 5, 0, 0),
    (5, enums.EN_CRAB, enums.EM_RANDOM, 5, 34, 0, 0),
    (5, enums.EN_CRAB, enums.EM_RANDOM, 24, 22, 0, 0),
    (5, enums.EN_SOLDIER1, enums.EM_CHASER, 4, 19, 0, 0),
    (5, enums.EN_SOLDIER1, enums.EM_CHASER, 12, 4, 0, 0),

    #-----------LEVEL 3-------------
    #
    # types:    6) SKIER
    #           7) BOAR
    #           8) SOLDIER2
    # 6 ---------------------------------------------------------------
    (6, enums.EN_SKIER, enums.EM_VERTICAL_LOOP, 24, -1, 24, 40),
    (6, enums.EN_BOAR, enums.EM_RANDOM, 10, 26, 0, 0),
    (6, enums.EN_BOAR, enums.EM_RANDOM, 23, 25, 0, 0),
    (6, enums.EN_BOAR, enums.EM_RANDOM, 10, 7, 0, 0),
    (6, enums.EN_BOAR, enums.EM_RANDOM, 24, 8, 0, 0),
    (6, enums.EN_BOAR, enums.EM_RANDOM, 6, 15, 0, 0),
    (6, enums.EN_SOLDIER2, enums.EM_CHASER, 16, 16, 0, 0),
    # 7 ---------------------------------------------------------------
    (7, enums.EN_SKIER, enums.EM_VERTICAL_LOOP, 2, -1, 2, 40),
    (7, enums.EN_SKIER, enums.EM_VERTICAL_LOOP, 27, -1, 27, 40),
    (7, enums.EN_BOAR, enums.EM_RANDOM, 22, 36, 0, 0),
    (7, enums.EN_BOAR, enums.EM_RANDOM, 23, 20, 0, 0),
    (7, enums.EN_BOAR, enums.EM_RANDOM, 14, 3, 0, 0),
    (7, enums.EN_BOAR, enums.EM_RANDOM, 5, 20, 0, 0),
    (7, enums.EN_BOAR, enums.EM_RANDOM, 17, 2, 0, 0),
    (7, enums.EN_SOLDIER2, enums.EM_CHASER, 15, 12, 0, 0),
    (7, enums.EN_SOLDIER2, enums.EM_CHASER, 15, 28, 0, 0),
    # 8 ---------------------------------------------------------------
    (8, enums.EN_SKIER, enums.EM_VERTICAL_LOOP, 9, -1, 9, 40),
    (8, enums.EN_SKIER, enums.EM_VERTICAL_LOOP, 24, -1, 24, 40),
    (8, enums.EN_BOAR, enums.EM_RANDOM, 12, 28, 0, 0),
    (8, enums.EN_BOAR, enums.EM_RANDOM, 1, 23, 0, 0),
    (8, enums.EN_BOAR, enums.EM_RANDOM, 19, 4, 0, 0),
    (8, enums.EN_BOAR, enums.EM_RANDOM, 26, 24, 0, 0),
    (8, enums.EN_BOAR, enums.EM_RANDOM, 17, 34, 0, 0),
    (8, enums.EN_BOAR, enums.EM_RANDOM, 2, 32, 0, 0),
    (8, enums.EN_BOAR, enums.EM_RANDOM, 28, 32, 0, 0),
    (8, enums.EN_SOLDIER2, enums.EM_CHASER, 26, 13, 0, 0),
    (8, enums.EN_SOLDIER2, enums.EM_CHASER, 7, 4, 0, 0),
    (8, enums.EN_SOLDIER2, enums.EM_CHASER, 7, 9, 0, 0),
    (8, enums.EN_SOLDIER2, enums.EM_CHASER, 7, 14, 0, 0),]

# hotspot data
HOTSPOT_DATA = [
    # Type            Map
    [enums.HS_LIFE,   0],
    [enums.HS_LIFE,   0],
    [enums.HS_AMMO,   0],
    [enums.HS_AMMO,   0],
    [enums.HS_SHIELD, 0],
    [enums.HS_SHIELD, 0],
    [enums.HS_BEACON, 0],
    [enums.HS_BEACON, 0],

    [enums.HS_LIFE,   1],
    [enums.HS_LIFE,   1],
    [enums.HS_AMMO,   1],
    [enums.HS_AMMO,   1],
    [enums.HS_SHIELD, 1],
    [enums.HS_BEACON, 1],

    [enums.HS_LIFE,   2],
    [enums.HS_AMMO,   2],
    [enums.HS_SHIELD, 2],
    [enums.HS_BEACON, 2],

    # -------------------

    [enums.HS_LIFE,   3],
    [enums.HS_LIFE,   3],
    [enums.HS_AMMO,   3],
    [enums.HS_AMMO,   3],
    [enums.HS_SHIELD, 3],
    [enums.HS_BEACON, 3],
    
    [enums.HS_LIFE,   4],
    [enums.HS_AMMO,   4],
    [enums.HS_AMMO,   4],
    [enums.HS_BEACON, 4],
    
    [enums.HS_AMMO,   5],
    [enums.HS_AMMO,   5],
    [enums.HS_SHIELD, 5],
    [enums.HS_SHIELD, 5],
    [enums.HS_SHIELD, 5],
    [enums.HS_BEACON, 5],
    
    # -------------------

    [enums.HS_LIFE,   6],
    [enums.HS_LIFE,   6],
    [enums.HS_AMMO,   6],
    [enums.HS_SHIELD, 6],
    [enums.HS_BEACON, 6],
    
    [enums.HS_LIFE,   7],
    [enums.HS_AMMO,   7],
    [enums.HS_AMMO,   7],
    [enums.HS_SHIELD, 7],
    [enums.HS_BEACON, 7],
        
    [enums.HS_SHIELD, 8],
    [enums.HS_SHIELD, 8],
    [enums.HS_SHIELD, 8],
    [enums.HS_AMMO,   8],
    [enums.HS_AMMO,   8],
    [enums.HS_BEACON, 8],]

# paths
FX_PATH = 'sounds/fx/'
MUS_PATH = 'sounds/music/'
FNT_PATH = 'images/fonts/'
SPR_PATH = 'images/sprites/'
ASS_PATH = 'images/assets/'

# colour palette (similar to Pico8 tones)
# 0 = darker, 1 = original, 2 = lighter
PALETTE = {
    'BLACK0': (0, 0, 0),
    'BLACK1': (1, 1, 1),
    'BLACK2': (45, 45, 45),
    
    'DARK_BLUE0' : (0, 0, 33),
    'DARK_BLUE1' : (29, 43, 83),
    'DARK_BLUE2' : (74, 88, 128),
    
    'PURPLE0' : (76, 0, 33),
    'PURPLE1' : (126, 37, 83),
    'PURPLE2' : (171, 82, 128),
    
    'DARK_GREEN0' : (0, 85, 31),
    'DARK_GREEN1' : (0, 135, 81),
    'DARK_GREEN2' : (45, 180, 126),
    
    'BROWN0' : (121, 32, 4),
    'BROWN1' : (171, 82, 54),
    'BROWN2' : (216, 127, 99),

    'DARK_GRAY0' : (45, 37, 29),
    'DARK_GRAY1' : (95, 87, 79),
    'DARK_GRAY2' : (140, 132, 124),
    
    'GRAY0' : (144, 145, 149),
    'GRAY1' : (194, 195, 199),
    'GRAY2' : (239, 240, 244),

    'WHITE0' : (205, 191, 182),
    'WHITE1' : (255, 241, 232),
    'WHITE2' : (250, 250, 250),
    
    'RED0' : (205, 0, 27),
    'RED1' : (255, 0, 77),
    'RED2' : (250, 45, 122),

    'ORANGE0' : (205, 113, 0),
    'ORANGE1' : (255, 163, 0),
    'ORANGE2' : (250, 208, 45),
    
    'YELLOW0' : (205, 186, 0),
    'YELLOW1' : (225, 200, 20),
    'YELLOW2' : (250, 250, 84),
    
    'GREEN0' : (0, 178, 4),
    'GREEN1' : (0, 228, 54),
    'GREEN2' : (45, 250, 99),
    
    'CYAN0' : (0, 123, 205),
    'CYAN1' : (41, 173, 255),
    'CYAN2' : (86, 218, 250),

    'MALVA0' : (81, 68, 106),
    'MALVA1' : (131, 118, 156),
    'MALVA2' : (172, 163, 201),
    
    'PINK0' : (205, 69, 118),
    'PINK1' : (255, 119, 168),
    'PINK2' : (250, 164, 213),
    
    'SAND0' : (205, 154, 120),
    'SAND1' : (255, 204, 170),
    'SAND2' : (250, 249, 215)}

# end-of-level messages (title, message)
END_LEVEL_MESSAGES = [
    ('Well done, Sergeant!', 'All mines in the level have been defused!'),
    ('Excellent work!', 'Level cleared with precision and determination!'),
    ('Mission accomplished!', 'All mines have been neutralised!'),
    ('Good work, Sergeant!', 'The area has been completely secured!'),
    ('Congratulations!', "You're an expert in bomb disposal!"),
    ('Objective achieved!', 'Level completed successfully!')]

# help for the main menu
HELP = (
    'Mark all the mines in each level with the available beacons '
    'as quickly as possible to clear the way for your troops. '
    'To do this, use the proximity information displayed on the screen. '
    'Watch out! A horde of enemies are waiting to get in your way...')

# credits for the main menu
CREDITS = (
    'Mine Squad Pi v1.1 (2026)     '
    'PROGRAMMING: salvaKantero     '
    'GRAPHICS: salvaKantero     '
    'MENU MUSIC: SigmaMusicArt     '
    'IN-GAME MUSIC: Spring Spring, Jonathan Shaw, Otto Halmen, HitCtrl, TheMightyRager, Beau Buckley, Umplix     '
    'SOUND EFFECTS: Juhani Junkala     '
    'BETA TESTING: lou_314     '
    'ACKNOWLEDGEMENTS: DaFluffyPotato, Rik Cross, Clear Code YT channel, '
    'Mark Vanstone, Ryan Lambie, Kenney...     '
    'PYTHON SOURCE CODE AND RESOURCES AVAILABLE AT https://github.com/salvakantero/MineSquadPi     '
    'Thanks for playing!!')
