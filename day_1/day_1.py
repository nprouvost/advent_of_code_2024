# whatever imports you need
import numpy as np

# create example code:
example = [
    "3   4",
    "4   3",
    "2   5",
    "1   3",
    "3   9",
    "3   3",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_1.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    # part 1
    list_1 = []
    list_2 = []
    for line in lines_array:
        list_numbers = line.split()
        number1 = int(list_numbers[0])
        number2 = int(list_numbers[-1])
        list_1.append(number1)
        list_2.append(number2)
    array_1 = np.array(list_1)
    array_2 = np.array(list_2)
    array_1 = np.sort(array_1)
    array_2 = np.sort(array_2)
    distances = np.abs(array_1 - array_2)
    # print(distances)
    print("the sum of distances is", np.sum(distances))

    # part 2
    unique_counter_1 = np.unique(array_1, return_counts=True)
    unique_counter_2 = np.unique(array_2, return_counts=True)
    similarity_count = 0
    for inumber, number in enumerate(unique_counter_1[0]):
        if number in unique_counter_2[0]:
            similarity_count += (
                number *
                unique_counter_1[1][inumber] *
                unique_counter_2[1][np.where(unique_counter_2[0] == number)][0]
            )
    print("the sum of similarities is", similarity_count)


if __name__ == "__main__":
    main()
