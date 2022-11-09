from data.pieces.piece import piece

############################################################
#                                                          #
# class bishop: child of piece                             #
#                                                          #
# purpose: bishop piece                                    #
#                                                          #
############################################################
class bishop(piece):
    ########################################################
    #                                                      #
    # function __init__:                                   #
    #                                                      #
    # purpose: set up the piece. set member variables      #
    #          call super init()                           #
    #                                                      #
    ########################################################
    def __init__(self, controller, location, owner):
        self.parent = piece
        self.controller = controller
        self.piece = 'b'
        self.name  = 'Bishop'
        self.parent.__init__(self, controller, location, owner, self.piece)

    ########################################################
    #                                                      #
    # function get_legal_moves                             #
    #                                                      #
    # purpose: make a list of all possible moves.          #
    #                                                      #
    # notes: ignores check because that is handled         #
    #        elsewhere to avoid infinite loops             #
    #                                                      #
    # returns: list of all possible moves                  #
    #                                                      #
    ########################################################
    def get_legal_moves(self):
        legal_moves = []
        for i in range(4):
            for j in range(1, 8):
                if i == 0:
                    pos = (self.x + j, self.y + j)
                elif i == 1:
                    pos = (self.x + j, self.y - j)
                elif i == 2:
                    pos = (self.x - j, self.y + j)
                else:
                    pos = (self.x - j, self.y - j)

                if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                    break
                elif self.controller.opponent.get_piece(pos)[0]:
                    legal_moves.append(pos)
                    break
                elif self.controller.get_piece(pos)[0]:
                    break
                else:
                    legal_moves.append(pos)

        return legal_moves
