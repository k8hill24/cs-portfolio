# Author: Kaitlyn Hill
# GitHub username: Hillkait
# Date: 6/8/2024
# Description: Final Project
"""
This project creates a Player and a ChessVar class and a mian call function to create  game of atomic chess.
The Player class initializes the name and color of the players
The ChessVar class initializes the board setup, calculates players turns and updates the board per valid move. Also determines
if the move is valid based on atomic chess rules and classic chess piece rules. Atomic chess has the surrounding squares clear
of all pieces if there is a capture (pawns not affected). Turns switch after every valid move.
"""


class Player:
    """ Class representing a player in atomic chess with a name and color """
    def __init__(self, name, color):
        # initializes the player with a name and color
        self._name = name
        self._color = color

    def get_name(self):
        # returns the name of given player
        return self._name

    def get_color(self):
        # returns the color of given player
        return self._color


class ChessVar:
    """
    Class used for playing atomic chess
    Controls turn order, the state of the game, and the board
    """
    def __init__(self, player1, player2):
        # initializes the game, board, and turn order
        self.board = self.setup_board()
        self.players = {player1.get_color(): player1, player2.get_color(): player2}
        self.turn = "white"
        self.game_state = "UNFINISHED"
        self.king_positions = {"white": (7, 4), "black": (0, 4)}

    def setup_board(self):
        # sets up the board
        return [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

    def get_state(self):
        # returns current state of the game per valid move
        return self.game_state

    def make_move(self, start_pos, end_pos):
        # moves from start position to end position
        if self.game_state != "UNFINISHED":
            return False

        from_row, from_col = self.convert_to_indices(start_pos)
        to_row, to_col = self.convert_to_indices(end_pos)

        piece = self.board[from_row][from_col]
        if not piece.startswith(self.turn[0]):
            return False

        if not self.valid_move(from_row, from_col, to_row, to_col):
            return False

        self.update(from_row, from_col, to_row, to_col)
        self.switch_turn()
        return True

    def valid_move(self, from_row, from_col, to_row, to_col):
        # checks if move is valid
        piece = self.board[from_row][from_col]
        if piece == "__":
            return False

        target_piece = self.board[to_row][to_col]
        if target_piece.startswith(self.turn[0]):
            return False

        if piece[1] == "K" and abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1:
            return True  # King can move one square in any direction

        if not self.is_valid_piece_move(piece, from_row, from_col, to_row, to_col):
            return False

        return True

    def is_valid_piece_move(self, piece, from_row, from_col, to_row, to_col):
        # checks and validates each pieces move
        if piece[1] == 'p':
            return self.valid_pawn_move(piece, from_row, from_col, to_row, to_col)
        elif piece[1] == 'R':
            return self.valid_rook_move(from_row, from_col, to_row, to_col)
        elif piece[1] == 'N':
            return self.valid_knight_move(from_row, from_col, to_row, to_col)
        elif piece[1] == 'B':
            return self.valid_bishop_move(from_row, from_col, to_row, to_col)
        elif piece[1] == 'Q':
            return self.valid_queen_move(from_row, from_col, to_row, to_col)
        elif piece[1] == 'K':
            return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1
        return False

    def valid_pawn_move(self, piece, from_row, from_col, to_row, to_col):
        direction = -1 if piece[0] == 'w' else 1
        start_row = 6 if piece[0] == 'w' else 1

        if from_col == to_col:
            if (from_row + direction == to_row and self.board[to_row][to_col] == "__") or \
                    (from_row == start_row and from_row + 2 * direction == to_row and self.board[to_row][to_col] == "__" and self.board[from_row + direction][to_col] == "__"):
                return True
        elif abs(from_col - to_col) == 1 and from_row + direction == to_row:
            return self.board[to_row][to_col] != "__"
        return False

    def valid_rook_move(self, from_row, from_col, to_row, to_col):
        if from_row != to_row and from_col != to_col:
            return False
        if from_row == to_row:
            step = 1 if from_col < to_col else -1
            for col in range(from_col + step, to_col, step):
                if self.board[from_row][col] != "__":
                    return False
        else:
            step = 1 if from_row < to_row else -1
            for row in range(from_row + step, to_row, step):
                if self.board[row][from_col] != "__":
                    return False
        return True

    def valid_knight_move(self, from_row, from_col, to_row, to_col):
        return (abs(from_row - to_row), abs(from_col - to_col)) in [(2, 1), (1, 2)]

    def valid_bishop_move(self, from_row, from_col, to_row, to_col):
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        row_step = 1 if from_row < to_row else -1
        col_step = 1 if from_col < to_col else -1
        for i in range(1, abs(from_row - to_row)):
            if self.board[from_row + i * row_step][from_col + i * col_step] != "__":
                return False
        return True

    def valid_queen_move(self, from_row, from_col, to_row, to_col):
        return self.valid_rook_move(from_row, from_col, to_row, to_col) or \
               self.valid_bishop_move(from_row, from_col, to_row, to_col)

    def update(self, from_row, from_col, to_row, to_col):
        # updates the board to show the valid move and new board
        piece = self.board[from_row][from_col]
        target_piece = self.board[to_row][to_col]

        if target_piece != "__":
            self.explosion(to_row, to_col)

        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = "__"

        if piece[1] == "K":
            self.king_positions[self.turn] = (to_row, to_col)

    def explosion(self, row, col):
        # makes the explosion around all the surrounding spots after a capture
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] != "__" and not (self.board[r][c][1] == "p" and (r != row or c != col)):
                        if self.board[r][c][1] == "K":
                            self.game_state = "WHITE_WON" if self.board[r][c][0] == "b" else "BLACK_WON"
                        self.board[r][c] = "__"

    def switch_turn(self):
        # switch turns between the players
        self.turn = "black" if self.turn == "white" else "white"

    def convert_to_indices(self, square):
        # converts algebraic notation to board indices
        col = ord(square[0]) - ord('a')
        row = 8 - int(square[1])
        return row, col

    def print_board(self):
        # prints the current board, including the row and column labels
        print("  a  b  c  d  e  f  g  h")
        for i in range(8):
            row = str(8 - i) + " "
            for j in range(8):
                row += self.board[i][j] + " "
            print(row + str(8 - i))
        print("  a  b  c  d  e  f  g  h")



def main():
    # initialize players
    player1_name = input("Enter the name of player 1 (white): ")
    player2_name = input("Enter the name of player 2 (black): ")
    player1 = Player(player1_name, "white")
    player2 = Player(player2_name, "black")

    # initialize game
    game = ChessVar(player1, player2)

    while game.get_state() == "UNFINISHED":
        game.print_board()
        current_player = game.players[game.turn]
        print(f"{current_player.get_name()} ({current_player.get_color()})'s turn")

        move = input("Enter move (e.g., 'a2 a4'): ")

        # validate moves
        if len(move) != 5 or move[2] != ' ':
            print("Invalid move format. Please enter in the format 'a2 a4'.")
            continue

        # making the moves
        start_pos, end_pos = move.split()
        if not game.make_move(start_pos, end_pos):
            print("Invalid move. Try again.")
            continue

    # finishing the game
    game.print_board()
    print("Game over.")
    if game.get_state() == "WHITE_WON":
        print(f"{player1.get_name()} ({player1.get_color()}) wins!")
    elif game.get_state() == "BLACK_WON":
        print(f"{player2.get_name()} ({player2.get_color()}) wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()