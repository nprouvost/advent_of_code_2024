# whatever imports you need
import functools
import numpy as np
from itertools import product


# create example code:
example = [
    "029A",
    "980A",
    "179A",
    "456A",
    "379A",
]

numerical_keypad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
    "boundaries": [
        (-1, 0), (-1, 1), (-1, 2), (3, 0), (4, 1), (4, 2),
        (0, -1), (1, -1), (2, -1), (0, 3), (1, 3), (2, 3), (3, 3),
    ],
}

directional_keypad = {
    "^": (0, 1),
    "v": (1, 1),
    "<": (1, 0),
    ">": (1, 2),
    "A": (0, 2),
    "boundaries": [
        (0, 0), (-1, 1), (-1, 2), (2, 0), (2, 1), (2, 2),
        (1, -1), (0, 3), (1, 3),
    ],
}


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def click_new_position(original_position, next_position):
    keypad = directional_keypad
    list_of_moves = []
    while original_position != next_position:
        # order matters here to have the fewest moves possible
        # first we go right cause it's the nearest to "A",
        # so only one is needed to reach the tile and then we can stay there for as
        # long as we need to
        if (
            (original_position[1] < next_position[1]) and
            ((original_position[0], original_position[1] + 1) not in keypad["boundaries"])
        ):
            original_position = (original_position[0], original_position[1] + 1)
            list_of_moves.append(">")
        # Then up cause it's also nearest to "A", either will only want to go right and up
        # or it will come first
        elif (
            (original_position[0] > next_position[0]) and
            ((original_position[0] - 1, original_position[1]) not in keypad["boundaries"])
        ):
            original_position = (original_position[0] - 1, original_position[1])
            list_of_moves.append("^")
        # then we go down cause it's the least way to go from right and top
        elif (
            (original_position[0] < next_position[0]) and
            ((original_position[0] + 1, original_position[1]) not in keypad["boundaries"])
        ):
            original_position = (original_position[0] + 1, original_position[1])
            list_of_moves.append("v")
        elif (
            (original_position[1] > next_position[1]) and
            ((original_position[0], original_position[1] - 1) not in keypad["boundaries"])
        ):
            original_position = (original_position[0], original_position[1] - 1)
            list_of_moves.append("<")
        else:
            raise ValueError("No move possible")
    list_of_moves.append("A")
    return original_position, "".join(list_of_moves)


def check_best_sequences(all_n_sequences_dict, directional_keypad, n_keypads=2):
    check_best_sequences = all_n_sequences_dict.copy()
    results_best_sequences = {}
    values_best_sequences = {}
    for imoves, moves in enumerate(check_best_sequences.keys()):
        print(imoves)
        for isequence, sequence in enumerate(check_best_sequences[moves]):
            check_best_sequences[moves][isequence] = sequence + "A"
            all_versions_sequences = {0: check_best_sequences[moves][isequence]}
            for i in range(n_keypads):
                keypad = directional_keypad
                position = keypad["A"]
                for letter in all_versions_sequences[i]:
                    original_position = position
                    next_position = keypad[letter]
                    position, str_of_moves = click_new_position(original_position, next_position)
                    if i + 1 not in all_versions_sequences:
                        all_versions_sequences[i + 1] = str_of_moves
                    else:
                        all_versions_sequences[i + 1] += str_of_moves
            if moves not in results_best_sequences:
                results_best_sequences[moves] = [len(all_versions_sequences[n_keypads])]
                values_best_sequences[moves] = [all_versions_sequences[n_keypads]]
            else:
                results_best_sequences[moves].append(len(all_versions_sequences[n_keypads]))
                values_best_sequences[moves].append(all_versions_sequences[n_keypads])
    return results_best_sequences, values_best_sequences


