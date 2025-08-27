
# ==============================================================================
# .::Enemy class::.
# Creates an enemy based on its graphics and characteristics. 
# It animates it and gives it movement based on a movement type 
# and boundary coordinates.
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

import constants
import enums

import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data, player_rect, enemy_images):
        # enemy_data = (map, type, movement, tile_x1, tile_y1, tile_x2, tile_y2)
        super().__init__()
        
        # enemy type: 
        # SCORPION, SNAKE, SOLDIER1
        # CRAB, PROJECTILE, SOLDIER2
        # SKIER, HABALI, SOLDIER3
        self.type = enemy_data[1]
        
        # movement type: HORIZONTAL, VERTICAL, RANDOM, CHASER
        self.movement = enemy_data[2]
        
        # from xy values
        self.x = self.x1 = enemy_data[3] * constants.TILE_SIZE
        self.y = self.y1 = enemy_data[4] * constants.TILE_SIZE
        # to xy values
        self.x2 = enemy_data[5] * constants.TILE_SIZE
        self.y2 = enemy_data[6] * constants.TILE_SIZE
        
        # speed of movement
        self.speed = 1
        self.vx = 0
        self.vy = 0
        # Variables para movimiento RANDOM
        self.distance_traveled = 0  # distancia recorrida desde el último cambio
        self.tile_distance = constants.TILE_SIZE  # distancia de un tile
        # Variables para movimiento CHASER
        self.chase_update_timer = 0  # temporizador para actualizar dirección de persecución
        self.chase_update_interval = 30  # frames entre actualizaciones (ajustable)
        # NUEVA: Zona de activación para CHASER (en tiles)
        self.activation_range = 5  # el enemigo se activa cuando el player está a 5 tiles o menos
        self.is_active = False  # si el enemigo está activo o no
        # NUEVA: Sistema de pausa entre movimientos
        self.pause_timer = 0  # temporizador de pausa actual
        self.pause_duration = 90  # duración de la pausa en frames (1.5 segundos a 60fps)
        self.is_paused = False  # si el enemigo está en pausa
        
        # player's current position (some enemies look at the player)
        self.player = player_rect

        # images - CREAR RECT ANTES DE CONFIGURAR MOVIMIENTO INICIAL
        self.image_list = enemy_images
        self.frame_index = 0  # frame number
        self.animation_timer = 12  # timer to change frame
        self.animation_speed = 12  # frame dwell time
        self.image = self.image_list[0]  # first frame
        self.rect = self.image.get_rect()

        # AHORA SÍ configurar el movimiento inicial (después de crear self.rect)
        if self.movement == enums.EM_HORIZONTAL:
            # determine initial direction based on x1 and x2 positions
            self.vx = self.speed if self.x2 > self.x1 else -self.speed
        elif self.movement == enums.EM_VERTICAL:
            # determine initial direction based on y1 and y2 positions
            self.vy = self.speed if self.y2 > self.y1 else -self.speed
        elif self.movement == enums.EM_RANDOM:
            # iniciar con dirección aleatoria
            self._set_random_direction()
        elif self.movement == enums.EM_CHASER:
            # no iniciar persiguiendo inmediatamente, esperar a estar activo
            pass

    def _set_random_direction(self):
        # establece una dirección aleatoria para el movimiento RANDOM
        directions = [
            (0, -self.speed),   # arriba
            (self.speed, 0),    # derecha
            (0, self.speed),    # abajo
            (-self.speed, 0)]   # izquierda
        self.vx, self.vy = random.choice(directions)
        self.distance_traveled = 0

    def _is_player_in_range(self):
        """Verifica si el jugador está dentro del rango de activación"""
        if self.player is None:
            return False
        
        # calcular distancia en tiles
        enemy_tile_x = (self.x + self.rect.width // 2) // constants.TILE_SIZE
        enemy_tile_y = (self.y + self.rect.height // 2) // constants.TILE_SIZE
        player_tile_x = self.player.centerx // constants.TILE_SIZE
        player_tile_y = self.player.centery // constants.TILE_SIZE
        
        # distancia usando teorema de Pitágoras
        distance = ((enemy_tile_x - player_tile_x) ** 2 + (enemy_tile_y - player_tile_y) ** 2) ** 0.5
        
        return distance <= self.activation_range

    # actualiza la dirección del movimiento CHASER hacia el jugador
    def _update_chaser_direction(self):
        if self.player is None:
            return
            
        # calcular diferencias
        dx = self.player.centerx - (self.x + self.rect.width // 2)
        dy = self.player.centery - (self.y + self.rect.height // 2)        
        # resetear velocidades
        self.vx = 0
        self.vy = 0        
        # determinar dirección principal (la mayor diferencia)
        if abs(dx) > abs(dy): # Moverse horizontalmente            
            self.vx = self.speed if dx > 0 else -self.speed
        else: # Moverse verticalmente            
            self.vy = self.speed if dy > 0 else -self.speed

    def animate(self):
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0  # reset the timer
            self.frame_index = (self.frame_index + 1) % len(self.image_list)  # cycle through frames        
        # assigns the original or flipped image based on movement direction
        current_frame = self.image_list[self.frame_index]
        # moving to the right
        if self.vx >= 0: self.image = current_frame
        # moving to the left
        else: self.image = pygame.transform.flip(current_frame, True, False)

    # check if enemy is visible within camera bounds
    def _is_visible(self, camera):
        return (
            # check right edge
            self.x + self.rect.width > camera.x and
            # check left edge
            self.x < camera.x + constants.SCREEN_MAP_UNSCALED_SIZE[0] and
            # check bottom edge
            self.y + self.rect.height > camera.y and
            # check top edge
            self.y < camera.y + constants.SCREEN_MAP_UNSCALED_SIZE[1])

    def update(self):   
        # movement handling
        if self.movement == enums.EM_HORIZONTAL: 
            self._update_horizontal_movement()
        elif self.movement == enums.EM_VERTICAL: 
            self._update_vertical_movement()
        elif self.movement == enums.EM_RANDOM:
            self._update_random_movement()
        elif self.movement == enums.EM_CHASER:
            self._update_chaser_movement()
            
        # apply the calculated position and the corresponding frame
        self.rect.x = self.x
        self.rect.y = self.y
        self.animate()

    def _update_horizontal_movement(self):
        # handle horizontal movement with boundary checking
        self.x += self.vx
        # determine left and right boundaries
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)        
        # detect when reaching either boundary and reverse direction
        if self.x <= min_x or self.x >= max_x:
            self.vx = -self.vx
            # ensure position stays within boundaries
            self.x = max(min_x, min(self.x, max_x))

    def _update_vertical_movement(self):
        # handle vertical movement with boundary checking
        self.y += self.vy
        # determine upper and lower boundaries
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)        
        # detect when reaching either boundary and reverse direction
        if self.y <= min_y or self.y >= max_y:
            self.vy = -self.vy
            # ensure position stays within boundaries
            self.y = max(min_y, min(self.y, max_y))

    def _update_random_movement(self):
        # maneja el movimiento aleatorio, cambiando dirección cada tile recorrido
        # mover en la dirección actual
        old_x, old_y = self.x, self.y
        self.x += self.vx
        self.y += self.vy        
        # calcular distancia recorrida en este frame
        distance_this_frame = ((self.x - old_x) ** 2 + (self.y - old_y) ** 2) ** 0.5
        self.distance_traveled += distance_this_frame        
        # si ha recorrido un tile completo, cambiar de dirección
        if self.distance_traveled >= self.tile_distance:
            self._set_random_direction()  # Siempre cambiar de dirección

    def _update_chaser_movement(self):
        # maneja el movimiento perseguidor con zona de activación y pausas
        
        # verificar si el jugador está en rango
        player_in_range = self._is_player_in_range()
        
        # actualizar estado de activación
        if player_in_range and not self.is_active:
            # jugador entra en rango - activar enemigo
            self.is_active = True
            self.is_paused = True  # empezar con una pausa
            self.pause_timer = 0
            self.vx = 0  # parar movimiento durante la pausa inicial
            self.vy = 0
        elif not player_in_range and self.is_active:
            # jugador sale del rango - desactivar enemigo
            self.is_active = False
            self.is_paused = False
            self.pause_timer = 0
            self.chase_update_timer = 0
            self.vx = 0  # parar movimiento
            self.vy = 0
            
        # solo procesar si está activo
        if self.is_active:
            # manejar sistema de pausas
            if self.is_paused:
                self.pause_timer += 1
                # durante la pausa, no moverse
                self.vx = 0
                self.vy = 0
                
                if self.pause_timer >= self.pause_duration:
                    # terminar pausa y empezar movimiento
                    self.is_paused = False
                    self.pause_timer = 0
                    self.chase_update_timer = 0
                    # actualizar dirección después de la pausa
                    self._update_chaser_direction()
            else:
                # no está en pausa - moverse y actualizar temporizador
                self.chase_update_timer += 1
                
                # mover en la dirección actual
                self.x += self.vx
                self.y += self.vy
                
                # verificar si es hora de pausar y cambiar dirección
                if self.chase_update_timer >= self.chase_update_interval:
                    # alinear al tile MÁS CERCANO antes de pausar (no siempre hacia abajo)
                    self.x = round(self.x / constants.TILE_SIZE) * constants.TILE_SIZE
                    self.y = round(self.y / constants.TILE_SIZE) * constants.TILE_SIZE
                    # iniciar pausa para el próximo cambio de dirección
                    self.is_paused = True
                    self.pause_timer = 0

    def draw(self, surface, camera):
        if self._is_visible(camera):
            # draw the enemy on the screen with camera offset
            screen_x = self.x - camera.x
            screen_y = self.y - camera.y
            surface.blit(self.image, (screen_x, screen_y))