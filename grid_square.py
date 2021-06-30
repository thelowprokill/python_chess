from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import ImageQt, Image

class grid_square(QtWidgets.QWidget):
    def __init__(self, x, y, config, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.config = config
        self.callback = callback
        self.setupUi()

    ########################################################
    #                                                      #
    # function update_sprite:                              #
    #                                                      #
    # args:                                                #
    #   s: pixmap of the piece sprite                      #
    #   flags: list of strings                             #
    #     l: last move                                     #
    #     s: selected                                      #
    #     c: can move                                      #
    #                                                      #
    # purpose: update the square with the correct          #
    #   information                                        #
    #                                                      #
    ########################################################
    def update_sprite(self, s, flags=[]):
        #print("sprite {}, at {}".format(s, (self.x, self.y)))
        self.piece.hide()
        if s != None:
            self.piece.setPixmap(s)
            self.piece.show()

        self.last_move.hide()
        self.selected.hide()
        self.can_move.hide()

        # show extra sprites
        for f in flags:
            if f == "l":
                self.last_move.show()
            elif f == "s":
                self.selected.show()
            elif f == "c":
                self.can_move.show()

    def setupUi(self):
        self.left   = 0
        self.top    = 0
        self.width  = self.config.cell_width
        self.height = self.config.cell_height
        self.setGeometry(self.left, self.top, self.width, self.height)

        if (self.x + self.y) % 2 == 1:
            pixmap = QtGui.QPixmap("sprites/board/black.png")
        else:
            pixmap = QtGui.QPixmap("sprites/board/white.png")

        self.background = QtWidgets.QLabel(self)
        self.background.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("sprites/board/last_move.png")
        self.last_move = QtWidgets.QLabel(self)
        self.last_move.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("sprites/board/selected.png")
        self.selected = QtWidgets.QLabel(self)
        self.selected.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("sprites/board/can_move.png")
        self.can_move = QtWidgets.QLabel(self)
        self.can_move.setPixmap(pixmap)

        self.piece = QtWidgets.QLabel(self)

        self.update_sprite(None, [])

    def mouseReleaseEvent(self, ev):
        print("Pressed at {},{}".format(self.x, self.y))
        self.callback((self.x, self.y))
