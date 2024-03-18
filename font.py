
# ==============================================================================
# .::Font class::.
# Faster and sharper at lower resolutions than the original FONT class.
# Is a slight adaptation of the original DaFluffyPotato source code.
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

import pygame

# creates a new font from an image path and a colour
class Font():
    def __init__(self, path, color, transparent):
        self.path = path
        self.color = color
        self.transparent = transparent # does not erase the background if True
        self.letters, self.letter_spacing, self.line_height = self.load_font_img()
        self.font_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e',
        'f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w',
        'x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5',
        '6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        self.space_width = self.letter_spacing[0]
        self.base_spacing = 1
        self.line_spacing = 2


    # change one colour for another
    def swap_color(self, image, old_color, new_color):
        image.set_colorkey(old_color)
        surf = image.copy()
        surf.fill(new_color)
        surf.blit(image,(0,0))
        return surf


    # returns a part of the surface
    def clip(self, surf, x, y, x_size, y_size):
        handle_surf = surf.copy()
        handle_surf.set_clip(pygame.Rect(x, y, x_size, y_size))
        image = surf.subsurface(handle_surf.get_clip())
        return image.copy()


    # generates the letters (and letter spacing) from the font image
    def load_font_img(self):
        fg_color = (255, 0, 0) # original red
        bg_color = (0, 0, 0) # black
        font_img = pygame.image.load(self.path).convert() # load font image
        font_img = self.swap_color(font_img, fg_color, self.color) # apply the requested font colour
        last_x = 0
        letters = []
        letter_spacing = []
        for x in range(font_img.get_width()): # for the entire width of the image
            if font_img.get_at((x, 0))[0] == 127: # gray separator
                # saves in the array the portion of the image with the letter we are interested in.
                letters.append(self.clip(font_img, last_x, 0, x - last_x, font_img.get_height()))
                # saves the width of the letter
                letter_spacing.append(x - last_x)
                last_x = x + 1
            x += 1
        if self.transparent:
            # erases the background colour of each letter in the array
            for letter in letters:
                letter.set_colorkey(bg_color) 

        return letters, letter_spacing, font_img.get_height()


    # draw the text
    def render(self, text, surf, loc):
        x_offset = 0
        y_offset = 0
        for char in text:
            if char not in ['\n', ' ']:
                # draw the letter and add the width
                surf.blit(self.letters[self.font_order.index(char)], (loc[0] + x_offset, loc[1] + y_offset))
                x_offset += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            elif char == ' ':
                x_offset += self.space_width + self.base_spacing
            else: # line feed
                y_offset += self.line_spacing + self.line_height
                x_offset = 0