def check_best_whole_sequences(
    best_sequences,
    all_n_sequences_dict,
    results_best_sequences,
    values_best_sequences,
    lines_array,
    numerical_keypad,
    move_dict,
):
    all_code_sequences = []
    for code in lines_array:
        all_sequences = {}
        keypad = numerical_keypad
        all_sequences[0] = code
        position = keypad["A"]
        for letter in all_sequences[0]:
            original_position = position
            next_position = keypad[letter]
            move = (next_position[0] - original_position[0], next_position[1] - original_position[1])
            position = next_position
            if move not in best_sequences:
                raise ValueError(f"Move {move} not in best_sequences")
            else:
                check_succesful_move = True
                # check if the best move is possible
                potential_best_sequence = best_sequences[move][0]
                potential_position = original_position
                for potential_letter in potential_best_sequence:
                    if potential_letter == "A":
                        break
                    potential_next_position = (
                        potential_position[0] + move_dict[potential_letter][0],
                        potential_position[1] + move_dict[potential_letter][1]
                    )
                    if potential_next_position in keypad["boundaries"]:
                        check_succesful_move = False
                        problematic_move = potential_next_position
                        break
                    potential_position = potential_next_position
                if check_succesful_move:
                    if 1 not in all_sequences:
                        all_sequences[1] = best_sequences[move][0]
                    else:
                        all_sequences[1] += best_sequences[move][0]
                    if 2 not in all_sequences:
                        all_sequences[2] = best_sequences[move][1]
                    else:
                        all_sequences[2] += best_sequences[move][1]
                else:
                    # need to calculate the best move with constraints
                    # so first find all the possible moves that fit the constraints
                    invalid_move = (problematic_move[0] - original_position[0], problematic_move[1] - original_position[1])
                    possible_moves = {move: []}
                    for ipart_sequence, part_sequence in enumerate(all_n_sequences_dict[move]):
                        potential_move = (0, 0)
                        for potential_letter in part_sequence:
                            if potential_letter == "A":
                                break
                            potential_move = (
                                potential_move[0] + move_dict[potential_letter][0],
                                potential_move[1] + move_dict[potential_letter][1]
                            )
                            if potential_move == invalid_move:
                                break
                        if potential_move != invalid_move:
                            possible_moves[move].append(ipart_sequence)
                    # then find the best move with constraints
                    results_best_sequences_with_constraints = {}
                    values_best_sequences_with_constraints = {}
                    for index in possible_moves[move]:
                        if move not in results_best_sequences_with_constraints:
                            results_best_sequences_with_constraints[move] = [results_best_sequences[move][index]]
                            values_best_sequences_with_constraints[move] = [values_best_sequences[move][index]]
                        else:
                            results_best_sequences_with_constraints[move].append(results_best_sequences[move][index])
                            values_best_sequences_with_constraints[move].append(values_best_sequences[move][index])
                    argmin = np.argmin(results_best_sequences_with_constraints[move])
                    if 1 not in all_sequences:
                        all_sequences[1] = all_n_sequences_dict[move][possible_moves[move][argmin]]
                    else:
                        all_sequences[1] += all_n_sequences_dict[move][possible_moves[move][argmin]]
                    if 2 not in all_sequences:
                        all_sequences[2] = values_best_sequences_with_constraints[move][argmin]
                    else:
                        all_sequences[2] += values_best_sequences_with_constraints[move][argmin]
        all_code_sequences.append(all_sequences)
    return all_code_sequences


def main():
    file_path = 'day_21.txt'
    lines_array = read_file_to_list(file_path)
    lines_array = example

    # part 1

    # build the best sequences in the last keypad for each move, then use the best sequences
    # to build the resulting paths for each code
    # do not forget that the keypad has a boundary, so we need to check if the move is possible
    # else we need to constrain the new best sequence to not go through the boundary

    all_directions = ["^", "v", "<", ">"]
    all_2_sequences = ["".join(sequence) for sequence in product(all_directions, repeat=2)]
    all_3_sequences = ["".join(sequence) for sequence in product(all_directions, repeat=3)]
    all_4_sequences = ["".join(sequence) for sequence in product(all_directions, repeat=4)]
    all_5_sequences = ["".join(sequence) for sequence in product(all_directions, repeat=5)]

    move_dict = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    all_n_sequences = all_directions + all_2_sequences + all_3_sequences + all_4_sequences + all_5_sequences

    all_n_sequences_dict = {}
    for sequence in all_n_sequences:
        total_moves = (0, 0)
        for i, letter in enumerate(sequence):
            total_moves = (total_moves[0] + move_dict[letter][0], total_moves[1] + move_dict[letter][1])
        if total_moves not in all_n_sequences_dict:
            all_n_sequences_dict[total_moves] = [sequence]
        else:
            all_n_sequences_dict[total_moves].append(sequence)

    results_best_sequences, values_best_sequences = check_best_sequences(
        all_n_sequences_dict,
        directional_keypad
    )

    best_sequences = {}
    for moves in results_best_sequences.keys():
        argmin = np.argmin(results_best_sequences[moves])
        best_sequences[moves] = (
            all_n_sequences_dict[moves][argmin],
            values_best_sequences[moves][argmin],
            results_best_sequences[moves][argmin]
        )

    all_code_sequences = check_best_whole_sequences(
        best_sequences,
        all_n_sequences_dict,
        results_best_sequences,
        values_best_sequences,
        lines_array,
        numerical_keypad,
        move_dict,
    )

    num_part_codes = [int(line[:-1]) for line in lines_array]
    results = [num_part_codes[i] * len(all_code_sequences[i][2]) for i in range(len(lines_array))]
    print(f"Part 1: {sum(results)}")

    # part 2
    # do it again, but with 25 directional keypads
    # so either find a much more clever way of dealing with the problem,
    # or start caching the results for each keypad somehow

    # results_best_sequences, values_best_sequences = check_best_sequences(
    #     all_n_sequences_dict,
    #     directional_keypad,
    #     n_keypads=25
    # )

    # best_sequences = {}
    # for moves in results_best_sequences.keys():
    #     argmin = np.argmin(results_best_sequences[moves])
    #     best_sequences[moves] = (
    #         all_n_sequences_dict[moves][argmin],
    #         values_best_sequences[moves][argmin],
    #         results_best_sequences[moves][argmin]
    #     )

    # all_code_sequences = check_best_whole_sequences(
    #     best_sequences,
    #     all_n_sequences_dict,
    #     results_best_sequences,
    #     values_best_sequences,
    #     lines_array,
    #     numerical_keypad,
    #     move_dict,
    # )

    # results = [num_part_codes[i] * len(all_code_sequences[i][2]) for i in range(len(lines_array))]
    # print(f"Part 2: {sum(results)}")







if __name__ == "__main__":
    main()
