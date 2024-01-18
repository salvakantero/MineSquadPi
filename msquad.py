


import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Definición de colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Configuración del juego
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE

# Función para generar el tablero de juego
def generate_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    mines = random.sample(range(GRID_SIZE * GRID_SIZE), GRID_SIZE)
    for mine in mines:
        row, col = divmod(mine, GRID_SIZE)
        board[row][col] = -1  # Marcamos las minas con -1
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE and board[i][j] != -1:
                    board[i][j] += 1  # Incrementamos el contador de minas vecinas
    return board

# Función para dibujar el tablero
def draw_board(screen, board, revealed):
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Dibuja un contorno negro alrededor de cada celda
            if revealed[row][col]:
                if board[row][col] == -1:
                    pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                elif board[row][col] > 0:
                    font = pygame.font.Font(None, 30)
                    text = font.render(str(board[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(text, text_rect)

# Función principal del juego
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Buscaminas")

    board = generate_board()
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                revealed[row][col] = True

        draw_board(screen, board, revealed)
        pygame.display.flip()

if __name__ == "__main__":
    main()