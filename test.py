import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Constantes
TILE_SIZE = 32
MAP_WIDTH = 15   # 15 tiles de ancho
MAP_HEIGHT = 40  # 40 tiles de alto

SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE   # 480 pixels
SCREEN_HEIGHT = 10 * TILE_SIZE         # 320 pixels (10 tiles visibles)

# Colores
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class TileMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.tiles = self.generate_map()
        
    def generate_map(self):
        """Genera un mapa vertical simple"""
        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Crear patrones por filas para ver mejor el scroll
                if y < 8:  # Zona superior - montañas
                    tile_type = 'mountain' if (x + y) % 3 == 0 else 'grass'
                elif y < 16:  # Zona de bosque
                    tile_type = 'tree' if (x + y) % 2 == 0 else 'grass'
                elif y < 24:  # Zona de tierra
                    tile_type = 'dirt' if x % 2 == 0 else 'grass'
                elif y < 32:  # Zona mixta
                    tile_type = random.choice(['grass', 'tree', 'dirt'])
                else:  # Zona inferior - agua
                    tile_type = 'water' if x % 3 != 0 else 'blue_grass'
                    
                row.append(tile_type)
            tiles.append(row)
        return tiles
    
    def get_tile_color(self, tile_type):
        """Retorna el color según el tipo de tile"""
        colors = {
            'grass': GREEN,
            'dirt': BROWN,
            'water': BLUE,
            'tree': DARK_GREEN,
            'mountain': GRAY,
            'blue_grass': (0, 200, 100)
        }
        return colors.get(tile_type, WHITE)
    
    def draw(self, screen, camera_y):
        """Dibuja la parte visible del mapa"""
        # Calcular qué filas están visibles
        start_row = max(0, camera_y // TILE_SIZE)
        end_row = min(self.height, start_row + (SCREEN_HEIGHT // TILE_SIZE) + 2)
        
        for y in range(start_row, end_row):
            for x in range(self.width):
                # Posición en pantalla
                screen_x = x * TILE_SIZE
                screen_y = y * TILE_SIZE - camera_y
                
                # Solo dibujar si está visible
                if -TILE_SIZE <= screen_y <= SCREEN_HEIGHT:
                    tile_type = self.tiles[y][x]
                    color = self.get_tile_color(tile_type)
                    pygame.draw.rect(screen, color, 
                                   (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    
                    # Dibujar borde del tile
                    pygame.draw.rect(screen, (0, 0, 0), 
                                   (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)




class Player:
    def __init__(self):
        self.x = (MAP_WIDTH // 2) * TILE_SIZE  # Centrado horizontalmente
        self.y = (MAP_HEIGHT // 2) * TILE_SIZE  # Centrado verticalmente
        self.speed = 2
        self.size = 24
        
    def update(self, keys):
        # Actualiza la posición del jugador
        if keys[pygame.K_UP]: self.y -= self.speed
        if keys[pygame.K_DOWN]: self.y += self.speed
        if keys[pygame.K_LEFT]: self.x -= self.speed
        if keys[pygame.K_RIGHT]: self.x += self.speed
        # Límites del mapa
        max_x = MAP_WIDTH * TILE_SIZE - self.size
        max_y = MAP_HEIGHT * TILE_SIZE - self.size
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))
    
    def draw(self, screen, camera_y):
        screen_y = self.y - camera_y
        # Dibujar el jugador como un círculo rojo con borde
        pygame.draw.circle(
            screen, RED, (int(self.x + self.size // 2), 
            int(screen_y + self.size // 2)), self.size // 2)
        pygame.draw.circle(
            screen, BLACK, (int(self.x + self.size // 2), 
            int(screen_y + self.size // 2)), self.size // 2, 2)




class Camera:
    def __init__(self):
        self.y = 0
    
    def update(self, player):
        # Intentar centrar verticalmente al jugador
        target_y = player.y - SCREEN_HEIGHT // 2
        # Límites de la cámara
        max_camera_y = MAP_HEIGHT * TILE_SIZE - SCREEN_HEIGHT
        self.y = max(0, min(target_y, max_camera_y))




def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mapa Vertical 15x40 - Solo Scroll Vertical")
    clock = pygame.time.Clock()
    
    # Crear objetos del juego
    tile_map = TileMap()
    player = Player()
    camera = Camera()
    
    # Fuente para mostrar información
    font = pygame.font.Font(None, 24)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()
        
        # Actualizar juego
        player.update(keys)
        camera.update(player)
        
        # Dibujar mapa
        tile_map.draw(screen, camera.y)
        
        # Dibujar jugador
        player.draw(screen, camera.y)
        
        # Mostrar información
        player_tile_x = int(player.x // TILE_SIZE)
        player_tile_y = int(player.y // TILE_SIZE)
        info_text = font.render(f"Posición: ({player_tile_x + 1}, {player_tile_y + 1})", True, (0, 0, 0))
        screen.blit(info_text, (10, 10))
        visible_rows = f"Filas visibles: {max(1, camera.y // TILE_SIZE + 1)} a {min(MAP_HEIGHT, camera.y // TILE_SIZE + 10)}"
        visible_text = font.render(visible_rows, True, (0, 0, 0))
        screen.blit(visible_text, (10, 30))
        
        pygame.display.flip()
        clock.tick(120)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()