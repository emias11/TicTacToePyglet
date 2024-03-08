class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return self.name


class Board:
    def __init__(self):
        self.board = {'7': ' ', '8': ' ', '9': ' ',
                      '4': ' ', '5': ' ', '6': ' ',
                      '1': ' ', '2': ' ', '3': ' '}

    def display_board(self):
        print(self.board['7'] + '|' + self.board['8'] + '|' + self.board['9'])
        print('-+-+-')
        print(self.board['4'] + '|' + self.board['5'] + '|' + self.board['6'])
        print('-+-+-')
        print(self.board['1'] + '|' + self.board['2'] + '|' + self.board['3'])

    def update_board(self, position, symbol):
        self.board[position] = symbol

    def is_position_available(self, position):
        return self.board[position] == ' '


class GameState:
    def __init__(self):
        self.board = Board()
        self.players = [Player("Player 1", "X"), Player("Player 2", "O")]
        self.current_player = self.players[0]
        self.game_over = False

    def switch_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def check_winner(self):
        b = self.board.board
        winning_conditions = [
            (b['7'], b['8'], b['9']),  # across the top
            (b['4'], b['5'], b['6']),  # across the middle
            (b['1'], b['2'], b['3']),  # across the bottom
            (b['7'], b['4'], b['1']),  # down the left side
            (b['8'], b['5'], b['2']),  # down the middle
            (b['9'], b['6'], b['3']),  # down the right side
            (b['7'], b['5'], b['3']),  # diagonal
            (b['1'], b['5'], b['9'])   # diagonal
        ]
        for condition in winning_conditions:
            if condition[0] == condition[1] == condition[2] != ' ':
                self.game_over = True
                return True
        return False

    def check_tie(self):
        for position in self.board.board.values():
            if position == ' ':
                return False
        self.game_over = True
        return True


class Game:
    def __init__(self):
        self.game_state = GameState()

    def play(self):
        while not self.game_state.game_over:
            self.game_state.board.display_board()
            print(f"It's your turn, {self.game_state.current_player} - Move to which place?")
            move = input()

            if move in self.game_state.board.board.keys() and self.game_state.board.is_position_available(move):
                self.game_state.board.update_board(move, self.game_state.current_player.symbol)

                if self.game_state.check_winner():
                    self.game_state.board.display_board()
                    print(f"\nGame Over.\n{self.game_state.current_player} won.")
                    break

                if self.game_state.check_tie():
                    self.game_state.board.display_board()
                    print("\nGame Over.\nIt's a Tie!!")
                    break

                self.game_state.switch_player()
            else:
                print("Invalid move. Try again.")

        restart = input("Do you want to play Again? (y/n)")
        if restart.lower() == "y":
            self.game_state = GameState()
            self.play()


if __name__ == "__main__":
    game = Game()
    game.play()
