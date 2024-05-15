
# ==============================================================================
# .::Constants::.
# Values that do not change are named to clarify the source code.
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

import enums

# game screen
WIN_SIZE = 800, 640 # main window size (windowed mode)
TILE_SIZE = 16 # size of each tile in pixels (square, 16*16)
MENU_SCALED_SIZE = 720, 594 # menu size scaled x3 (windowed mode)
MENU_UNSCALED_SIZE = 240, 198 # menu size (unscaled)
MAP_SCALED_SIZE = 720, 480 # map size scaled x3 (windowed mode)
MAP_UNSCALED_SIZE = 240, 160 # map size (unscaled)
MAP_TILE_SIZE = 15, 10 # map size in tiles
SBOARD_SCALED_SIZE = 720, 114 # scoreboard size scaled x3 (windowed mode)
SBOARD_UNSCALED_SIZE = 240, 38 # scoreboard size (unscaled)
H_MARGIN = 40 # horizontal distance between the edge and the playing area (windowed mode)
V_MARGIN = 20 # vertical distance between the edge and the playing area (windowed mode)
NUM_MINES = 5, 6, 8, 10, 12 # number of mines per map

# player
TIME_REMAINING = 20000 # remaining shield and x-rays time (+-20 secs.)
MAX_AMMO = 50 # maximum number of bullets
AMMO_ROUND = 20 # bullets per reload
ANIM_SPEED_IDLE = 16 # loops between each frame change
ANIM_SPEED_WALK = 6 # loops between each frame change in walking state
# XY starting position
PLAYER_X_INI = (MAP_UNSCALED_SIZE[0] // 2) - (TILE_SIZE // 2)
PLAYER_Y_INI = MAP_UNSCALED_SIZE[1] - TILE_SIZE


# animated tiles
#ANIM_TILES = {
#    # frame_1   frame_2
#    'T4.png' : 'T80.png',   # computer 1
#    'T8.png' : 'T81.png',   # computer 2
#    'T9.png' : 'T82.png',   # corpse
#    'T70.png' : 'T83.png',  # toxic waste
#    'T71.png' : 'T84.png'   # lava
#}


# colour palette (similar to Pico8 tones)
# 0 = darker, 1 = original, 2 = lighter
PALETTE = {
    'BLACK0': (0, 0, 0),
    'BLACK1': (25, 25, 25),
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
    
    'RED0' : (255, 0, 27),
    'RED1' : (255, 0, 77),
    'RED2' : (250, 45, 122),

    'ORANGE0' : (205, 113, 0),
    'ORANGE1' : (255, 163, 0),
    'ORANGE2' : (250, 208, 45),
    
    'YELLOW0' : (205, 186, 0),
    'YELLOW1' : (255, 236, 39),
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
    'SAND2' : (250, 249, 215)
}

# enemies per map (x1, y1, x2, y2, vx, vy, type)
# types:
#	1) SCORPION 
#   2) SNAKE
#   3) SOLDIER1
#   4) CRAB
#   5) PROJECTILE
#   6) SOLDIER2
#   7) HABALI
#   8) WOLF
#   9) SOLDIER3
#  10) CITIZEN1
#  11) CITIZEN2
#  12) SOLDIER4
ENEMIES_DATA = [
    #-----------LEVEL 1-------------
    # 0
    (128, 112, 32, 112, -1, 0, 1),
	(16, 16, 224, 48, 1, 1, 2),
	(0, 0, 0, 0, 0, 0, 0),
    # 1
	(192, 112, 32, 112, -2, 0, 1),
	(208, 16, 144, 64, -.5, .5, 2),
	(80, 64, 80, 16, 0, -1, 3),
    # 2
	(112, 144, 112, 32, 0, -1, 4),
	(208, 112, 16, 80, -1, -1, 2),
	(0, 0, 0, 0, 0, 0, 0),
    # 3
	(160, 48, 32, 48, -2, 0, 1),
	(16, 80, 208, 112, 2, 2, 3),
	(0, 0, 0, 0, 0, 0, 0),
    # 4
	(64, 80, 64, 16, 0, -1, 3),
	(144, 16, 144, 128, 0, 1, 3),
	(208, 112, 208, 96, 0, 0, 5),
  
    #-----------LEVEL 2-------------
    # 5
    (32, 96, 32, 112, 0, 0, 5),
	(192, 16, 128, 128, -1, 1, 2),
	(0, 0, 0, 0, 0, 0, 0),
    # 6
    (176, 48, 64, 48, -.5, 0, 1),
	(48, 128, 32, 16, -1, -1, 3),
	(64, 48, 176, 48, 1, 0, 1),
    # 7
    (64, 16, 80, 128, 1, 1, 2),
	(96, 32, 160, 32, 1, 0, 1),
	(16, 96, 16, 16, 0, -1, 3),
    # 8
    (48, 112, 208, 80, 1, -1, 2),
	(192, 48, 48, 16, -2, -2, 2),
	(16, 80, 16, 16, 0, -.5, 3),
    # 9
	(32, 48, 192, 48, 1, 0, 1),
	(160, 112, 112, 112, -1, 0, 1),
    (192, 48, 32, 48, -1, 0, 1),

    #-----------LEVEL 3-------------
    # 10
	(80, 128, 112, 128, 0, 0, 5),
	(112, 112, 144, 112, 1, 0, 2),
	(0, 0, 0, 0, 0, 0, 0),
    # 11
	(192, 64, 32, 32, -1, -1, 2),
	(48, 128, 224, 112, 1, -1, 2),
	(16, 64, 32, 64, 0, 0, 5),
    # 12
	(160, 128, 160, 16, 0, -2, 3),
	(112, 32, 112, 128, 0, 2, 3),
	(64, 128, 16, 16, -2, -2, 2),
    # 13
	(176, 96, 32, 96, -2, 0, 1),
	(32, 64, 192, 64, 1, 0, 1),
	(192, 32, 64, 32, -2, 0, 1),
    # 14
	(64, 16, 64, 128, 0, 2, 3),
	(112, 128, 112, 16, 0, -2, 3),
	(16, 112, 16, 16, 0, -2, 3),

    #-----------LEVEL 4-------------
    # 15
	(112, 144, 112, 32, 0, -1, 4),
	(208, 144, 16, 48, -.5, -.5, 3),
	(128, 16, 128, 144, 0, 2, 3),
    # 16
	(160, 128, 96, 128, -1, 0, 3),
	(208, 128, 208, 96, 0, -.5, 3),
	(80, 112, 128, 112, .5, 0, 0),
    # 17
	(64, 128, 48, 32, -1, -1, 2),
	(208, 128, 208, 32, 0, -2, 3),
	(128, 32, 160, 112, 1, 1, 2),
    # 18
	(16, 32, 32, 128, 1, 1, 2),
	(128, 128, 128, 32, 0, -2, 3),
	(160, 32, 160, 128, 0, 2, 3),
    # 19
	(48, 32, 192, 64, 2, 2, 2),
	(48, 128, 192, 128, 2, 0, 1),
	(192, 96, 64, 96, -1, 0, 1),
]

# hotspot data
# index = map number; (type, x, y, visible?)
HOTSPOT_DATA = [
    [enums.AMMO, 13, 3, True],
    [enums.SHIELD, 13, 7, True],
    [enums.SHIELD, 1, 7, True],
    [enums.XRAY, 13, 1, True],
    [enums.XRAY, 7, 8, True],
    [enums.SHIELD, 5, 3, True],
    [enums.AMMO, 11, 3, True],
    [enums.SHIELD, 13, 6, True],
    [enums.XRAY, 6, 8, True],
    [enums.SHIELD, 6, 1, True],
    [enums.AMMO, 8, 4, True],
    [enums.SHIELD, 2, 8, True],
    [enums.XRAY, 13, 3, True],
    [enums.XRAY, 12, 2, True],
    [enums.AMMO, 1, 7, True],
    [enums.SHIELD, 1, 3, True],
    [enums.AMMO, 13, 4, True],
    [enums.AMMO, 8, 2, True],
    [enums.SHIELD, 13, 6, True],
    [enums.XRAY, 1, 8, True],
    [enums.SHIELD, 7, 2, True],
    [enums.AMMO, 1, 5, True],
    [enums.SHIELD, 7, 8, True],
    [enums.XRAY, 7, 8, True],
    [enums.AMMO, 1, 6, True],
    [enums.XRAY, 6, 7, True],
    [enums.SHIELD, 2, 3, True],
    [enums.XRAY, 12, 6, True],
    [enums.SHIELD, 12, 1, True],
    [enums.AMMO, 6, 1, True],
    [enums.SHIELD, 13, 4, True],
    [enums.SHIELD, 3, 2, True],
    [enums.AMMO, 4, 6, True],
    [enums.SHIELD, 9, 8, True],
]   

# help for the main menu
HELP = 'Select (START NEW GAME) to start a game from the beginning '
HELP += 'or (CONTINUE GAME) to continue the previous game from the last completed level! '
HELP += '(ESC) to exit...'

# credits for the main menu
CREDITS  = 'Mine Squad Pi v1.0 (2024)     '
CREDITS += 'PROGRAMMING: salvaKantero     '
CREDITS += 'GRAPHICS: salvaKantero     '
CREDITS += 'MENU MUSIC: SigmaMusicArt     '
CREDITS += 'IN-GAME MUSIC: ?????     '
CREDITS += 'SOUND EFFECTS: ?????     '
CREDITS += 'ACKNOWLEDGEMENTS: DaFluffyPotato, Rik Cross, Clear Code YT channel, '
CREDITS += 'Mark Vanstone, Ryan Lambie, Mundo Python YT channel, Kenney...     '
CREDITS += 'SOME IMAGES OF THIS GAME HAVE BEEN GENERATED BY MICROSOFT COPILOT!     '
CREDITS += 'PYTHON SOURCE CODE AND RESOURCES AVAILABLE AT https://github.com/salvakantero/MineSquadPi     '
CREDITS += 'Thanks for playing!!'
