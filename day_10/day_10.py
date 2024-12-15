# whatever imports you need
import numpy as np


# create example code:
example = [
    "0123",
    "1234",
    "8765",
    "9876",
]

example_2 = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def search_next_number(number, neighbors, neighbors_positions):
    correct_neighbors = {}
    n_correct_neighbors = 0
    for ineighbor, neighbor in enumerate(neighbors):
        if neighbor == number:
            correct_neighbors[n_correct_neighbors] = neighbors_positions[ineighbor]
            n_correct_neighbors += 1
    return correct_neighbors


def main():
    file_path = 'day_10.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example
    # lines_array = example_2

    all_heights = []

    for iline, line in enumerate(lines_array):
        all_heights.append([int(char) for char in line])

    all_heights = np.array(all_heights)

    # part 1
    zeros_dict = {}
    zeros_id = 0
    for i in range(0, len(all_heights)):
        for j in range(0, len(all_heights[0])):
            if all_heights[i][j] == 0:
                zeros_dict[zeros_id] = (i, j)
                zeros_id += 1

    lim_y = len(all_heights)
    lim_x = len(all_heights[0])

    trailheads_paths = {}
    for key in zeros_dict.keys():
        number_positions = [zeros_dict[key]]
        neighbors_value = 1
        while neighbors_value < 10:
            new_numbers_pos = []
            for position in number_positions:
                neighbors = []
                neighbors_positions = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if i != 0 and j != 0:
                            continue
                        if (
                            position[0] + i >= 0 and
                            position[1] + j >= 0 and
                            position[0] + i < lim_y and
                            position[1] + j < lim_x
                        ):
                            neighbors.append(all_heights[position[0] + i][position[1] + j])
                            neighbors_positions.append((position[0] + i, position[1] + j))
                correct_neighbors = search_next_number(neighbors_value, neighbors, neighbors_positions)
                new_numbers_pos += list(correct_neighbors.values())
            if len(new_numbers_pos) == 0:
                break
            neighbors_value += 1
            number_positions = new_numbers_pos
        if neighbors_value == 10:
            trailheads_paths[key] = number_positions
    # print("trailheads_paths", trailheads_paths)
    trailheads_summits = {}
    for key, value in trailheads_paths.items():
        trailheads_summits[key] = set(value)
    # print("trailheads_summits", trailheads_summits)
    print("the total trailhead score is", sum([len(value) for value in trailheads_summits.values()]))

    # part 2
    print("the total trailhead rating is", sum([len(value) for value in trailheads_paths.values()]))


if __name__ == "__main__":
    main()
