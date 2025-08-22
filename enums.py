
# ==============================================================================
# .::Enumerations::.  (false enumerations, in fact)
# Values that are named to clarify the source code.
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

# game states
GS_RUNNING, GS_OVER = 0, 1

# music states
MS_UNMUTED, MS_MUTED = 0, 1

# players
PL_BLAZE, PL_PIPER = 0, 1

# player states
PS_IDLE_UP, PS_IDLE_DOWN, PS_IDLE_LEFT, PS_IDLE_RIGHT, \
PS_WALK_UP, PS_WALK_DOWN, PS_WALK_LEFT, PS_WALK_RIGHT = 0, 1, 2, 3, 4, 5, 6, 7

#coordinate axes
CA_HORIZONTAL, CA_VERTICAL = 0, 1

# directions of movement
DI_UP, DI_DOWN, DI_LEFT, DI_RIGHT = 0, 1, 2, 3

# map data [tile types]
TT_NO_ACTION, TT_OBSTACLE, TT_MINE, TT_KILLER = 0, 1, 2, 3

# map data [mines info]
MI_MINE, MI_FREE, MI_BEACON = -1, 0, 9 # proximity: 1,2,3,4,5,6,7,8

# enemy types
EN_SCORPION, EN_SNAKE, EN_SOLDIER1, EN_CRAB, EN_PROJECTILE, EN_SOLDIER2, EN_SKIER, \
EN_HABALI, EN_SOLDIER3 = 0, 1, 2, 3, 4, 5, 6, 7, 8

# enemy movement patterns
EM_HORIZONTAL, EM_VERTICAL, EM_RANDOM, EM_PURSUER = 0, 1, 2, 3

# hotspots
HS_LIFE, HS_SHIELD, HS_AMMO, HS_CANDY, HS_APPLE, HS_CHOCO, HS_COIN = 0, 1, 2, 3, 4, 5, 6

# fonts; S=small L=large / F=foreground B=background
S_F_BROWN, S_B_BROWN, S_F_WHITE, S_B_WHITE, S_F_GREEN, S_B_GREEN, L_F_WHITE, L_B_WHITE, \
L_F_RED, L_B_BLACK, L_F_BROWN, L_B_BROWN = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

# menu options
MO_START, MO_SETTINGS, MO_EXIT, MO_SCREEN_MODE, MO_SCANLINES, \
MO_CONTROL, MO_EXIT_SETTINGS = 0, 1, 2, 3, 4, 5, 6

# control types
CT_CLASSIC, CT_GAMER, CT_RETRO, CT_JOYSTICK, CT_COMMON = 0, 1, 2, 3, 4

# sprite groups
SG_BLASTS, SG_ENEMIES, SG_HOTSPOT, SG_SHOT = 0, 1, 2, 3

# screen modes
SM_WINDOW, SM_4_3, SM_16_9 = 0, 1, 2

