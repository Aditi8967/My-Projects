from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty


class MyButton(Button):
    def __init__(self, row, col, core, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.row = row
        self.col = col
        self.core = core
        self.was_pressed = False

    def on_press(self):
        if self.was_pressed or self.core.game_over[0]:
            return
        self.was_pressed = True
        self.text = self.core.get_label()
        self.core.play(self.row, self.col)


class TicTacToeCore:
    def __init__(self, game_over):
        self.game_over = game_over
        self.player = -1
        self.values = [[0]*3, [0]*3, [0]*3]
        self.row_prod = [0]*3
        self.col_prod = [0]*3
        self.main_diag = 0
        self.other_diag = 0

    def get_label(self):
        if self.player < 0:
            return 'X'
        else:
            return 'O'

    def win(self, num):
        return num == 3 or num == -3

    def play(self, row, col):
        # Return true when win
        if self.values[row][col] != 0 or self.game_over[0]:
            return False  # Already played
        self.values[row][col] = self.player
        self.row_prod[row] += self.player
        self.col_prod[col] += self.player
        if row == col:
            self.main_diag += self.player
        if row + col == 2:
            self.other_diag += self.player
        if self.win(self.row_prod[row]) or self.win(self.col_prod[col]) or self.win(self.main_diag) \
                or self.win(self.other_diag):
            self.game_over[0] = True
            print('{} WINS!'.format(self.get_label()))
            return True
        self.player *= -1
        return False


class MainWindow(GridLayout):
    game_over = ListProperty([False])

    def __init__(self):
        super(MainWindow, self).__init__()
        self.core = TicTacToeCore(self.game_over)
        self.buttons = []
        self.cols = 3
        self.rows = 3
        for i in range(3):
            for j in range(3):
                self.buttons.append(MyButton(row=i, col=j, core=self.core, text=""))
                self.add_widget(self.buttons[-1])

    def on_game_over(self, instance, pos):
        for i in range(len(self.buttons)):
            self.remove_widget(self.buttons[i])
        self.add_widget(Button(text="{} wins!".format(self.core.get_label())))


class TicTacToe(App):

    def build(self):
        return MainWindow()


if __name__ == "__main__":
    TicTacToe().run()
