# whatever imports you need
import numpy as np
import functools


# create example code:
example = [
    "0 1 10 99 999",
]

example2 = [
    "125 17",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_11.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example2
    # lines_array = example

    stones = lines_array[0].split()
    stones = [int(stone) for stone in stones]
    stones = np.array(stones)

    # # part 1
    # # brute force solution
    # for i in range(0, 25):
    #     new_stones = []
    #     for stone in stones:
    #         if stone == 0:
    #             new_stones.append(1)
    #         elif len(str(stone)) % 2 == 0:
    #             half = len(str(stone)) // 2
    #             new_stones.append(int(str(stone)[:half]))
    #             new_stones.append(int(str(stone)[half:]))
    #         else:
    #             new_stones.append(stone * 2024)
    #     stones = np.array(new_stones)
    # print("after blinking 25 times", len(stones))

    # vectorized solution
    for i in range(0, 25):
        zeros = np.where(stones == 0)[0]
        new_stones_0 = [1] * len(zeros)
        stones_copy = stones.copy()
        digits_checks = 0
        all_even_digits = np.zeros(len(stones), dtype=bool)
        ndigits = {}
        new_stones_1 = []
        new_stones_2 = []
        while np.any(stones_copy // 1 != 0):
            digits_checks += 1
            if digits_checks % 2 == 0:
                mask_step = (stones_copy // 10 == 0) & (stones_copy // 1 != 0)
                all_even_digits = all_even_digits | mask_step
                ndigits[digits_checks] = np.array(range(len(stones)))[mask_step]
                half_digit_checks = digits_checks // 2
                new_stones_1 += list(stones[mask_step] // (10 ** half_digit_checks))
                new_stones_2 += list(stones[mask_step] % (10 ** half_digit_checks))
            stones_copy = stones_copy // 10
        rest = list(set(range(len(stones))) - set(list(zeros)) - set(np.array(range(len(stones)))[all_even_digits]))
        new_stones_3 = stones[rest] * 2024
        new_stones = np.array(new_stones_0 + list(new_stones_1) + list(new_stones_2) + list(new_stones_3))
        stones = new_stones
    print("blinking", i + 1, "len(stones)", len(stones))

    # part 2
    stones = lines_array[0].split()
    stones = [int(stone) for stone in stones]
    stones = np.array(stones)
    # cached solution
    @functools.cache
    def num_stones(stone, n):
        if n == 0:
            return 1
        if stone == 0:
            return num_stones(1, n - 1)
        if len(str(stone)) % 2 == 0:
            half = len(str(stone)) // 2
            return num_stones(int(str(stone)[:half]), n - 1) + num_stones(int(str(stone)[half:]), n - 1)
        return num_stones(stone * 2024, n - 1)

    tot_num_stones = 0
    for stone in stones:
        add_num = num_stones(stone, 75)
        tot_num_stones += add_num
    print("after blinking 75 times", tot_num_stones)


if __name__ == "__main__":
    main()
