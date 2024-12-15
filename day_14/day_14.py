# whatever imports you need
import numpy as np


# create example code:
example = [
    "p=0,4 v=3,-3",
    "p=6,3 v=-1,-3",
    "p=10,3 v=-1,2",
    "p=2,0 v=2,-1",
    "p=0,0 v=1,3",
    "p=3,0 v=-2,-2",
    "p=7,6 v=-1,-3",
    "p=3,0 v=-1,-2",
    "p=9,3 v=2,3",
    "p=7,3 v=-1,2",
    "p=2,4 v=2,-3",
    "p=9,5 v=-3,-3",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_14.txt'
    lines_array = read_file_to_list(file_path)
    type_ = "input"
    # lines_array = example
    # type_ = "example"

    all_positions = []
    all_velocities = []
    for iline, line in enumerate(lines_array):
        position, velocity = line.split(" v=")
        position = position.replace("p=", "").split(",")
        position = [int(pos) for pos in position]
        velocity = velocity.split(",")
        velocity = [int(vel) for vel in velocity]
        all_positions.append(position)
        all_velocities.append(velocity)

    all_positions = np.array(all_positions)
    all_velocities = np.array(all_velocities)
    room_size_x = 101 if (type_ == "input") else 11
    room_size_y = 103 if (type_ == "input") else 7

    # part 1
    n_steps = 100
    new_positions = all_positions.copy()
    new_positions[:, 0] = (new_positions[:, 0] + n_steps * all_velocities[:, 0]) % room_size_x
    new_positions[:, 1] = (new_positions[:, 1] + n_steps * all_velocities[:, 1]) % room_size_y

    mask_quadrant_1 = (new_positions[:, 0] < room_size_x // 2) & (new_positions[:, 1] < room_size_y // 2)
    mask_quadrant_2 = (new_positions[:, 0] > room_size_x // 2) & (new_positions[:, 1] < room_size_y // 2)
    mask_quadrant_3 = (new_positions[:, 0] < room_size_x // 2) & (new_positions[:, 1] > room_size_y // 2)
    mask_quadrant_4 = (new_positions[:, 0] > room_size_x // 2) & (new_positions[:, 1] > room_size_y // 2)
    quadrant_1 = new_positions[mask_quadrant_1]
    quadrant_2 = new_positions[mask_quadrant_2]
    quadrant_3 = new_positions[mask_quadrant_3]
    quadrant_4 = new_positions[mask_quadrant_4]

    safety_factor = len(quadrant_1) * len(quadrant_2) * len(quadrant_3) * len(quadrant_4)
    print("safety factor", safety_factor)

    # part 2
    # no idea how a christmas tree is defined, could be just a very big triangle, so look for steps
    # where the number of adjacencies between robots is high and print the positions.
    # since "most of the robots" build the tree, expect at least 250 adjacencies and increase the
    # number each time a wrong solution is found

    # stopped increasing at 300 because first wrong solution was very high (5927), just check from there on

    goal_adjacency = 300
    n_adjacency = 0
    n_steps = 5927
    while n_adjacency < goal_adjacency:
        n_adjacency = 0
        n_steps += 1
        print("n_steps", n_steps)
        new_positions = all_positions.copy()
        new_positions[:, 0] = (new_positions[:, 0] + n_steps * all_velocities[:, 0]) % room_size_x
        new_positions[:, 1] = (new_positions[:, 1] + n_steps * all_velocities[:, 1]) % room_size_y

        for i in range(len(new_positions)):
            for j in range(i + 1, len(new_positions)):
                if (
                    (np.abs(new_positions[i][0] - new_positions[j][0]) <= 1) and
                    (np.abs(new_positions[i][1] - new_positions[j][1]) <= 1)
                ):
                    n_adjacency += 1
        print("n_adjacency", n_adjacency)

    display = np.zeros((room_size_y, room_size_x))
    for position in new_positions:
        display[position[1], position[0]] += 1
    display_str = display.copy().astype(str)
    display_str[display_str == "0.0"] = "."
    display_str[display_str == "1.0"] = "X"
    display_str[display_str == "2.0"] = "X"
    display_str[display_str == "3.0"] = "X"

    # display[display > 1] = "X"
    # display[display == 0] = "."
    # with np.printoptions(threshold=np.inf, edgeitems=10, linewidth=400):
    #     print(display_str)
    for iline, line in enumerate(display_str):
        print("".join(line))

    # better way to solve part 2?, not checked, just written while waiting for the above to finish
    # goal_adjacency = 250
    # n_adjacency = 0
    # n_steps = 0
    # big_adjacencies = []
    # while len(big_adjacencies) < 5:
    #     n_adjacency = 0
    #     n_steps += 1
    #     print("n_steps", n_steps)
    #     new_positions = all_positions.copy()
    #     new_positions[:, 0] = (new_positions[:, 0] + n_steps * all_velocities[:, 0]) % room_size_x
    #     new_positions[:, 1] = (new_positions[:, 1] + n_steps * all_velocities[:, 1]) % room_size_y

    #     for i in range(len(new_positions)):
    #         for j in range(i + 1, len(new_positions)):
    #             if (
    #                 (np.abs(new_positions[i][0] - new_positions[j][0]) <= 1) and
    #                 (np.abs(new_positions[i][1] - new_positions[j][1]) <= 1)
    #             ):
    #                 n_adjacency += 1
    #     # n_adjacency = n_adjacency // 2
    #     if n_adjacency > goal_adjacency:
    #         big_adjacencies.append(n_steps)
    #     print("n_adjacency", n_adjacency)

    # for n_steps in big_adjacencies:
    #     print("n_steps", n_steps)
    #     new_positions = all_positions.copy()
    #     new_positions[:, 0] = (new_positions[:, 0] + n_steps * all_velocities[:, 0]) % room_size_x
    #     new_positions[:, 1] = (new_positions[:, 1] + n_steps * all_velocities[:, 1]) % room_size_y
    #     display = np.zeros((room_size_y, room_size_x))
    #     for position in new_positions:
    #         display[position[1], position[0]] += 1
    #     display_str = display.copy().astype(str)
    #     display_str[display_str == "0.0"] = "."
    #     display_str[display_str == "1.0"] = "X"
    #     display_str[display_str == "2.0"] = "X"
    #     display_str[display_str == "3.0"] = "X"

    #     # display[display > 1] = "X"
    #     # display[display == 0] = "."
    #     # with np.printoptions(threshold=np.inf, edgeitems=10, linewidth=400):
    #     #     print(display_str)
    #     for iline, line in enumerate(display_str):
    #         print("".join(line))


if __name__ == "__main__":
    main()
