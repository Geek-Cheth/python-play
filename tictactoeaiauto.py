import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_SIZE = 300
GRID_SIZE = 3
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
LINE_WIDTH = 5
CIRCLE_WIDTH = 15
CROSS_WIDTH = 10
CIRCLE_RADIUS = CELL_SIZE // 3
OFFSET = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (200, 0, 0)
LIGHT_RED = (255, 100, 100)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

# Board and game state
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = "X"  # Player always starts as "X"
game_over = False

# Draw grid
def draw_grid():
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, SCREEN_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE), (SCREEN_SIZE, x * CELL_SIZE), LINE_WIDTH)

# Draw X
def draw_x(row, col):
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.line(screen, LIGHT_RED, (center_x - OFFSET, center_y - OFFSET), (center_x + OFFSET, center_y + OFFSET), CROSS_WIDTH)
    pygame.draw.line(screen, LIGHT_RED, (center_x - OFFSET, center_y + OFFSET), (center_x + OFFSET, center_y - OFFSET), CROSS_WIDTH)

# Draw O
def draw_o(row, col):
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, BLUE, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

# Check winner
def check_winner():
    global game_over
    # Check rows and columns
    for i in range(GRID_SIZE):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            game_over = True
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            game_over = True
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        game_over = True
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        game_over = True
        return board[0][2]

    # Check for draw
    if all(all(cell is not None for cell in row) for row in board):
        game_over = True
        return "Draw"

    return None

# AI move
def ai_move():
    global current_player
    # AI checks for a winning move
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                board[row][col] = "O"
                if check_winner() == "O":
                    draw_o(row, col)
                    current_player = "X"
                    return
                board[row][col] = None

    # AI blocks the player
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                board[row][col] = "X"
                if check_winner() == "X":
                    board[row][col] = "O"
                    draw_o(row, col)
                    current_player = "X"
                    return
                board[row][col] = None

    # Otherwise, pick a random move
    empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if board[row][col] is None]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = "O"
        draw_o(row, col)
        current_player = "X"

# Main game loop
def main():
    global current_player
    running = True
    draw_grid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == "X":
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE

                if board[row][col] is None:
                    board[row][col] = current_player
                    draw_x(row, col)
                    current_player = "O"

                    winner = check_winner()
                    if winner:
                        print(f"Winner: {winner}")
                        running = False

        if current_player == "O" and not game_over:
            pygame.time.wait(500)  # Delay for realism
            ai_move()

            winner = check_winner()
            if winner:
                print(f"Winner: {winner}")
                running = False

        pygame.display.update()

if __name__ == "__main__":
    main()
