
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
MAP_TILE_SIZE = 30, 40 # map size in tiles
MAP_PIXEL_SIZE = MAP_TILE_SIZE[0] * TILE_SIZE, MAP_TILE_SIZE[1] * TILE_SIZE # map size in pixels
H_MARGIN = 40 # horizontal distance between the edge and the playing area (windowed mode)
V_MARGIN = 20 # vertical distance between the edge and the playing area (windowed mode)
NUM_MINES =   20, 24, 28, 32, 36, 40, 44, 48, 52 # number of mines per map
NUM_BEACONS = 28, 28, 30, 38, 40, 42, 48, 50, 52 # number of flags/beacons per map
# player
TIME_REMAINING = 20000 # remaining shield time (approximately 20 seconds)
MAX_AMMO = 20 # maximum number of bullets
AMMO_ROUND = 10 # bullets per reload
ANIM_SPEED_IDLE = 16 # loops between each frame change
ANIM_SPEED_WALK = 6 # loops between each frame change in walking state
# XY starting position
PLAYER_X_INI = int(MAP_TILE_SIZE[0] // 4) * TILE_SIZE
PLAYER_Y_INI = (MAP_TILE_SIZE[1] - 1) * TILE_SIZE
# enemies
RANDOM_ENEMY_PAUSE_DURATION = 30 # duration of pause in frames
CHASER_ENEMY_PAUSE_DURATION = 60 # duration of pause in frames
CHASER_ACTIVATION_RANGE = 6  # the enemy activates when the player is X tiles or less away
ENEMY_RESPAWN_TIME = 10000  # time in milliseconds before enemy respawns (10 seconds)
ENEMY_RESPAWN_SAFE_DISTANCE = 5  # minimum distance in tiles between player and enemy respawn position
# SCORPION, SNAKE, SOLDIER1, CRAB, PROJECTILE, SOLDIER2, SKIER, WILDBOAR, SOLDIER3
ENEMY_LIFE = 1, 1, 2, 2, 3, 3, 2, 3, 4
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

# enemies per map (map, type, movement, tile_x1, tile_y1, tile_x2, tile_y2)
ENEMIES_DATA = [
    #-----------STAGE 1-------------
    #
    # types:    1) SCORPION 
    #           2) SNAKE 
    #           3) SOLDIER1
    # 0
    (0, enums.EN_SCORPION, enums.EM_HORIZONTAL, 2, 36, 13, 36),
    (0, enums.EN_SCORPION, enums.EM_VERTICAL, 23, 2, 23, 34),
    (0, enums.EN_SNAKE, enums.EM_RANDOM, 25, 5, 0, 0),
    (0, enums.EN_SOLDIER0, enums.EM_CHASER, 5, 5, 0, 0),
    # 1
    (1, enums.EN_SCORPION, enums.EM_HORIZONTAL, 2, 35, 13, 35),
    (1, enums.EN_SCORPION, enums.EM_VERTICAL, 20, 35, 20, 10),
    (1, enums.EN_SNAKE, enums.EM_RANDOM, 25, 5, 0, 0),
    (1, enums.EN_SOLDIER0, enums.EM_CHASER, 5, 5, 0, 0),
    # 2
    (2, enums.EN_SCORPION, enums.EM_HORIZONTAL, 2, 35, 13, 35),
    (2, enums.EN_SCORPION, enums.EM_VERTICAL, 20, 35, 20, 10),
    (2, enums.EN_SNAKE, enums.EM_RANDOM, 25, 5, 0, 0),
    (2, enums.EN_SOLDIER0, enums.EM_CHASER, 5, 5, 0, 0),

    #-----------STAGE 2-------------
    #
    # types:    4) CRAB
    #           5) PROJECTILE
    #           6) SOLDIER2
    # 3
    (32, 96, 32, 112, 0, 0, 5),
    (192, 16, 128, 128, -1, 1, 2),
    # 4
    (176, 48, 64, 48, -.5, 0, 1),
    (48, 128, 32, 16, -1, -1, 3),
    (64, 48, 176, 48, 1, 0, 1),
    # 5
    (64, 16, 80, 128, 1, 1, 2),
    (96, 32, 160, 32, 1, 0, 1),
    (16, 96, 16, 16, 0, -1, 3),

    #-----------LEVEL 3-------------
    #
    # types:    7) SKIER
    #           8) BOAR
    #           9) SOLDIER3
    # 6
    (80, 128, 112, 128, 0, 0, 5),
    (112, 112, 144, 112, 1, 0, 2),
    # 7
    (192, 64, 32, 32, -1, -1, 2),
    (48, 128, 224, 112, 1, -1, 2),
    (16, 64, 32, 64, 0, 0, 5),
    # 8
    (160, 128, 160, 16, 0, -2, 3),
    (112, 32, 112, 128, 0, 2, 3),
    (64, 128, 16, 16, -2, -2, 2)]

# hotspot data
HOTSPOT_DATA = [
    # Type              Map
    [enums.HS_SHIELD,   0],
    [enums.HS_LIFE,     0],
    [enums.HS_AMMO,     0]]

# end-of-level messages (title, message)
END_LEVEL_MESSAGES = [
    ('Well done, Sergeant!', 'All mines in the level have been defused!'),
    ('Excellent work!', 'Level cleared with precision and determination!'),
    ('Mission accomplished!', 'All mines have been neutralised!'),
    ('Good work, Sergeant!', 'The area has been completely secured!'),
    ('Congratulations!', "You're an expert in bomb disposal!"),
    ('Objective achieved!', 'Level completed successfully!')]

# help for the main menu
HELP = 'Press a menu option to continue or ESC to exit...     '
HELP += 'Mark all the mines in each level with the available beacons '
HELP += 'as quickly as possible to clear the way for your troops. '
HELP += 'To do so, use the proximity information displayed on the screen. '
HELP += 'Watch out! a horde of enemies is waiting to make things difficult for you... '

# credits for the main menu
CREDITS  = 'Mine Squad Pi v1.0 (2025)     '
CREDITS += 'PROGRAMMING: salvaKantero     '
CREDITS += 'GRAPHICS: salvaKantero     '
CREDITS += 'MENU MUSIC: SigmaMusicArt     '
CREDITS += 'IN-GAME MUSIC: "Never Ceasing Militarism", "March", "National March of Quan and Raiku"'
CREDITS += ', "Some militaristic tune" by Spring Spring     '
CREDITS += '"The Tread of War", "Market on the Sea", "Cant Stop Winning" by Jonathan Shaw     '
CREDITS += '"Thunderchild" by Otto Halmen     "RPG title" by HitCtrl     '
CREDITS += '"Ashen" by TheMightyRager     "Battle" by Beau Buckley     "Game Over" by Umplix     '
CREDITS += 'SOUND EFFECTS: Juhani Junkala     '
CREDITS += 'ACKNOWLEDGEMENTS: DaFluffyPotato, Rik Cross, Clear Code YT channel, '
CREDITS += 'Mark Vanstone, Ryan Lambie, Kenney...     '
CREDITS += 'PYTHON SOURCE CODE AND RESOURCES AVAILABLE AT https://github.com/salvakantero/MineSquadPi     '
CREDITS += 'Thanks for playing!!'
