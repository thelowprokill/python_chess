from text_display import text_display
from board import board
import sys


class game_text:
    def __init__(self):
        self.display = text_display()
        self.board = board(self, self.display, 1)
        self.menu()

    def menu(self):
        options = []
        options.append(("1", True,  self.new_game,                "New Game",      "Starting New Game."))
        options.append(("2", True,  self.board.load_game,         "Load Game",     "Loading Game"))
        options.append(("3", False, self.display.not_implemented, "Options",       ""))
        options.append(("q", True,  sys.exit,                     "Exit the game", "By"))
        valid, f, d, t = self.display.render_menu(options)
        print(t)
        print("")
        if not valid:
            self.display.not_implemented(d)
            self.menu()
        else:
            f()

    def new_game(self):
        self.turn = 1
        self.board.new_game()
        self.redraw()

    ########################################################
    #                                                      #
    # function move:                                       #
    #                                                      #
    # purpose: move for a player                           #
    #                                                      #
    # returns: true on success false otherwise             #
    #                                                      #
    ########################################################
    def move(self):
        player = self.board.white if self.turn == 1 else self.board.black
        self.board.turn = self.turn
        player.clear_cue()

        success = False
        while not success:
            res = False
            first_attempt = True
            while not res:
                p = self.display.select_piece("White" if self.turn == 1 else "Black", first_attempt)
                first_attempt = False
                try:
                    p = (int(p[0]), int(p[1]))
                    res, piece = player.get_piece(p)
                except:
                    self.check_commands(p[0], p[1])

            moves = piece.get_legal_moves()
            castle_moves = []
            if piece.piece == "K":
                castle_moves = player.can_castle()
            moves = player.check_for_check(piece, moves)
            castle_moves = player.check_for_check(piece, castle_moves)

            if len(moves) + len(castle_moves) > 0:
                d = self.display.select_move(moves + castle_moves, piece)
                try:
                    d = (int(d[0]), int(d[1]))
                    for m in castle_moves:
                        if m[0] == d[0] and m[1] == d[1]:
                            d = m
                            break
                    print("selected loc = {}.".format(d))
                    if d in moves + castle_moves:
                        success = player.move_move(p, d, True)
                        if success == False:
                            print("Failed to move {} to {}".format(piece.piece, d))
                        else:
                            self.last_move = (p[0], p[1], d[0], d[1])
                except:
                    self.check_commands(d[0], d[1])
            else:
                self.display.no_moves(piece)

    def redraw(self):
        self.display.clear()
        self.board.white.update_display(self.display.input)
        self.board.black.update_display(self.display.input)
        p = self.board.white if self.turn == 1 else self.black
        player = "White" if self.turn == 1 else "Black"
        if p.is_mate():
            self.display_is_mate(player)
        elif p.is_check():
            self.display.is_check(player)

        self.display.draw()


if __name__ == "__main__":
    g = game_text()
