import random

def create_board(board_size, num_bombs):
    # Creamos una matriz vacía para el tablero
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]

    # Colocamos las bombas aleatoriamente
    bombs_placed = 0
    while bombs_placed < num_bombs:
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        if board[row][col] == 0:
            board[row][col] = '*'
            bombs_placed += 1

    # Asignamos números a las casillas que no tienen bombas
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 0:
                # Calculamos cuántas bombas hay alrededor
                count = 0
                if row > 0 and col > 0 and board[row-1][col-1] == '*':
                    count += 1
                if row > 0 and board[row-1][col] == '*':
                    count += 1
                if row > 0 and col < board_size - 1 and board[row-1][col+1] == '*':
                    count += 1
                if col > 0 and board[row][col-1] == '*':
                    count += 1
                if col < board_size - 1 and board[row][col+1] == '*':
                    count += 1
                if row < board_size - 1 and col > 0 and board[row+1][col-1] == '*':
                    count += 1
                if row < board_size - 1 and board[row+1][col] == '*':
                    count += 1
                if row < board_size - 1 and col < board_size - 1 and board[row+1][col+1] == '*':
                    count += 1
                board[row][col] = count

    return board

def print_board(board):
    for row in board:
        print(' '.join(str(x) for x in row))

def play_game():
    board_size = 10
    num_bombs = 10
    board = create_board(board_size, num_bombs)

    print("¡Bienvenido al buscaminas!")
    print("Hay " + str(num_bombs) + " bombas ocultas.")
    print_board(board)

    while True:
        row = int(input("Ingrese el número de fila: "))
        col = int(input("Ingrese el número de columna: "))
        if board[row][col] == '*':
            print("¡BOOM! Has perdido.")
            print_board(board)
            return
        elif board[row][col] > 0:
            print("Hay " + str(board[row][col]) + " bombas alrededor.")
        else:
            print("¡No hay bombas cerca!")
        board[row][col] = 'X'
        print_board(board)

play_game()
