import random


class TicTacToe:
    def __init__(self):
        self.board = [['-' for i in range(3)] for j in range(3)]

    def print_instructions(self):
        print("Welcome to TicTacToe!")
        print("Player 0 is X and Player 1 is O")
        print("Take turns placing your pieces — first to three in a row wins!")

    def print_board(self):
        print("  0 1 2")
        for i in range(3):
            print(str(i), end=" ")
            for j in range(3):
                print(self.board[i][j], end=" ")
            print()

    # assumes integer input
    def is_valid_move(self, row, col):
        if row == '' or col == '':
            return False
        row = int(row)
        col = int(col)
        if row >= 3 or row < 0 or col >= 3 or col < 0:
            return False
        if self.board[row][col] == '-':
            return True
        return False

    # assumes valid row, col
    def place_player(self, player, row, col):
        if player == 0:
            self.board[row][col] = 'X'
        else:
            self.board[row][col] = 'O'

    # consider if enter string / nothing
    def take_manual_turn(self, player):
        # TODO: Ask the user for a row, col until a valid response
        #  is given them place the player's icon in the right spot
        row = input("Enter a row: ")
        col = input("Enter a col: ")
        while not self.is_valid_move(row, col):
            print("Invalid move.")
            row = input("Enter a VALID row: ")
            col = input("Enter a VALID col: ")
        self.place_player(player, int(row), int(col))

    def take_random_turn(self, player):
        rrow = random.randint(0, 2)
        rcol = random.randint(0, 2)
        while not self.is_valid_move(rrow, rcol):
            rrow = random.randint(0, 2)
            rcol = random.randint(0, 2)
        self.place_player(player, rrow, rcol)

    def take_turn(self, player):
        if player == 0:
            self.take_manual_turn(player)
        else:
            self.take_random_turn(player)

    def check_col_win(self, player):
        # 'X'
        if player == 0:
            return (self.board[0][0] == self.board[1][0] and self.board[0][0] == self.board[2][0] and self.board[0][0] == 'X') or (self.board[0][1] == self.board[1][1] and self.board[1][1] == self.board[2][1] and self.board[1][1] == 'X') or (self.board[0][2] == self.board[1][2] and self.board[1][2] == self.board[2][2] and self.board[2][2] == 'X')
        else:
            # 'O'
            return (self.board[0][0] == self.board[1][0] and self.board[0][0] == self.board[2][0] and self.board[0][0] == 'O') or (self.board[0][1] == self.board[1][1] and self.board[1][1] == self.board[2][1] and self.board[1][1] == 'O') or (self.board[0][2] == self.board[1][2] and self.board[1][2] == self.board[2][2] and self.board[2][2] == 'O')
        

    def check_row_win(self, player):
        # 'X'
        if player == 0:
            for row in self.board:
                if row[0] == row[1] and row[1] == row[2] and row[1] == 'X':
                    return True
        # 'O'
        if player == 1:
            for row in self.board:
                if row[0] == row[1] and row[1] == row[2] and row[1] == 'O':
                    #print("hellor1")
                    return True
        return False

    def check_diag_win(self, player):
        if player == 0:
            return (self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[1][1] == 'X') or (self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2] and self.board[1][1] == 'X')
        else:
            return (self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[1][1] == 'O') or (self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2] and self.board[1][1] == 'O')

    def check_win(self, player):
        return self.check_col_win(player) or self.check_row_win(player) or self.check_diag_win(player)

    def check_tie(self):
        finished = True
        for row in self.board:
            for col in row:
                if col == '-':
                    finished = False
                    break
        return (not self.check_win(0) and not self.check_win(1)) and finished

    def play_game(self):
        # TODO: Play game
        self.print_instructions()
        self.print_board()
        player = 0

        while not self.check_win((player + 1) % 2) and not self.check_tie():
            print("X's Turn") if player == 0 else print("O's Turn")
            self.take_turn(player)
            player += 1
            player %= 2
            self.print_board()

        if self.check_tie():
            print("It was a tie")
        else:
            print("X wins!") if (player + 1) % 2 == 0 else print("O wins!")

