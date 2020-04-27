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
    _merge_lists(steps, _top_cross(cube))
    _merge_lists(steps, _top_face(cube))
    _merge_lists(steps, _second_row(cube))
    _merge_lists(steps, _bottom_cross(cube))
    _merge_lists(steps, _bottom_corners(cube))
    _reduce_steps(steps)
    print(steps)
    print(len(steps))
    return steps


def _top_cross(cube):
    steps = list()
    rotations, other_colors = _determine_start_cond(cube)
    _merge_lists(steps, _rotate_white_face(cube, rotations))
    for top_cross_edge in range(1, 5):  # 1, 2, 3, 4 == red, blue, green, orange
        _merge_lists(steps, _top_cross_position_edge(cube, top_cross_edge))

    return steps


def _top_face(cube):
    steps = list()

    while not _top_complete(cube):
        _merge_lists(steps, _top_corners_on_top(cube))
        _merge_lists(steps, _top_corners_on_bottom(cube))

    return steps


def _second_row(cube):
    steps = list()

    while not _all_edges_solved(cube):
        if not _bottom_row_has_second_row_edge(cube, steps):
            continue
        _move_edge_from_second_row(cube, steps)

    return steps


def _bottom_cross(cube):
    steps = list()
    _merge_lists(steps, _bottom_make_cross(cube))
    print("Cross")
    _merge_lists(steps, _bottom_place_edges(cube))
    print("Placed Edges")

    return steps


def _bottom_corners(cube):
    steps = list()
    _merge_lists(steps, _bottom_place_corners(cube))
    _merge_lists(steps, _bottom_orient_corners(cube))
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
                    index += 1
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

# generic helper functions


def rotate_list_cw(given_list):
    hold = None
    prev = given_list[-1]
    for i in range(len(given_list)):
        hold = given_list[i]
        given_list[i] = prev
        prev = hold


def rotate_list_ccw(given_list):
    hold = None
    prev = given_list[0]
    for i in range(len(given_list)-1, -1, -1):
        hold = given_list[i]
        given_list[i] = prev
        prev = hold


# top face helper steps


def _top_corners_on_bottom(cube):
    steps = list()

    top_corners = {0: [RubiksCube.BLUE, RubiksCube.RED], # corner index: [l_adj, r_adj]
                   2: [RubiksCube.RED, RubiksCube.GREEN],
                   7: [RubiksCube.GREEN, RubiksCube.ORANGE],
                   5: [RubiksCube.ORANGE, RubiksCube.BLUE]}

    face_order = [1, 3, 4, 2]
    corner_order = [0, 2, 7, 5]

    for face in face_order:
        face_index = face_order.index(face)
        edge, l_adj, r_adj = cube.get_cell(face, corner_order[face_index], True)

        if RubiksCube.WHITE not in (edge, l_adj, r_adj):
            continue

        corner = [-1, 0, 1]  # 0 is White

        adjacency = (l_adj, edge, r_adj)
        white_position = 1
        while adjacency[white_position] != RubiksCube.WHITE:
            rotate_list_cw(corner)
            white_position = (white_position + 1) % 3

        corner_ind = corner.index(1)
        face_color = adjacency[corner_ind]
        index_of_corner = face_order.index(face_color)

        rotate = ( face_index - index_of_corner) % 4

        for roto in range(rotate):
            steps.append(cube.rotate(RubiksCube.WHITE))

        if RubiksCube.WHITE == edge:

            steps.append(cube.rotate(face))
            steps.append(cube.rotate(RubiksCube.BACK))
            steps.append(cube.rotate(face, RubiksCube.ROTATE_CCW))

        elif RubiksCube.WHITE == l_adj:
            r_face = face_order[(face_order.index(face) - 1) % 4]

            steps.append(cube.rotate(r_face, RubiksCube.ROTATE_CCW))
            steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CCW))
            steps.append(cube.rotate(r_face))

        else:

            l_face = face_order[(face_order.index(face) + 1) % 4]

            steps.append(cube.rotate(face))
            steps.append(cube.rotate(l_face))
            steps.append(cube.rotate(RubiksCube.BACK))
            steps.append(cube.rotate(RubiksCube.BACK))
            steps.append(cube.rotate(l_face, RubiksCube.ROTATE_CCW))
            steps.append(cube.rotate(face, RubiksCube.ROTATE_CCW))


        for a_roto in range(rotate):
            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CCW))

    return steps


