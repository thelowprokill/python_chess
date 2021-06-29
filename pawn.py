from piece import piece

############################################################
#                                                          #
# class pawn: child of piece                               #
#                                                          #
# purpose: pawn piece                                      #
#                                                          #
############################################################
class pawn(piece):
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
        self.piece = 'p'
        self.name  = 'Pawn'
        self.controller = controller
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
        pos = (self.x, self.y - 1 * self.owner)
        opp = self.controller.opponent.get_piece(pos)[0]
        sel = self.controller.get_piece(pos)[0]
        if not opp and not sel:
            legal_moves.append(pos)

            pos = (pos[0], pos[1] - 1 * self.owner)
            if self.x == self.starting_x and self.y == self.starting_y:
                opp = self.controller.opponent.get_piece(pos)[0]
                sel = self.controller.get_piece(pos)[0]
                if not opp and not sel:
                    legal_moves.append(pos)

        for i in range(2):
            pos = (self.x + (-1 if i == 0 else 1), self.y - 1 * self.owner)
            opp = self.controller.opponent.get_piece(pos)[0]
            if opp:
                legal_moves.append(pos)

        return legal_moves



if __name__ == "__main__":
    p = pawn(None, (1,1), 1)
    print(p.get_pos())
    print(p.get_legal_moves())
    p.move((1,3))
    print(p.get_pos())
    print(p.get_legal_moves())
