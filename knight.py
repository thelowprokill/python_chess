from piece import piece

############################################################
#                                                          #
# class knight: child of piece                             #
#                                                          #
# purpose: knight piece                                    #
#                                                          #
############################################################
class knight(piece):
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
        self.piece = 'k'
        self.name  = 'Knight'
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

        m = (self.x + 1, self.y + 2)
        if m[0] <= 7 and m[0] >= 0 and m[1] <= 7 and m[1] >= 0:
            if not self.controller.get_piece(m)[0]:
                legal_moves.append(m)
        m = (self.x + 1, self.y - 2)
        if m[0] <= 7 and m[0] >= 0 and m[1] <= 7 and m[1] >= 0:
            if not self.controller.get_piece(m)[0]:
                legal_moves.append(m)

        m = (self.x - 1, self.y + 2)
        if m[0] <= 7 and m[0] >= 0 and m[1] <= 7 and m[1] >= 0:
            if not self.controller.get_piece(m)[0]:
                legal_moves.append(m)
        m = (self.x - 1, self.y - 2)
        if m[0] <= 7 and m[0] >= 0 and m[1] <= 7 and m[1] >= 0:
            if not self.controller.get_piece(m)[0]:
                legal_moves.append(m)

        m = (self.x + 2, self.y + 1)
        if m[0] <= 7 and m[0] >= 0 and m[1] <= 7 and m[1] >= 0:
            if not self.controller.get_piece(m)[0]:
                legal_moves.append(m)
        m = (self.x + 2, self.y - 1)
        if m[0] <= 7 and m[0] >= 0 and m[1] <= 7 and m[1] >= 0:
            if not self.controller.get_piece(m)[0]:
                legal_moves.append(m)

        m = (self.x - 2, self.y + 1)
        if m[0] <= 7 and m[0] >= 0 and m[1] <= 7 and m[1] >= 0:
            if not self.controller.get_piece(m)[0]:
                legal_moves.append(m)
        m = (self.x - 2, self.y - 1)
        if m[0] <= 7 and m[0] >= 0 and m[1] <= 7 and m[1] >= 0:
            if not self.controller.get_piece(m)[0]:
                legal_moves.append(m)

        return legal_moves
