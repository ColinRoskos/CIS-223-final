# solver implementations
#
# Implements the solving steps and returns a list for steps to solve the given rubik's cube
#
# Authors : Colin Roskos, Winsten Coellens


def solve(cube):
    """
    when passed a RubicksCube object, returns a rubicks cube solution list.
    :param cube:
    :return:
    """
    steps = list()  # step [(side, direction), ... ]
    steps.append(_top_cross(cube))
    steps.append(_top_face(cube))
    steps.append(_second_row(cube))
    steps.append(_bottom_cross(cube))
    steps.append(_bottom_corners(cube))

    return steps


def _top_cross(cube):
    raise (NotImplementedError())


def _top_face(cube):
    raise (NotImplementedError())


def _second_row(cube):
    raise (NotImplementedError())


def _bottom_cross(cube):
    raise (NotImplementedError())


def _bottom_corners(cube):
    raise (NotImplementedError())


def main():
    raise (NotImplementedError())


if __name__ == "__main__":
    main()
