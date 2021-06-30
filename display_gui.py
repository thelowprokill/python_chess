import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import board
from grid_square import grid_square
from threading import Thread

############################################################
#                                                          #
# class config:                                            #
#                                                          #
# purpose: default settings move to a config loader later  #
#                                                          #
############################################################
class config:
    def __init__(self):
        self.win_width = 850
        self.win_height = 850
        self.cell_width  = 100
        self.cell_height = 100

############################################################
#                                                          #
# class MainWindow:                                        #
#                                                          #
# purpose: gui                                             #
#                                                          #
############################################################
class MainWindow(QtWidgets.QMainWindow):
    ########################################################
    #                                                      #
    # function __init__:                                   #
    #                                                      #
    # purpose: set up the gui                              #
    #                                                      #
    ########################################################
    def __init__(self, game_board, game_controller, parent = None):
        super().__init__(parent)
        self.game_board = game_board
        self.game_controller = game_controller
        self.board = []
        self.config = config()
        self.init_sprites()
        self.init_gui()

    ########################################################
    #                                                      #
    # function menu:                                       #
    #                                                      #
    # purpose: set up the menu                             #
    #                                                      #
    ########################################################
    def menu(self):
        pass

    ########################################################
    #                                                      #
    # function init_gui:                                   #
    #                                                      #
    # purpose: set up the gui                              #
    #                                                      #
    ########################################################
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
                square = grid_square(j, i, self.config, self.button_press)
                square.pos = (j, i)
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

        self.menu = QtWidgets.QHBoxLayout()
        self.new_game_label = QtWidgets.QLabel()
        self.new_game_label.clicked.connect(self.new_game)

        ##########################################
        ### /footer                            ###
        ##########################################

    def new_game(self, l)

    ########################################################
    #                                                      #
    # function button_press:                               #
    #                                                      #
    # purpose: start new thread                            #
    #                                                      #
    ########################################################
    def button_press(self, l):
        self.l = l
        move_thread = Thread(target = self.move())
        move_thread.start()

    ########################################################
    #                                                      #
    # function move:                                       #
    #                                                      #
    # purpose: intermediate function for button press.     #
    #   sends press to game_controller in another thread   #
    #                                                      #
    ########################################################
    def move(self):
        self.game_controller.move(self.l)

    ########################################################
    #                                                      #
    # function draw:                                       #
    #                                                      #
    # purpose: update the display                          #
    #                                                      #
    ########################################################
    def draw(self):
        for item in self.board:
            l = item[0]
            s = item[1]
            f = item[2]
            index = l[1] * 8 + l[0]
            self.buttons[index].update_sprite(s, f)

    ########################################################
    #                                                      #
    # function input:                                      #
    #                                                      #
    # purpose: add pieces to draw buffer                   #
    #                                                      #
    ########################################################
    def input(self, l, p, c, flags=[]):
        if p == "":
            self.board.append((l, None, flags))
            return
        for item in self.sprites:
            faction = item[0]
            piece   = item[1]
            sprite  = item[2]
            if p == piece and c == faction:
                self.board.append((l, sprite, flags))

    ########################################################
    #                                                      #
    # function clear:                                      #
    #                                                      #
    # purpose: clear draw buffer                           #
    #                                                      #
    ########################################################
    def clear(self):
        self.board = []
        for b in self.buttons:
            b.update_sprite(None, [])

    ########################################################
    #                                                      #
    # function closeEvent:                                 #
    #                                                      #
    # purpose: close the application                       #
    #                                                      #
    ########################################################
    def closeEvent(self, event):
        sys.exit()

    ########################################################
    #                                                      #
    # function init_sprites:                               #
    #                                                      #
    # purpose: build list of sprites                       #
    #                                                      #
    ########################################################
    def init_sprites(self):
        self.sprites = []
        # white
        pixmap = QtGui.QPixmap("sprites/white/pawn.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("w", "p", pixmap))
        pixmap = QtGui.QPixmap("sprites/white/rook.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("w", "r", pixmap))
        pixmap = QtGui.QPixmap("sprites/white/knight.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("w", "k", pixmap))
        pixmap = QtGui.QPixmap("sprites/white/bishop.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("w", "b", pixmap))
        pixmap = QtGui.QPixmap("sprites/white/queen.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("w", "q", pixmap))
        pixmap = QtGui.QPixmap("sprites/white/king.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("w", "K", pixmap))

        # black
        pixmap = QtGui.QPixmap("sprites/black/pawn.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("b", "p", pixmap))
        pixmap = QtGui.QPixmap("sprites/black/rook.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("b", "r", pixmap))
        pixmap = QtGui.QPixmap("sprites/black/knight.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("b", "k", pixmap))
        pixmap = QtGui.QPixmap("sprites/black/bishop.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("b", "b", pixmap))
        pixmap = QtGui.QPixmap("sprites/black/queen.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("b", "q", pixmap))
        pixmap = QtGui.QPixmap("sprites/black/king.png")
        pixmap = pixmap.scaled(self.config.cell_width, self.config.cell_height, QtCore.Qt.KeepAspectRatio)
        self.sprites.append(("b", "K", pixmap))

########################################################
#                                                      #
# function build_app:                                  #
#                                                      #
# purpose: prevents including QtWidgets in game_gui.py #
#                                                      #
########################################################
def build_app():
    app = QtWidgets.QApplication(sys.argv)
    return app

########################################################
#                                                      #
# function start_gui:                                  #
#                                                      #
# purpose: prevents including QtWidgets in game_gui.py #
#                                                      #
########################################################
def start_gui(app):
    sys.exit(app.exec_())
