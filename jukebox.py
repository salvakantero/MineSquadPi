
# ==============================================================================
# .::Jukebox class::.
# Create a playlist with the tracks randomly shuffled
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
import random



class Jukebox():
    # class constants
    DEFAULT_VOLUME = 0.5
    FILE_EXTENSION = '.ogg'

    def __init__(self, path, base_filename, tracks, volume=DEFAULT_VOLUME):
        self.track_list = list(range(0, tracks)) # sorted playlist
        self.track_index = 0 # current theme song number
        self.path = path # path to the folder with the music tracks
        self.base_filename = base_filename # common name of the files
        # set volume once
        pygame.mixer.music.set_volume(volume)



    # generates a new random list of the x available tracks
    def shuffle(self):
        random.shuffle(self.track_list)
        self.track_index = 0



    def update(self):
        if not pygame.mixer.music.get_busy(): # if a track is not playing...
            self._load_next() # load in memory the following track
            pygame.mixer.music.play()
     


    ##### auxiliary functions #####

    # load the next track from the playlist
    # for example: 'sounds/music/'+'mus_ingame_'+'9' + '.ogg'
    def _load_next(self):
        track_num = self.track_list[self.track_index]
        pygame.mixer.music.load(f"{self.path}{self.base_filename}{track_num}{self.FILE_EXTENSION}")
        # next number in the playlist
        self.track_index = (self.track_index + 1) % len(self.track_list)
