from controller import controller
import save_load as sl
import sys

############################################################
#                                                          #
# class board:                                             #
#                                                          #
# purpose: manages both players and turn taking            #
#                                                          #
############################################################
class board:
    ########################################################
    #                                                      #
    # function __init__:                                   #
    #                                                      #
    # purpose: set up the board                            #
    #                                                      #
    ########################################################
    def __init__(self, parent, display, display_type):
        self.parent       = parent
        self.display      = display
        self.display_type = display_type
        self.turn         = 1
        self.init_commands()

    ########################################################
    #                                                      #
    # function game_over:                                  #
    #                                                      #
    # purpose: check for checkmate                         #
    #                                                      #
    # returns: returns checkmate                           #
    #                                                      #
    ########################################################
    def game_over(self):
        p = self.white if self.turn == 1 else self.black
        return p.is_mate()

    ########################################################
    #                                                      #
    # function game:                                       #
    #                                                      #
    # purpose: main loop for the game                      #
    #                                                      #
    ########################################################
    def game(self):
        self.redraw()
        while not self.game_over():
            self.move()
            self.turn = self.turn * -1
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
        player = self.white if self.turn == 1 else self.black
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

    ########################################################
    #                                                      #
    # function redraw:                                     #
    #                                                      #
    # purpose: adds all pieces to render. Tells the        #
    #          display to render the board                 #
    #                                                      #
    ########################################################
    def redraw(self):
        self.display.clear()
        self.white.update_display(self.display.input)
        self.black.update_display(self.display.input)
        p = self.white if self.turn == 1 else self.black
        player = "White" if self.turn == 1 else "Black"
        if p.is_mate():
            self.display.is_mate(player)
        elif p.is_check():
            self.display.is_check(player)

        self.display.draw()

    ########################################################
    #                                                      #
    # function new_game:                                   #
    #                                                      #
    # purpose: constructs both sides and starts game loop  #
    #                                                      #
    ########################################################
    def new_game(self):
        self.last_move = (0,0,0,0)
        self.white = controller(1)
        self.black = controller(-1)
        self.white.construct(self.black)
        self.black.construct(self.white)
        self.game()

    ########################################################
    #                                                      #
    # function save_game:                                  #
    #                                                      #
    # purpose: writes game data to specified file.         #
    #                                                      #
    # notes: gets filename from user if GUI. otherwise     #
    #        saves to data/save.dat. extra data is for     #
    #        castling, en passant, and current turn        #
    #                                                      #
    # returns: success                                     #
    #                                                      #
    ########################################################
    def save_game(self):
        sl.save_game(self)
        self.game()

    ########################################################
    #                                                      #
    # function load_game:                                  #
    #                                                      #
    # purpose: reads game data from specified file.        #
    #                                                      #
    # notes: gets filename from user if GUI. otherwise     #
    #        loads from data/save.dat. extra data is for   #
    #        castling, en passant, and current turn        #
    #                                                      #
    # returns: success                                     #
    #                                                      #
    ########################################################
    def load_game(self):
        sl.load_game(self)
        self.game()

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
        self.commands.append(("s", self.save_game, "Saving Game", "Save the current game state."))
        self.commands.append(("l", self.load_game, "Loading Game", "Load saved game, losses current progress."))
        self.commands.append(("r", self.redraw, "Redrawing board", "Redraws the board. In case it gets to far up."))
        self.commands.append(("m", self.parent.menu, "Main Menu", "Main Menu"))
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
    b = board()
