# whatever imports you need
import numpy as np

from dataclasses import dataclass


# create example code:
example = [
    "x00: 1",
    "x01: 1",
    "x02: 1",
    "y00: 0",
    "y01: 1",
    "y02: 0",
    "",
    "x00 AND y00 -> z00",
    "x01 XOR y01 -> z01",
    "x02 OR y02 -> z02",
]

example2 = [
    "x00: 1",
    "x01: 0",
    "x02: 1",
    "x03: 1",
    "x04: 0",
    "y00: 1",
    "y01: 1",
    "y02: 1",
    "y03: 1",
    "y04: 1",
    "",
    "ntg XOR fgs -> mjb",
    "y02 OR x01 -> tnw",
    "kwq OR kpj -> z05",
    "x00 OR x03 -> fst",
    "tgd XOR rvg -> z01",
    "vdt OR tnw -> bfw",
    "bfw AND frj -> z10",
    "ffh OR nrd -> bqk",
    "y00 AND y03 -> djm",
    "y03 OR y00 -> psh",
    "bqk OR frj -> z08",
    "tnw OR fst -> frj",
    "gnj AND tgd -> z11",
    "bfw XOR mjb -> z00",
    "x03 OR x00 -> vdt",
    "gnj AND wpb -> z02",
    "x04 AND y00 -> kjc",
    "djm OR pbm -> qhw",
    "nrd AND vdt -> hwm",
    "kjc AND fst -> rvg",
    "y04 OR y02 -> fgs",
    "y01 AND x02 -> pbm",
    "ntg OR kjc -> kwq",
    "psh XOR fgs -> tgd",
    "qhw XOR tgd -> z09",
    "pbm OR djm -> kpj",
    "x03 XOR y03 -> ffh",
    "x00 XOR y04 -> ntg",
    "bfw OR bqk -> z06",
    "nrd XOR fgs -> wpb",
    "frj XOR qhw -> z04",
    "bqk OR frj -> z07",
    "y03 OR x01 -> nrd",
    "hwm AND bqk -> z03",
    "tgd XOR rvg -> z12",
    "tnw OR pbm -> gnj",
]

example3 = [
    "x00: 0",
    "x01: 1",
    "x02: 0",
    "x03: 1",
    "x04: 0",
    "x05: 1",
    "y00: 0",
    "y01: 0",
    "y02: 1",
    "y03: 1",
    "y04: 0",
    "y05: 1",
    "",
    "x00 AND y00 -> z05",
    "x01 AND y01 -> z02",
    "x02 AND y02 -> z01",
    "x03 AND y03 -> z03",
    "x04 AND y04 -> z04",
    "x05 AND y05 -> z00",
]


