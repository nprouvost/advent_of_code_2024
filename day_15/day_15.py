# whatever imports you need
import numpy as np


# create example code:
example = [
    "########",
    "#..O.O.#",
    "##@.O..#",
    "#...O..#",
    "#.#.O..#",
    "#...O..#",
    "#......#",
    "########",
    "",
    "<^^>>>vv<v>>v<<",
]

example2 = [
    "##########",
    "#..O..O.O#",
    "#......O.#",
    "#.OO..O.O#",
    "#..O@..O.#",
    "#O#..O...#",
    "#O..O..O.#",
    "#.OO.O.OO#",
    "#....O...#",
    "##########",
    "",
    "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^",
    "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v",
    "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<",
    "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^",
    "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><",
    "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^",
    ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^",
    "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>",
    "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>",
    "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^",
]

example3 = [
    "#######",
    "#...#.#",
    "#.....#",
    "#..OO@#",
    "#..O..#",
    "#.....#",
    "#######",
    "",
    "<vv<<^^<<^^",

]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def check_box_movable(box, direction, boxes, walls):
    check_next = (box[0] + direction[0], box[1] + direction[1])
    if check_next in walls:
        return False
    elif check_next in boxes:
        return check_box_movable(check_next, direction, boxes, walls)
    else:
        return True


def check_big_box_movable(boxL, boxR, direction, boxesL, boxesR, walls):
    check_nextL = (boxL[0] + direction[0], boxL[1] + direction[1])
    check_nextR = (boxR[0] + direction[0], boxR[1] + direction[1])
    if (check_nextL in walls) or (check_nextR in walls):
        return False, []
    if direction[0] == 0:
        # for left and right movement, the only difference is that the boxes have size two
        if (direction[1] < 0) and (check_nextL in boxesR):
            next_boxL = (check_nextL[0], check_nextL[1] - 1)
            next_boxR = (check_nextR[0], check_nextR[1] - 1)
            movable, list_moved = check_big_box_movable(next_boxL, next_boxR, direction, boxesL, boxesR, walls)
            if movable:
                return movable, list_moved + [(boxL, boxR)]
            else:
                return movable, list_moved
        elif (direction[1] > 0) and (check_nextR in boxesL):
            next_boxL = (check_nextL[0], check_nextL[1] + 1)
            next_boxR = (check_nextR[0], check_nextR[1] + 1)
            movable, list_moved = check_big_box_movable(next_boxL, next_boxR, direction, boxesL, boxesR, walls)
            if movable:
                return movable, list_moved + [(boxL, boxR)]
            else:
                return movable, list_moved
        else:
            return True, [(boxL, boxR)]

    else:
        # for up and down movement, the size of the boxes is one, but each box has two positions
        # that must be checked

        # same situation as with size one
        if (check_nextL in boxesL) and (check_nextR in boxesR):
            movable, list_moved = check_big_box_movable(check_nextL, check_nextR, direction, boxesL, boxesR, walls)
            if movable:
                return movable, list_moved + [(boxL, boxR)]
            else:
                return movable, list_moved

        # if the boxes are shifted by one
        elif check_nextL in boxesR:
            next_boxL = (check_nextL[0], check_nextL[1] - 1)
            next_boxR = check_nextL
            # check if the other corner touches a box
            if check_nextR in boxesL:
                next_boxL2 = check_nextR
                next_boxR2 = (check_nextR[0], check_nextR[1] + 1)
                first_box, list_moved1 = check_big_box_movable(next_boxL, next_boxR, direction, boxesL, boxesR, walls)
                second_box, list_moved2 = check_big_box_movable(
                    next_boxL2,
                    next_boxR2,
                    direction,
                    boxesL,
                    boxesR,
                    walls,
                )
                if first_box and second_box:
                    list_moved = list_moved1 + list_moved2 + [(boxL, boxR)]
                    return True, list_moved
                else:
                    return False, list_moved1 + list_moved2
            else:
                movable, list_moved = check_big_box_movable(next_boxL, next_boxR, direction, boxesL, boxesR, walls)
                if movable:
                    return movable, list_moved + [(boxL, boxR)]
                else:
                    return movable, list_moved
        elif (check_nextR in boxesL):
            next_boxL = check_nextR
            next_boxR = (check_nextR[0], check_nextR[1] + 1)
            movable, list_moved = check_big_box_movable(next_boxL, next_boxR, direction, boxesL, boxesR, walls)
            if movable:
                return movable, list_moved + [(boxL, boxR)]
            else:
                return movable, list_moved
        else:
            return True, [(boxL, boxR)]


