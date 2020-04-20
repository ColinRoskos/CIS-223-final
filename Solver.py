# solver implementations
#
# Implements the solving steps and returns a list for steps to solve the given rubik's cube
#
# Authors : Colin Roskos, Winsten Coellens
from RubicksCube import RubiksCube as RubiksCube
from RubicksCube import RubiksFace as RF


def solve(cube):
    """
    when passed a RubicksCube object, returns a rubicks cube solution list.
    :param cube:
    :return:
    """
    steps = list()  # step [(side, direction), ... ]
    # _merge_lists(steps, _top_cross(cube))
    # _merge_lists(steps, _top_face(cube))
    # _merge_lists(steps, _second_row(cube))
    _merge_lists(steps, _bottom_cross(cube))
    cube.print_cube()
    _merge_lists(steps, _bottom_corners(cube))
    cube.print_cube()
    print(steps)
    _reduce_steps(steps)
    print(steps)
    print(len(steps))
    return steps


def _top_cross(cube):
    raise (NotImplementedError())


def _top_face(cube):
    raise (NotImplementedError())


def _second_row(cube):
    raise (NotImplementedError())


def _bottom_cross(cube):
    steps = list()
    _merge_lists(steps, _bottom_make_cross(cube))
    cube.print_cube()
    _merge_lists(steps, _bottom_place_edges(cube))
    cube.print_cube()

    return steps


def _bottom_corners(cube):
    steps = list()
    _merge_lists(steps, _bottom_place_corners(cube))
    cube.print_cube()
    _merge_lists(steps, _bottom_orient_corners(cube))
    cube.print_cube()
    return steps


def _reduce_steps(step_list):
    if len(step_list) < 2:
        return
    index = 1
    import copy
    list_copy = copy.copy(step_list)

    none_removed = False
    while not none_removed:
        none_removed = True
        # replace anti-steps
        index = 1
        while index < len(step_list):
            if step_list[index-1][0] != step_list[index][0]:
               index += 1
               continue
            if step_list[index-1][1] == step_list[index][1]:
               index += 1
               continue

            step_list.pop(index)
            step_list.pop(index-1)
            index -= 1
            none_removed = False

        # replace 3 rotations
        index = 1
        while index + 1 < len(step_list) and not len(step_list) < 3:
            a = step_list[index-1][0]
            b = step_list[index][0]
            c = step_list[index+1][0]

            if step_list[index-1][0] == step_list[index][0] == step_list[index+1][0] :
                if not( step_list[index-1][1] == step_list[index][1] == step_list[index+1][1] ) :
                    continue
                face = step_list[index][0]
                orientation = (step_list[index][1] + 1) % 2
                to_pop = [step_list[index-1], step_list[index], step_list[index+1]]
                step_list.pop(index-1)
                step_list.pop(index)
                step_list.pop((index+1))
                step_list.insert(index - 1, (face, orientation))
                none_removed = False

            index += 1


#   Bottom helper steps

def _bottom_orient_corners(cube):
    steps = list()
    corner = 7
    bot_col = RubiksCube.BACK

    rotation = 0
    while rotation < 4:
        if not (cube.get_cell(bot_col, corner) == bot_col):
            _merge_lists(steps, _bottom_orient_corners_alg(cube))
            _merge_lists(steps, _bottom_orient_corners_alg(cube))
            if not(cube.get_cell(bot_col, corner) == bot_col):
                _merge_lists(steps, _bottom_orient_corners_alg(cube))
                _merge_lists(steps, _bottom_orient_corners_alg(cube))

        steps.append(cube.rotate(bot_col, RubiksCube.ROTATE_CW))
        rotation += 1

    return steps