def _top_corners_on_top(cube):
    steps = list()

    top_corners = {0: [RubiksCube.BLUE, RubiksCube.RED], # corner index: [l_adj, r_adj]
                   2: [RubiksCube.RED, RubiksCube.GREEN],
                   7: [RubiksCube.GREEN, RubiksCube.ORANGE],
                   5: [RubiksCube.ORANGE, RubiksCube.BLUE]}
    face_order = [1, 3, 4, 2]
    corner_order = [0, 2, 7, 5]

    for corner in top_corners:
        edge, l_adj, r_adj = cube.get_cell(RubiksCube.WHITE, corner, True)

        if edge != RubiksCube.WHITE:
            if RubiksCube.WHITE in (l_adj, r_adj):
                index_of_corner = corner_order.index(corner)
                face_color = face_order[index_of_corner]

                steps.append(cube.rotate(face_color))
                steps.append(cube.rotate(RubiksCube.BACK))
                steps.append(cube.rotate(face_color, RubiksCube.ROTATE_CCW))


            continue

        if l_adj == top_corners[corner][0] and r_adj == top_corners[corner][1]:  # corner is in position
            continue

        index_of_corner = corner_order.index(corner)
        face_color = face_order[index_of_corner]

        index_of_face = face_order.index(r_adj)
        rotate = (index_of_corner - index_of_face) % 4


        steps.append(cube.rotate(face_color))
        steps.append(cube.rotate(RubiksCube.BACK))
        steps.append(cube.rotate(face_color, RubiksCube.ROTATE_CCW))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CCW))

        for roto in range(rotate):
            steps.append(cube.rotate(RubiksCube.WHITE))

        r_face = face_order[(face_order.index(face_color) - 1) % 4]
        steps.append(cube.rotate(r_face, RubiksCube.ROTATE_CCW))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CCW))
        steps.append(cube.rotate(r_face, RubiksCube.ROTATE_CW))

        for a_roto in range(rotate):
            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CCW))

    return steps


def _top_cross_position_edge(cube, edge_face_color):
    steps = list()

    if _top_edge_complete(cube, edge_face_color):
        return steps

    _merge_lists(steps, _move_top_edge_in_top(cube, edge_face_color))  # white is up, but in wrong position
    if len(steps) > 0:
        return steps

    _merge_lists(steps, _move_top_edge_in_position(cube, edge_face_color))  # edge is on top, but color is facing up
    if len(steps) > 0:
        return steps

    _merge_lists(steps, _move_top_edge_from_second_row(cube, edge_face_color))  # both orient, edge is in middle row
    if len(steps) > 0:
        return steps

    _merge_lists(steps, _move_top_edge_from_bottom_edge(cube, edge_face_color))  # white on bottom, color out.
    if len(steps) > 0:
        return steps

    _merge_lists(steps, _move_top_edge_from_bottom_color_down(cube, edge_face_color)) # color on bottom, white out.


def _top_edge_complete(cube, edge_face_color):
    face_color_to_edge = {RubiksCube.RED: 1, RubiksCube.GREEN: 4, RubiksCube.ORANGE: 6, RubiksCube.BLUE: 3}

    edge, adj = cube.get_cell(RubiksCube.WHITE, face_color_to_edge[edge_face_color], True)
    if edge != RubiksCube.WHITE:
        return False
    if adj != edge_face_color:
        return False
    return True


def _top_complete(cube):

    to_check = {RubiksCube.WHITE: [0, 1, 2, 3, 4, 5, 6, 7], RubiksCube.RED: [5, 6, 7],
                RubiksCube.GREEN: [0, 3, 5], RubiksCube.ORANGE: [0, 1, 2], RubiksCube.BLUE: [2, 4, 7]}

    for check in to_check:
        for cell in to_check[check]:
            if check != cube.get_cell(check, cell):
                return False

    return True