def main():
    file_path = 'day_15.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example6

    grid = np.array([list(line) for line in lines_array if line.startswith("#")])
    all_directions = []
    for line in lines_array:
        if not line.startswith("#"):
            all_directions += list(line)
    directions = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    walls = []
    boxes = []
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "@":
                robot = (i, j)
            if char == "O":
                boxes.append((i, j))
            if char == "#":
                walls.append((i, j))

    # part 1
    for direction in all_directions:
        next_position = (robot[0] + directions[direction][0], robot[1] + directions[direction][1])
        if next_position not in walls:
            if next_position in boxes:
                box_movable = check_box_movable(next_position, directions[direction], boxes, walls)
                if box_movable:
                    position = next_position
                    box_indices = []
                    while position in boxes:
                        box_indices.append(boxes.index(position))
                        position = (position[0] + directions[direction][0], position[1] + directions[direction][1])
                    robot = next_position
                    for i in box_indices:
                        boxes[i] = (boxes[i][0] + directions[direction][0], boxes[i][1] + directions[direction][1])
            else:
                robot = next_position

    boxes_array = np.array(boxes)
    boxes_coordinates = boxes_array[:, 0] * 100 + boxes_array[:, 1]
    print("boxes_coordinates", sum(boxes_coordinates))

    # part 2
    new_grid = []
    for iline, line in enumerate(grid):
        new_line = []
        for jline, char in enumerate(line):
            if char == "#":
                new_line.append("#")
                new_line.append("#")
            elif char == "O":
                new_line.append("[")
                new_line.append("]")
            elif char == "@":
                new_line.append("@")
                new_line.append(".")
            elif char == ".":
                new_line.append(".")
                new_line.append(".")
            else:
                raise ValueError("unexpected character")
        new_grid.append(new_line)

    wider_grid = np.array(new_grid)

    walls2 = []
    boxesL = []
    boxesR = []
    for i, line in enumerate(wider_grid):
        for j, char in enumerate(line):
            if char == "@":
                robot = (i, j)
            elif char == "[":
                boxesL.append((i, j))
            elif char == "]":
                boxesR.append((i, j))
            elif char == "#":
                walls2.append((i, j))
            else:
                if char != ".":
                    raise ValueError("char not recognized", char)

    for idirection, direction in enumerate(all_directions):
        next_position = (robot[0] + directions[direction][0], robot[1] + directions[direction][1])
        if next_position not in walls2:
            if next_position in boxesL:
                box_movable, list_moved = check_big_box_movable(
                    next_position,
                    boxesR[boxesL.index(next_position)],
                    directions[direction],
                    boxesL,
                    boxesR,
                    walls2,
                )
                # avoid double counting
                set_moved = set(list_moved)
                if box_movable:
                    robot = next_position
                    all_indices = []
                    for positions in set_moved:
                        positionL = positions[0]
                        positionR = positions[1]
                        indexL = boxesL.index(positionL)
                        indexR = boxesR.index(positionR)
                        if indexL == indexR:
                            all_indices.append(indexL)
                        else:
                            raise ValueError("indices not the same for left and right")
                    for i in all_indices:
                        boxesL[i] = (boxesL[i][0] + directions[direction][0], boxesL[i][1] + directions[direction][1])
                        boxesR[i] = (boxesR[i][0] + directions[direction][0], boxesR[i][1] + directions[direction][1])

            elif next_position in boxesR:
                box_movable, list_moved = check_big_box_movable(
                    boxesL[boxesR.index(next_position)],
                    next_position,
                    directions[direction],
                    boxesL,
                    boxesR,
                    walls2,
                )
                # avoid double counting
                set_moved = set(list_moved)
                if box_movable:
                    robot = next_position
                    all_indices = []
                    for positions in set_moved:
                        positionL = positions[0]
                        positionR = positions[1]
                        indexL = boxesL.index(positionL)
                        indexR = boxesR.index(positionR)
                        if indexL == indexR:
                            all_indices.append(indexL)
                        else:
                            raise ValueError("indices not the same for left and right")
                    for i in all_indices:
                        boxesL[i] = (boxesL[i][0] + directions[direction][0], boxesL[i][1] + directions[direction][1])
                        boxesR[i] = (boxesR[i][0] + directions[direction][0], boxesR[i][1] + directions[direction][1])

            else:
                robot = next_position

    boxesL_array = np.array(boxesL)
    boxesL_coordinates = boxesL_array[:, 0] * 100 + boxesL_array[:, 1]
    print("boxesL_coordinates", sum(boxesL_coordinates))


if __name__ == "__main__":
    main()
