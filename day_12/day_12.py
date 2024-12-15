# whatever imports you need
import numpy as np


# create example code:
example = [
    "AAAA",
    "BBCD",
    "BBCC",
    "EEEC",
]

example2 = [
    "OOOOO",
    "OXOXO",
    "OOOOO",
    "OXOXO",
    "OOOOO",
]

example3 = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE",
]

example4 = [
    "EEEEE",
    "EXXXX",
    "EEEEE",
    "EXXXX",
    "EEEEE",
]

example5 = [
    "AAAAAA",
    "AAABBA",
    "AAABBA",
    "ABBAAA",
    "ABBAAA",
    "AAAAAA",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_12.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example
    # lines_array = example2
    # lines_array = example3
    # lines_array = example4
    # lines_array = example5

    garden = np.array([list(line) for line in lines_array])

    # part 1
    # build regions and calculate area and perimeter
    regions = []
    used = set()
    for i, line in enumerate(garden):
        for j, char in enumerate(line):
            if (i, j) not in used:
                region_type = char
                region = [(i, j)]
                positions = [(i, j)]
                used.add(positions[0])
                while positions:
                    new_positions = []
                    for position in positions:
                        for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            if (
                                0 <= position[0] + dy < len(garden) and
                                0 <= position[1] + dx < len(garden[0]) and
                                garden[position[0] + dy][position[1] + dx] == region_type
                            ):
                                if (position[0] + dy, position[1] + dx) not in used:
                                    region.append((position[0] + dy, position[1] + dx))
                                    new_positions.append((position[0] + dy, position[1] + dx))
                                    used.add((position[0] + dy, position[1] + dx))
                    positions = new_positions
                regions.append(region)
    areas = [len(region) for region in regions]

    perimeters = []
    for region in regions:
        perimeter = 0
        for position in region:
            for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if (
                    (position[0] + dy, position[1] + dx) not in region
                ):
                    perimeter += 1
        perimeters.append(perimeter)

    print("cost part 1", sum([area * perimeter for area, perimeter in zip(areas, perimeters)]))

    # part 2
    # reorder regions in case they are not sorted due to the path taken in part 1
    regions = [sorted(region) for region in regions]

    # calculate sides
    sides = []
    used = set()
    for iregion, region in enumerate(regions):
        side = 0
        perimeter_positions = {"up": [], "down": [], "left": [], "right": []}
        for position in region:
            # if iregion == 0:
            #     from IPython import embed; embed()
            if (position[0] + 1, position[1]) not in region:
                no_adjacent = True
                for dx in [-1, 1]:
                    if (position[0], position[1] + dx) in perimeter_positions["down"]:
                        no_adjacent = False
                if no_adjacent:
                    side += 1
                perimeter_positions["down"].append(position)
            if (position[0] - 1, position[1]) not in region:
                no_adjacent = True
                for dx in [-1, 1]:
                    if (position[0], position[1] + dx) in perimeter_positions["up"]:
                        no_adjacent = False
                if no_adjacent:
                    side += 1
                perimeter_positions["up"].append(position)
            if (position[0], position[1] + 1) not in region:
                no_adjacent = True
                for dy in [-1, 1]:
                    if (position[0] + dy, position[1]) in perimeter_positions["right"]:
                        no_adjacent = False
                if no_adjacent:
                    side += 1
                perimeter_positions["right"].append(position)
            if (position[0], position[1] - 1) not in region:
                no_adjacent = True
                for dy in [-1, 1]:
                    if (position[0] + dy, position[1]) in perimeter_positions["left"]:
                        no_adjacent = False
                if no_adjacent:
                    side += 1
                perimeter_positions["left"].append(position)
        sides.append(side)
    print("cost part 2", sum([area * side for area, side in zip(areas, sides)]))


if __name__ == "__main__":
    main()
