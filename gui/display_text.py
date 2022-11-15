import numpy as np

############################################################
#                                                          #
# class text_display: child of piece                       #
#                                                          #
# purpose: handle user interface in terminal               #
#                                                          #
############################################################
class display_text:
    ########################################################
    #                                                      #
    # function __init__:                                   #
    #                                                      #
    # purpose: set up the display                          #
    #                                                      #
    ########################################################
    def __init__(self):
        self.locations = np.zeros((8, 8), dtype="str")
        self.clear()

    ########################################################
    #                                                      #
    # function no_moves:                                   #
    #                                                      #
    # purpose: informs the user that the selected piece    #
    #          has no legal moves                          #
    #                                                      #
    ########################################################
    def no_moves(self, piece):
        print("Piece {} at {} has no legal moves.".format(piece.piece, piece.get_pos()))

    ########################################################
    #                                                      #
    # function select_piece:                               #
    #                                                      #
    # purpose: prompt user to select a piece               #
    #                                                      #
    ########################################################
    def select_piece(self, who, first_attempt):
        if not first_attempt:
            print("Try again. There is no friendly piece there")
        print("{}'s move".format(who))
        print("Please select a piece.")
        x = input("X: ")
        y = input("Y: ")
        return (x, y)

    ########################################################
    #                                                      #
    # function select_move:                                #
    #                                                      #
    # purpose: prompt user to select a move                #
    #                                                      #
    ########################################################
    def select_move(self, moves, piece):
        print("Selected {} at {}".format(piece.name, piece.get_pos()))
        print("Available moves are...")
        print(moves)
        print("Select a destination.")
        x = input("X: ")
        y = input("Y: ")
        return (x, y)

    ########################################################
    #                                                      #
    # function input:                                      #
    #                                                      #
    # purpose: add a piece to the render                   #
    #                                                      #
    ########################################################
    def input(self, l, p, c, flags=[]):
        np = translate_piece(p, c)
        self.locations[l[1]][l[0]] = np

    ########################################################
    #                                                      #
    # function is_check:                                   #
    #                                                      #
    # purpose: tell the user when someone is in check      #
    #                                                      #
    ########################################################
    def is_check(self, who):
        self.check = True
        self.who   = who

    ########################################################
    #                                                      #
    # function is_mate:                                    #
    #                                                      #
    # purpose: tell the user when someone is in checkmate  #
    #                                                      #
    ########################################################
    def is_mate(self, who):
        self.mate = True
        self.who  = who

    ########################################################
    #                                                      #
    # function clear:                                      #
    #                                                      #
    # purpose: reset the board render                      #
    #                                                      #
    ########################################################
    def clear(self):
        for i in range(8):
            for j in range(8):
                self.locations[i][j] = "  "

        self.check = False
        self.mate  = False
        self.who   = ""

    ########################################################
    #                                                      #
    # function not_implemented:                            #
    #                                                      #
    # purpose: inform user that the function does not      #
    #   exist yet.                                         #
    #                                                      #
    ########################################################
    def not_implemented(self, fn):
        print("I'm sorry, {} has not been implemented yet.".format(fn))

    ########################################################
    #                                                      #
    # function invalid:                                    #
    #                                                      #
    # purpose: inform user of an invalid menu option       #
    #                                                      #
    ########################################################
    def invalid(self, option):
        print("{} is not a valid option".format(option))

    ########################################################
    #                                                      #
    # function render_menu:                                #
    #                                                      #
    # purpose: draw the main menu with links to features   #
    #   of the game.                                       #
    #                                                      #
    ########################################################
    def render_menu(self, menu_options):
        print("\n")
        print("=========================================")
        print("=============== Main Menu ===============")
        for option in menu_options:
            c = option[0]
            d = option[3]
            print("[{}]: {}".format(c, d))
        print("")
        decision = input("option: ")
        for option in menu_options:
            c = option[0]
            v = option[1]
            f = option[2]
            d = option[3]
            t = option[4]
            if c == decision:
                return v, f, d, t
        self.invalid(decision)
        return self.render_menu(menu_options)

    ########################################################
    #                                                      #
    # function draw:                                       #
    #                                                      #
    # purpose: render stored board                         #
    #                                                      #
    ########################################################
    def draw(self):
        print("+===+===+===+===+===+===+===+===+===+===+")
        print("|   ", end="")
        for i in range(8):
            print("| {} ".format(i), end="")
        print("|   |")
        for i in range(8):
            print("+===+===+===+===+===+===+===+===+===+===+")
            print("| {} ".format(i), end="")
            for j in range(8):
                if (i + j) % 2 == 1:
                    print("|-{}-".format(self.locations[i][j][0]), end="")
                else:
                    print("| {} ".format(self.locations[i][j][0]), end="")

            print("| {} |".format(i))
        print("+===+===+===+===+===+===+===+===+===+===+")
        print("|   ", end="")
        for i in range(8):
            print("| {} ".format(i), end="")
        print("|   |")
        print("+===+===+===+===+===+===+===+===+===+===+")

        if self.mate:
            print("Checkmate. {} wins".format(self.who))
        elif self.check:
            print("{} in check".format(self.who))


######################################################
#                                                    #
# function translate_piece:                          #
#                                                    #
# purpose: convert character input to chess pieces   #
#   9812: white king                                 #
#   9813: white queen                                #
#   9814: white rook                                 #
#   ...                                              #
#   9818: black king                                 #
#   9819: blakc queen                                #
#   9820: blakc rook                                 #
#   ...                                              #
#                                                    #
######################################################
def translate_piece(p, owner):
    base = 9812 # white king
    offset = 0 if owner == 'b' else 6
    if p == 'K':
        return chr(base + offset)
    elif p == 'q':
        return chr(1 + base + offset)
    elif p == 'r':
        return chr(2 + base + offset)
    elif p == 'b':
        return chr(3 + base + offset)
    elif p == 'k':
        return chr(4 + base + offset)
    elif p == 'p':
        return chr(5 + base + offset)