@dataclass
class Gate:
    id: int
    input_1: str
    input_2: str
    operation: str
    output: str


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_24.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example
    # lines_array = example2
    # lines_array = example3

    dict_operations = {
        'AND': np.bitwise_and,
        'OR': np.bitwise_or,
        'XOR': np.bitwise_xor,
        # 'NOT': np.bitwise_not,
        # 'LSHIFT': np.left_shift,
        # 'RSHIFT': np.right_shift,
    }

    inputs = {}
    gates = []
    i = 0
    for line in lines_array:
        if line == "":
            continue
        if ("AND" in line) or ("OR" in line) or ("XOR" in line):
            gate = Gate(id=i, input_1='', input_2='', operation='', output='')
            gate.input_1 = line.split()[0]
            gate.input_2 = line.split()[2]
            gate.operation = line.split()[1]
            gate.output = line.split()[4]
            gates.append(gate)
            i += 1
        else:
            key, value = line.split(': ')
            inputs[key] = bool(int(value))

    outputs = {}
    order_gates = []
    unused_gates = gates.copy()
    while len(unused_gates) > 0:
        for gate in unused_gates:
            used_gates = []
            if (gate.input_1 in inputs) and (gate.input_2 in inputs):
                inputs[gate.output] = dict_operations[gate.operation](inputs[gate.input_1], inputs[gate.input_2])
                outputs[gate.id] = inputs[gate.output]
                order_gates.append(gate)
                used_gates.append(gate)
        for gate in used_gates:
            unused_gates.remove(gate)

    # part 1
    list_z_wires = sorted([key for key in inputs.keys() if key.startswith('z')])[::-1]
    list_z_wires_result = [str(int(inputs[wire])) for wire in list_z_wires]
    binary_str = ''.join(list_z_wires_result)
    print("Part 1:", int(binary_str, 2))

    # part 2
    # addition between two numbers bitwise is XOR for the same bits
    # but need to add carry bit (the AND of the original bits), so need to XOR the carry bit
    # with the result of the addition of the two bits
    # and need to keep the AND of the carry bit of the first bit and the XOR of the second bit
    # to find the carry bit of the second bit by ORing it to the AND of the second bit inputs
    # Now we have the carry bit of the second bit, we can go on for the next bit...

    # since there is no NOT operation, we cannot build the circuit differently, therefore
    # the circuit must be built in the following way:

    # written as a sequence for first bit
    # a XOR b = c  (first bit)
    # a AND b = d  (carry bit)

    # second bit
    # e XOR f = g  (second bit without carry)
    # d XOR g = h  (second bit of the addition)
    # e AND f = i  (maybe carry bit of the second bit, using the input of the second bit)
    # g AND d = j  (maybe carry bit of the second bit, using the carry bit of the first bit)
    # i OR j = k  (carry bit of the second bit)

    # third bit and so on -> loop of second bit
    # ...

    def build_circuit(inputs_, gates_):
        all_used_gates = []
        wrong_wires = []
        gate_to_reconnect = {}
        unused_gates = gates_.copy()
        current_bit = "00"
        carry_bit_previous_bit = ""
        potential_used_gates = []
        for igate, gate in enumerate(unused_gates):
            used_gates = []
            if set([gate.input_1, gate.input_2]) == set((f"x{current_bit}", f"y{current_bit}")):
                if gate.operation == "XOR":
                    if gate.output != f"z{current_bit}":
                        wrong_wires.append(gate.output)
                        for jgate, gate2 in enumerate(unused_gates):
                            if gate2.output == f"z{current_bit}":
                                wrong_wires.append(gate2.output)
                                gate_to_reconnect[igate] = f"z{current_bit}"
                                gate_to_reconnect[jgate] = gate.output
                    used_gates.append(gate)
                elif gate.operation == "AND":
                    carry_bit_previous_bit = gate.output
                    potential_used_gates.append(gate)
        for to_reconnect in gate_to_reconnect.keys():
            unused_gates[to_reconnect].output = gate_to_reconnect[to_reconnect]
        for gate in used_gates:
            unused_gates.remove(gate)
        all_used_gates += used_gates
        while current_bit != "44":
            used_gates = []
            potential_used_gates = []
            gate_to_reconnect = {}

            XOR_new_bit_output = ""
            AND_new_bit_output = ""
            new_bit_real_output = ""
            AND_carry_bit_XOR_new_bit_output = ""
            new_carry_bit = ""

            current_bit = str(int(current_bit) + 1) if len(str(int(current_bit) + 1)) > 1 else "0" + str(int(current_bit) + 1)  # noqa
            for gate in unused_gates:
                if {gate.input_1, gate.input_2} == {f"x{current_bit}", f"y{current_bit}"}:
                    if gate.operation == "XOR":
                        XOR_new_bit_output = gate.output
                        potential_used_gates.append(gate)
                    elif gate.operation == "AND":
                        AND_new_bit_output = gate.output
                        potential_used_gates.append(gate)
            for igate, gate in enumerate(unused_gates):
                if {gate.input_1, gate.input_2} == {carry_bit_previous_bit, XOR_new_bit_output}:
                    # let's here ignore the case where carry_bit_previous_bit and XOR_new_bit_output
                    # are both inputs of a gate, but were both wrongly wired in last step
                    if gate.operation == "XOR":
                        new_bit_real_output = gate.output
                        if gate.output != f"z{current_bit}":
                            wrong_wires.append(gate.output)
                            for jgate, gate2 in enumerate(unused_gates):
                                if gate2.output == f"z{current_bit}":
                                    wrong_wires.append(gate2.output)
                                    gate_to_reconnect[igate] = f"z{current_bit}"
                                    gate_to_reconnect[jgate] = gate.output
                                    if carry_bit_previous_bit == gate_to_reconnect[igate]:
                                        carry_bit_previous_bit = gate.output
                        used_gates.append(gate)
                    if gate.operation == "AND":
                        AND_carry_bit_XOR_new_bit_output = gate.output
                        potential_used_gates.append(gate)
            if gate_to_reconnect:
                for to_reconnect in gate_to_reconnect.keys():
                    unused_gates[to_reconnect].output = gate_to_reconnect[to_reconnect]
                gate_to_reconnect = {}
            # handle cases where {carry_bit_previous_bit, XOR_new_bit_output} is not found
            if new_bit_real_output == "":
                # either carry_bit_previous_bit or XOR_new_bit_output was wrong or both
                # if carry_bit_previous_bit is wrong, we need to find the gate that has XOR_new_bit_output as input
                for igate, gate in enumerate(unused_gates):
                    # not 100% secure, there is still the case that two wires directly one after the other
                    # are wrongly wired, but let's ignore this case for now
                    if XOR_new_bit_output in {gate.input_1, gate.input_2}:
                        if gate.operation == "XOR" and gate.output == f"z{current_bit}":
                            for jgate, gate2 in enumerate(unused_gates):
                                if XOR_new_bit_output in {gate2.input_1, gate2.input_2} and gate2.operation == "AND":
                                    new_list = list({gate2.input_1, gate2.input_2})
                                    new_list.remove(XOR_new_bit_output)
                                    actual_carry_bit_previous_bit = new_list[0]
                                    for kgate, gate3 in enumerate(unused_gates):
                                        if gate3.output == carry_bit_previous_bit:
                                            wrong_wires.append(gate3.output)
                                            gate_to_reconnect[kgate] = actual_carry_bit_previous_bit
                                            used_gates.append(gate3)
                                            potential_used_gates.remove(gate3)
                                            for lgate, gate4 in enumerate(unused_gates):
                                                if gate4.output == actual_carry_bit_previous_bit:
                                                    wrong_wires.append(gate4.output)
                                                    gate_to_reconnect[lgate] = gate.output
                                    carry_bit_previous_bit = actual_carry_bit_previous_bit
                                    new_bit_real_output = gate.output
                # if XOR_new_bit_output is wrong, we need to find the gate that has carry_bit_previous_bit as input
                if new_bit_real_output == "":
                    for igate, gate in enumerate(unused_gates):
                        if carry_bit_previous_bit in {gate.input_1, gate.input_2}:
                            if gate.operation == "XOR" and gate.output == f"z{current_bit}":
                                for jgate, gate2 in enumerate(unused_gates):
                                    if carry_bit_previous_bit in {gate2.input_1, gate2.input_2} and gate2.operation == "AND":  # noqa
                                        new_list = list({gate2.input_1, gate2.input_2})
                                        new_list.remove(carry_bit_previous_bit)
                                        actual_XOR_new_bit_output = new_list[0]
                                        for kgate, gate3 in enumerate(unused_gates):
                                            if gate3.output == XOR_new_bit_output:
                                                wrong_wires.append(gate3.output)
                                                gate_to_reconnect[kgate] = actual_XOR_new_bit_output
                                                used_gates.append(gate3)
                                                potential_used_gates.remove(gate3)
                                                for lgate, gate4 in enumerate(unused_gates):
                                                    if gate4.output == actual_XOR_new_bit_output:
                                                        wrong_wires.append(gate4.output)
                                                        gate_to_reconnect[lgate] = gate.output
                                        XOR_new_bit_output = actual_XOR_new_bit_output
                                        new_bit_real_output = gate.output
                # we ignore the case where both are wrong, since it would very difficult to find the right gates

                for to_reconnect in gate_to_reconnect.keys():
                    unused_gates[to_reconnect].output = gate_to_reconnect[to_reconnect]
                gate_to_reconnect = {}
                # redo previous step with updated wires
                for igate, gate in enumerate(unused_gates):
                    if {gate.input_1, gate.input_2} == {carry_bit_previous_bit, XOR_new_bit_output}:
                        # let's here ignore the case where carry_bit_previous_bit and XOR_new_bit_output
                        # are both inputs of a gate, but were both wrongly wired in last step
                        if gate.operation == "XOR":
                            new_bit_real_output = gate.output
                            if gate.output != f"z{current_bit}":
                                wrong_wires.append(gate.output)
                                for jgate, gate2 in enumerate(unused_gates):
                                    if gate2.output == f"z{current_bit}":
                                        wrong_wires.append(gate2.output)
                                        gate_to_reconnect[igate] = f"z{current_bit}"
                                        gate_to_reconnect[jgate] = gate.output
                            used_gates.append(gate)
                        if gate.operation == "AND":
                            AND_carry_bit_XOR_new_bit_output = gate.output
                            potential_used_gates.append(gate)

            # we still need to find the carry bit of the new bit and check if AND_new_bit_output
            # and AND_carry_bit_XOR_new_bit_output are correctly wired
            for igate, gate in enumerate(unused_gates):
                if {gate.input_1, gate.input_2} == {AND_new_bit_output, AND_carry_bit_XOR_new_bit_output}:
                    if gate.operation == "OR":
                        new_carry_bit = gate.output
                        potential_used_gates.append(gate)
            # handle cases where {AND_new_bit_output, AND_carry_bit_XOR_new_bit_output} is not found
            if new_carry_bit == "":
                for igate, gate in enumerate(unused_gates):
                    if AND_new_bit_output in {gate.input_1, gate.input_2}:
                        if gate.operation == "OR":
                            new_list = list({gate.input_1, gate.input_2})
                            new_list.remove(AND_new_bit_output)
                            potential_and_old_carry_bit_mix_new_output = new_list[0]
                            potential_new_carry_bit = gate.output
                            next_bit = str(int(current_bit) + 1) if len(str(int(current_bit) + 1)) > 1 else "0" + str(int(current_bit) + 1)  # noqa
                            # check that the potential carry bit is used for the new output bit
                            # ignore the case where the new output bit is wrongly wired on top of the old carry bit
                            for jgate, gate2 in enumerate(unused_gates):
                                if (
                                    (potential_new_carry_bit in {gate2.input_1, gate2.input_2}) and
                                    (gate2.operation == "XOR") and
                                    (gate2.output == f"z{next_bit}")
                                ):
                                    # now we are "sure" that the potential_new_carry_bit is the carry bit of the new bit
                                    # so we need to exchange wires for AND_carry_bit_XOR_new_bit_output
                                    for kgate, gate3 in enumerate(unused_gates):
                                        if gate3.output == AND_carry_bit_XOR_new_bit_output:
                                            wrong_wires.append(gate3.output)
                                            gate_to_reconnect[kgate] = potential_and_old_carry_bit_mix_new_output
                                            used_gates.append(gate3)
                                            for lgate, gate4 in enumerate(unused_gates):
                                                if gate4.output == potential_and_old_carry_bit_mix_new_output:
                                                    wrong_wires.append(gate4.output)
                                                    gate_to_reconnect[lgate] = AND_carry_bit_XOR_new_bit_output
                # if new_carry_bit still empty, then AND_carry_bit_XOR_new_bit_output is probably wrong
                # check it in the same way as above
                if new_carry_bit == "":
                    for igate, gate in enumerate(unused_gates):
                        if AND_carry_bit_XOR_new_bit_output in {gate.input_1, gate.input_2}:
                            if gate.operation == "OR":
                                new_list = list({gate.input_1, gate.input_2})
                                new_list.remove(AND_carry_bit_XOR_new_bit_output)
                                potential_new_bit_output = new_list[0]
                                potential_new_carry_bit = gate.output
                                next_bit = str(int(current_bit) + 1) if len(str(int(current_bit) + 1)) > 1 else "0" + str(int(current_bit) + 1)  # noqa
                                # check that the potential carry bit is used for the new output bit
                                # ignore the case where the new output bit is wrongly wired on top of the old carry bit
                                for jgate, gate2 in enumerate(unused_gates):
                                    if (
                                        potential_new_bit_output in {gate2.input_1, gate2.input_2} and
                                        gate2.operation == "XOR" and
                                        gate2.output == f"z{next_bit}"
                                    ):
                                        # now we are "sure" that the potential_new_carry_bit is the carry bit of
                                        # the new bit so we need to exchange wires for AND_new_bit_output
                                        for kgate, gate3 in enumerate(unused_gates):
                                            if gate3.output == AND_new_bit_output:
                                                wrong_wires.append(gate3.output)
                                                gate_to_reconnect[kgate] = potential_new_bit_output
                                                used_gates.append(gate3)
                                                potential_used_gates.remove(gate3)
                                                for lgate, gate4 in enumerate(unused_gates):
                                                    if gate4.output == potential_new_bit_output:
                                                        wrong_wires.append(gate4.output)
                                                        gate_to_reconnect[lgate] = AND_new_bit_output
                # we ignore the case where both are wrong, since it would very difficult to find the right gates
                for to_reconnect in gate_to_reconnect.keys():
                    unused_gates[to_reconnect].output = gate_to_reconnect[to_reconnect]
                gate_to_reconnect = {}
                # redo previous step with updated wires
                for igate, gate in enumerate(unused_gates):
                    if {gate.input_1, gate.input_2} == {AND_new_bit_output, AND_carry_bit_XOR_new_bit_output}:
                        if gate.operation == "OR":
                            new_carry_bit = gate.output
                            potential_used_gates.append(gate)
            carry_bit_previous_bit = new_carry_bit
            all_used_gates += used_gates
        return all_used_gates, wrong_wires

    all_used_gates, wrong_wires = build_circuit(inputs, gates)

    wrong_wires = list(set(wrong_wires))
    print("Part 2:", sorted(wrong_wires))
    # solution is gsd,kth,qnf,tbt,vpm,z12,z26,z32
    # need to delete whitespaces, quotes and parentheses from the output

    # edge cases mentioned above ignored, if they appear, most of them would only lead to missing
    # wrong wires in the output. To solve that, either perform the addition bit by bit
    # (for each bit with (0,1), (1,0), (0,0), (1,1), everything else 0 and again when
    # the previous bit has (1,1) as input for a carry bit)
    # and check the output to find the wrong wires

    # or do the same as above, but instead of building the circuit, go backward and build a tree to find
    # any inconsistencies in the circuit.


if __name__ == "__main__":
    main()
