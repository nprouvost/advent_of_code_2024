# whatever imports you need
import numpy as np


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_25.txt'
    lines_array = read_file_to_list(file_path)

    i = 0
    keys = []
    locks = []
    is_key = False
    is_lock = False
    for line in lines_array:
        if line == "":
            continue
        else:
            i = i % 7
            if i == 0:
                is_lock = False
                is_key = False
                if line == "#####":
                    is_lock = True
                    lock = []
                else:
                    is_key = True
                    key = []

            if is_key:
                key.append(list(line))
                if i == 6:
                    keys.append(key)
            elif is_lock:
                lock.append(list(line))
                if i == 6:
                    locks.append(lock)
            else:
                raise ValueError("line is not part of a key or a lock")
            i += 1

    keys = np.array(keys)
    locks = np.array(locks)
    locks_len = []
    for lock in locks:
        locks_len.append([sum(lock[:, i] == "#") for i in range(len(lock[0]))])

    keys_len = []
    for key in keys:
        keys_len.append([sum(key[:, i] == "#") for i in range(len(key[0]))])

    keys_len = np.array(keys_len)
    locks_len = np.array(locks_len)

    unique_pairs = set()
    for ikey, key_len in enumerate(keys_len):
        for ilock, lock_len in enumerate(locks_len):
            if np.all((key_len + lock_len) < 8):
                unique_pairs.add((ikey, ilock))
    print("Part 1:", len(unique_pairs))


if __name__ == "__main__":
    main()
