# whatever imports you need
from itertools import combinations
import numpy as np


# create example code:
example = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def calculate_next_antinode_part1(pairs_positions):
    pairs_1 = pairs_positions[:, 0]
    pairs_2 = pairs_positions[:, 1]
    distance_y = pairs_2[:, 0] - pairs_1[:, 0]
    distance_x = pairs_2[:, 1] - pairs_1[:, 1]
    next_antinode_1 = np.stack([pairs_1[:, 0] - distance_y, pairs_1[:, 1] - distance_x], axis=1)
    next_antinode_2 = np.stack([pairs_2[:, 0] + distance_y, pairs_2[:, 1] + distance_x], axis=1)
    return np.concatenate([next_antinode_1, next_antinode_2])


def calculate_all_antinodes_part2(pairs_positions, map_boundaries):
    pairs_1 = pairs_positions[:, 0]
    pairs_2 = pairs_positions[:, 1]
    distance_y = pairs_2[:, 0] - pairs_1[:, 0]
    distance_x = pairs_2[:, 1] - pairs_1[:, 1]
    all_antinodes = np.concatenate([pairs_1, pairs_2])
    # pretty inefficient, only stops when all antinodes of a type are out of bounds...
    while True:
        next_antinode_1 = np.stack([pairs_1[:, 0] - distance_y, pairs_1[:, 1] - distance_x], axis=1)
        next_antinode_2 = np.stack([pairs_2[:, 0] + distance_y, pairs_2[:, 1] + distance_x], axis=1)
        expected_antinodes = np.concatenate([next_antinode_1, next_antinode_2])
        mask_out_of_bounds = (
            (expected_antinodes[:, 0] >= map_boundaries[0][0]) &
            (expected_antinodes[:, 0] < map_boundaries[0][1]) &
            (expected_antinodes[:, 1] >= map_boundaries[1][0]) &
            (expected_antinodes[:, 1] < map_boundaries[1][1])
        )
        if not mask_out_of_bounds.any():
            break
        all_antinodes = np.concatenate([all_antinodes, expected_antinodes])
        pairs_1 = next_antinode_1
        pairs_2 = next_antinode_2

    return all_antinodes


def main():
    file_path = 'day_8.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example
    dict_of_antennae = {}

    for i, line in enumerate(lines_array):
        for j, char in enumerate(line):
            if char == '.':
                continue
            position = [i, j]
            if char not in dict_of_antennae.keys():
                dict_of_antennae[char] = [position]
            else:
                dict_of_antennae[char].append([i, j])

    print(dict_of_antennae)
    map_boundaries = [[0, len(lines_array)], [0, len(lines_array[0])]]

    # part 1
    antinodes = set()

    for antenna_type in dict_of_antennae.keys():
        all_pairs = np.array(list(combinations(dict_of_antennae[antenna_type], 2)))
        expected_antinodes = calculate_next_antinode_part1(all_pairs)
        mask_out_of_bounds = (
            (expected_antinodes[:, 0] >= map_boundaries[0][0]) &
            (expected_antinodes[:, 0] < map_boundaries[0][1]) &
            (expected_antinodes[:, 1] >= map_boundaries[1][0]) &
            (expected_antinodes[:, 1] < map_boundaries[1][1])
        )
        antinodes.update([tuple(antinode) for antinode in expected_antinodes[mask_out_of_bounds]])

    print("the number of antinodes is", len(antinodes))

    # part 2
    antinodes_2 = set()
    for antenna_type in dict_of_antennae.keys():
        all_pairs = np.array(list(combinations(dict_of_antennae[antenna_type], 2)))
        expected_antinodes_2 = calculate_all_antinodes_part2(all_pairs, map_boundaries)
        mask_out_of_bounds = (
            (expected_antinodes_2[:, 0] >= map_boundaries[0][0]) &
            (expected_antinodes_2[:, 0] < map_boundaries[0][1]) &
            (expected_antinodes_2[:, 1] >= map_boundaries[1][0]) &
            (expected_antinodes_2[:, 1] < map_boundaries[1][1])
        )
        antinodes_2.update([tuple(antinode) for antinode in expected_antinodes_2[mask_out_of_bounds]])

    print("the number of antinodes_2 is", len(antinodes_2))


if __name__ == "__main__":
    main()
