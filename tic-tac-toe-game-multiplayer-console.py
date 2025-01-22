def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def is_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    print("Welcome to Tic Tac Toe!")
    print_board(board)

    while True:
        try:
            print(f"Player {current_player}, make your move (row and column, 1-3):")
            row, col = map(int, input("Enter row and column: ").split())
            row, col = row - 1, col - 1

            if board[row][col] != " ":
                print("Cell already taken. Choose a different cell.")
                continue

            board[row][col] = current_player
            print_board(board)

            if is_winner(board, current_player):
                print(f"Player {current_player} wins!")
                break

            if is_draw(board):
                print("It's a draw!")
                break

            current_player = "O" if current_player == "X" else "X"

        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column numbers between 1 and 3.")

if __name__ == "__main__":
    tic_tac_toe()
