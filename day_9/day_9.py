# whatever imports you need
from itertools import combinations
import numpy as np


# create example code:
example = [
    "2333133121414131402",
]

example2 = [
    "12345",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def get_next_file_id(positions, file_id_to_move):
    file_id_to_move -= 1
    while file_id_to_move not in positions.keys():
        file_id_to_move -= 1
    return file_id_to_move


def main():
    file_path = 'day_9.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example
    input_string = lines_array[0]

    # part 1
    free_array = []
    positions = {}
    free_positions = []
    start = 0
    for inumber, number in enumerate(input_string):
        if len(input_string) % 2 == 0:
            if inumber == len(input_string) - 1:
                break
        number = int(number)
        if inumber % 2 == 0:
            file_id = inumber // 2
            for i in range(start, start + number):
                if file_id not in positions.keys():
                    positions[file_id] = [i]
                else:
                    positions[file_id] += [i]
            start += number
        else:
            free_array += [number]
            for i in range(start, start + number):
                free_positions += [i]
            start += number

    for position in positions.keys():
        positions[position] = np.array(positions[position])

    # start shuffling values according to the new file-compacting system
    # print("positions", positions)
    file_id_to_move = max(positions.keys())
    moveable_blocks = len(positions[file_id_to_move])
    # print("moveable_blocks", moveable_blocks)
    # print("file_id_to_move", file_id_to_move)
    for infree, nfree in enumerate(free_array):
        if nfree == 0:
            continue
        if (free_positions[0] > max(positions[file_id_to_move])):
            # print("free_positions[0] > max(positions[file_id_to_move])", free_positions[0], max(positions[file_id_to_move]))
            break
        if nfree > moveable_blocks:
            # print("nfree > moveable_blocks", nfree, moveable_blocks)
            while nfree > moveable_blocks:
                positions[file_id_to_move] = np.sort(positions[file_id_to_move])[::-1]
                positions[file_id_to_move][:moveable_blocks] = free_positions[:moveable_blocks]
                free_positions = free_positions[moveable_blocks:]
                nfree -= moveable_blocks
                file_id_to_move = get_next_file_id(positions, file_id_to_move)
                moveable_blocks = len(positions[file_id_to_move])
        if nfree < moveable_blocks:
            # print("nfree < moveable_blocks", nfree, moveable_blocks)
            # print("positions", positions)
            positions[file_id_to_move] = np.sort(positions[file_id_to_move])[::-1]
            positions[file_id_to_move][:nfree] = free_positions[:nfree]
            # print("positions", positions)
            free_positions = free_positions[nfree:]
            moveable_blocks -= nfree
        elif nfree == moveable_blocks:
            # print("nfree == moveable_blocks", nfree, moveable_blocks)
            positions[file_id_to_move] = np.sort(positions[file_id_to_move])[::-1]
            positions[file_id_to_move][:nfree] = free_positions[:nfree]
            free_positions = free_positions[nfree:]
            file_id_to_move = get_next_file_id(positions, file_id_to_move)
            moveable_blocks = len(positions[file_id_to_move])

    checksum_res = 0
    for position in positions.keys():
        checksum_res += sum(positions[position]*position)
    print("the checksum is", checksum_res)

    # part 2
    # redo arrays from part 1
    free_rooms = {}
    positions = {}
    free_positions = {}
    start = 0
    for inumber, number in enumerate(input_string):
        if len(input_string) % 2 == 0:
            if inumber == len(input_string) - 1:
                break
        number = int(number)
        if inumber % 2 == 0:
            file_id = inumber // 2
            for i in range(start, start + number):
                if file_id not in positions.keys():
                    positions[file_id] = [i]
                else:
                    positions[file_id] += [i]
            start += number
        else:
            free_id = inumber // 2
            free_rooms[free_id] = number
            for i in range(start, start + number):
                if free_id not in free_positions.keys():
                    free_positions[free_id] = [i]
                else:
                    free_positions[free_id] += [i]
            start += number

    for position in positions.keys():
        positions[position] = np.array(positions[position])

    free_array = np.array(free_array)

    # start shuffle values according to the new file-compacting system

    decreasing_sorted_file_ids = np.sort(list(positions.keys()))[::-1]
    for i, file_id in enumerate(decreasing_sorted_file_ids):
        if np.any(np.array(list(free_rooms.values())) >= len(positions[file_id])):
            pos_free_id_to_fill = np.argmax(np.array(list(free_rooms.values())) >= len(positions[file_id]))
            if free_positions[pos_free_id_to_fill][0] < min(positions[file_id]):
                free_id_to_fill = np.array(list(free_rooms.keys()))[pos_free_id_to_fill]
                positions[file_id] = free_positions[free_id_to_fill][:len(positions[file_id])]
                free_positions[free_id_to_fill] = free_positions[free_id_to_fill][len(positions[file_id]):]
                free_rooms[free_id_to_fill] -= len(positions[file_id])

    # print("positions", positions)
    checksum_res = 0
    for position in positions.keys():
        checksum_res += sum(positions[position]*position)
    print("the checksum is", checksum_res)


if __name__ == "__main__":
    main()
