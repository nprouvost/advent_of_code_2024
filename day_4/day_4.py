# whatever imports you need
import numpy as np

# create example code:
example = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def check_right(line: str, i: int, j: int, word: str):
    word_len = len(word)
    if j < len(line) - (word_len - 1):
        if "".join(line[j:j + word_len]) == word:
            return 1
    return 0


def check_left(line: str, i: int, j: int, word: str):
    word_len = len(word)
    if j > word_len - 2:
        if "".join(line[j - (word_len - 1):j + 1]) == word[::-1]:
            return 1
    return 0


def check_down(lines_array, i, j, word):
    word_len = len(word)
    if i < len(lines_array) - (word_len - 1):
        if "".join(lines_array[i:i + word_len, j]) == word:
            return 1
    return 0


def check_up(lines_array, i, j, word):
    word_len = len(word)
    if i > word_len - 2:
        if "".join(lines_array[i - (word_len - 1):i + 1, j]) == word[::-1]:
            return 1
    return 0


def check_diagonal_right_down(lines_array: list, i: int, j: int, word: str):
    word_len = len(word)
    if i < len(lines_array) - (word_len - 1) and j < len(lines_array[0]) - (word_len - 1):
        if (
            "".join([lines_array[i + n][j + n] for n in range(word_len)]) == word
        ):
            return 1
    return 0


def check_diagonal_left_down(lines_array: list, i: int, j: int, word: str):
    word_len = len(word)
    if i < len(lines_array) - (word_len - 1) and j > (word_len - 2):
        if (
            "".join([lines_array[i + n][j - n] for n in range(word_len)]) == word
        ):
            return 1
    return 0


def check_diagonal_right_up(lines_array: list, i: int, j: int, word: str):
    word_len = len(word)
    if i > (word_len - 2) and j < len(lines_array[0]) - (word_len - 1):
        if (
            "".join([lines_array[i - n][j + n] for n in range(word_len)]) == word
        ):
            return 1
    return 0


def check_diagonal_left_up(lines_array: list, i: int, j: int, word: str):
    word_len = len(word)
    if i > (word_len - 2) and j > (word_len - 2):
        if ("".join([lines_array[i - n][j - n] for n in range(word_len)])) == word:
            return 1
    return 0


def check_cross(lines_array: list, i: int, j: int, word: str):
    word_len = len(word)
    assert word_len % 2 == 1
    cross_arm_len = int((word_len - 1) / 2)
    if (
        i < len(lines_array) - (word_len - 2) and
        i > (word_len - 3) and
        j > (word_len - 3) and
        j < len(lines_array[0]) - (word_len - 2)
    ):
        if cross_arm_len == 1:
            if (
                (
                    "".join([lines_array[i - 1][j - 1], lines_array[i][j], lines_array[i + 1][j + 1]]) == word or
                    "".join([lines_array[i - 1][j - 1], lines_array[i][j], lines_array[i + 1][j + 1]]) == word[::-1]
                ) and (
                    "".join([lines_array[i - 1][j + 1], lines_array[i][j], lines_array[i + 1][j - 1]]) == word or
                    "".join([lines_array[i - 1][j + 1], lines_array[i][j], lines_array[i + 1][j - 1]]) == word[::-1]
                )
            ):
                return 1
        elif (
            (
                "".join(
                    [lines_array[i - n][j - n] for n in range(cross_arm_len)] +
                    lines_array[i][j] +
                    [lines_array[i + n][j + n] for n in range(cross_arm_len)]
                ) == word or
                "".join(
                    [lines_array[i - n][j - n] for n in range(cross_arm_len)] +
                    lines_array[i][j] +
                    [lines_array[i + n][j + n] for n in range(cross_arm_len)]
                ) == word[::-1]
            ) and (
                "".join(
                    [lines_array[i - n][j + n] for n in range(cross_arm_len)] +
                    lines_array[i][j] +
                    [lines_array[i + n][j - n] for n in range(cross_arm_len)]
                ) == word or
                "".join(
                    [lines_array[i - n][j + n] for n in range(cross_arm_len)] +
                    lines_array[i][j] +
                    [lines_array[i + n][j - n] for n in range(cross_arm_len)]
                ) == word[::-1]
            )
        ):
            return 1
    return 0


def main():
    file_path = 'day_4.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    for i, line in enumerate(lines_array):
        lines_array[i] = list(line)

    lines_array = np.array(lines_array)

    # part 1
    word = "XMAS"
    sum_xmas_right = 0
    sum_xmas_left = 0
    sum_xmas_down = 0
    sum_xmas_up = 0
    sum_xmas_diagonal_right_down = 0
    sum_xmas_diagonal_left_down = 0
    sum_xmas_diagonal_right_up = 0
    sum_xmas_diagonal_left_up = 0
    for iline, line in enumerate(lines_array):
        for ichar, char in enumerate(line):
            if char == word[0]:
                sum_xmas_right += check_right(line, iline, ichar, word)
                sum_xmas_left += check_left(line, iline, ichar, word)
                sum_xmas_down += check_down(lines_array, iline, ichar, word)
                sum_xmas_up += check_up(lines_array, iline, ichar, word)
                sum_xmas_diagonal_right_down += check_diagonal_right_down(lines_array, iline, ichar, word)
                sum_xmas_diagonal_left_down += check_diagonal_left_down(lines_array, iline, ichar, word)
                sum_xmas_diagonal_right_up += check_diagonal_right_up(lines_array, iline, ichar, word)
                sum_xmas_diagonal_left_up += check_diagonal_left_up(lines_array, iline, ichar, word)
    print(
        "the number of XMAS in the array is",
        (
            sum_xmas_right + sum_xmas_left + sum_xmas_down + sum_xmas_up +
            sum_xmas_diagonal_right_down + sum_xmas_diagonal_left_down +
            sum_xmas_diagonal_right_up + sum_xmas_diagonal_left_up
        )
    )

    # part 2
    word2 = "MAS"
    sumx_mas = 0
    for iline, line in enumerate(lines_array):
        for ichar, char in enumerate(line):
            if char == word2[1]:
                sumx_mas += check_cross(lines_array, iline, ichar, word2)

    print("the number of MAS crosses in the array is", sumx_mas)


if __name__ == "__main__":
    main()