def _bottom_orient_corners_alg(cube):
    steps = list()

    R = RubiksCube.RIGHT
    D = RubiksCube.FRONT

    steps.append(cube.rotate(R, RubiksCube.ROTATE_CCW))
    steps.append(cube.rotate(D, RubiksCube.ROTATE_CCW))
    steps.append(cube.rotate(R, RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(D, RubiksCube.ROTATE_CW))

    return steps

def _bottom_place_corners(cube):
    # corners (TR), (RB), (BL), (LT)
    sides = [RubiksCube.TOP, RubiksCube.RIGHT, RubiksCube.BOTTOM, RubiksCube.LEFT]
    corners = [7, 5, 0, 2]
    orientaion_pattern = [  # (L, U, R)
        (RubiksCube.LEFT, RubiksCube.BACK, RubiksCube.RIGHT),  # Top 'Forwards'
        (RubiksCube.TOP, RubiksCube.BACK, RubiksCube.BOTTOM),
        (RubiksCube.RIGHT, RubiksCube.BACK, RubiksCube.LEFT),
        (RubiksCube.BOTTOM, RubiksCube.BACK, RubiksCube.TOP)
    ]

    # determine orientation
    # order TR, RB, BL, LT

    corner_index = 0
    index_not_found = True
    while corner_index < 4 and index_not_found:
        color, l_adj, r_adj = cube.get_cell(RubiksCube.BACK, corners[corner_index], True)
        det = (color, l_adj, r_adj)
        if sides[corner_index] in det and orientaion_pattern[corner_index][0] in det and orientaion_pattern[corner_index][2] in det:
            index_not_found = False
        corner_index += 1
    if corner_index == 4:
        corner_index = 0

    steps = list()
    limiter = 0
    while not _bottom_check_corner_positions(cube, orientaion_pattern) and limiter < 2:
        _merge_lists(steps, _bottom_corner_placer(cube, orientaion_pattern[corner_index]))
        limiter += 1
    corner_index = 0
    corner_placed = False
    while corner_index < 4 and not corner_placed:
        color, l_adj, r_adj = cube.get_cell(RubiksCube.BACK, 7, True)
        det = (color, l_adj, r_adj)
        if sides[0] in det and orientaion_pattern[0][0] in det and orientaion_pattern[0][2] in det:
            corner_placed = True
            continue
        sides.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
        corner_index += 1

    return steps


def _bottom_check_corner_positions(cube, orientation_patterns):
    corner_index = 0
    corners = [7, 5, 0, 2]
    orientaion_patterns = [  # (L, U, R)
        (RubiksCube.LEFT, RubiksCube.BACK, RubiksCube.RIGHT),  # Top 'Forwards'
        (RubiksCube.TOP, RubiksCube.BACK, RubiksCube.BOTTOM),
        (RubiksCube.RIGHT, RubiksCube.BACK, RubiksCube.LEFT),
        (RubiksCube.BOTTOM, RubiksCube.BACK, RubiksCube.TOP)
    ]
    sides = [RubiksCube.TOP, RubiksCube.RIGHT, RubiksCube.BOTTOM, RubiksCube.LEFT]
    while corner_index < 4:
        color, l_adj, r_adj = cube.get_cell(RubiksCube.BOTTOM, corners[corner_index], True)
        det = (color, l_adj, r_adj)
        if not(sides[corner_index] in det and orientaion_patterns[corner_index][2] in det):
            return False
        corner_index += 1
    return True


def _bottom_corner_placer(cube, orientation_pattern):
    steps = list()

    steps.append(cube.rotate(orientation_pattern[1], RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(orientation_pattern[2], RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(orientation_pattern[1], RubiksCube.ROTATE_CCW))
    steps.append(cube.rotate(orientation_pattern[0], RubiksCube.ROTATE_CCW))
    steps.append(cube.rotate(orientation_pattern[1], RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(orientation_pattern[2], RubiksCube.ROTATE_CCW))
    steps.append(cube.rotate(orientation_pattern[1], RubiksCube.ROTATE_CCW))
    steps.append(cube.rotate(orientation_pattern[0], RubiksCube.ROTATE_CW))

    return steps


def _bottom_place_edges(cube):
    steps = list()

    # note: reference the RubicksCube.py for orientation
    faces = [RubiksCube.TOP, RubiksCube.LEFT, RubiksCube.BOTTOM, RubiksCube.RIGHT]
    edges = [RF.B_C, RF.L_C, RF.T_C, RF.R_C]
    colors = [-1, -1, -1, -1]
    rotate = 0
    for index in range(len(edges)):
        color, adj = cube.get_cell(RubiksCube.BACK, edges[index], True)
        colors[index] = adj
        if adj == RubiksCube.TOP:
            rotate = (index + 2) % 4
    _merge_lists(steps, _rotate_cross(cube, rotate))
    cube.print_cube()
    for rot in range(rotate):
        colors.insert(0, colors[-1])
        colors.pop()

    needs_swap = [0, 0, 0, 0]
    for index in range(len(colors)):
        if colors[index] != faces[index]:
            needs_swap[index] = 1

    # index 0 will not need a swap.
    # index 1, 3 may need an across swap
    # index 2 may need a swap left or right
    # if index 2 swaps left or right, then index 1, 3 might need an across swap.
    if colors[2] != RubiksCube.BOTTOM:
        # is left swap?
        color = colors[2]
        rotation = 0
        if RubiksCube.BOTTOM == colors[3]:
            rotation = 2
            _merge_lists(steps, _rotate_cross(cube, rotation))
            colors[2] = colors[3]
            colors[3] = color

            cube.print_cube()
        # is right swap.
        else:
            rotation = 1
            _merge_lists(steps, _rotate_cross(cube, rotation))
            colors[2] = colors[1]
            colors[1] = color
        _merge_lists(steps, _bottom_swap_edge_left(cube))
        _merge_lists(steps, _rotate_cross(cube, rotation * -1))

    if colors[1] != faces[1]:
        _merge_lists(steps, _rotate_cross(cube, 1))
        _merge_lists(steps, _bottom_swap_edge_accross(cube))
        _merge_lists(steps, _rotate_cross(cube, -1))

    return steps


def _bottom_swap_edge_accross(cube):
    steps = list()

    _merge_lists(steps, _bottom_swap_edge_left(cube))
    steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CCW))
    _merge_lists(steps, _bottom_swap_edge_left(cube))
    steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
    _merge_lists(steps, _bottom_swap_edge_left(cube))

    return steps


def _bottom_swap_edge_left(cube):
    steps = list()

    right = RubiksCube.RIGHT
    upper = RubiksCube.BACK

    steps.append(cube.rotate(right, RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(upper, RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(right, RubiksCube.ROTATE_CCW))
    steps.append(cube.rotate(upper, RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(right, RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(upper, RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(upper, RubiksCube.ROTATE_CW))
    steps.append(cube.rotate(right, RubiksCube.ROTATE_CCW))
    steps.append(cube.rotate(upper, RubiksCube.ROTATE_CW))

    return steps


def _bottom_make_cross(cube):
    steps = list()
    if (_check_bottom(cube, 'L')):
        _merge_lists(steps, _bottom_cross_alg(cube, 1))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
        _merge_lists(steps, _bottom_cross_alg(cube, 4))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
        _merge_lists(steps, _bottom_cross_alg(cube, 1))
        return steps
    if (_check_bottom(cube, '|')):
        ell_ori = _get_ell_orientation(cube)
        _merge_lists(steps, _rotate_cross(cube, ell_ori))
        _merge_lists(steps, _bottom_cross_alg(cube, 4))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
        _merge_lists(steps, _bottom_cross_alg(cube, 1))
        _merge_lists(steps, _rotate_cross(cube, ell_ori * -1))
        return steps
    if not (_check_bottom(cube, '+')):
        line_ori = _get_line_orientation(cube)
        _merge_lists(steps, _rotate_cross(cube, line_ori))
        _merge_lists(steps, _bottom_cross_alg(cube, 1))
        _merge_lists(steps, _rotate_cross(cube, line_ori * -1))
        return steps
    return steps


def _check_bottom(cube, check):
    """
    checks for given condition or greater condition.
    If condition exists, returns True, Else False.
    :param cube:
    :param check:
    :return:
    """
    if check not in ("L", "|", "+"): # only four cases exist; point, L, line, cross.
        raise ValueError

    bottom = cube.get_cell(5, 6)
    top = cube.get_cell(5, 1)
    left = cube.get_cell(5, 3)
    right = cube.get_cell(5, 4)

    if check == "L":
        for t_b in (top, bottom):
            for l_r in (left, right):
                if t_b == l_r:
                    if top == bottom:
                        return False # is cross
                    return True
        check = "|"

    if check == "|":
        if top == bottom:
            if left == right:
                return False # is cross
            return True

    # else looking for cross
    if top == bottom and left == right and top == left:
        return True

    return False


def _get_ell_orientation(cube):
    """
    returns the number of rotations needed to put the 'L' in the correct orientation for the algorithm (left-top)
    :param cube: RubicksCube
    :return: int
    """
    bottom = cube.get_cell(5, 6)
    left = cube.get_cell(5, 3)
    if bottom == left:
        return 1

    if bottom == RubiksCube.BACK:    # 'L' is in the right-bottom position
        return 2

    if left != RubiksCube.BACK:      # 'L' is in the top-right position
        return 3

    return 0    # 'L' is in correct orientation


def _get_line_orientation(cube):
    """
    returns 1 if the line is not in the correct orientation, else 0
    :param cube: RubicksCube
    :return: int
    """
    bottom = cube.get_cell(5, 6)
    if bottom == RubiksCube.BACK:
        return 1
    return 0


def _bottom_cross_alg(cube, front_side):
    if front_side not in (1, 4):
        raise ValueError("Must be side 1 or 4")
    r_l = [3, front_side, 2]    # [ L, F, R ]
    if front_side == 4:
        r_l.reverse()
    return [cube.rotate(r_l[1], RubiksCube.ROTATE_CW), cube.rotate(r_l[2], RubiksCube.ROTATE_CW),
            cube.rotate(5, RubiksCube.ROTATE_CW), cube.rotate(r_l[2], RubiksCube.ROTATE_CCW),
            cube.rotate(5, RubiksCube.ROTATE_CCW), cube.rotate(r_l[1], RubiksCube.ROTATE_CCW)]


def _rotate_cross(cube, num_rot):
    step_list = list()
    dir = RubiksCube.ROTATE_CW
    if num_rot < 0:
        num_rot = num_rot * -1
        dir = RubiksCube.ROTATE_CCW
    for x in range(num_rot):
        step_list.append(cube.rotate(RubiksCube.BACK, dir))
    return step_list


def _merge_lists(orig, app):
    for item in app:
        orig.append(item)


def main():
    face_0 = RF(0, [0,0,0,0,0,0,0,0])
    face_1 = RF(1, [3,4,2,1,1,1,1,1])
    face_2 = RF(2, [1,2,2,1,2,4,2,2])
    face_3 = RF(3, [3,3,1,3,2,3,3,4])
    face_4 = RF(4, [4,4,4,4,4,5,3,5])
    face_5 = RF(5, [2,5,3,5,5,5,5,5])
    cube = RubiksCube(face_0,face_1,face_2,face_3,face_4,face_5)
    cube.print_cube()
    solve(cube)


if __name__ == "__main__":
    main()
