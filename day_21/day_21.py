# whatever imports you need
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
    all_sequences_dict = all_n_sequences_dict.copy()
    results_best_sequences = {}
    values_best_sequences = {}
    for imoves, moves in enumerate(all_sequences_dict.keys()):
        # print(imoves)
        for isequence, sequence in enumerate(all_sequences_dict[moves]):
            all_sequences_dict[moves][isequence] = sequence + "A"
            all_versions_sequences = {0: all_sequences_dict[moves][isequence]}
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
                    invalid_move = (problematic_move[0] - original_position[0], problematic_move[1] - original_position[1])  # noqa
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
    # lines_array = example

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
    all_n_sequences_dict[(0, 0)].append("")

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

    # first approach: just try brute force and look how long it takes:
    # answer: way too long

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

    # takes too long, try by using the best sequence for each move and then use it to find the best sequence
    # for each step until steps 13, then use the best sequence for 13 steps on the 13th step
    # maybe need to create it for every position with constraints (the ones on the same row or column
    # as the inner boundary)

    # we already have the best sequences for each move, so we can use them to create the best sequence
    # with constraints

    # numerical_keypad constraints
    contraints_numerical_keypad = {
        (0, 0): {},
        (1, 0): {},
        (2, 0): {},
        (3, 1): {},
        (3, 2): {},
    }
    results_constraints_numerical_keypad = {
        (0, 0): {},
        (1, 0): {},
        (2, 0): {},
        (3, 1): {},
        (3, 2): {},
    }
    values_constraints_numerical_keypad = {
        (0, 0): {},
        (1, 0): {},
        (2, 0): {},
        (3, 1): {},
        (3, 2): {},
    }
    constraint_sequences_numerical_dict = {
        (0, 0): {},
        (1, 0): {},
        (2, 0): {},
        (3, 1): {},
        (3, 2): {},
    }

    def create_constraints(constraint, invalid_sequence, constraints_dict, results_dict, values_dict, constraint_sequences_dict, all_n_sequences_dict):  # noqa
        if ("v" in invalid_sequence) or ("^" in invalid_sequence):
            value_to_check = 0
        else:
            value_to_check = 1
        if ("<" in invalid_sequence) or ("^" in invalid_sequence):
            sign_to_check = -1
        else:
            sign_to_check = 1
        for move in all_n_sequences_dict.keys():
            if move[value_to_check] == sign_to_check * len(invalid_sequence):
                possible_sequences = all_n_sequences_dict[move]
                constraint_sequences = []
                for isequence, sequence in enumerate(possible_sequences):
                    if sequence.startswith(invalid_sequence):
                        continue
                    constraint_sequences.append(isequence)
                    if move not in constraints_dict[constraint]:
                        constraints_dict[constraint][move] = [sequence]
                        results_dict[constraint][move] = [results_best_sequences[move][isequence]]
                        values_dict[constraint][move] = [values_best_sequences[move][isequence]]
                    else:
                        constraints_dict[constraint][move].append(sequence)
                        results_dict[constraint][move].append(results_best_sequences[move][isequence])
                        values_dict[constraint][move].append(values_best_sequences[move][isequence])
                constraint_sequences_dict[constraint][move] = constraint_sequences
        return constraints_dict, results_dict, values_dict, constraint_sequences_dict

    # constraint for (0, 0)
    contraints_numerical_keypad, results_constraints_numerical_keypad, values_constraints_numerical_keypad, constraint_sequences_numerical_dict = create_constraints(  # noqa
        (0, 0),
        "vvv",
        contraints_numerical_keypad,
        results_constraints_numerical_keypad,
        values_constraints_numerical_keypad,
        constraint_sequences_numerical_dict,
        all_n_sequences_dict
    )

    # constraint for (1, 0)
    contraints_numerical_keypad, results_constraints_numerical_keypad, values_constraints_numerical_keypad, constraint_sequences_numerical_dict = create_constraints(  # noqa
        (1, 0),
        "vv",
        contraints_numerical_keypad,
        results_constraints_numerical_keypad,
        values_constraints_numerical_keypad,
        constraint_sequences_numerical_dict,
        all_n_sequences_dict
    )

    # constraint for (2, 0)
    contraints_numerical_keypad, results_constraints_numerical_keypad, values_constraints_numerical_keypad, constraint_sequences_numerical_dict = create_constraints(  # noqa
        (2, 0),
        "v",
        contraints_numerical_keypad,
        results_constraints_numerical_keypad,
        values_constraints_numerical_keypad,
        constraint_sequences_numerical_dict,
        all_n_sequences_dict
    )

    # constraint for (3, 1)
    contraints_numerical_keypad, results_constraints_numerical_keypad, values_constraints_numerical_keypad, constraint_sequences_numerical_dict = create_constraints(  # noqa
        (3, 1),
        "<",
        contraints_numerical_keypad,
        results_constraints_numerical_keypad,
        values_constraints_numerical_keypad,
        constraint_sequences_numerical_dict,
        all_n_sequences_dict
    )

    # constraint for (3, 2)
    contraints_numerical_keypad, results_constraints_numerical_keypad, values_constraints_numerical_keypad, constraint_sequences_numerical_dict = create_constraints(  # noqa
        (3, 2),
        "<<",
        contraints_numerical_keypad,
        results_constraints_numerical_keypad,
        values_constraints_numerical_keypad,
        constraint_sequences_numerical_dict,
        all_n_sequences_dict
    )

    # directional_keypad constraints
    contraints_directional_keypad = {
        (0, 1): {},
        (0, 2): {},
        (1, 0): {},
    }
    results_constraints_directional_keypad = {
        (0, 1): {},
        (0, 2): {},
        (1, 0): {},
    }
    values_constraints_directional_keypad = {
        (0, 1): {},
        (0, 2): {},
        (1, 0): {},
    }
    constraint_sequences_directional_dict = {
        (0, 1): {},
        (0, 2): {},
        (1, 0): {},
    }
    # constraint for (1, 0)
    contraints_directional_keypad, results_constraints_directional_keypad, values_constraints_directional_keypad, constraint_sequences_directional_dict = create_constraints(  # noqa
        (1, 0),
        "^",
        contraints_directional_keypad,
        results_constraints_directional_keypad,
        values_constraints_directional_keypad,
        constraint_sequences_directional_dict,
        all_n_sequences_dict
    )

    # constraint at (0, 1)
    contraints_directional_keypad, results_constraints_directional_keypad, values_constraints_directional_keypad, constraint_sequences_directional_dict = create_constraints(  # noqa
        (0, 1),
        "<",
        contraints_directional_keypad,
        results_constraints_directional_keypad,
        values_constraints_directional_keypad,
        constraint_sequences_directional_dict,
        all_n_sequences_dict
    )

    # constraint at (0, 2)
    contraints_directional_keypad, results_constraints_directional_keypad, values_constraints_directional_keypad, constraint_sequences_directional_dict = create_constraints(  # noqa
        (0, 2),
        "<<",
        contraints_directional_keypad,
        results_constraints_directional_keypad,
        values_constraints_directional_keypad,
        constraint_sequences_directional_dict,
        all_n_sequences_dict
    )

    best_sequences_directional_constrained = {}
    for constraint in contraints_directional_keypad.keys():
        for move in results_constraints_directional_keypad[constraint].keys():
            argmin = np.argmin(results_constraints_directional_keypad[constraint][move])
            true_argmin = constraint_sequences_directional_dict[constraint][move][argmin]
            best_sequences_directional_constrained[move] = (
                all_n_sequences_dict[move][true_argmin],
                values_constraints_directional_keypad[constraint][move][argmin],
                results_constraints_directional_keypad[constraint][move][argmin]
            )

    def check_next_step(start_pos, move, chosen_sequence):
        position = start_pos
        new_sequence = ""
        for letter in chosen_sequence:
            original_position = position
            next_position = directional_keypad[letter]
            next_move = (next_position[0] - original_position[0], next_position[1] - original_position[1])
            if (original_position in contraints_directional_keypad) and (next_move in contraints_directional_keypad[original_position]):  # noqa
                new_sequence += best_sequences_directional_constrained[next_move][0]
            else:
                new_sequence += best_sequences[next_move][0]
            position = next_position
        return len(new_sequence)

    best_sequences_numerical_constrained = {}
    for constraint in contraints_numerical_keypad.keys():
        for move in results_constraints_numerical_keypad[constraint].keys():
            argmin = np.argmin(results_constraints_numerical_keypad[constraint][move])
            # sometimes min is ill defined, in that case, check the best at the third step
            array_1 = np.array(results_constraints_numerical_keypad[constraint][move])
            if sum(array_1 == min(array_1)) > 1:
                potential_argmins = np.where(array_1 == min(array_1))[0]
                next_values = []
                for potential_argmin in potential_argmins:
                    next_values.append(check_next_step(constraint, move, values_constraints_numerical_keypad[constraint][move][potential_argmin]))  # noqa
                # don't do it for the fourth step, doesn't seem to be needed for the input
                argmin = potential_argmins[np.argmin(next_values)]
            true_argmin = constraint_sequences_numerical_dict[constraint][move][argmin]
            best_sequences_numerical_constrained[move] = (
                all_n_sequences_dict[move][true_argmin],
                values_constraints_numerical_keypad[constraint][move][argmin],
                results_constraints_numerical_keypad[constraint][move][argmin]
            )

    # now that we have the best sequences with constraints, we can use them to build the best sequence
    # to the 13th directional keypad

    all_versions_sequences = {}
    all_versions_numerical_sequences_constraints = {}
    all_versions_directional_sequences_constraints = {}
    n_keypads = 13
    for i in range(n_keypads):
        print("creating best sequences, keypad", i)
        all_versions_sequences[i] = {}
        all_versions_numerical_sequences_constraints[i] = {}
        all_versions_directional_sequences_constraints[i] = {}
        if i == 0:
            for move in best_sequences.keys():
                all_versions_sequences[i][move] = best_sequences[move][0]
            for move in best_sequences_numerical_constrained.keys():
                all_versions_numerical_sequences_constraints[i][move] = best_sequences_numerical_constrained[move][0]
            for move in best_sequences_directional_constrained.keys():
                all_versions_directional_sequences_constraints[i][move] = best_sequences_directional_constrained[move][0]  # noqa
        else:
            position = directional_keypad["A"]
            for move in best_sequences.keys():
                for iletter, letter in enumerate(all_versions_sequences[i - 1][move]):
                    original_position = position
                    next_position = directional_keypad[letter]
                    next_move = (next_position[0] - original_position[0], next_position[1] - original_position[1])
                    if (original_position in contraints_directional_keypad) and (next_move in contraints_directional_keypad[original_position]):  # noqa
                        if move not in all_versions_sequences[i]:
                            all_versions_sequences[i][move] = best_sequences_directional_constrained[next_move][0]  # noqa
                        else:
                            all_versions_sequences[i][move] += best_sequences_directional_constrained[next_move][0]  # noqa
                    else:
                        if move not in all_versions_sequences[i]:
                            all_versions_sequences[i][move] = best_sequences[next_move][0]
                        else:
                            all_versions_sequences[i][move] += best_sequences[next_move][0]
                    position = next_position
            position = directional_keypad["A"]
            for move in best_sequences_numerical_constrained.keys():
                for iletter, letter in enumerate(all_versions_numerical_sequences_constraints[i - 1][move]):
                    original_position = position
                    next_position = directional_keypad[letter]
                    next_move = (next_position[0] - original_position[0], next_position[1] - original_position[1])
                    if (original_position in contraints_directional_keypad) and (next_move in contraints_directional_keypad[original_position]):  # noqa
                        if move not in all_versions_numerical_sequences_constraints[i]:
                            all_versions_numerical_sequences_constraints[i][move] = best_sequences_directional_constrained[next_move][0]  # noqa
                        else:
                            all_versions_numerical_sequences_constraints[i][move] += best_sequences_directional_constrained[next_move][0]  # noqa
                    else:
                        if move not in all_versions_numerical_sequences_constraints[i]:
                            all_versions_numerical_sequences_constraints[i][move] = best_sequences[next_move][0]
                        else:
                            all_versions_numerical_sequences_constraints[i][move] += best_sequences[next_move][0]
                    position = next_position
            position = directional_keypad["A"]
            for move in best_sequences_directional_constrained.keys():
                for iletter, letter in enumerate(all_versions_directional_sequences_constraints[i - 1][move]):
                    original_position = position
                    next_position = directional_keypad[letter]
                    next_move = (next_position[0] - original_position[0], next_position[1] - original_position[1])
                    if (original_position in contraints_directional_keypad) and (next_move in contraints_directional_keypad[original_position]):  # noqa
                        if move not in all_versions_directional_sequences_constraints[i]:
                            all_versions_directional_sequences_constraints[i][move] = best_sequences_directional_constrained[next_move][0]  # noqa
                        else:
                            all_versions_directional_sequences_constraints[i][move] += best_sequences_directional_constrained[next_move][0]  # noqa
                    else:
                        if move not in all_versions_directional_sequences_constraints[i]:
                            all_versions_directional_sequences_constraints[i][move] = best_sequences[next_move][0]
                        else:
                            all_versions_directional_sequences_constraints[i][move] += best_sequences[next_move][0]
                    position = next_position

    # now we have the best sequences for the 13th keypad, we can use them to find the best sequence for the 26th keypad
    all_code_sequences = []
    steps_to_use = [12, 12]
    tot_len = {}
    for code in lines_array:
        tot_len_code = 0
        all_sequences = {}
        all_sequences[0] = code
        for istep, step in enumerate(steps_to_use):
            if istep == 0:
                keypad = numerical_keypad
                key_to_get = 0
            else:
                keypad = directional_keypad
                key_to_get = istep
            position = keypad["A"]
            for letter in all_sequences[key_to_get]:
                original_position = position
                next_position = keypad[letter]
                next_move = (next_position[0] - original_position[0], next_position[1] - original_position[1])
                if istep == 0:
                    if (original_position in contraints_numerical_keypad) and (next_move in contraints_numerical_keypad[original_position]):  # noqa
                        if (key_to_get + 1) not in all_sequences:
                            all_sequences[key_to_get + 1] = all_versions_numerical_sequences_constraints[step][next_move]  # noqa
                        else:
                            all_sequences[key_to_get + 1] += all_versions_numerical_sequences_constraints[step][next_move]  # noqa
                    else:
                        if (key_to_get + 1) not in all_sequences:
                            all_sequences[key_to_get + 1] = all_versions_sequences[step][next_move]
                        else:
                            all_sequences[key_to_get + 1] += all_versions_sequences[step][next_move]
                elif istep == len(steps_to_use) - 1:
                    if (original_position in contraints_directional_keypad) and (next_move in contraints_directional_keypad[original_position]):  # noqa
                        tot_len_code += len(all_versions_directional_sequences_constraints[step][next_move])
                    else:
                        tot_len_code += len(all_versions_sequences[step][next_move])
                else:
                    if (original_position in contraints_directional_keypad) and (next_move in contraints_directional_keypad[original_position]):  # noqa
                        if (key_to_get + 1) not in all_sequences:
                            all_sequences[key_to_get + 1] = all_versions_directional_sequences_constraints[step][next_move]  # noqa
                        else:
                            all_sequences[key_to_get + 1] += all_versions_directional_sequences_constraints[step][next_move]  # noqa
                    else:
                        if (key_to_get + 1) not in all_sequences:
                            all_sequences[key_to_get + 1] = all_versions_sequences[step][next_move]
                        else:
                            all_sequences[key_to_get + 1] += all_versions_sequences[step][next_move]
                position = next_position
        tot_len[code] = tot_len_code
        all_code_sequences.append(all_sequences)

    if len(steps_to_use) == 1:
        num_part_codes = [int(line[:-1]) for line in lines_array]
        results = [num_part_codes[i] * len(all_code_sequences[i][1]) for i in range(len(lines_array))]
        print(f"Part 2: {sum(results)}")
    else:
        num_part_codes = [int(line[:-1]) for line in lines_array]
        results = [num_part_codes[i] * tot_len[lines_array[i]] for i in range(len(lines_array))]
        print(f"Part 2: {sum(results)}")


if __name__ == "__main__":
    main()
