
# ==============================================================================
# .::KeyboardRGB class::.
# Manages RGB lighting effects for Raspberry Pi 500+ keyboard
# ==============================================================================
#
#  This file is part of "Mine Squad Pi". Copyright (C) 2026 @salvakantero
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

# HSV colors (hue 0-255, saturation 0-255, value/brightness 0-255)
RGB_OFF = (0, 0, 0)
RGB_GREEN = (85, 255, 255)      # control keys
RGB_CYAN = (128, 255, 255)      # action keys (fire, beacon)
RGB_RED = (0, 255, 255)         # mine explosion
RGB_ORANGE = (21, 255, 255)     # enemy/hazard damage
RGB_BLUE = (170, 255, 255)      # beacon placed



class KeyboardRGB():
    # mapping from pygame key constants to Pi 500+ key names
    PYGAME_TO_KEYNAME = {
        # arrow keys
        pygame.K_UP: 'UP', pygame.K_DOWN: 'DOWN',
        pygame.K_LEFT: 'LEFT', pygame.K_RIGHT: 'RIGHT',
        # WASD
        pygame.K_w: 'W', pygame.K_a: 'A', pygame.K_s: 'S', pygame.K_d: 'D',
        # QAOP (retro)
        pygame.K_q: 'Q', pygame.K_o: 'O', pygame.K_p: 'P',
        # action keys
        pygame.K_SPACE: 'SPC', pygame.K_b: 'B',
        pygame.K_COMMA: 'COMM', pygame.K_m: 'M'
    }

    def __init__(self, is_pi500plus):
        self.available = False
        self.keyboard = None
        self.saved_leds = None
        self.saved_effect = None
        self.key_to_led_idx = {}        # maps key names to LED indices
        self.control_led_indices = []   # LED indices for current control keys

        if not is_pi500plus:
            return

        try:
            from RPiKeyboardConfig import RPiKeyboardConfig
            self.keyboard = RPiKeyboardConfig()
            self.available = True
            self._build_key_mapping()
        except ImportError:
            pass


    # builds the mapping from key names to LED indices
    def _build_key_mapping(self):
        try:
            all_keys = self.keyboard.get_all_keynames(layer=0)
            for key_info in all_keys:
                name = key_info.get('name', '')
                position = key_info.get('position', None)
                if name and position:
                    led_idx = self.keyboard.led_matrix_to_idx(position)
                    if led_idx is not None:
                        self.key_to_led_idx[name] = led_idx
        except Exception:
            pass


    # saves the current RGB configuration to restore it later
    def save_state(self):
        if not self.available:
            return
        try:
            self.saved_leds = self.keyboard.get_current_direct_leds()
            self.saved_effect = self.keyboard.get_current_effect()
        except Exception:
            self.saved_leds = None
            self.saved_effect = None


    # restores the previously saved RGB configuration
    def restore_state(self):
        if not self.available or self.saved_leds is None:
            return
        try:
            # restore each LED to its saved state
            for idx, (h, s, v) in enumerate(self.saved_leds):
                self.keyboard.set_led_by_idx(idx=idx, colour=(h, s, v))
            self.keyboard.send_leds()
        except Exception:
            pass


    # converts a pygame key constant to LED index
    def _pygame_key_to_led_idx(self, pygame_key):
        key_name = self.PYGAME_TO_KEYNAME.get(pygame_key)
        if key_name:
            return self.key_to_led_idx.get(key_name)
        return None


    # turns off all keyboard LEDs
    def clear_all(self):
        if not self.available:
            return
        try:
            for idx in range(len(self.key_to_led_idx)):
                self.keyboard.set_led_by_idx(idx=idx, colour=RGB_OFF)
            self.keyboard.send_leds()
        except Exception:
            pass


    # lights up the control keys based on current configuration
    def light_control_keys(self, config):
        if not self.available:
            return
        try:
            # clear all LEDs first
            self.clear_all()

            # collect control keys to illuminate
            control_keys = [
                config.up_key, config.down_key,
                config.left_key, config.right_key
            ]
            action_keys = [
                config.fire_key, config.beacon_key, config.beacon_key2
            ]

            # store LED indices for control keys (to preserve during effects)
            self.control_led_indices = []

            # light control keys in green
            for pygame_key in control_keys:
                led_idx = self._pygame_key_to_led_idx(pygame_key)
                if led_idx is not None:
                    self.control_led_indices.append(led_idx)
                    self.keyboard.set_led_by_idx(idx=led_idx, colour=RGB_GREEN)

            # light action keys in cyan
            for pygame_key in action_keys:
                led_idx = self._pygame_key_to_led_idx(pygame_key)
                if led_idx is not None:
                    self.control_led_indices.append(led_idx)
                    self.keyboard.set_led_by_idx(idx=led_idx, colour=RGB_CYAN)

            self.keyboard.send_leds()
        except Exception:
            pass


    # generic flash effect (color on all non-control keys)
    def _flash_effect(self, colour):
        if not self.available:
            return
        try:
            # get total number of LEDs
            total_leds = len(self.keyboard.get_current_direct_leds())
            # light all keys in the specified color except control keys
            for idx in range(total_leds):
                if idx not in self.control_led_indices:
                    self.keyboard.set_led_by_idx(idx=idx, colour=colour)
            self.keyboard.send_leds()
        except Exception:
            pass


    # flash effect for mine explosion (red on all non-control keys)
    def effect_mine_explosion(self):
        self._flash_effect(RGB_RED)


    # flash effect for enemy/hazard damage (orange on all non-control keys)
    def effect_enemy_damage(self):
        self._flash_effect(RGB_ORANGE)


    # flash effect for beacon placed (blue on all non-control keys)
    def effect_beacon(self):
        self._flash_effect(RGB_BLUE)


    # restore control keys after an effect (turns off non-control keys)
    def effect_end(self):
        if not self.available:
            return
        try:
            # get total number of LEDs
            total_leds = len(self.keyboard.get_current_direct_leds())
            # turn off all non-control keys
            for idx in range(total_leds):
                if idx not in self.control_led_indices:
                    self.keyboard.set_led_by_idx(idx=idx, colour=RGB_OFF)
            self.keyboard.send_leds()
        except Exception:
            pass