# whatever imports you need
import numpy as np


# create example code:
example = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#...",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def move_to_next_object(position, all_objects_positions, direction, room_length):
    set_of_traveled_positions = set()
    if direction == "up":
        if (
            position[1] in all_objects_positions[:, 1] and
            np.any(position[0] > all_objects_positions[all_objects_positions[:, 1] == position[1]][:, 0])
        ):
            mask = (
                np.array(all_objects_positions[:, 1] == position[1]) &
                np.array(all_objects_positions[:, 0] < position[0])
            )
            object_reached = all_objects_positions[mask][np.argmax(all_objects_positions[mask][:, 0])]
            for position_value in range(object_reached[0] + 1, position[0] + 1):
                set_of_traveled_positions.add((position_value, position[1]))
            next_position = (int(object_reached[0]) + 1, position[1])
            next_direction = "right"
        else:
            for position_value in range(0, position[0]):
                set_of_traveled_positions.add((position_value, position[1]))
            return "out", direction, set_of_traveled_positions
    elif direction == "down":
        if (
            position[1] in all_objects_positions[:, 1] and
            np.any(position[0] < all_objects_positions[all_objects_positions[:, 1] == position[1]][:, 0])
        ):
            mask = (
                np.array(all_objects_positions[:, 1] == position[1]) &
                np.array(all_objects_positions[:, 0] > position[0])
            )
            object_reached = all_objects_positions[mask][np.argmin(all_objects_positions[mask][:, 0])]
            for position_value in range(position[0], object_reached[0]):
                set_of_traveled_positions.add((position_value, position[1]))
            next_position = (int(object_reached[0]) - 1, position[1])
            next_direction = "left"
        else:
            for position_value in range(position[0], room_length):
                set_of_traveled_positions.add((position_value, position[1]))
            return "out", direction, set_of_traveled_positions
    elif direction == "left":
        if (
            position[0] in all_objects_positions[:, 0] and
            np.any(position[1] > all_objects_positions[all_objects_positions[:, 0] == position[0]][:, 1])
        ):
            mask = (
                np.array(all_objects_positions[:, 0] == position[0]) &
                np.array(all_objects_positions[:, 1] < position[1])
            )
            object_reached = all_objects_positions[mask][np.argmax(all_objects_positions[mask][:, 1])]
            for position_value in range(object_reached[1] + 1, position[1] + 1):
                set_of_traveled_positions.add((position[0], position_value))
            next_position = (position[0], int(object_reached[1]) + 1)
            next_direction = "up"
        else:
            for position_value in range(0, position[1]):
                set_of_traveled_positions.add((position[0], position_value))
            return "out", direction, set_of_traveled_positions
    elif direction == "right":
        if (
            position[0] in all_objects_positions[:, 0] and
            np.any(position[1] < all_objects_positions[all_objects_positions[:, 0] == position[0]][:, 1])
        ):
            mask = (
                np.array(all_objects_positions[:, 1] > position[1]) &
                np.array(all_objects_positions[:, 0] == position[0])
            )
            object_reached = all_objects_positions[mask][np.argmin(all_objects_positions[mask][:, 1])]
            for position_value in range(position[1], object_reached[1]):
                set_of_traveled_positions.add((position[0], position_value))
            next_position = (position[0], int(object_reached[1]) - 1)
            next_direction = "down"
        else:
            for position_value in range(position[1], room_length):
                set_of_traveled_positions.add((position[0], position_value))
            return "out", direction, set_of_traveled_positions
    return next_position, next_direction, set_of_traveled_positions


def main():
    file_path = 'day_6.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    # part 1
    all_objects_positions = []
    for iline, line in enumerate(lines_array):
        list_line = list(line)
        for iposition, position in enumerate(list_line):
            if position == "^":
                first_position = (iline, iposition)
                first_direction = "up"
            if position == "#":
                all_objects_positions.append([iline, iposition])

    guard_position = first_position
    direction = first_direction
    all_objects_positions = np.array(all_objects_positions)
    all_guard_positions = set()
    while guard_position != "out":
        guard_position, direction, set_of_traveled_positions = move_to_next_object(
            guard_position, all_objects_positions, direction, len(lines_array)
        )
        all_guard_positions.update(set_of_traveled_positions)

    print("the number of positions visited is", len(all_guard_positions))

    # part 2
    # test all possibilities
    all_objects_positions = list(all_objects_positions)
    all_objects_positions_variations = []
    for visited_position in all_guard_positions:
        if visited_position == first_position:
            continue
        all_objects_positions_to_mute = all_objects_positions.copy()
        all_objects_positions_to_mute.append(np.array((visited_position)))
        all_objects_positions_variations.append(np.array(all_objects_positions_to_mute))

    nloops = 0
    for i, all_objects_positions_variation in enumerate(all_objects_positions_variations):
        guard_position = first_position
        direction = first_direction
        all_guard_positions_variations = set()
        while guard_position != "out":
            previous_direction = direction
            guard_position, direction, set_of_traveled_positions = move_to_next_object(
                guard_position, all_objects_positions_variation, direction, len(lines_array)
            )
            set_of_traveled_positions_with_direction = set()
            for position in set_of_traveled_positions:
                set_of_traveled_positions_with_direction.add((position, previous_direction))
            if bool(set_of_traveled_positions_with_direction & all_guard_positions_variations):
                nloops += 1
                break
            else:
                all_guard_positions_variations.update(set_of_traveled_positions_with_direction)
    print("the number of loops is", nloops)


if __name__ == "__main__":
    main()
