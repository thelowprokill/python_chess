############################################################
#                                                          #
# class piece:                                             #
#                                                          #
# purpose: parent class of all pieces                      #
#                                                          #
############################################################
class piece:
    ########################################################
    #                                                      #
    # function __init__:                                   #
    #                                                      #
    # purpose: set up the piece. set member variables      #
    #                                                      #
    ########################################################
    def __init__(self, controller, location, owner, piece):
        self.x = location[0]
        self.y = location[1]
        self.starting_x = location[0]
        self.starting_y = location[1]
        self.controller = controller
        self.owner = owner
        self.piece = piece
        self.moved = False

    ########################################################
    #                                                      #
    # function move:                                       #
    #                                                      #
    # purpose: move the piece without checking to another  #
    #          location                                    #
    #                                                      #
    ########################################################
    def move(self, m):
        self.x = m[0]
        self.y = m[1]

    ########################################################
    #                                                      #
    # function has_moved:                                  #
    #                                                      #
    # purpose: update moved if piece is not at starting    #
    #          location                                    #
    #                                                      #
    ########################################################
    def has_moved(self):
        if self.x != self.starting_x or self.y != self.starting_y:
            self.moved = True

    ########################################################
    #                                                      #
    # function get_pos:                                    #
    #                                                      #
    # purpose: get current location                        #
    #                                                      #
    ########################################################
    def get_pos(self):
        return (self.x, self.y)
