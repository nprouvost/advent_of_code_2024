# whatever imports you need


# create example code:
example = [
    "1",
    "10",
    "100",
    "2024",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def create_secret_number(secret_number):
    secret_number_original = secret_number
    secret_number = secret_number * 64
    secret_number = secret_number ^ secret_number_original
    secret_number = secret_number % 16777216

    secret_number_original = secret_number
    secret_number = int(secret_number / 32)
    secret_number = secret_number ^ secret_number_original
    secret_number = secret_number % 16777216

    secret_number_original = secret_number
    secret_number = secret_number * 2048
    secret_number = secret_number ^ secret_number_original
    secret_number = secret_number % 16777216

    return secret_number


def main():
    file_path = 'day_22.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    sequences_dict = {}
    secret_numbers = [int(line) for line in lines_array]
    list_of_secret_numbers = []
    for number in secret_numbers:
        list_of_changes = []
        dict_of_changes = {}
        for i in range(2000):
            original_price = int(str(number)[-1])
            number = create_secret_number(number)
            price = int(str(number)[-1])
            list_of_changes.append(price - original_price)
            if i > 2:
                if tuple(list_of_changes[-4:]) not in dict_of_changes:
                    dict_of_changes[tuple(list_of_changes[-4:])] = price
                    if tuple(list_of_changes[-4:]) not in sequences_dict:
                        sequences_dict[tuple(list_of_changes[-4:])] = [price]
                    else:
                        sequences_dict[tuple(list_of_changes[-4:])].append(price)
        list_of_secret_numbers.append(number)

    print(f"Part 1: {sum(list_of_secret_numbers)}")

    max_sequence = 0
    for key, value in sequences_dict.items():
        if sum(value) > max_sequence:
            max_sequence = sum(value)
            max_sequence_key = key
    print(f"Part 2: {max_sequence, max_sequence_key}")


if __name__ == "__main__":
    main()
