from piece        import piece
from pawn         import pawn
from rook         import rook
from knight       import knight
from bishop       import bishop
from queen        import queen
from king         import king

############################################################
#                                                          #
# class controller:                                        #
#                                                          #
# purpose: holds all the pieces and controls the logic for #
#          one player.                                     #
#                                                          #
############################################################
class controller:
    ########################################################
    #                                                      #
    # Function __init__:                                   #
    #                                                      #
    # purpose: set the starting locations of each piece    #
    #          initialize member variables                 #
    #                                                      #
    ########################################################
    def __init__(self, owner):
        self.my_pieces = []
        self.owner = owner

        for i in range(8):
            self.my_pieces.append(pawn(self, (i, 1 if owner == -1 else 6), owner))

        home_row = 0 if owner == -1 else 7
        self.my_pieces.append(rook(  self, (0, home_row), owner))
        self.my_pieces.append(knight(self, (1, home_row), owner))
        self.my_pieces.append(bishop(self, (2, home_row), owner))
        self.my_pieces.append(queen( self, (3, home_row), owner))
        self.my_pieces.append(king(  self, (4, home_row), owner))
        self.my_pieces.append(bishop(self, (5, home_row), owner))
        self.my_pieces.append(knight(self, (6, home_row), owner))
        self.my_pieces.append(rook(  self, (7, home_row), owner))

        self.cue = None

    ########################################################
    #                                                      #
    # Function construct:                                  #
    #                                                      #
    # purpose: second init. set opponent                   #
    #                                                      #
    ########################################################
    def construct(self, opponent):
        self.opponent = opponent

    ########################################################
    #                                                      #
    # Function get_king:                                   #
    #                                                      #
    # purpose: gets the king from list of pieces           #
    #                                                      #
    # returns: king object                                 #
    #                                                      #
    ########################################################
    def get_king(self):
        for p in self.my_pieces:
            if p.piece == "K":
                return p
        print("Error: failed to find king")

    ########################################################
    #                                                      #
    # Function can_castle:                                 #
    #                                                      #
    # purpose: find legal castling moves                   #
    #                                                      #
    # returns: list of moves with 'ck' or 'cq' on the end  #
    #          to specify king's side or queen's side and  #
    #          distinguish the move as a special move      #
    #                                                      #
    ########################################################
    def can_castle(self):
        rooks = []
        king = None

        ################################
        ### find pieces k, r, r      ###
        ################################

        for p in self.my_pieces:
            if p.piece == "K":
                king = p
            if p.piece == "r":
                rooks.append(p)
        if len(rooks) == 0 or king.moved:
            return []

        ################################
        ### /find pieces k, r, r     ###
        ################################

        ################################
        ### check if they have moved ###
        ################################

        moves = []
        for r in rooks:
            if not r.moved:
                if r.x == 7 and not self.get_piece((5, r.y))[0] and not self.get_piece((6, r.y))[0]:
                    moves.append((king.x + 2, king.y, "ck"))

                elif r.x == 0 and not self.get_piece((3, r.y))[0] and not self.get_piece((2, r.y))[0] and not self.get_piece((1, r.y))[0]:
                    moves.append((king.x - 2, king.y, "cq"))
        return moves

        ################################
        ### check if they have moved ###
        ################################


    ########################################################
    #                                                      #
    # Function has_moved:                                  #
    #                                                      #
    # purpose: update moved attribute of pieces            #
    #                                                      #
    ########################################################
    def has_moved():
        for p in self.my_pieces:
            p.has_moved()

    ########################################################
    #                                                      #
    # Function is_check:                                   #
    #                                                      #
    # purpose: find if player in check                     #
    #                                                      #
    # returns: check status                                #
    #                                                      #
    ########################################################
    def is_check(self):
        k = self.get_king()
        moves = self.opponent.get_all_moves()
        k_pos = k.get_pos()
        if k_pos in moves:
            return True
        return False

    ########################################################
    #                                                      #
    # Function is_mate:                                    #
    #                                                      #
    # purpose: find if player in checkmate                 #
    #                                                      #
    # notes: slow                                          #
    #                                                      #
    # returns: checkmate status                            #
    #                                                      #
    ########################################################
    def is_mate(self):
        # no checkmate without check
        if not self.is_check():
            return False

        # check for a legal move
        moves = []
        for p in self.my_pieces:
            p_moves = p.get_legal_moves()
            p_moves = self.check_for_check(p, p_moves)
            moves.extend(self.check_for_check(p, p_moves))

        if len(moves) > 0:
            return False
        return True


    ########################################################
    #                                                      #
    # Function get_piece:                                  #
    #                                                      #
    # purpose: get piece at location                       #
    #                                                      #
    # returns: bool found, piece                           #
    #                                                      #
    ########################################################
    def get_piece(self, l):
        for p in self.my_pieces:
            if p.get_pos() == l:
                return True, p
        return False, None

    ########################################################
    #                                                      #
    # Function get_all_moves:                              #
    #                                                      #
    # purpose: get all possible moves                      #
    #                                                      #
    # notes: excludes check and castling, because neither  #
    #        are relevant for this application.            #
    #                                                      #
    # returns: list of moves                               #
    #                                                      #
    ########################################################
    def get_all_moves(self):
        legal_moves = []
        for p in self.my_pieces:
            moves = p.get_legal_moves()
            legal_moves.extend(moves)
        return legal_moves

    ########################################################
    #                                                      #
    # Function update_display:                             #
    #                                                      #
    # purpose: adds every piece and location to render     #
    #                                                      #
    #                                                      #
    ########################################################
    def update_display(self, callback):
        for p in self.my_pieces:
            callback(p.get_pos(), p.piece, 'w' if self.owner == 1 else 'b')

    ########################################################
    #                                                      #
    # Function capture:                                    #
    #                                                      #
    # purpose: removes piece and adds to cue               #
    #                                                      #
    # notes: piece is added to cue so that valid move      #
    #        testing can return the piece when done        #
    #                                                      #
    ########################################################
    def capture(self, l):
        b, p = self.get_piece(l)
        if b:
            self.cue = p
            self.my_pieces.remove(p)
        return b

    ########################################################
    #                                                      #
    # Function replace_piece:                              #
    #                                                      #
    # purpose: puts removed piece back on the board        #
    #                                                      #
    ########################################################
    def replace_piece(self):
        if self.cue != None:
            self.my_pieces.append(self.cue)

    ########################################################
    #                                                      #
    # Function clear_cue:                                  #
    #                                                      #
    # purpose: finalize removal of piece                   #
    #                                                      #
    ########################################################
    def clear_cue(self):
        self.cue = None

    ########################################################
    #                                                      #
    # Function move_move: why it is name this... IDK       #
    #                                                      #
    # purpose: move a piece capturing any opponent piece   #
    #          occupying the square.                       #
    #                                                      #
    # notes: special parameter official to replace the     #
    #        rook when testing if a castle move is valid   #
    #                                                      #
    ########################################################
    def move_move(self, m_from, m_to, official=False):
        v, p = self.get_piece(m_from)
        if not v:
            return False

        ################################
        ### Castling                 ###
        ################################

        # could be made more elegant
        if p.piece == "K":
            castle_moves = self.can_castle()
            if m_to in castle_moves:
                if self.is_check():
                    return False
                for i in range(p.x, m_to[0]):
                    p.move((i, p.y))
                    if self.opponent.capture((i, p.y)):
                        self.opponent.replace_piece()
                        return False
                    if self.is_check():
                        p.move(m_from)
                        return False

                b, r = self.get_piece((7 if m_to[2] == "ck" else 0, p.y))
                if b:
                    if not official:
                        p.move(m_from)
                        return True
                    r.move((m_to[0] + (-1 if m_to[2] == "ck" else 1), m_to[1]))
                    p.move(m_to)
                    return True
                p.move(m_from)
                return False

        ################################
        ### /Castling                ###
        ################################

        ################################
        ### Normal moves             ###
        ################################

        legal_moves = p.get_legal_moves()
        if m_to not in legal_moves:
            return False

        p.move(m_to)
        self.opponent.capture(m_to)
        if self.is_check():
            p.move(m_from)
            self.opponent.replace_piece()
            return False

        return True

        ################################
        ### /Normal moves            ###
        ################################

    ########################################################
    #                                                      #
    # Function check_for_check:                            #
    #                                                      #
    # purpose: removes moves that are illegal because they #
    #          put the player in check                     #
    #                                                      #
    ########################################################
    def check_for_check(self, p, moves_p):
        pos = p.get_pos()
        moves = []
        for m in moves_p:
            if self.move_move(pos, m):
                moves.append(m)
            self.opponent.replace_piece()
            p.move(pos)
        return moves
