
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
import threading
import time

from RPiKeyboardConfig.keyboard import Preset




# HSV colors (hue 0-255, saturation 0-255, value/brightness 0-255)
HSV_OFF = (0, 0, 0)
HSV_WHITE = (0, 0, 250) # control keys
HSV_CYAN = (128, 255, 250) # action keys
HSV_RED = (0, 255, 255) # mine explosion
HSV_ORANGE = (10, 250, 250) # enemy/hazard damage
HSV_GREEN = (85, 200, 255) # beacon placed
HSV_BLUE = (170, 255, 255) # hotspot



class KeyboardRGB():
    # mapping from pygame key constants to Pi 500+ key names
    PYGAME_TO_KEYNAME = {
        # arrow keys
        pygame.K_UP: 'KC_UP', pygame.K_DOWN: 'KC_DOWN',
        pygame.K_LEFT: 'KC_LEFT', pygame.K_RIGHT: 'KC_RIGHT',
        # WASD
        pygame.K_w: 'KC_W', pygame.K_a: 'KC_A', 
        pygame.K_s: 'KC_S', pygame.K_d: 'KC_D',
        # QAOP
        pygame.K_q: 'KC_Q', pygame.K_o: 'KC_O', 
        pygame.K_p: 'KC_P',
        # action keys
        pygame.K_SPACE: 'KC_SPACE', pygame.K_b: 'KC_B',
        pygame.K_COMMA: 'KC_COMMA', pygame.K_m: 'KC_M',
        pygame.K_ESCAPE: 'KC_ESCAPE'
    }


    def __init__(self, is_pi500plus):
        self.available = False
        self.keyboard = None
        self.saved_leds = None
        self.saved_effect = None
        self.key_to_led_idx = {}        # maps key names to LED indices
        self.control_led_indices = []   # LED indices for current control keys
        self.action_led_indices = []    # LED indices for current action keys

        if not is_pi500plus:
            return

        try:
            from RPiKeyboardConfig import RPiKeyboardConfig
            self.keyboard = RPiKeyboardConfig()
            self.available = True
            self._build_key_mapping()
        except Exception:
            pass


    # builds the mapping from key names to LED indices
    def _build_key_mapping(self):
        all_keys = self.keyboard.get_all_keynames(layer=0)
        for key_info in all_keys:
            name = key_info.get('name', '')
            position = key_info.get('position', None)
            if name and position:
                try:
                    led_idx = self.keyboard.led_matrix_to_idx(matrix=position)
                    self.key_to_led_idx[name] = led_idx
                except ValueError:
                    continue


    # enables direct LED control mode (required before setting individual LEDs)
    def enable_direct_mode(self):
        if not self.available:
            return
        try:
            self.keyboard.set_led_direct_effect()
        except Exception:
            pass


    # restores the previously saved RGB configuration
    def restore_state(self):
        if not self.available:
            return
        try:
            self.keyboard.revert_to_saved_preset()
        except Exception as e:
            print(f"Error restaurando estado: {e}")


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
            self.keyboard.set_led_direct_effect()
            total_leds = len(self.keyboard.get_current_direct_leds())
            for idx in range(total_leds):
                self.keyboard.set_led_by_idx(idx=idx, colour=HSV_OFF)
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
                config.fire_key, config.beacon_key, config.beacon_key2,
                config.mute_key, config.pause_key
            ]

            # store LED indices for control/action keys
            self.control_led_indices = []
            self.action_led_indices = []

            # light control keys in white
            for pygame_key in control_keys:
                led_idx = self._pygame_key_to_led_idx(pygame_key)
                if led_idx is not None:
                    self.control_led_indices.append(led_idx)
                    self.keyboard.set_led_by_idx(idx=led_idx, colour=HSV_WHITE)

            # light action keys in cyan
            for pygame_key in action_keys:
                led_idx = self._pygame_key_to_led_idx(pygame_key)
                if led_idx is not None:
                    self.action_led_indices.append(led_idx)
                    self.keyboard.set_led_by_idx(idx=led_idx, colour=HSV_CYAN)

            self.keyboard.send_leds()
        except Exception:
            pass


    # generic flash effect (color on all keys)
    def _flash_effect(self, colour):
        if not self.available:
            return
        try:
            self.keyboard.set_led_direct_effect()
            total_leds = len(self.keyboard.get_current_direct_leds())
            # light all keys in the specified color
            for idx in range(total_leds):
                self.keyboard.set_led_by_idx(idx=idx, colour=colour)
            self.keyboard.send_leds()
        except Exception:
            pass


    # restore control keys after an effect (turns off non-control keys)
    def effect_end(self):
        if not self.available:
            return
        try:
            self.keyboard.set_led_direct_effect()
            total_leds = len(self.keyboard.get_current_direct_leds())

            for idx in range(total_leds):
                if idx in self.control_led_indices:
                    self.keyboard.set_led_by_idx(idx=idx, colour=HSV_WHITE)
                elif idx in self.action_led_indices:
                    self.keyboard.set_led_by_idx(idx=idx, colour=HSV_CYAN)
                else:
                    self.keyboard.set_led_by_idx(idx=idx, colour=HSV_OFF)

            self.keyboard.send_leds()
        except Exception:
            pass


    # flash effect for mine explosion
    def effect_mine_explosion(self):
        if not self.available:
            return
        def _run_effect():
            splash_preset = Preset(effect=41, speed=255, 
                fixed_hue=True, hue=0, sat=255)
            self.keyboard.set_temp_effect(preset=splash_preset)
            time.sleep(1.2)
            self.effect_end()
        threading.Thread(target=_run_effect, daemon=True).start()


    # flash effect for enemy/hazard damage (orange on all non-control keys)
    def effect_enemy_damage(self):
        self._flash_effect(HSV_ORANGE)


    # flash effect for beacon placed (green on all non-control keys)
    def effect_beacon(self):
        self._flash_effect(HSV_GREEN)


    # flash effect for hotspot (blue on all non-control keys)
    def effect_hotspot(self):
        self._flash_effect(HSV_BLUE)


