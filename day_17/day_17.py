# whatever imports you need
import numpy as np

# create example code:
example = [
    "Register A: 729",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 0,1,5,4,3,0",
]

example2 = [
    "Register A: 2024",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 0,3,5,4,3,0",
]


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def value_from_operand(operand, registers):
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers["Register A"]
    elif operand == 5:
        return registers["Register B"]
    elif operand == 6:
        return registers["Register C"]
    else:
        raise ValueError("Invalid operand")


def execute_instruction(instruction_pointer, registers, instructions):
    output = []
    if instructions[instruction_pointer] == 0:
        registers["Register A"] = int(
            registers["Register A"] /
            (2**value_from_operand(instructions[instruction_pointer + 1], registers))
        )
        instruction_pointer = instruction_pointer + 2

    elif instructions[instruction_pointer] == 1:
        registers["Register B"] = registers["Register B"] ^ instructions[instruction_pointer + 1]
        instruction_pointer = instruction_pointer + 2

    elif instructions[instruction_pointer] == 2:
        registers["Register B"] = value_from_operand(instructions[instruction_pointer + 1], registers) % 8
        instruction_pointer = instruction_pointer + 2

    elif instructions[instruction_pointer] == 3:
        if registers["Register A"] == 0:
            instruction_pointer = instruction_pointer + 2
        else:
            instruction_pointer = instructions[instruction_pointer + 1]

    elif instructions[instruction_pointer] == 4:
        registers["Register B"] = registers["Register B"] ^ registers["Register C"]
        instruction_pointer = instruction_pointer + 2

    elif instructions[instruction_pointer] == 5:
        output.append(value_from_operand(instructions[instruction_pointer + 1], registers) % 8)
        instruction_pointer = instruction_pointer + 2

    elif instructions[instruction_pointer] == 6:
        registers["Register B"] = int(
            registers["Register A"] /
            (2**value_from_operand(instructions[instruction_pointer + 1], registers))
        )
        instruction_pointer = instruction_pointer + 2

    elif instructions[instruction_pointer] == 7:
        registers["Register C"] = int(
            registers["Register A"] /
            (2**value_from_operand(instructions[instruction_pointer + 1], registers))
        )
        instruction_pointer = instruction_pointer + 2

    else:
        raise ValueError("Invalid instruction")

    return instruction_pointer, registers, instructions, output


def main():
    file_path = 'day_17.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example2

    registers = {}
    for line in lines_array:
        if "Register" in line:
            register = line.split(":")
            registers[register[0]] = int(register[1])
        elif "Program" in line:
            program = list(map(int, line.split(":")[1].split(",")))

    # part 1
    total_output = []
    instruction_pointer = 0
    while instruction_pointer < len(program):
        instruction_pointer, registers, program, output = execute_instruction(instruction_pointer, registers, program)
        total_output += output
    print("the output is", total_output)

    # part 2
    # reset values
    registers = {}
    for line in lines_array:
        if "Register" in line:
            register = line.split(":")
            registers[register[0]] = int(register[1])
        elif "Program" in line:
            program = list(map(int, line.split(":")[1].split(",")))

    # observation: in the programm, A is only divided by 8 each step, so to get 16 numbers,
    # A needs to be between 2**45 and 2**48.
    # second observation: trying 2**45 as a starting point, the last two bits are 3,0 as we want
    # third observation:
    # each bit flips following the same pattern, just one after the other, in powers of 8 steps
    # so we can find the change in value of the last bits one after the other by simply taking the
    # correct power of 8 and then go recursively backward until we reach the first bit. If the
    # desired number does not appear (can happen, e.g.the first sequence is 1,0,1,3,5,4,7,6 and does not contain 2)
    # we can simply go to the next bit and repeat the process until it works

    new_value = 2**45
    registers["Register A"] = new_value
    total_output = []
    instruction_pointer = 0
    while instruction_pointer < len(program):
        instruction_pointer, registers, program, output = execute_instruction(instruction_pointer, registers, program)
        total_output += output

    program_array = np.array(program)

    while total_output != program:
        total_output_array = np.array(total_output)

        next_bit_to_flip = max(np.array(list(range(len(program_array))))[total_output_array != program_array])
        next_bit_to_flip = int(next_bit_to_flip)

        new_value = new_value + 8**next_bit_to_flip

        total_output = []
        registers["Register A"] = new_value
        registers["Register B"] = 0
        registers["Register C"] = 0
        instruction_pointer = 0
        while instruction_pointer < len(program):
            instruction_pointer, registers, program, output = execute_instruction(instruction_pointer, registers, program)
            total_output += output

        if new_value > 2**45 + 2**42:
            print("too far")
            break

    print("the output is", total_output)
    print("the last value inputed in register A is", new_value)


if __name__ == "__main__":
    main()
