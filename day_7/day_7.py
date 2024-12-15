# whatever imports you need
from itertools import product


# create example code:
example = [
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 1813",
    "292: 11 6 16 20",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_7.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    # part 1
    equation_dict = {}
    for iline, line in enumerate(lines_array):
        equation = line.split(":")
        equation_dict[int(equation[0])] = list(equation[1].split())

    operators = ["+", "*"]
    correct_results = []
    for key, value in equation_dict.items():
        operator_combinations = list(product(operators, repeat=len(value) - 1))
        for operator_combination in operator_combinations:
            test = ""
            for i in range(len(value) - 1):
                test += "("
            for ival, val in enumerate(value):
                test += val
                if ival > 0:
                    test += ")"
                if ival < len(value) - 1:
                    test += operator_combination[ival]
            if key == eval(test):
                correct_results.append(key)
                break
    print("the sum of the correct results is", sum(correct_results))

    # part 2

    operators = ["+", "*", "||"]
    correct_results_2 = []
    for key, value in equation_dict.items():
        operator_combinations = list(product(operators, repeat=len(value) - 1))
        for operator_combination in operator_combinations:
            for ival, val in enumerate(value):
                if ival == 0:
                    test_result = val
                if ival > 0:
                    test_result = str(test_result)
                    if operator_combination[ival - 1] == "||":
                        test_result = int(test_result + val)
                    else:
                        test_result = eval(test_result + operator_combination[ival - 1] + val)
            if key == test_result:
                correct_results_2.append(key)
                break
    print("the sum of the correct results is", sum(correct_results_2))


if __name__ == "__main__":
    main()
