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
    def __init__(self):
        pass

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
        self.turn = 1

    ########################################################
    #                                                      #
    # function select_piece:                               #
    #                                                      #
    # purpose: selects a piece at given location           #
    #                                                      #
    # returns: its legal moves                             #
    #                                                      #
    ########################################################
    def select_piece(self, position):
        player = self.white if self.turn == 1 else self.black
        res, piece = player.get_piece(position)
        if piece == None:
            return None, [], []
        else:
          moves = piece.get_legal_moves()
          castle_moves = []
          if piece.piece == "K":
              castle_moves = player.can_castle()
          moves = player.check_for_check(piece, moves)
          castle_moves = player.check_for_check(piece, castle_moves)
          return piece, moves, castle_moves


    ########################################################
    #                                                      #
    # function move_piece:                                 #
    #                                                      #
    # purpose: moves a selected piece at given location to #
    #   a new location.                                    #
    #                                                      #
    # returns: success                                     #
    #                                                      #
    ########################################################
    def move_piece(self, m_from, m_to):
        player = self.white if self.turn == 1 else self.black
        piece, moves, castle_moves = self.select_piece(m_from)
        for m in castle_moves:
            if m[0] == m_to[0] and m[1] == m_to[1]:
                m_to = m
                break
        if m_to in moves + castle_moves:
            success = player.move_move(m_from, m_to, True)
            if success:
                self.turn = self.turn * -1
                self.last_move = (m_from[0], m_from[1], m_to[0], m_to[1])
        return success

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

if __name__ == "__main__":
    b = board()
