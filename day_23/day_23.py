# whatever imports you need
import numpy as np
from time import time

# create example code:
example = [
    "kh-tc",
    "qp-kh",
    "de-cg",
    "ka-co",
    "yn-aq",
    "qp-ub",
    "cg-tb",
    "vc-aq",
    "tb-ka",
    "wh-tc",
    "yn-cg",
    "kh-ub",
    "ta-co",
    "de-co",
    "tc-td",
    "tb-wq",
    "wh-td",
    "ta-ka",
    "td-qp",
    "aq-cg",
    "wq-ub",
    "ub-vc",
    "de-ta",
    "wq-aq",
    "wq-vc",
    "wh-yn",
    "ka-de",
    "kh-ta",
    "co-tc",
    "wh-qp",
    "tb-vc",
    "td-yn",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_23.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    all_connections_tuple = [tuple(line.split('-')) for line in lines_array]

    # Part 1
    all_connections_dict = {}
    for iconnection, connection in enumerate(all_connections_tuple):
        if connection[0] in all_connections_dict:
            all_connections_dict[connection[0]].append(connection[1])
        else:
            all_connections_dict[connection[0]] = [connection[1]]
        if connection[1] in all_connections_dict:
            all_connections_dict[connection[1]].append(connection[0])
        else:
            all_connections_dict[connection[1]] = [connection[0]]

    # program bottleneck, takes 6 seconds to run, way too much...
    start = time()
    sets_of_three = []
    for key, values in all_connections_dict.items():
        for value in values:
            if set(all_connections_dict[key]) & set(all_connections_dict[value]):
                for third_member in (set(all_connections_dict[key]) & set(all_connections_dict[value])):
                    set_of_three = set([key, value, third_member])
                    if set_of_three not in sets_of_three:
                        sets_of_three.append(set_of_three)
    end = time()
    print("creation of sets_of_three took:", end - start, "seconds to run")

    sets_with_t = []
    for set_of_three in sets_of_three:
        for element in set_of_three:
            if element[0] == 't':
                sets_with_t.append(set_of_three)
                break

    print("Part 1:", len(sets_with_t))

    # Part 2
    # find the largest set of mutually connected elements
    # every key has 13 connections, so we try such a set with 13 connections, and remove all
    # keys until finding the only keys with 13 connections, else go down in required number of keys

    max_len = 13
    max_set = set()
    while not max_set:
        reduced_connections_dict = all_connections_dict.copy()
        while len(reduced_connections_dict) > max_len:
            copy_reduced_connections_dict = reduced_connections_dict.copy()
            for key, values in reduced_connections_dict.items():
                values_with_correct_intersections = []
                for key2 in values:
                    if key2 in reduced_connections_dict:
                        set_potential_connections = set(reduced_connections_dict[key]) & set(reduced_connections_dict[key2])  # noqa
                        values_with_correct_intersections.append(len(set_potential_connections))
                    else:
                        values_with_correct_intersections.append(0)
                values_with_correct_intersections = np.array(values_with_correct_intersections)
                if sum(values_with_correct_intersections >= max_len - 2) < (max_len - 1):
                    copy_reduced_connections_dict.pop(key, None)
            reduced_connections_dict = copy_reduced_connections_dict
        if len(reduced_connections_dict) == max_len:
            max_set = set(reduced_connections_dict.keys())
            break
        max_len -= 1
    print("Part 2: ordered max_set:", sorted(list(max_set)))

    # solution is bv,cm,dk,em,gs,jv,ml,oy,qj,ri,uo,xk,yw
    # -> need to remove the whitespaces and quotes, from the print statement


if __name__ == "__main__":
    main()
