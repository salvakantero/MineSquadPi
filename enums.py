
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

# tile behaviours
NO_ACTION, OBSTACLE, PLATFORM_TILE, ITEM, KILLER, DOOR = 0, 1, 2, 3, 4, 5 
# game states
RUNNING, OVER = 0, 1
# directions of movement
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
# music states
UNMUTED, MUTED = 0, 1
# player states
IDLE, WALKING_X, WALKING_Y = 0, 1, 2
# enemy types
NONE, INFECTED, PELUSOID, AVIRUS, PLATFORM_SPR, FANTY = 0, 1, 2, 3, 4, 5
# fanty enemy states
IDLE, CHASING, RETREATING = 0, 1, 2
# hotspot types
SHIELD, XRAY, AMMO, CHECKPOINT, BURGER, CAKE, DONUT = 0, 1, 2, 3, 4, 5, 6
# fonts; S=small L=large F=foreground B=background
S_F_BROWN, S_B_BROWN, S_F_WHITE, S_B_WHITE, L_F_WHITE, L_B_WHITE, L_F_RED, L_B_RED, L_F_BROWN, L_B_BROWN = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# menu
START, LOAD, OPTIONS, EXIT, FULLSCREEN, SCANLINES, VIEW, CONTROL, EXIT_OPTIONS = 0, 1, 2, 3, 4, 5, 6, 7, 8
# keyboard control types
CLASSIC, GAMER, RETRO, JOYSTICK = 0, 1, 2, 3
# sprite groups
ALL, ENEMIES, HOTSPOT, PLATFORM, SHOT = 0, 1, 2, 3, 4
# full screen modes
OFF, X600, X720 = 0, 1, 2
# views
ISO, ZENITH = 0, 1