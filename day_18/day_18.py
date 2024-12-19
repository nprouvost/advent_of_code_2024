# whatever imports you need
import numpy as np


# create example code:
example = [
    "5,4",
    "4,2",
    "4,5",
    "3,0",
    "2,1",
    "6,3",
    "2,4",
    "1,5",
    "0,6",
    "3,3",
    "2,6",
    "5,1",
    "1,2",
    "5,5",
    "2,5",
    "6,5",
    "1,4",
    "0,4",
    "6,4",
    "1,1",
    "6,1",
    "1,0",
    "0,5",
    "1,6",
    "2,0",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_18.txt'
    lines_array = read_file_to_list(file_path)
    example_ = False
    # lines_array = example
    # example_ = True

    # part 1
    field_size = 7 if example_ else 71
    set_unvisited = set()
    set_visited = set()
    distance_dict = {}
    walls = []
    for iline, line in enumerate(lines_array):
        if example_:
            if iline == 12:
                break
        else:
            if iline == 1024:
                break
        walls.append(tuple(map(int, line.split(','))))
    for i in range(field_size):
        for j in range(field_size):
            if (i, j) not in walls:
                set_unvisited.add((i, j))
                distance_dict[(i, j)] = np.inf
        walls.append((i, -1))
        walls.append((i, field_size))
        walls.append((-1, i))
        walls.append((field_size, i))

    # implement dijkstra algorithm

    start = (0, 0)
    end = (field_size - 1, field_size - 1)
    distance_dict[start] = 0

    distance_dict_unvisited = distance_dict.copy()

    while end not in set_visited:
        current = list(distance_dict_unvisited.keys())[np.argmin(list(distance_dict_unvisited.values()))]
        set_visited.add(current)
        set_unvisited.remove(current)
        current_distance = distance_dict_unvisited.pop(current)
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if neighbor in set_unvisited:
                neighbor_distance = current_distance + 1
                if neighbor_distance < distance_dict[neighbor]:
                    distance_dict[neighbor] = neighbor_distance
                    distance_dict_unvisited[neighbor] = neighbor_distance

    print("Part 1:", distance_dict[end])

    # part 2
    # brute force solution, just try out when it stops working
    start_byte = 12 if example_ else 1024
    for nbyte in range(start_byte, len(lines_array)):
        set_unvisited = set()
        set_visited = set()
        distance_dict = {}
        walls = []
        for iline, line in enumerate(lines_array):
            if iline == nbyte:
                break
            walls.append(tuple(map(int, line.split(','))))
        for i in range(field_size):
            for j in range(field_size):
                if (i, j) not in walls:
                    set_unvisited.add((i, j))
                    distance_dict[(i, j)] = np.inf
            walls.append((i, -1))
            walls.append((i, field_size))
            walls.append((-1, i))
            walls.append((field_size, i))

        # implement dijkstra algorithm

        start = (0, 0)
        end = (field_size - 1, field_size - 1)
        distance_dict[start] = 0

        distance_dict_unvisited = distance_dict.copy()
        smallest_distance_unvisited = min(list(distance_dict_unvisited.values()))

        while (end not in set_visited) and (smallest_distance_unvisited != np.inf):
            current = list(distance_dict_unvisited.keys())[np.argmin(list(distance_dict_unvisited.values()))]
            set_visited.add(current)
            set_unvisited.remove(current)
            current_distance = distance_dict_unvisited.pop(current)
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if neighbor in set_unvisited:
                    neighbor_distance = current_distance + 1
                    if neighbor_distance < distance_dict[neighbor]:
                        distance_dict[neighbor] = neighbor_distance
                        distance_dict_unvisited[neighbor] = neighbor_distance
            if len(set_unvisited) != 0:
                smallest_distance_unvisited = min(list(distance_dict_unvisited.values()))

        if distance_dict[end] == np.inf:
            break
    print("Part 2:", lines_array[nbyte - 1])

    # other solutions, not implemented:
    # - A* algorithm to find the shortest path to improve the performance
    # - find another method to see when the way is blocked, e.g. build a list of critical points
    # with only one possible tile to go at the step mentioned in part 1 and check if the next byte blocks one of them,
    # if not, update the list of critical points by checking only the neighbors of the new byte,
    # since they are the only possible new critical points, should be much faster


if __name__ == "__main__":
    main()
