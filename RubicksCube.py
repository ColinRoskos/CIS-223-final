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

import copy

cube_map = [  # side (face, cell), or corner ((left_face, cell), (right_face, cell))
    #        0           1             2            3       4           5            6           7
    [((2, 2), (1, 5)), (1, 6), ((1, 7), (3, 0)), (2, 4), (3, 3), ((4, 0), (2, 7)), (4, 1), ((3, 5), (4, 2))],  # face_0
    [((2, 0), (5, 5)), (5, 6), ((5, 7), (3, 2)), (2, 1), (3, 1), ((0, 0), (2, 2)), (0, 1), ((3, 0), (0, 2))],  # face_1
    [((5, 5), (1, 0)), (1, 3), ((1, 5), (0, 0)), (5, 3), (0, 3), ((4, 5), (5, 0)), (4, 3), ((0, 5), (4, 0))],  # face_2
    [((0, 2), (1, 7)), (1, 4), ((1, 2), (5, 7)), (0, 4), (5, 4), ((4, 2), (0, 7)), (4, 4), ((5, 2), (4, 7))],  # face_3
    [((2, 7), (0, 5)), (0, 6), ((0, 7), (3, 5)), (2, 6), (3, 6), ((5, 0), (2, 5)), (5, 1), ((3, 7), (5, 2))],  # face_4
    [((2, 5), (4, 5)), (4, 6), ((4, 7), (3, 7)), (2, 3), (3, 4), ((1, 0), (2, 0)), (1, 1), ((3, 2), (1, 2))],  # face_5
]

class RubiksCube:
    # note on mechanics of the block:
    #   Only faces can rotate.
    #   faces can rotate CW or CCW
    #       This will be based on orientation from the 'Entire Block' representation from above.

    ROTATE_CW = 0
    ROTATE_CCW = 1

    FRONT = WHITE = 0
    TOP = RED = 1
    LEFT = BLUE = 2
    RIGHT = GREEN = 3
    BOTTOM = ORANGE = 4
    BACK = YELLOW = 5

    def __init__(self, face_0=None, face_1=None, face_2=None, face_3=None, face_4=None, face_5=None):
        self.face_0 = face_0 or RubiksFace(0)
        self.face_1 = face_1 or RubiksFace(1)
        self.face_2 = face_2 or RubiksFace(2)
        self.face_3 = face_3 or RubiksFace(3)
        self.face_4 = face_4 or RubiksFace(4)
        self.face_5 = face_5 or RubiksFace(5)

        self.faces = [self.face_0,
                      self.face_1,
                      self.face_2,
                      self.face_3,
                      self.face_4,
                      self.face_5]

    def alter_color(self, face, cell, new_color):
        self.faces[face].set_cell(cell, new_color)

    # def solve(self):
    # TODO
    # White-cross ->
    # White Solid ->
    # Two rows ->
    # yellow cross (mismatch) ->
    # yellow cross (complete) ->
    # intermetiate corner -> complete

    def print_cube(self):
        self.face_0.print_face()
        print("\n")
        self.face_1.print_face()
        print("\n")
        self.face_2.print_face()
        print("\n")
        self.face_3.print_face()
        print("\n")
        self.face_4.print_face()
        print("\n")
        self.face_5.print_face()

    def rotate(self, face, direction):
        """
        rotates a face on the rubik's cube
        :param face: the face to rotate
        :param direction: the direction to rotate, 0 - clockwise, 1 - counter-clockwise
        :return:
        """

        self.faces[face].rotate(direction)
        self._rotate_edge(cube_map[face], direction)

        return (face, direction)

    def _rotate_edge(self, edges, direction):
        cube_copy = copy.deepcopy(self)

        rotation_pattern = [5, 3, 0, 6, 1, 7, 4, 2]
        if direction == 1:  # counter-clockwise
            rotation_pattern.reverse()

        for index in range(0, len(rotation_pattern)):
            to_ = edges[index]
            from_ = edges[rotation_pattern[index]]
            if isinstance(from_[0], tuple):
                for index_i in range(0, 2):
                    item_f = from_[index_i]
                    item_t = to_[index_i]
                    color = cube_copy.faces[item_f[0]].get_cell(item_f[1])
                    self.alter_color(item_t[0], item_t[1], color)
            else:
                color = cube_copy.faces[from_[0]].get_cell(from_[1])
                self.alter_color(to_[0], to_[1], color)

    def get_cell(self, face, index, adjecent=False):
        cell = self.faces[face].get_cell(index)
        if adjecent:
            adjacent_cell = cube_map[face][index]
            if isinstance(adjacent_cell[0], tuple):
                l_adj = self.get_cell(adjacent_cell[0][0], adjacent_cell[0][1])
                r_adj = self.get_cell(adjacent_cell[1][0], adjacent_cell[1][1])
                return cell, l_adj, r_adj

            adj = self.get_cell(adjacent_cell[0], adjacent_cell[1])
            return cell, adj

        return cell


class RubiksFace:
    # A face is represented by a face color, and 8 face squares
    #
    #       Single Side:
    #           --- --- ---
    #          | 0 | 1 | 2 |
    #           --- --- ---
    #          | 3 | X | 4 |
    #           --- --- ---
    #          | 5 | 6 | 7 |
    #           --- --- ---

    T_L = 0
    T_C = 1
    T_R = 2
    L_C = 3
    R_C = 4
    B_L = 5
    B_C = 6
    B_R = 7

    def __init__(self, face_color=None, face=None):
        self.face_color = face_color
        self.face = None

        if face is not None:
            self.face = face
        else:
            self.face = [face_color, face_color, face_color, face_color, face_color, face_color, face_color, face_color]

    def print_face(self):
        print("\t --- --- ---")
        print("\t| %s | %s | %s |" % (self.face[0], self.face[1], self.face[2]))
        print("\t --- --- ---")
        print("\t| %s | X | %s |" % (self.face[3], self.face[4]))
        print("\t --- --- ---")
        print("\t| %s | %s | %s |" % (self.face[5], self.face[6], self.face[7]))
        print("\t --- --- ---")

    def rotate(self, direction):
        holding = copy.copy(self.face)
        rotation_list = [5, 3, 0, 6, 1, 7, 4, 2]
        if direction == 1:
            rotation_list.reverse()
        for index in range(0, len(self.face)):
            self.face[index] = holding[rotation_list[index]]

    def get_cell(self, tile):
        return self.face[tile]

    def set_cell(self, cell, new_color):
        self.face[cell] = new_color


class RubiksCell:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


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


def main():
    r_cube = RubiksCube()
    r_cube.rotate(1, 0)
    r_cube.print_cube()


if __name__ == "__main__":
    main()