def _move_top_edge_from_bottom_color_down(cube, edge_face_color):
    steps = list()
    edge_order = [1, 3, 4, 2]

    edges_to_check = [(RubiksCube.RED, 1), (RubiksCube.GREEN, 4), (RubiksCube.ORANGE, 6), (RubiksCube.BLUE, 3)]

    for check in edges_to_check:
        edge, adj = cube.get_cell(check[0], check[1], True)

        if RubiksCube.WHITE != edge:
            continue
        if edge_face_color != adj:
            continue

        position = edge_order.index(check[0])
        goes = edge_order.index(edge_face_color)
        rotations = (position - goes) % 4

        for roto in range(rotations):
            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CW))

        r_face = edge_order[(edge_order.index(check[0]) - 1) % 4]

        steps.append(cube.rotate(check[0], RubiksCube.ROTATE_CCW))
        steps.append(cube.rotate(r_face, RubiksCube.ROTATE_CCW))
        steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CCW))
        steps.append(cube.rotate(r_face))
        steps.append(cube.rotate(check[0]))
        steps.append(cube.rotate(check[0]))

        for a_roto in range(rotations):
            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CCW))

        return steps
    return steps


def _move_top_edge_from_bottom_edge(cube, edge_face_color):
    steps = list()
    edge_order = [1, 2, 4, 3]

    edges_to_check = [(RubiksCube.RED, 1), (RubiksCube.GREEN, 4), (RubiksCube.ORANGE, 6), (RubiksCube.BLUE, 3)]

    for check in edges_to_check:
        edge, adj = cube.get_cell(check[0], check[1], True)

        if edge_face_color != edge:
            continue
        if RubiksCube.WHITE != adj:
            continue

        position = edge_order.index(check[0])
        goes = edge_order.index(edge_face_color)
        rotations = (position - goes) % 4

        for roto in range(rotations):
            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CW))

        steps.append(cube.rotate(check[0]))
        steps.append(cube.rotate(check[0]))

        for a_roto in range(rotations):
            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CCW))

        return steps
    return steps


def _move_top_edge_from_second_row(cube, edge_face_color):
    steps = list()
    edge_order = [1, 3, 4, 2]
    edges_to_check = [(RubiksCube.RED, 3), (RubiksCube.GREEN, 1), (RubiksCube.ORANGE, 4), (RubiksCube.BLUE, 6)]

    for check in edges_to_check:
        edge, adj = cube.get_cell(check[0], check[1], True)

        if RubiksCube.WHITE not in (edge, adj): # is not a top edge
            continue
        if edge_face_color not in (edge, adj): # is not an edge we are looking for
            continue

        position = edge_order.index(check[0])
        goes = edge_order.index(edge_face_color)
        rotations = (position - goes) % 4

        for roto in range(rotations):
            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CW))

        if edge == RubiksCube.WHITE:
            r_face = edge_order[(position - 1) % 4]

            steps.append(cube.rotate(r_face, RubiksCube.ROTATE_CCW))
            steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CCW))
            steps.append(cube.rotate(r_face))
            steps.append(cube.rotate(check[0]))
            steps.append(cube.rotate(check[0]))

        else:
            l_face = edge_order.index((edge_face_color) + 1) % 4

            steps.append(cube.rotate(l_face, RubiksCube.ROTATE_CW))
            steps.append(cube.rotate(RubiksCube.BACK, RubiksCube.ROTATE_CW))
            steps.append(cube.rotate(l_face, RubiksCube.ROTATE_CCW))
            steps.append(cube.rotate(check[0]))
            steps.append(cube.rotate(check[0]))

        for a_roto in range(rotations):
            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CCW))

        return steps
    return steps


