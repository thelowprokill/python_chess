from piece import piece

############################################################
#                                                          #
# class king: child of piece                               #
#                                                          #
# purpose: king piece                                      #
#                                                          #
############################################################
class king(piece):
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
        self.piece = 'K'
        self.name  = 'King'
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

        for i in range(3):
            for j in range(3):
                pos = (self.x - 1 + i, self.y - 1 + j)
                if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                    pass
                elif self.controller.get_piece(pos)[0]:
                    pass
                else:
                    legal_moves.append(pos)


        return legal_moves
