# 
import pyglet
from pyglet import shapes, text

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

    def update_board(self, position, symbol):
        self.board[position] = symbol

    def is_position_available(self, position):
        return self.board[position] == ' '
 
      
class GameState:
    def __init__(self, board):
        self.board = board
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
    
class TicTacToeGame:
    def __init__(self):
        self.window_size = 300
        self.rows = 3
        self.cols = 3
        self.game_window = pyglet.window.Window(self.window_size, self.window_size)
        self.board = Board()
        self.game_state = GameState(self.board)

        self.grid_batch = pyglet.graphics.Batch()
        self.moves_batch = pyglet.graphics.Batch()
        self.grid_lines = []
        self.moves = []

        self.draw_grid()

        @self.game_window.event
        def on_draw():
            self.game_window.clear()
            self.grid_batch.draw()
            self.moves_batch.draw()

        @self.game_window.event
        def on_mouse_press(x, y, button, modifiers):
            self.handle_mouse_press(x, y)

    def draw_grid(self):
        for row in range(1, self.rows):
            y = row * (self.window_size / self.rows)
            self.grid_lines.append(shapes.Line(0, y, self.window_size, y, width=3, batch=self.grid_batch))

        for col in range(1, self.cols):
            x = col * (self.window_size // self.cols)
            self.grid_lines.append(shapes.Line(x, 0, x, self.window_size, width=3, batch=self.grid_batch))

    def handle_mouse_press(self, x, y):

        # works out the grid number for the x and y direction
        grid_x = int(x // (self.window_size / self.cols)) + 1
        grid_y = int(y // (self.window_size / self.rows)) + 1
        # converts grid coordinates to dictionary index (1-9)
        grid_box_key = str(grid_y + (grid_x - 1) * self.rows)

        if self.board.is_position_available(grid_box_key):
            self.board.update_board(grid_box_key, self.game_state.current_player.symbol)
            # finds the central point of that grid box, to draw the
            center_x = (grid_x - 0.5) * (self.window_size / self.cols)
            center_y = (grid_y - 0.5) * (self.window_size / self.rows)
            self.moves.append(text.Label(self.game_state.current_player.symbol, font_size=36, x=center_x, y=center_y,
                                    anchor_x='center', anchor_y='center', batch=self.moves_batch))

            if self.game_state.check_winner():
                self.game_over(f"{self.game_state.current_player.name} with symbol {self.game_state.current_player.symbol} won.")

            elif self.game_state.check_tie():
                self.game_over("It's a Tie!!")

            self.game_state.switch_player()

    def game_over(self, message):
        end_window = pyglet.window.Window(self.window_size, self.window_size, caption="Game Over")
        label = pyglet.text.Label(message, font_size=15, x=self.window_size/2, y=self.window_size/2,
                                  anchor_x='center', anchor_y='center')
        
        self.game_window.close()

        @end_window.event
        def on_draw():
            end_window.clear()
            label.draw()

if __name__ == "__main__":
    game = TicTacToeGame()
    pyglet.app.run()