def _move_top_edge_in_position(cube, edge_face_color):
    steps = list()
    edge_order = [1, 2, 4, 3]
    face_color_to_edge = {RubiksCube.RED: 1, RubiksCube.GREEN: 4, RubiksCube.ORANGE: 6, RubiksCube.BLUE: 3}

    for face in face_color_to_edge.keys():
        if face == edge_face_color:
            continue  # already handled in previous step
        edge, adj = cube.get_cell(face, face_color_to_edge[face], True)
        if edge != edge_face_color:  # white is facing up
            continue
        if adj == RubiksCube.WHITE:
            location = face_color_to_edge[face]
            position = edge_order.index(location)
            goes = edge_order.index(edge_face_color)
            rotation = goes - position % 4

            for roto in range(rotation):
                steps.append(cube.rotate(RubiksCube.WHITE))

            steps.append(cube.rotate(edge_face_color))

            for a_roto in range(rotation):
                steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CCW))

            steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CCW))
            r_face = edge_order[(edge_order.index(edge_face_color) - 1) % 4]
            steps.append(cube.rotate(r_face))
            steps.append(cube.rotate(RubiksCube.WHITE))

            return steps # shortcuts any remaining cells

    return steps


def _move_top_edge_in_top(cube, edge_face_color):
    steps = list()
    edge_order = [1, 2, 4, 3]
    face_color_to_edge = {RubiksCube.RED: 6, RubiksCube.GREEN: 3, RubiksCube.ORANGE: 1, RubiksCube.BLUE: 4}

    for face in face_color_to_edge.keys():
        edge, adj = cube.get_cell(face, face_color_to_edge[face], True)
        if adj != RubiksCube.WHITE: # white is not facing up
            continue
        if adj == edge_face_color:
            location = face_color_to_edge[face]
            position = edge_order.index(location) % 4
            goes = edge_order.index(edge_face_color)
            rotation = goes - position % 4

            for roto in range(rotation):
                steps.append(cube.rotate(RubiksCube.WHITE))

            steps.append(cube.rotate(edge_face_color))

            for a_roto in range(rotation):
                steps.append(cube.rotate(RubiksCube.WHITE, RubiksCube.ROTATE_CCW))

            steps.append(cube.rotate(edge_face_color, RubiksCube.ROTATE_CCW))

    return steps




def _rotate_white_face(cube, rotations):
    steps = list()
    direction = 0
    if rotations < 0:
        rotations *= -1
        direction = 1
    for rotation in range(rotations):
        steps.append(cube.rotate(RubiksCube.WHITE, direction))

    return steps


def _determine_start_cond(cube):

    rotation = 0
    face_order = [1, 3, 4, 2]
    edge_pos = (1, 4, 6, 3)
    edges = []
    for index in range(4): # white; top, right, bottom, left.
        cell, adj = cube.get_cell(RubiksCube.WHITE, edge_pos[index], True)
        if cell == RubiksCube.WHITE:
            edges.append(adj)
        else:
            edges.append(-1)

    for face in face_order:
        if face in edges:
            face_index = face_order.index(face)
            rotation =  face_index - edges.index(face)

    return rotation, edges



#  Middle row helper steps


def _bottom_row_has_second_row_edge(cube, steps):
    queryable_edges = ((cube.ORANGE, 6), (cube.BLUE, 3), (cube.RED, 1), (cube.GREEN, 4))  # orage, blue, red, green

    for query_index in range(len(queryable_edges)):
        edge, adj = cube.get_cell(queryable_edges[query_index][0], queryable_edges[query_index][1], True)
        if edge == 5 or adj == 5:
            continue

        advance = query_index
        while edge != queryable_edges[advance][0]:
            advance = (advance + 1) % 4
            steps.append(cube.rotate(5, 1))

        direction = 0
        offset = 1
        if adj != queryable_edges[(advance + 1) % 4][0]:
            direction = 1
            offset = -1
        steps.append(cube.rotate(5, direction))
        steps.append(cube.rotate(queryable_edges[(advance + offset) % 4][0], direction))
        steps.append(cube.rotate(5, (direction + 1) % 2))
        steps.append(cube.rotate(queryable_edges[(advance + offset) % 4][0], (direction + 1) % 2))
        steps.append(cube.rotate(5, (direction + 1) % 2))
        steps.append(cube.rotate(queryable_edges[advance][0], (direction + 1) % 2))
        steps.append(cube.rotate(5, direction))
        steps.append(cube.rotate(queryable_edges[advance][0], direction))

        return True
    return False


