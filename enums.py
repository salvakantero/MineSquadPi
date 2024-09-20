
# ==============================================================================
# .::Enumerations::.  (false enumerations, in fact)
# Values that are named to clarify the source code.
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

# game states
GS_RUNNING, GS_OVER = 0, 1

# music states
MS_UNMUTED, MS_MUTED = 0, 1

# players
PL_BLAZE, PL_PIPER, PL_NORMAN = 0, 1, 2

# player states
PS_IDLE_UP, PS_IDLE_DOWN, PS_IDLE_LEFT, PS_IDLE_RIGHT, \
PS_WALK_UP, PS_WALK_DOWN, PS_WALK_LEFT, PS_WALK_RIGHT = 0, 1, 2, 3, 4, 5, 6, 7

#coordinate axes
CA_HORIZONTAL, CA_VERTICAL = 0, 1

# directions of movement
D_UP, D_DOWN, D_LEFT, D_RIGHT = 0, 1, 2, 3

# tile behaviours
TB_NO_ACTION, TB_OBSTACLE, TB_MINE, TB_ITEM, TB_KILLER = 0, 1, 2, 3, 4

# map data [mines]
MD_MINE, MD_FREE, MD_FLAG = -1, 0, 9

# enemy types
NONE, SCORPION, SNAKE, SOLDIER1, CRAB, PROJECTILE, SOLDIER2, HABALI, \
WOLF, SOLDIER3, CITIZEN1, CITIZEN2, SOLDIER4 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12

# hotspot types
SHIELD, BIN, AMMO, LIFE, SWEET1, SWEET2, COIN, CHOCO = 0, 1, 2, 3, 4, 5, 6, 7

# fonts; S=small L=large F=foreground B=background
S_F_BROWN, S_B_BROWN, S_F_WHITE, S_B_WHITE, S_F_GREEN, S_B_GREEN, L_F_WHITE, L_B_WHITE, \
L_F_RED, L_B_BLACK, L_F_BROWN, L_B_BROWN = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

# menu
MO_START, MO_LOAD, MO_OPTIONS, MO_EXIT, MO_SCREEN_MODE, MO_SCANLINES, MO_VIEW, \
MO_CONTROL, MO_EXIT_OPTIONS = 0, 1, 2, 3, 4, 5, 6, 7, 8

# keyboard control types
CT_CLASSIC, CT_GAMER, CT_RETRO, CT_JOYSTICK = 0, 1, 2, 3

# sprite groups
SG_ALL, SG_ENEMIES, SG_HOTSPOT, SG_SHOT = 0, 1, 2, 3

# screen modes
SM_WINDOW, SM_X600, SM_X720 = 0, 1, 2

# views
V_ISO, V_ZENITH = 0, 1
