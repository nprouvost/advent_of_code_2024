# whatever imports you need
import numpy as np


# create example code:
example = [
    "Button A: X+94, Y+34",
    "Button B: X+22, Y+67",
    "Prize: X=8400, Y=5400",
    "",
    "Button A: X+26, Y+66",
    "Button B: X+67, Y+21",
    "Prize: X=12748, Y=12176",
    "",
    "Button A: X+17, Y+86",
    "Button B: X+84, Y+37",
    "Prize: X=7870, Y=6450",
    "",
    "Button A: X+69, Y+23",
    "Button B: X+27, Y+71",
    "Prize: X=18641, Y=10279",
]


class Machine:
    def __init__(self, cost_button_A=3, cost_button_B=1):
        self.status = np.array([0, 0])
        self.cost_button_A = cost_button_A
        self.cost_button_B = cost_button_B
        self.button_A = []
        self.button_B = []
        self.prizes = []

    def set_button_A(self, button):
        self.button_A = button

    def set_button_B(self, button):
        self.button_B = button

    def set_prize(self, prize):
        self.prizes = prize

    def get_prizes(self):
        return np.array(self.prizes)

    def get_button_A(self):
        return np.array(self.button_A)

    def get_button_B(self):
        return np.array(self.button_B)

    def get_status(self):
        return self.status

    def use_button_A(self, n):
        button = self.get_button_A()
        self.status[0] += button[0] * n
        self.status[1] += button[1] * n
        return self.status, self.cost_button_A * n

    def use_button_B(self, n):
        button = self.get_button_B()
        self.status[0] += button[0] * n
        self.status[1] += button[1] * n
        return self.status, self.cost_button_B * n

    def reset_status(self):
        self.status = np.array([0, 0])


# read file to list of lines
def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines


def main():
    file_path = 'day_13.txt'
    lines_array = read_file_to_list(file_path)
    # lines_array = example

    machines = []
    for line in lines_array:
        if line != "":
            if "Button A" in line:
                machines.append(Machine())
                machine = machines[-1]
                button = [int(x.split("+")[-1]) for x in line.split(":")[1].split(",")]
                machine.set_button_A(button)
            elif "Button B" in line:
                machine = machines[-1]
                button = [int(x.split("+")[-1]) for x in line.split(":")[1].split(",")]
                machine.set_button_B(button)
            elif "Prize" in line:
                machine = machines[-1]
                prize = [int(x.split("=")[-1]) for x in line.split(":")[1].split(",")]
                machine.set_prize(prize)

    # part 1
    all_min_costs = []
    for imachine, machine in enumerate(machines):
        is_reachable = False
        all_costs = []
        all_n_button_b = []
        all_n_button_a = []
        for i in range(0, 101):
            n = 100 - i
            machine.reset_status()
            status, cost = machine.use_button_B(n)
            if (
                (((machine.get_prizes()[0] - status[0]) % machine.get_button_A()[0]) == 0) and
                (((machine.get_prizes()[1] - status[1]) % machine.get_button_A()[1]) == 0)
            ):
                if (
                    ((machine.get_prizes()[0] - status[0]) // machine.get_button_A()[0]) ==
                    ((machine.get_prizes()[1] - status[1]) // machine.get_button_A()[1])
                ):
                    n_button_a = (machine.get_prizes()[0] - status[0]) // machine.get_button_A()[0]
                    if n_button_a > 100:
                        continue
                    n_button_b = n
                    all_n_button_a.append(n_button_a)
                    all_n_button_b.append(n_button_b)
                    all_costs.append(n_button_a * machine.cost_button_A + n_button_b * machine.cost_button_B)
        if all_costs:
            is_reachable = True
        if is_reachable:
            all_min_costs.append(min(all_costs))

    print("Minimum cost", sum(all_min_costs))

    # part 2
    all_min_costs = []
    for imachine, machine in enumerate(machines):
        machine.reset_status()
        old_prizes = machine.get_prizes()
        new_prizes = old_prizes + np.array([10000000000000, 10000000000000])
        machine.set_prize(new_prizes)

        # solve system of equations
        # x = n_button_a * button_A[0] + n_button_b * button_B[0]
        # y = n_button_a * button_A[1] + n_button_b * button_B[1]
        # therefore n_button_a = (x - n_button_b * button_B[0]) / button_A[0]
        # y = (x - n_button_b * button_B[0]) / button_A[0] * button_A[1] + n_button_b * button_B[1]
        # and y - x * button_A[1] / button_A[0] = n_button_b * (button_B[1] - button_A[1] * button_B[0] / button_A[0])
        # therefore n_button_b = (y - x * button_A[1] / button_A[0]) / (button_B[1] - button_A[1] * button_B[0] / button_A[0])  # noqa
        #  = (y * button_A[0] - x * button_A[1]) / (button_A[0] * button_B[1] - button_A[1] * button_B[0])
        # Insert in n_button_a gives
        # n_button_a = (x * button_B[1] - y * button_A[1]) / (button_A[0] * button_B[1] - button_A[1] * button_B[0])

        x, y = machine.get_prizes()
        if (machine.get_button_A()[0] * machine.get_button_B()[1] == machine.get_button_A()[1] * machine.get_button_B()[0]):  # noqa
            raise ValueError("problem ill defined")

        # is_integer() works only on float, so we need to convert the result to float first by mutliplying with 1.0
        n_button_b = 1.0 * (
            (
                y * machine.get_button_A()[0] -
                x * machine.get_button_A()[1]
            ) / (
                machine.get_button_A()[0] * machine.get_button_B()[1] -
                machine.get_button_A()[1] * machine.get_button_B()[0]
            )
        )
        n_button_a = 1.0 * (
            (
                x * machine.get_button_B()[1] -
                y * machine.get_button_B()[0]
            ) / (
                machine.get_button_A()[0] * machine.get_button_B()[1] -
                machine.get_button_A()[1] * machine.get_button_B()[0]
            )
        )

        if n_button_a.is_integer() and n_button_b.is_integer():
            n_button_a = int(n_button_a)
            n_button_b = int(n_button_b)
            all_min_costs.append(n_button_a * machine.cost_button_A + n_button_b * machine.cost_button_B)
    print("Minimum cost", sum(all_min_costs))


if __name__ == "__main__":
    main()