def _move_edge_from_second_row(cube, steps):
    queryable_edges = ((cube.ORANGE, 3), (cube.BLUE, 1), (cube.RED, 4), (cube.GREEN, 6))  # orage, blue, red, green

    for query_index in range(len(queryable_edges)):
        edge, adj = cube.get_cell(queryable_edges[query_index][0], queryable_edges[query_index][1], True)
        if edge == 5:
            continue
        if adj == 5:
            continue
        if edge == queryable_edges[query_index][0] and adj == queryable_edges[(query_index + 1) % 4][0]:
            continue

        direction = 0
        offset = 1
        steps.append(cube.rotate(5, direction))
        steps.append(cube.rotate(queryable_edges[(query_index + offset) % 4][0], direction))
        steps.append(cube.rotate(5, (direction + 1) % 2))
        steps.append(cube.rotate(queryable_edges[(query_index + offset) % 4][0], (direction + 1) % 2))
        steps.append(cube.rotate(5, (direction + 1) % 2))
        steps.append(cube.rotate(queryable_edges[query_index][0], (direction + 1) % 2))
        steps.append(cube.rotate(5, direction))
        steps.append(cube.rotate(queryable_edges[query_index][0], direction))


def _all_edges_solved(cube):
    queryable_edges = ((cube.ORANGE, 3), (cube.BLUE, 1), (cube.RED, 4), (cube.GREEN, 6))

    for query_index in range(len(queryable_edges)):
        edge, adj = cube.get_cell(queryable_edges[query_index][0], queryable_edges[query_index][1], True)
        if edge == 5:
            return 0
        if adj == 5:
            return 0
        if edge != queryable_edges[query_index][0] or adj != queryable_edges[(query_index + 1) % 4][0]:
            return 0

    return 1


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
    sides = [RubiksCube.TOP, RubiksCube.LEFT, RubiksCube.BOTTOM, RubiksCube.RIGHT]
    corners = [7, 5, 0, 2]
    orientaion_pattern = [  # (L, U, R) of current algorithm 'forwards'
        (RubiksCube.LEFT, RubiksCube.BACK, RubiksCube.RIGHT),  # Top 'Forwards'
        (RubiksCube.BOTTOM, RubiksCube.BACK, RubiksCube.TOP),
        (RubiksCube.RIGHT, RubiksCube.BACK, RubiksCube.LEFT),
        (RubiksCube.TOP, RubiksCube.BACK, RubiksCube.BOTTOM)
    ]

    correct_colors = [
        (RubiksCube.BACK, RubiksCube.RIGHT, RubiksCube.TOP),
        (RubiksCube.BACK, RubiksCube.TOP, RubiksCube.LEFT),
        (RubiksCube.BACK, RubiksCube.LEFT, RubiksCube.BOTTOM),
        (RubiksCube.BACK, RubiksCube.BOTTOM, RubiksCube.RIGHT)
    ]

    # determine orientation
    # order TR, RB, BL, LT
    steps = list()
    corner_index = 0
    index_found = False
    while corner_index < 8 and not index_found:
        color, l_adj, r_adj = cube.get_cell(RubiksCube.BACK, corners[corner_index % 4], True)
        det = (color, l_adj, r_adj)
        if correct_colors[corner_index % 4][0] in det and correct_colors[corner_index % 4][1] in det and correct_colors[corner_index % 4][2] in det:
            index_found = True
            continue
        corner_index += 1
        if corner_index == 4:
            default = 0
            limiter = 0
            while not _bottom_check_corner_positions(cube, orientaion_pattern) and limiter < 2:
                _merge_lists(steps, _bottom_corner_placer(cube, orientaion_pattern[default]))
                limiter += 1

    corner_index = corner_index % 4

    limiter = 0
    while not _bottom_check_corner_positions(cube, orientaion_pattern) and limiter < 2:
        _merge_lists(steps, _bottom_corner_placer(cube, orientaion_pattern[corner_index]))
        limiter += 1

    return steps


