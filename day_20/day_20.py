# whatever imports you need
import multiprocessing
import numpy as np
from time import time
from functools import partial


# create example code:
example = [
    "###############",
    "#...#...#.....#",
    "#.#.#.#.#.###.#",
    "#S#...#.#.#...#",
    "#######.#.#.###",
    "#######.#.#...#",
    "#######.#.###.#",
    "###..E#...#...#",
    "###.#######.###",
    "#...###...#...#",
    "#.#####.#.###.#",
    "#.#...#.#.#...#",
    "#.#.#.#.#.#.###",
    "#...#...#...###",
    "###############",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def find_reduction(wall, distance_dict_original):
    distance_before = 0
    distance_after = 0
    for direction in [(1, 0), (0, -1)]:
        check_position = (wall[0] + direction[0], wall[1] + direction[1])
        check_inverse = (wall[0] - direction[0], wall[1] - direction[1])
        if (
            (check_position in distance_dict_original) and
            (check_inverse in distance_dict_original)
        ):
            if distance_dict_original[check_position] < distance_dict_original[check_inverse]:
                distance_before = distance_dict_original[check_position]
                distance_after = distance_dict_original[check_inverse]
            else:
                distance_before = distance_dict_original[check_inverse]
                distance_after = distance_dict_original[check_position]
    # the gained distance is the distance between the two points minus the two space difference
    # between the two newly connected points
    return distance_after - distance_before - 2


def main():
    file_path = 'day_20.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    labyrinth = np.array([list(line) for line in lines_array])

    walls = set()
    distance_dict_original = {}
    for irow, row in enumerate(labyrinth):
        for icol, col in enumerate(row):
            if col == "#":
                walls.add((irow, icol))
            elif col == "S":
                start = (irow, icol)
                distance_dict_original[(irow, icol)] = 0
            elif col == "E":
                end = (irow, icol)
                distance_dict_original[(irow, icol)] = np.inf
            else:
                distance_dict_original[(irow, icol)] = np.inf

    positions = [start]
    while end not in positions:
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_position = (positions[-1][0] + direction[0], positions[-1][1] + direction[1])
            if new_position not in walls and new_position not in positions:
                distance_dict_original[new_position] = distance_dict_original[positions[-1]] + 1
                positions.append(new_position)

    # part 1
    # definitely a very inefficient way to do it, but
    # for part1, follow the very subtle hint in the problem
    # description and parallelize to make it slower
    # due to spawning the pool 'cause it's fun

    # anyway, the preparation steps are the actual bottleneck in
    # runtime since they are so slow... ~2s

    walls_to_remove = []
    for wall in walls:
        for neighbor in [(1, 0), (0, 1)]:
            check_position = (wall[0] + neighbor[0], wall[1] + neighbor[1])
            check_inverse = (wall[0] - neighbor[0], wall[1] - neighbor[1])
            if (
                (check_position in distance_dict_original) and
                (check_inverse in distance_dict_original)
            ):
                walls_to_remove.append(wall)
                break

    find_reduction_partial = partial(find_reduction, distance_dict_original=distance_dict_original)

    start_t_1 = time()
    list_reductions = []
    for wall in walls_to_remove:
        list_reductions.append(find_reduction_partial(wall))
    end_t_1 = time()
    print("time", end_t_1 - start_t_1)
    counter_dict = {}
    for reduction in list_reductions:
        if reduction in counter_dict:
            counter_dict[reduction] += 1
        else:
            counter_dict[reduction] = 1
    array_reductions = np.array(list_reductions)
    print("Part 1: the number of reductions of at least 100 is", np.sum(array_reductions >= 100))

    print("multiprocessing")
    start_t_2 = time()
    with multiprocessing.Pool(4) as p:
        list_reductions = p.map(find_reduction_partial, walls_to_remove)
    end_t_2 = time()
    print("time", end_t_2 - start_t_2)
    array_reductions = np.array(list_reductions)

    # part 2
    # well we can more or less throw away part 1

    # So this was actually a facepalm exercise for me: I was trying to find a way to
    # move within the walls ith the cheats and reach the end point somehow from the walls,
    # this is the commented out solution at the end, which is horribly slow and would need
    # a lot of improvements. However, there is no such constraint
    # in the problem description, so the solution is just to find any two points with a
    # distance in the grid smaller than 21 but a distance in the labyrinth larger than
    # 100 + their distance in the grid... which is very easy and not even that slow
    # as a loop

    all_valid_points = positions.copy()
    possible_cheats = {}
    for istart, valid_start_point in enumerate(all_valid_points):
        for iend, valid_end_point in enumerate(all_valid_points[istart + 100:]):
            if (
                (
                    abs(valid_end_point[0] - valid_start_point[0]) +
                    abs(valid_end_point[1] - valid_start_point[1])
                ) > 20
            ):
                continue
            else:
                nmoves = abs(valid_end_point[0] - valid_start_point[0]) + abs(valid_end_point[1] - valid_start_point[1])
                distance_gained = (
                    distance_dict_original[valid_end_point] -
                    distance_dict_original[valid_start_point] -
                    nmoves
                )
                if distance_gained < 100:
                    continue
                if distance_gained not in possible_cheats:
                    possible_cheats[distance_gained] = [(valid_start_point, valid_end_point)]
                else:
                    possible_cheats[distance_gained].append((valid_start_point, valid_end_point))

    print("Part 2: the number of possible cheats is", sum([len(possible_cheats[key]) for key in possible_cheats]))

    # walls_distance_dict = {}
    # for wall in walls:
    #     walls_distance_dict[wall] = np.inf

    # def path_in_walls(start, end):
    #     n_moves = 0
    #     set_unvisited = walls.copy()
    #     set_unvisited.add(start)
    #     set_unvisited.add(end)
    #     walls_distances = walls_distance_dict.copy()
    #     walls_distances[start] = 0
    #     walls_distances[end] = np.inf
    #     while (end in set_unvisited) and (n_moves < 21):
    #         current = list(walls_distances.keys())[np.argmin(list(walls_distances.values()))]
    #         curent_distance = walls_distances.pop(current)
    #         set_unvisited.remove(current)
    #         if current == end:
    #             return True, curent_distance
    #         for neighbor in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    #             new_position = (current[0] + neighbor[0], current[1] + neighbor[1])
    #             if new_position in set_unvisited:
    #                 if walls_distances[new_position] > curent_distance + 1:
    #                     walls_distances[new_position] = curent_distance + 1
    #         n_moves = curent_distance

    #     return False, np.inf

    # all_valid_points = positions.copy()
    # possible_cheats = {}
    # for istart, valid_start_point in enumerate(all_valid_points):
    #     print(istart)
    #     for iend, valid_end_point in enumerate(all_valid_points[istart + 100:]):
    #         if (
    #             (
    #                 abs(valid_end_point[0] - valid_start_point[0]) +
    #                 abs(valid_end_point[1] - valid_start_point[1])
    #             ) > 20
    #         ):
    #             continue
    #         else:
    #             path_exist, nmoves = path_in_walls(valid_start_point, valid_end_point)
    #             if path_exist:
    #                 distance_gained = (
    #                     distance_dict_original[valid_end_point] -
    #                     distance_dict_original[valid_start_point] -
    #                     nmoves
    #                 )
    #                 if distance_gained < 100:
    #                     continue
    #                 if distance_gained not in possible_cheats:
    #                     possible_cheats[distance_gained] = [(valid_start_point, valid_end_point)]
    #                 else:
    #                     possible_cheats[distance_gained].append((valid_start_point, valid_end_point))

    # print("Part 2: the number of possible cheats is", sum([len(possible_cheats[key]) for key in possible_cheats]))


if __name__ == "__main__":
    main()
