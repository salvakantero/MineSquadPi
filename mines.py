
import pygame
import sys
import random

pygame.init()

# definición de colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# configuración del juego
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE

# función para generar el tablero de juego
def generate_board():
    # tablero de 10x10 ceros
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    # lista de minas (10 posiciones aleatorias en el tablero)
    mines = random.sample(range(GRID_SIZE * GRID_SIZE), GRID_SIZE)
    for mine in mines:
        # según el nº de casilla obtiene la fila,columna
        row, col = divmod(mine, GRID_SIZE)
        # marca la casilla con mina (-1)
        board[row][col] = -1
        # marca las casillas adyacentes
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE and board[i][j] != -1:
                    board[i][j] += 1
    return board

# función para dibujar el tablero
def draw_board(screen, board, revealed):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # rectángulo del tamaño de la celda
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect) # fondo gris
            pygame.draw.rect(screen, BLACK, rect, 1) # borde negro
            if revealed[row][col]:
                # si en la casilla hay una mina
                if board[row][col] == -1:
                    # pinta un círculo negro en el centro de la casilla
                    pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                # si en la casilla hay una advertencia
                elif board[row][col] > 0:
                    # pinta el nº en el centro de la casilla
                    font = pygame.font.Font(None, 30)
                    text = font.render(str(board[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(text, text_rect)

# función principal del juego
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Buscaminas")
    # tablero de 10x10 con las minas y sus advertencias
    board = generate_board()
    # tablero booleano adicional de 10x10 para las casillas reveladas
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    # bucle principal
    while True:
        for event in pygame.event.get():
            # sale del programa
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # click del ratón
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # calcula la fila/columna del click
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                # y revela la casilla
                revealed[row][col] = True
        # refresca el tablero
        draw_board(screen, board, revealed)
        pygame.display.flip()

if __name__ == "__main__":
    main()