
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
    def __init__(self, enemy_data, player_rect, enemy_images, map):
        super().__init__()
        # enemy_data = (map, type, movement, tile_x1, tile_y1, tile_x2, tile_y2)
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
        # speed
        self.speed = 1
        self.vx = 0
        self.vy = 0
        # RANDOM movement variables
        self.distance_traveled = 0  # distance traveled in current direction (px)
        self.random_pause_timer = 0  # paused time counter for RANDOM movement
        self.random_pause_duration = 30 # duration of pause in frames (0.5 seconds at 60fps)
        self.random_is_paused = False  # if currently paused
        # CHASER movement variables
        self.chase_update_timer = 0  # temporizador para actualizar dirección de persecución
        self.chase_update_interval = 30  # frames entre actualizaciones (ajustable)
        # NUEVA: Zona de activación para CHASER (en tiles)
        self.activation_range = 5  # el enemigo se activa cuando el player está a 5 tiles o menos
        self.is_active = False  # si el enemigo está activo o no
        # NUEVA: Sistema de pausa entre movimientos
        self.pause_timer = 0  # temporizador de pausa actual
        self.pause_duration = 90  # duración de la pausa en frames (1.5 segundos a 60fps)
        self.is_paused = False  # si el enemigo está en pausa
        # NUEVA: Control de movimiento tile por tile
        self.target_x = 0  # posición objetivo X para el movimiento actual
        self.target_y = 0  # posición objetivo Y para el movimiento actual
        self.moving_to_target = False  # si está moviéndose hacia un objetivo
        
        # player's current position (some enemies look at the player)
        self.player = player_rect

        # images - CREAR RECT ANTES DE CONFIGURAR MOVIMIENTO INICIAL
        self.image_list = enemy_images
        self.frame_index = 0  # frame number
        self.animation_timer = 12  # timer to change frame
        self.animation_speed = 12  # frame dwell time
        self.image = self.image_list[0]  # first frame
        self.rect = self.image.get_rect()
        self.map = map

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


    def _set_random_direction(self):
        # establece una dirección aleatoria para el movimiento RANDOM
        directions = [
            (0, -self.speed),   # arriba
            (self.speed, 0),    # derecha
            (0, self.speed),    # abajo
            (-self.speed, 0)]   # izquierda
        self.vx, self.vy = random.choice(directions)
        self.distance_traveled = 0

    def _check_collision(self, rect, axis, direction):
        """Verifica colisiones con tiles de obstáculo (adaptado del player)"""
        if axis == enums.CA_HORIZONTAL:
            if direction > 0:  # moviéndose a la derecha
                tile_x = (rect.right - 1) // constants.TILE_SIZE
            else:  # moviéndose a la izquierda
                tile_x = rect.left // constants.TILE_SIZE
            tile_y = rect.y // constants.TILE_SIZE
        else:  # vertical
            tile_x = rect.x // constants.TILE_SIZE
            if direction > 0:  # moviéndose hacia abajo
                tile_y = (rect.bottom - 1) // constants.TILE_SIZE
            else:  # moviéndose hacia arriba
                tile_y = rect.top // constants.TILE_SIZE
        # returns True if the tile is an obstacle
        return self.map.get_tile_type(tile_x, tile_y) == enums.TT_OBSTACLE

    def _is_position_valid(self, x, y):
        """Verifica si una posición está dentro de los límites del mapa y no hay obstáculos"""
        # Asumiendo que tienes acceso a las dimensiones del mapa
        map_width = constants.MAP_TILE_SIZE[0] * constants.TILE_SIZE  # o como accedas al ancho del mapa
        map_height = constants.MAP_TILE_SIZE[1] * constants.TILE_SIZE  # o como accedas al alto del mapa
        
        # Verificar límites del mapa
        if not (x >= 0 and y >= 0 and 
                x + self.rect.width <= map_width and 
                y + self.rect.height <= map_height):
            return False
            
        # Crear un rect temporal para verificar obstáculos
        temp_rect = pygame.Rect(x, y, self.rect.width, self.rect.height)
        
        # Verificar si hay obstáculos en el camino
        # Verificar múltiples puntos del rect para mayor precisión
        points_to_check = [
            (temp_rect.left, temp_rect.top),
            (temp_rect.right - 1, temp_rect.top), 
            (temp_rect.left, temp_rect.bottom - 1),
            (temp_rect.right - 1, temp_rect.bottom - 1)
        ]
        
        for px, py in points_to_check:
            tile_x = px // constants.TILE_SIZE
            tile_y = py // constants.TILE_SIZE
            if self.map.get_tile_type(tile_x, tile_y) == enums.TT_OBSTACLE:
                return False
                
        return True
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
        
        # alinear posición actual al tile más cercano
        self.x = round(self.x / constants.TILE_SIZE) * constants.TILE_SIZE
        self.y = round(self.y / constants.TILE_SIZE) * constants.TILE_SIZE
        
        # calcular diferencias en tiles
        enemy_tile_x = self.x // constants.TILE_SIZE
        enemy_tile_y = self.y // constants.TILE_SIZE
        player_tile_x = self.player.centerx // constants.TILE_SIZE
        player_tile_y = self.player.centery // constants.TILE_SIZE
        
        dx = player_tile_x - enemy_tile_x
        dy = player_tile_y - enemy_tile_y
        
        # determinar dirección (solo UN tile de movimiento) y verificar límites
        target_x = self.x
        target_y = self.y
        
        if abs(dx) > abs(dy):  # Moverse horizontalmente
            if dx > 0:  # jugador está a la derecha
                target_x = self.x + constants.TILE_SIZE
            else:  # jugador está a la izquierda
                target_x = self.x - constants.TILE_SIZE
        else:  # Moverse verticalmente
            if dy > 0:  # jugador está abajo
                target_y = self.y + constants.TILE_SIZE
            else:  # jugador está arriba
                target_y = self.y - constants.TILE_SIZE
        
        # verificar si el objetivo está dentro de los límites del mapa
        if self._is_position_valid(target_x, target_y):
            self.target_x = target_x
            self.target_y = target_y
        else:
            # si el objetivo está fuera del mapa, quedarse en la posición actual
            self.target_x = self.x
            self.target_y = self.y
        
        # configurar velocidad hacia el objetivo
        dx_target = self.target_x - self.x
        dy_target = self.target_y - self.y
        
        if dx_target != 0:
            self.vx = self.speed if dx_target > 0 else -self.speed
            self.vy = 0
        else:
            self.vx = 0
            self.vy = self.speed if dy_target > 0 else -self.speed
        
        self.moving_to_target = True

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
        new_x = self.x + self.vx
        
        # verificar límites del mapa además de los límites específicos del enemigo
        if self._is_position_valid(new_x, self.y):
            self.x = new_x
            # determine left and right boundaries
            min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)        
            # detect when reaching either boundary and reverse direction
            if self.x <= min_x or self.x >= max_x:
                self.vx = -self.vx
                # ensure position stays within boundaries
                self.x = max(min_x, min(self.x, max_x))
        else:
            # fuera de los límites del mapa - revertir dirección
            self.vx = -self.vx

    def _update_vertical_movement(self):
        # handle vertical movement with boundary checking
        new_y = self.y + self.vy
        
        # verificar límites del mapa además de los límites específicos del enemigo
        if self._is_position_valid(self.x, new_y):
            self.y = new_y
            # determine upper and lower boundaries
            min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)        
            # detect when reaching either boundary and reverse direction
            if self.y <= min_y or self.y >= max_y:
                self.vy = -self.vy
                # ensure position stays within boundaries
                self.y = max(min_y, min(self.y, max_y))
        else:
            # fuera de los límites del mapa - revertir dirección
            self.vy = -self.vy

    def _update_random_movement(self):
        # maneja el movimiento aleatorio con pausas entre cambios de dirección
        
        # manejar sistema de pausas para RANDOM
        if self.random_is_paused:
            self.random_pause_timer += 1
            # durante la pausa, no moverse
            self.vx = 0
            self.vy = 0
            
            if self.random_pause_timer >= self.random_pause_duration:
                # terminar pausa y cambiar dirección
                self.random_is_paused = False
                self.random_pause_timer = 0
                self.distance_traveled = 0
                self._set_random_direction()
        else:
            # no está en pausa - moverse normalmente
            # verificar límites del mapa antes de moverse
            new_x = self.x + self.vx
            new_y = self.y + self.vy
            
            if self._is_position_valid(new_x, new_y):
                # mover en la dirección actual
                old_x, old_y = self.x, self.y
                self.x = new_x
                self.y = new_y     
                # calcular distancia recorrida en este frame
                distance_this_frame = ((self.x - old_x) ** 2 + (self.y - old_y) ** 2) ** 0.5
                self.distance_traveled += distance_this_frame        
                # si ha recorrido un tile completo, iniciar pausa
                if self.distance_traveled >= constants.TILE_SIZE:
                    # alinear al tile más cercano antes de pausar
                    self.x = round(self.x / constants.TILE_SIZE) * constants.TILE_SIZE
                    self.y = round(self.y / constants.TILE_SIZE) * constants.TILE_SIZE
                    # iniciar pausa antes del próximo cambio de dirección
                    self.random_is_paused = True
                    self.random_pause_timer = 0
            else:
                # fuera de los límites del mapa - cambiar dirección inmediatamente
                self.distance_traveled = constants.TILE_SIZE # forzar cambio de dirección
                self.random_is_paused = True
                self.random_pause_timer = 0

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
            self.moving_to_target = False
            self.vx = 0  # parar movimiento durante la pausa inicial
            self.vy = 0
        elif not player_in_range and self.is_active:
            # jugador sale del rango - desactivar enemigo
            self.is_active = False
            self.is_paused = False
            self.pause_timer = 0
            self.moving_to_target = False
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
                    # terminar pausa y empezar movimiento hacia el siguiente tile
                    self.is_paused = False
                    self.pause_timer = 0
                    # calcular nuevo objetivo (un tile hacia el jugador)
                    self._update_chaser_direction()
            else:
                # no está en pausa - moverse hacia el objetivo
                if self.moving_to_target:
                    # mover hacia el tile objetivo
                    self.x += self.vx
                    self.y += self.vy
                    
                    # verificar si hemos llegado al tile objetivo
                    reached_target = False
                    if self.vx > 0 and self.x >= self.target_x:  # moviéndose a la derecha
                        self.x = self.target_x
                        reached_target = True
                    elif self.vx < 0 and self.x <= self.target_x:  # moviéndose a la izquierda
                        self.x = self.target_x
                        reached_target = True
                    elif self.vy > 0 and self.y >= self.target_y:  # moviéndose hacia abajo
                        self.y = self.target_y
                        reached_target = True
                    elif self.vy < 0 and self.y <= self.target_y:  # moviéndose hacia arriba
                        self.y = self.target_y
                        reached_target = True
                    
                    if reached_target:
                        # llegamos al objetivo - iniciar pausa
                        self.moving_to_target = False
                        self.vx = 0
                        self.vy = 0
                        self.is_paused = True
                        self.pause_timer = 0

    def draw(self, surface, camera):
        if self._is_visible(camera):
            # draw the enemy on the screen with camera offset
            screen_x = self.x - camera.x
            screen_y = self.y - camera.y
            surface.blit(self.image, (screen_x, screen_y))