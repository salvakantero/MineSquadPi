
# ==============================================================================
# .::Enumerations::.  (false enumerations, in fact)
# Values that are named to clarify the source code.
# ==============================================================================
#
#  This file is part of "Red Planet Pi". Copyright (C) 2023 @salvakantero
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
IDLE, WALKING, JUMPING, FALLING = 0, 1, 2, 3
# enemy types (and platform)
NONE, INFECTED, PELUSOID, AVIRUS, PLATFORM_SPR, FANTY = 0, 1, 2, 3, 4, 5
# fanty enemy states
IDLE, CHASING, RETREATING = 0, 1, 2
# hotspot types
TNT, KEY, AMMO, OXYGEN, CHECKPOINT, BURGER, CAKE, DONUT, GATE_TILE = 0, 1, 2, 3, 4, 5, 6, 7, 8
# fonts; S=small L=large F=foreground B=background
S_F_GREEN, S_B_GREEN, S_F_WHITE, S_B_WHITE, L_F_WHITE, L_B_WHITE, L_F_SAND, L_B_SAND = 0, 1, 2, 3, 4, 5, 6, 7
# menu
START, LOAD, OPTIONS, EXIT, FULLSCREEN, SCANLINES, MAP_TRANSITION, CONTROL, EXIT_OPTIONS = 0, 1, 2, 3, 4, 5, 6, 7, 8
# keyboard control types
CLASSIC, GAMER, RETRO, JOYSTICK = 0, 1, 2, 3
# sprite groups
ALL, ENEMIES, HOTSPOT, GATE, PLATFORM, DUST, SHOT = 0, 1, 2, 3, 4, 5, 6
# full screen modes
OFF, X600, X720 = 0, 1, 2