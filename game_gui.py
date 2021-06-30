import display_gui
from board import board
import sys

############################################################
#                                                          #
# class game_display_gui:                                  #
#                                                          #
# purpose: game_controller for display_gui based game      #
#                                                          #
############################################################
class game_gui:
    ########################################################
    #                                                      #
    # function __init__:                                   #
    #                                                      #
    # purpose: set up the game init ui                     #
    #                                                      #
    ########################################################
    def __init__(self):
        self.piece = None
        self.moves = []
        self.castle_moves = []
        self.last_move = (-1, -1, -1, -1)
        self.board = board()
        self.app = display_gui.build_app()
        self.display = display_gui.MainWindow(self.board, self)
        self.new_game()
        self.render()
        self.display.show()

        display_gui.start_gui(self.app)

    ########################################################
    #                                                      #
    # function new_game:                                   #
    #                                                      #
    # purpose: set up a new game                           #
    #                                                      #
    ########################################################
    def new_game(self):
        self.board.new_game()

    ########################################################
    #                                                      #
    # function load_game:                                  #
    #                                                      #
    # purpose: set up a previous game                      #
    #                                                      #
    ########################################################
    def load_game(self):
        self.board.load_game()

    ########################################################
    #                                                      #
    # function move:                                       #
    #                                                      #
    # purpose: move for a player                           #
    #                                                      #
    ########################################################
    def move(self, l):
        res = self.select_piece(l)
        if not res and self.piece != None:
            self.select_move(l)

    ########################################################
    #                                                      #
    # function select_piece:                               #
    #                                                      #
    # purpose: selects a piece form the correct board      #
    #                                                      #
    ########################################################
    def select_piece(self, l):
        turn = self.board.turn
        player = self.board.white if turn == 1 else self.board.black
        player.clear_cue()

        piece, moves, castle_moves = self.board.select_piece(l)

        if len(moves) + len(castle_moves) > 0:
            self.piece = piece
            self.moves = moves
            self.castle_moves = castle_moves
            self.render()
            True
        else:
            False

    ########################################################
    #                                                      #
    # function select_move:                                #
    #                                                      #
    # purpose: moves selected piece                        #
    #                                                      #
    ########################################################
    def select_move(self, l):
        turn = self.board.turn
        player = self.board.white if turn == 1 else self.board.black

        success = self.board.move_piece(self.piece.get_pos(), l)
        if success:
            self.piece = None
            self.moves = []
            self.castle_moves = []
            self.render()

    ########################################################
    #                                                      #
    # function input:                                      #
    #                                                      #
    # purpose: intermediate input to add flags for gui     #
    #                                                      #
    ########################################################
    def input(self, l, p, c):
        flags = []
        if self.board.last_move[2] == l[0] and self.board.last_move[3] == l[1]:
            flags.append("l")

        pos = self.piece.get_pos() if self.piece != None else (-2, -2)
        if pos[0] == l[0] and pos[1] == l[1]:
            flags.append("s")

        for m in self.moves:
            if m[0] == l[0] and m[1] == l[1]:
                flags.append("c")
                break

        self.display.input(l, p, c, flags)

    ########################################################
    #                                                      #
    # function input_with_no_piece:                        #
    #                                                      #
    # purpose: shows last move and available moves where   #
    #   no piece is at                                     #
    #                                                      #
    ########################################################
    def input_with_no_piece(self):
        if self.board.last_move[0] != -1 and self.board.last_move[1] != -1:
            self.display.input((self.board.last_move[0], self.board.last_move[1]), "", "", "l")

        for m in self.moves:
            w, _ = self.board.white.get_piece(m)
            b, _ = self.board.black.get_piece(m)
            if not w and not b:
                self.display.input(m, "", "", "c")

        for m in self.castle_moves:
            w, _ = self.board.white.get_piece(m)
            b, _ = self.board.black.get_piece(m)
            if not w and not b:
                self.display.input(m, "", "", "c")


    ########################################################
    #                                                      #
    # function render:                                     #
    #                                                      #
    # purpose: updates display                             #
    #                                                      #
    ########################################################
    def render(self):
        self.display.clear()
        self.input_with_no_piece()
        self.board.white.update_display(self.input)
        self.board.black.update_display(self.input)
        p = self.board.white if self.board.turn == 1 else self.board.black
        player = "White" if self.board.turn == 1 else self.board.black

        self.display.draw()

if __name__ == "__main__":
    g = game_gui()
