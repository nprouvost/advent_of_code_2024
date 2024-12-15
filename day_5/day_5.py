# whatever imports you need

# create example code:
example = [
    "47|53",
    "97|13",
    "97|61",
    "97|47",
    "75|29",
    "61|13",
    "75|53",
    "29|13",
    "97|29",
    "53|29",
    "61|53",
    "97|53",
    "61|29",
    "47|13",
    "75|47",
    "97|75",
    "47|61",
    "75|61",
    "47|29",
    "75|13",
    "53|13",
    "",
    "75,47,61,53,29",
    "97,61,53,29,13",
    "75,29,13",
    "75,97,47,61,53",
    "61,13,29",
    "97,13,75,29,47",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def reorder_update(update, rules_dict):
    for iprint, print_ in enumerate(update[::-1]):
        if iprint == len(update) - 1:
            reordered_update = update
        elif print_ in rules_dict.keys():
            if bool(set(rules_dict[print_]) & set(update[::-1][iprint + 1:])):
                overlap = set(rules_dict[print_]) & set(update[::-1][iprint + 1:])
                for i, remaining_print in enumerate(update):
                    if remaining_print in overlap:
                        first_position = i
                        break
                reordered_update = (
                    update[:first_position] +
                    [print_] +
                    update[first_position:len(update) - iprint - 1] +
                    update[len(update) - iprint:]
                )
                # because recursion is fun
                reordered_update = reorder_update(reordered_update, rules_dict)
                break
    return reordered_update


def main():
    file_path = 'day_5.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    rules_array = []
    updates_list = []
    switch = False
    for line in lines_array:
        if line == "":
            switch = True
            continue
        if not switch:
            rules_array.append(line)
        else:
            updates_list.append(line)

    updates_array = []
    for update in updates_list:
        update_list = update.split(",")
        for i, print_ in enumerate(update_list):
            update_list[i] = int(print_)
        updates_array.append(update_list)

    rules_dict = {}
    for rule in rules_array:
        rule_list = rule.split("|")
        for i, print_ in enumerate(rule_list):
            rule_list[i] = int(print_)
        if rule_list[0] not in rules_dict.keys():
            rules_dict[rule_list[0]] = [rule_list[1]]
        else:
            rules_dict[rule_list[0]].append(rule_list[1])

    # part 1
    good_updates = []
    middle_prints = []
    for update in updates_array:
        # check backwards if the previous prints are in the rules for any print
        # if not, add the update to the good updates
        for iprint, print_ in enumerate(update[::-1]):
            if iprint == len(update) - 1:
                good_updates.append(update)
                assert len(update) % 2 == 1
                middle_prints.append(update[len(update) // 2])
            if print_ in rules_dict.keys():
                # check intersection of the sets
                if bool(set(rules_dict[print_]) & set(update[::-1][iprint + 1:])):
                    break

    print("sum of middle prints", sum(middle_prints))

    # part 2
    bad_updates = []
    bad_middle_prints = []
    for update in updates_array:
        if update not in good_updates:
            reordered_update = reorder_update(update, rules_dict)
            bad_updates.append(reordered_update)
            # assert len(reordered_update) % 2 == 1
            bad_middle_prints.append(reordered_update[len(reordered_update) // 2])
    print("sum of bad middle prints", sum(bad_middle_prints))


if __name__ == "__main__":
    main()
