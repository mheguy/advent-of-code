import itertools

from advent_of_code.shared.utils import run_solution


def main(lines: list[str]) -> None:
    p1_total = 0
    p2_total = 0
    for line in lines:
        current_array = [int(i) for i in line.split()]
        layers = [current_array.copy()]

        while any(current_array):
            new_array = []
            for cur_i, next_i in itertools.pairwise(current_array):
                new_array.append(next_i - cur_i)

            layers.append(new_array)
            current_array.clear()
            current_array.extend(new_array)

        layers.reverse()

        for lower, upper in itertools.pairwise(layers):
            upper.insert(0, upper[0] - lower[0])
            upper.append(upper[-1] + lower[-1])

        p1_total += layers[-1][-1]
        p2_total += layers[-1][0]

    print("P1 answer:", p1_total)
    print("P1 answer:", p2_total)


if __name__ == "__main__":
    run_solution("2023", "dec_09", main)
