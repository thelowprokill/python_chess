from display_text import display_text
from board import board
import sys


############################################################
#                                                          #
# class game_text:                                         #
#                                                          #
# purpose: game_controller for text based game             #
#                                                          #
############################################################
class game_text:
    ########################################################
    #                                                      #
    # function __init__:                                   #
    #                                                      #
    # purpose: set up the game                             #
    #                                                      #
    ########################################################
    def __init__(self):
        self.display = display_text()
        self.board = board()
        self.init_commands()
        self.menu()

    ########################################################
    #                                                      #
    # function menu:                                       #
    #                                                      #
    # purpose: generates a menu to be displayed by         #
    #   display_text                                       #
    #                                                      #
    ########################################################
    def menu(self):
        options = []
        options.append(("1", True,  self.new_game,  "New Game",      "Starting New Game."))
        options.append(("2", True,  self.load_game, "Load Game",     "Loading Game"))
        options.append(("3", False, None,           "Options",       ""))
        options.append(("q", True,  sys.exit,       "Exit the game", "By"))
        valid, f, d, t = self.display.render_menu(options)
        print(t)
        print("")
        if not valid:
            self.display.not_implemented(d)
            self.menu()
        else:
            f()

    ########################################################
    #                                                      #
    # function new_game:                                   #
    #                                                      #
    # purpose: set up a new game                           #
    #                                                      #
    ########################################################
    def new_game(self):
        self.board.new_game()
        self.game_loop()

    ########################################################
    #                                                      #
    # function load_game:                                  #
    #                                                      #
    # purpose: set up a previous game                      #
    #                                                      #
    ########################################################
    def load_game(self):
        self.board.load_game()
        self.game_loop()

    ########################################################
    #                                                      #
    # function game_loop:                                  #
    #                                                      #
    # purpose: main loop for the game                      #
    #                                                      #
    ########################################################
    def game_loop(self):
        self.redraw()
        while not self.board.game_over():
            self.move()
            self.redraw()

    ########################################################
    #                                                      #
    # function move:                                       #
    #                                                      #
    # purpose: move for a player                           #
    #                                                      #
    ########################################################
    def move(self):
        turn = self.board.turn
        player = self.board.white if turn == 1 else self.board.black
        player.clear_cue()

        success = False
        first_attempt = True
        while not success:
            res = False
            while not res:
                p = self.display.select_piece("White" if turn == 1 else "Black", first_attempt)
                try:
                    p = (int(p[0]), int(p[1]))
                    first_attempt = False
                    piece, moves, castle_moves = self.board.select_piece(p)
                    res = len(moves) + len(castle_moves) > 0
                    if not res:
                        if piece != None:
                            self.display.no_moves(piece)
                except:
                    self.check_commands(p[0], p[1])

            d = self.display.select_move(moves + castle_moves, piece)
            try:
                d = (int(d[0]), int(d[1]))
                success = self.board.move_piece(p, d)
                if success == False:
                    print("Failed to move {} to {}".format(piece.piece, d))
                    return False
            except:
               self.check_commands(d[0], d[1])

    ########################################################
    #                                                      #
    # function redraw:                                     #
    #                                                      #
    # purpose: draws the board                             #
    #                                                      #
    ########################################################
    def redraw(self):
        self.display.clear()
        self.board.white.update_display(self.display.input)
        self.board.black.update_display(self.display.input)
        p = self.board.white if self.board.turn == 1 else self.board.black
        player = "White" if self.board.turn == 1 else "Black"
        if p.is_mate():
            self.display_is_mate(player)
        elif p.is_check():
            self.display.is_check(player)

        self.display.draw()

    ########################################################
    #                                                      #
    # function command_help:                               #
    #                                                      #
    # purpose: shows the player a list of possible         #
    #          commands                                    #
    #                                                      #
    ########################################################
    def command_help(self):
        for command in self.commands:
            c = command[0]
            d = command[3]
            print("{}: {}".format(c, d))

    ########################################################
    #                                                      #
    # function init_commands:                              #
    #                                                      #
    # purpose: generates list of possible commands with    #
    #          functions to be called as well as string to #
    #          print before calling them                   #
    #                                                      #
    ########################################################
    def init_commands(self):
        self.commands = []
        self.commands.append(("q", sys.exit, "Exiting Game", "Exit the game."))
        self.commands.append(("n", self.new_game, "Starting New Game", "Start a new game."))
        self.commands.append(("s", self.board.save_game, "Saving Game", "Save the current game state."))
        self.commands.append(("l", self.load_game, "Loading Game", "Load saved game, losses current progress."))
        self.commands.append(("r", self.redraw, "Redrawing board", "Redraws the board. In case it gets to far up."))
        self.commands.append(("m", self.menu, "Main Menu", "Main Menu"))
        self.commands.append(("h", self.command_help, "Help", "Shows list of available commands."))

    ########################################################
    #                                                      #
    # function check_commands:                             #
    #                                                      #
    # purpose: decides what command to execute. if command #
    #          is not found tell the user how to get the   #
    #          help list up.                               #
    #                                                      #
    ########################################################
    def check_commands(self, x, y):
        for command in self.commands:
            c = command[0]
            f = command[1]
            l = command[2]
            if x == c or y == c:
                print(l)
                f()
                return
        print("I did not understand that input, use \"h\" for help")

if __name__ == "__main__":
    g = game_text()
