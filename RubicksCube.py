#  Rubick's Cube representation
#       This representation will contain all child objects as well.
#  Notes:
#       White Side -> Front -> 0
#       Red Side -> Top -> 1
#       Blue Side -> Left -> 2
#       Green Side -> Right -> 3
#       Orange Side -> Bottom -> 4
#       Yellow Side -> Back -> 5
#
#       How sides are represented.
#
#       Single Side:
#           --- --- ---
#          | 0 | 1 | 2 |
#           --- --- ---
#          | 3 | X | 4 |
#           --- --- ---
#          | 5 | 6 | 7 |
#           --- --- ---
#
#       Entire Block:
#
#             ---
#            | 1 |
#         --- --- ---
#        | 2 | 0 | 3 |
#         --- --- ---
#            | 4 |
#             ---
#            | 5 |
#             ---
#



class RubiksCube:
    # note on mechanics of the block:
    #   Only faces can rotate.
    #   faces can rotate CW or CCW
    #       This will be based on orientation from the 'Entire Block' representation from above.


    def __init__(self, face_0, face_1, face_2, face_3, face_4, face_5):
        self.face_0 = face_0
        self.face_1 = face_1
        self.face_2 = face_2
        self.face_3 = face_3
        self.face_4 = face_4
        self.face_5 = face_5

    def alter_color(self, face, cell, piece):
        # TODO

    def solve(self):
        #TODO
        ### White-cross -> White Solid -> Two rows -> yellow cross (mismatch) -> yellow cross (complete) -> intermetiate corner -> complete


class RubiksFace:

    def __init__(self):
        #TODO


class RubiksCell:

    def __init__(self, color):
        self.color = color

class RubicksMiddleCell(RubiksCell):
    def __init__(self, color, adjacent_cell):
        self.color = color
        self.adjacent_cell = adjacent_cell

class RubiksCornerCell(RubiksCell):
    # note:
    #   layout of this cell is with this orientation:
    #       L/(this cell)\R
    #       /             \
    #
    #   all of these cells have a white or yellow equivalent cell.

    def __init__(self, color, left_adj_cell, right_adj_cell):
        self.color = color
        self.left_adj_cell = left_adj_cell
        self.right_adj_cell = right_adj_cell


