# whatever imports you need
import numpy as np


# create example code:
example = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############",
]

example2 = [
    "#################",
    "#...#...#...#..E#",
    "#.#.#.#.#.#.#.#.#",
    "#.#.#.#...#...#.#",
    "#.#.#.#.###.#.#.#",
    "#...#.#.#.....#.#",
    "#.#.#.#.#.#####.#",
    "#.#...#.#.#.....#",
    "#.#.#####.#.###.#",
    "#.#.#.......#...#",
    "#.#.###.#####.###",
    "#.#.#...#.....#.#",
    "#.#.#.#####.###.#",
    "#.#.#.........#.#",
    "#.#.#.#########.#",
    "#S#.............#",
    "#################",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_16.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example2

    labyrinth = np.array([list(line) for line in lines_array])

    set_unvisited = set()
    walls = set()
    set_visited = set()
    distance_dict = {}
    for irow, row in enumerate(labyrinth):
        for icol, col in enumerate(row):
            if col == "#":
                walls.add((irow, icol))
            elif col == "S":
                start = (irow, icol)
                distance_dict[(irow, icol)] = 0
                set_unvisited.add((irow, icol))
            elif col == "E":
                end = (irow, icol)
                set_unvisited.add((irow, icol))
                distance_dict[(irow, icol)] = np.inf
            else:
                set_unvisited.add((irow, icol))
                distance_dict[(irow, icol)] = np.inf

    directions = {"E": (0, 1), "W": (0, -1), "N": (-1, 0), "S": (1, 0)}
    directions_dict = {start: {directions["E"]}}

    distance_dict_unvisited = distance_dict.copy()

    # part 1
    # implement Dijkstra algorithm with additional directions information
    while end not in set_visited:
        current = list(distance_dict_unvisited.keys())[np.argmin(list(distance_dict_unvisited.values()))]
        curent_distance = distance_dict_unvisited.pop(current)
        set_unvisited.remove(current)
        set_visited.add(current)
        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
        ]
        neighbors_directions = ["S", "N", "E", "W"]
        opposite_directions = {"S": "N", "N": "S", "E": "W", "W": "E"}
        for ineighbor, neighbor in enumerate(neighbors):
            if neighbor in walls:
                continue
            if neighbor in set_visited:
                continue
            if neighbor in set_unvisited:
                for direction in directions_dict[current]:
                    if direction == directions[neighbors_directions[ineighbor]]:
                        if distance_dict[neighbor] > curent_distance + 1:
                            directions_dict[neighbor] = {direction}
                            distance_dict[neighbor] = curent_distance + 1
                            distance_dict_unvisited[neighbor] = curent_distance + 1
                        elif distance_dict[neighbor] == curent_distance + 1:
                            directions_dict[neighbor].add(direction)
                    elif direction == directions[opposite_directions[neighbors_directions[ineighbor]]]:
                        raise ValueError("Goes in opposite direction", directions_dict[current], direction)
                    else:
                        if distance_dict[neighbor] > curent_distance + 1001:
                            directions_dict[neighbor] = {directions[neighbors_directions[ineighbor]]}
                            distance_dict[neighbor] = curent_distance + 1001
                            distance_dict_unvisited[neighbor] = curent_distance + 1001
                        elif distance_dict[neighbor] == curent_distance + 1001:
                            directions_dict[neighbor].add(directions[neighbors_directions[ineighbor]])
            else:
                raise ValueError("Some index not in walls, nor set_unvisited or set_visited")

    print("the minimum distance to the end is", distance_dict[end])
    # print("distance_dict", distance_dict)

    # part 2

    # find how many positions are in any best paths
    set_paths_positions = set()
    set_paths_positions.add(end)
    interesting_positions = {end}
    while interesting_positions:
        new_interesting_positions = set()
        for position in interesting_positions:
            for direction in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                new_position = (position[0] + direction[0], position[1] + direction[1])
                if new_position in set_visited:
                    if (
                        (distance_dict[new_position] == (distance_dict[position] - 1)) or
                        (distance_dict[new_position] == (distance_dict[position] - 1001)) or
                        (distance_dict[new_position] == (distance_dict[position] + 999))
                    ):
                        # -1 and -1001 obvious, but 999 happens when two paths mix together, one will
                        # have one more turn (+1000) and the second one will have one less turn but turn on the
                        # first mixed move (-1 common move), so the difference is (1000 - 1) = 999
                        # however, this caveat is too broad, so we need to check if the two paths are really
                        # good paths, add a few checks -> the next move should add 1001 to the distance
                        # of the smaller path it should belong to the set of paths positions already found
                        # in the previous step
                        if (distance_dict[new_position] == (distance_dict[position] + 999)):
                            test_position = (position[0] - direction[0], position[1] - direction[1])
                            if (test_position in set_visited):
                                if (
                                    (distance_dict[test_position] == (distance_dict[position] + 1001)) and
                                    (test_position in set_paths_positions)
                                ):
                                    new_interesting_positions.add(new_position)
                                    set_paths_positions.add(new_position)
                        else:
                            new_interesting_positions.add(new_position)
                            set_paths_positions.add(new_position)
        interesting_positions = new_interesting_positions

    # print("all points in the best paths", set_paths_positions)

    print("the number of positions in the best paths is", len(set_paths_positions))


if __name__ == "__main__":
    main()
