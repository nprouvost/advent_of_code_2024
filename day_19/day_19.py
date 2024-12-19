# whatever imports you need
import numpy as np
import functools

# create example code:
example = [
    "r, wr, b, g, bwu, rb, gb, br",
    "",
    "brwrr",
    "bggr",
    "gbbr",
    "rrbgbr",
    "ubwu",
    "bwurrg",
    "brgr",
    "bbrgwb",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_19.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    patterns = lines_array[0].split(", ")

    designs = lines_array[2:] if lines_array[1] == "" else lines_array[1:]

    # get the max number of letters in a pattern
    max_length = max([len(pattern) for pattern in patterns])

    # part 1
    designs_possible = []
    for design in designs:
        positions = {0}
        positions_array = np.array(list(positions))
        while np.all(positions_array < len(design)):
            new_positions = set()
            for position in positions:
                for nletters in range(1, max_length + 1):
                    if design[position:position + nletters] in patterns:
                        new_positions.add(position + nletters)
            if len(new_positions) == 0:
                break
            positions = new_positions
        positions_array = np.array(list(positions))
        if np.any(positions_array >= len(design)):
            designs_possible.append(design)
        # else:
        #     print(design, "not possible")
    print(f"Part 1: {len(designs_possible)}")

    # part 2
    # well, caching makes it just so much faster than part 1 that it gets ridiculous to have
    # even written a loop... Anyway I'm letting the original solutions here

    @functools.cache
    def get_n_possibilities(design):
        n_possibilities = 0
        for nletters in range(1, max_length + 1):
            if nletters > len(design):
                continue
            if design[:nletters] in patterns:
                if nletters == len(design):
                    n_possibilities += 1
                else:
                    smaller_design = design[nletters:]
                    n_possibilities += get_n_possibilities(smaller_design)
        return n_possibilities

    n_possibilities_design = []
    for idesign, design in enumerate(designs):
        n_possibilities_design.append(get_n_possibilities(design))

    print(f"Part 2: {sum(n_possibilities_design)}")


if __name__ == "__main__":
    main()