def _bottom_check_corner_positions(cube, orientation_patterns):
    corner_index = 0
    corners = [7, 5, 0, 2]
    adjacent_patterns = [  # (L, U, R)
        (RubiksCube.RIGHT, RubiksCube.TOP),  # Top 'Forwards'
        (RubiksCube.TOP, RubiksCube.LEFT),
        (RubiksCube.LEFT, RubiksCube.BOTTOM),
        (RubiksCube.BOTTOM, RubiksCube.RIGHT)
    ]
    sides = [RubiksCube.TOP, RubiksCube.LEFT, RubiksCube.BOTTOM, RubiksCube.RIGHT]
    while corner_index < 4:
        color, l_adj, r_adj = cube.get_cell(RubiksCube.BACK, corners[corner_index], True)
        det = (color, l_adj, r_adj)
        if not(sides[corner_index] in det and adjacent_patterns[corner_index][0] in det and adjacent_patterns[corner_index][1] in det):
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
            rotate = (4 - index)
    _merge_lists(steps, _rotate_cross(cube, rotate))
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
            rotation = 0
            _merge_lists(steps, _rotate_cross(cube, rotation))
            colors[2] = colors[3]
            colors[3] = color

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

    right = RubiksCube.LEFT
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
    if (_check_bottom(cube, '.')): # is dot
        _merge_lists(steps, _bottom_cross_alg(cube, 1))
        _merge_lists(steps, _bottom_cross_alg(cube, 4))
        _merge_lists(steps, _bottom_cross_alg(cube, 1))
        return steps

    if (_check_bottom(cube, 'L')): # is Line
        ell_ori = _get_ell_orientation(cube)
        _merge_lists(steps, _rotate_cross(cube, ell_ori))
        _merge_lists(steps, _bottom_cross_alg(cube, 4))
        _merge_lists(steps, _bottom_cross_alg(cube, 1))
        _merge_lists(steps, _rotate_cross(cube, ell_ori * -1))
        return steps

    if not (_check_bottom(cube, '+')): # is line
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
    if check not in (".", "L", "|", "+"): # only four cases exist; point, L, line, cross.
        raise ValueError

    bottom = cube.get_cell(5, 6)
    top = cube.get_cell(5, 1)
    left = cube.get_cell(5, 3)
    right = cube.get_cell(5, 4)

    if check == ".":
        for t_b in (top, bottom):
            for l_r in (left, right):
                if t_b == l_r:
                    if top == bottom:
                        return False # is cross
                    return False # is L
                if top == bottom or left == right:
                    return False # is line
        return True  # is .

    if check == "L":
        for t_b in (top, bottom):
            for l_r in (left, right):
                if t_b == l_r:
                    if top == bottom:
                        return False # is cross
                    return True
                if top == bottom or left == right:
                    return False # is line

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
    returns the number of rotations needed to put the 'L' in the correct orientation for the 'L' algorithm (left-top from Orange perspective)
    :param cube: RubicksCube
    :return: int
    """
    bottom = cube.get_cell(5, 1)
    left = cube.get_cell(5, 4)
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
    r_l = [2, front_side, 3]    # [ L, F, R ]
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
    if app is None:
        return
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
    cube.print_cube()

    print("\n\n------------------------------------------------------------------\n\n")

    face_0 = RF(0, [0,0,0,0,0,0,0,0])
    face_1 = RF(1, [4,4,5,2,5,1,1,1])
    face_2 = RF(2, [5,5,2,2,2,5,5,2])
    face_3 = RF(3, [3,3,3,3,3,3,4,3])
    face_4 = RF(4, [4,4,4,1,3,1,4,5])
    face_5 = RF(5, [2,2,1,1,1,2,5,4])

    cube = RubiksCube(face_0,face_1,face_2,face_3,face_4,face_5)
    cube.print_cube()
    solve(cube)
    cube.print_cube()

    print("\n\n------------------------------------------------------------------\n\n")

    face_0 = RF(0, [5,5,0,3,2,4,0,5])
    face_1 = RF(1, [1,3,3,5,5,2,4,3])
    face_2 = RF(2, [5,3,1,2,0,0,0,5])
    face_3 = RF(3, [4,1,1,5,4,2,4,4])
    face_4 = RF(4, [3,2,4,1,0,2,3,0])
    face_5 = RF(5, [1,4,2,1,2,3,1,0])

    cube = RubiksCube(face_0,face_1,face_2,face_3,face_4,face_5)
    cube.print_cube()
    solve(cube)
    cube.print_cube()


if __name__ == "__main__":
    main()
