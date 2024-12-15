# whatever imports you need
import regex as re
import numpy as np

# create example code:
example = ["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]
example_2 = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def find_multiplication(line: str):
    # find all the multiplication operations
    return re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)


def find_multiplication_matches_start(line: str):
    # find all the matches of the multiplication operations and return their start positions
    return [m.start() for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", line)]


def main():
    file_path = 'day_3.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example_2

    # part 1
    list_all_mul = []
    for line in lines_array:
        list_line_multiplications = find_multiplication(line)
        for tuple in list_line_multiplications:
            int1 = int(tuple[0])
            int2 = int(tuple[1])
            list_all_mul.append(int1 * int2)
    print("the sum of all multiplications is", sum(list_all_mul))

    # part 2
    big_string = "".join(lines_array)
    multiplication_start = find_multiplication_matches_start(big_string)
    do_matches = [m.start() for m in re.finditer(r"do\(\)", big_string)]
    dont_matches = [m.start() for m in re.finditer(r"don't\(\)", big_string)]

    correct_multiplications = []
    assert len(multiplication_start) == len(list_all_mul)
    for imul, start in enumerate(multiplication_start):
        if dont_matches[0] > start:
            correct_multiplications.append(list_all_mul[imul])
        elif do_matches[0] > start:
            continue
        else:
            dont_matches_arr = np.array(dont_matches)
            do_matches_arr = np.array(do_matches)
            dont_diff = start - dont_matches_arr
            do_diff = start - do_matches_arr
            if do_diff[do_diff > 0].min() < dont_diff[dont_diff > 0].min():
                correct_multiplications.append(list_all_mul[imul])

    # print(correct_multiplications)
    print("the sum of all correct multiplications is", sum(correct_multiplications))


if __name__ == "__main__":
    main()
