import data.key as key
import data.crypto as crypto
from data.controller import controller
from data.pieces.piece        import piece
from data.pieces.pawn         import pawn
from data.pieces.rook         import rook
from data.pieces.knight       import knight
from data.pieces.bishop       import bishop
from data.pieces.queen        import queen
from data.pieces.king         import king

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
# save format:                                         #
#        White board                                   #
#        00000000                                      #
#        00000000                                      #
#        00000000                                      #
#        00000000                                      #
#        00000000                                      #
#        00000000                                      #
#        pppppppp                                      #
#        rkbqKbkr                                      #
#        kings_rook_moved  =0                          #
#        queens_rook_moved =0                          #
#        king_moved        =0                          #
#                                                      #
#        Black board                                   #
#        rkbqKbkr                                      #
#        pppppppp                                      #
#        00000000                                      #
#        00000000                                      #
#        00000000                                      #
#        00000000                                      #
#        00000000                                      #
#        00000000                                      #
#        kings_rook_moved  =0                          #
#        queens_rook_moved =0                          #
#        king_moved        =0                          #
#                                                      #
#        whose_turn =1                                 #
#        last_move  =(from_x, from_y, to_x, to_y)      #
#                                                      #
# returns: success                                     #
#                                                      #
########################################################

def save_game(board, fn = "games/save.dat"):
    ##############################
    ### gather data            ###
    ##############################

    string = "White board\n"
    string = string + get_pieces_string(board.white)
    moved  = find_moved_pieces(board.white)
    string = "{}\nkings_rook_moved  ={}".format(string, moved[0])
    string = "{}\nqueens_rook_moved ={}".format(string, moved[1])
    string = "{}\nking_moved        ={}".format(string, moved[2])
    string = "{}\n\n".format(string)

    string = string + "Black board\n"
    string = string + get_pieces_string(board.black)
    moved  = find_moved_pieces(board.black)
    string = "{}\nkings_rook_moved  ={}".format(string, moved[0])
    string = "{}\nqueens_rook_moved ={}".format(string, moved[1])
    string = "{}\nking_moved        ={}".format(string, moved[2])
    string = "{}\n\n".format(string)

    string = "{}whose_turn ={}\n".format(string, board.turn)
    string = "{}last_move  ={}".format(string, board.last_move)

    ##############################
    ### /gather data           ###
    ##############################

    ##############################
    ### write data             ###
    ##############################

    fp = open(fn, "w+")
    string = crypto.in_code(key.key(), string)
    fp.write(string)
    fp.close()

    ##############################
    ### /write data            ###
    ##############################

    return True

############################################################
#                                                          #
# function get_pieces_string:                              #
#                                                          #
# purpose: converts players board into 8, 8 byte strings   #
#                                                          #
############################################################
def get_pieces_string(player):
    string = ""
    for i in range(8):
        for j in range(8):
            b, p = player.get_piece((j, i))
            if b:
                string = string + p.piece
            else:
                string = string + "0"
        string = string + "\n"
    return string

############################################################
#                                                          #
# function find_moved_pieces:                              #
#                                                          #
# purpose: finds which pieces have been moved              #
#                                                          #
############################################################
def find_moved_pieces(player):
    kings_rook  = True
    queens_rook = True
    king        = True
    for p in player.my_pieces:
        if p.piece == "r" and p.starting_x == 7:
            kings_rook = p.moved
        if p.piece == "r" and p.starting_x == 0:
            queens_rook = p.moved
        if p.piece == "K":
            king = p.moved

    return (int(kings_rook), int(queens_rook), int(king))

############################################################
#                                                          #
# function load_game:                                      #
#                                                          #
# purpose: loads saved game from file fn                   #
#                                                          #
############################################################
def load_game(board, fn = "games/save.dat"):
    ##############################
    ### read data              ###
    ##############################

    string = ""
    save = open(fn, "r")
    for line in save:
        string = string + line
    save.close()
    string = crypto.de_code(key.key(), string)

    ##############################
    ### /read data             ###
    ##############################

    ##############################
    ### extract data           ###
    ##############################

    splits = string.split("\n")
    white_board = splits[1:9]
    white_kings_rook  = bool(int(splits[10].split("=")[1]))
    white_queens_rook = bool(int(splits[11].split("=")[1]))
    white_king        = bool(int(splits[12].split("=")[1]))

    black_board = splits[15:23]
    black_kings_rook  = bool(int(splits[24].split("=")[1]))
    black_queens_rook = bool(int(splits[25].split("=")[1]))
    black_king        = bool(int(splits[26].split("=")[1]))

    turn = int(splits[28].split("=")[1])
    move = splits[29].split("=")[1]
    move = move.replace("(", "").replace(")", "").replace(" ", "").split(",")

    ##############################
    ### /extract data          ###
    ##############################

    ##############################
    ### convert to useful data ###
    ##############################

    last_move = []
    for i in range(4):
        last_move.append(int(move[i]))

    white = load_pieces_from_string(white_board, 1)
    black = load_pieces_from_string(black_board, -1)
    white.construct(black)
    black.construct(white)

    ##############################
    ### /convert to useful data ##
    ##############################

    ##############################
    ### set moved pieces       ###
    ##############################

    b, p = white.get_piece((0, 7))
    if b and p.piece == 'r':
        p.moved = white_queens_rook
    b, p = white.get_piece((7, 7))
    if b and p.piece == 'r':
        p.moved = white_kings_rook
    b, p = black.get_piece((0, 0))
    if b and p.piece == 'r':
        p.moved = black_queens_rook
    b, p = black.get_piece((7, 0))
    if b and p.piece == 'r':
        p.moved = black_kings_rook

    wk = white.get_king()
    wk.moved = white_king
    bk = black.get_king()

    bk.moved = black_king
    ##############################
    ### /set moved pieces      ###
    ##############################

    ##############################
    ### finalize board         ###
    ##############################

    board.white = white
    board.black = black

    board.turn = turn
    board.last_move = (last_move[0], last_move[1], last_move[2], last_move[3])

    ##############################
    ### /finalize board        ###
    ##############################

############################################################
#                                                          #
# function load_pieces_from_string:                        #
#                                                          #
# purpose: converts 8, 8 byte strings into a players board #
#                                                          #
############################################################
def load_pieces_from_string(string, owner):
    player = controller(owner)
    player.my_pieces = []
    x = 0
    y = 0
    for l in string:
        for c in l:
            if c == "p":
                player.my_pieces.append(pawn  (player, (x, y), owner))
            elif c == "r":
                # set this to false so that I don't have to find the rook later
                this_rook = rook(player, (x, y), owner)
                this_rook.moved = True
                player.my_pieces.append(this_rook)
            elif c == "k":
                player.my_pieces.append(knight(player, (x, y), owner))
            elif c == "b":
                player.my_pieces.append(bishop(player, (x, y), owner))
            elif c == "q":
                player.my_pieces.append(queen (player, (x, y), owner))
            elif c == "K":
                player.my_pieces.append(king  (player, (x, y), owner))

            x = x + 1
        x = 0
        y = y + 1
    return player

