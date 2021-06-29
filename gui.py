import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import board
from grid_square import grid_square
from threading import Thread

class config:
    def __init__(self):
        self.win_width = 850
        self.win_height = 850
        self.cell_width  = 100
        self.cell_height = 100

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.board = []
        self.config = config()
        self.init_sprites()
        self.init_gui()
        self.game_thread = Thread(target = self.init_board)
        self.game_thread.start()

    def init_board(self):
        self.game_board = board.board(self)


    def init_gui(self):

        ##########################################
        ### Window                             ###
        ##########################################

        self.window = QtWidgets.QWidget()
        self.window.resize(int(self.config.win_width), int(self.config.win_height))
        self.setFixedWidth(int(self.config.win_width))
        self.setFixedHeight(int(self.config.win_height))
        self.layout = QtWidgets.QVBoxLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

        ##########################################
        ### /Window                            ###
        ##########################################

        ##########################################
        ### Header                             ###
        ##########################################



        ##########################################
        ### /Header                            ###
        ##########################################

        ##########################################
        ### Body                               ###
        ##########################################

        self.body = QtWidgets.QVBoxLayout()
        self.buttons = []
        for i in range(8):
            new_layout = QtWidgets.QHBoxLayout()
            for j in range(8):
                square = grid_square(i, j, self.config, self.button_press)
                square.pos = (i, j)
                new_layout.addWidget(square)
                self.buttons.append(square)

            self.body.addLayout(new_layout)

        self.layout.addLayout(self.body)

        ##########################################
        ### /Body                              ###
        ##########################################

        ##########################################
        ### footer                             ###
        ##########################################


        ##########################################
        ### /footer                            ###
        ##########################################


    def button_press(self, l):
        print("Button pressed at {}".format(l))

    def init_sprites(self):
        self.sprites = []
        pixmap = QtGui.QPixmap("sprites/pawn.png")
        self.sprites.append(("p", pixmap))

    def draw(self):
        print("Draw")
        for item in self.board:
            l = item[0]
            s = item[1]
            f = item[2]
            index = l[1] * 8 + l[0]
            self.buttons[index].update_sprite(s, f)

    def input(self, l, p, c, flags=[]):
        print("{}{} at {}, flags = {}".format(c, p, l, flags))
        if p == "":
            self.board.append((l, None, flags))
            return
        for item in self.sprites:
            piece = item[0]
            sprite = item[1]
            if p == piece:
                self.board.append((l, sprite, flags))

    def select_piece(self, who, first_attempt):
        if not first_attempt:
            print("Try again")
        print("{}'s move".format(who))
        self.move_x = -1
        self.move_y = -1
        while(True):
            if self.move_x != -1 and self.move_y != -1:
                return (self.move_x, self.move_y)

    def select_move(self, moves, piece):
        print("Selected piece {} at {}".format(piece.piece, piece.get_pos()))
        self.move_x = -1
        self.move_y = -1
        while(True):
            if self.move_x != -1 and self.move_y != -1:
                return (self.move_x, self.move_y)

    def clear(self):
        self.board = []
        pass

    def closeEvent(self, event):
        print("closed")
        sys.exit()

def start_gui():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.clear()
    win.draw()
    win.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    start_gui()
