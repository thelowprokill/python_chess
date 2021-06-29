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

    def update_sprite(self, s, flags=[]):
        print("sprite {}, at {}".format(s, (self.x, self.y)))
        if s != None:
            self.piece.setPixmap(s)

        self.last_move.hide()
        self.selected.hide()
        self.can_move.hide()

        # show extra sprites
        for f in flags:
            if f == "l":
                print("last")
                self.last_move.show()
            elif f == "s":
                print("selected")
                self.selected.show()
            elif f == "c":
                print("can")
                self.can_move.show()


    def setupUi(self):
        self.left   = 0
        self.top    = 0
        self.width  = self.config.cell_width
        self.height = self.config.cell_height
        self.setGeometry(self.left, self.top, self.width, self.height)

        if (self.x + self.y) % 2 == 1:
            pixmap = QtGui.QPixmap("sprites/black.png")
        else:
            pixmap = QtGui.QPixmap("sprites/white.png")

        self.background = QtWidgets.QLabel(self)
        self.background.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("sprites/last_move.png")
        self.last_move = QtWidgets.QLabel(self)
        self.last_move.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("sprites/selected.png")
        self.selected = QtWidgets.QLabel(self)
        self.selected.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("sprites/can_move.png")
        self.can_move = QtWidgets.QLabel(self)
        self.can_move.setPixmap(pixmap)

        self.piece = QtWidgets.QLabel(self)

    def mouseReleaseEvent(self, ev):
        print("Pressed at {},{}".format(self.x, self.y))
        self.callback((self.x, self.y))
