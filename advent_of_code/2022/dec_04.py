# Find if set is completely contained in other
from advent_of_code.shared.utils import run_solution


def main(lines: list[str]) -> None:
    full_overlap = 0
    for line in lines:
        elves = line.split(",")
        assignment_sets = []
        for elf in elves:
            lower, upper = elf.split("-")
            assignment_sets.append(set(range(int(lower), int(upper) + 1)))

        if assignment_sets[0].issubset(assignment_sets[1]) or assignment_sets[0].issuperset(assignment_sets[1]):
            full_overlap += 1

    print(full_overlap)

    any_overlap = 0
    for line in lines:
        elves = line.split(",")
        assignment_sets = []
        for elf in elves:
            lower, upper = elf.split("-")
            assignment_sets.append(set(range(int(lower), int(upper) + 1)))

        if assignment_sets[0].intersection(assignment_sets[1]):
            any_overlap += 1

    print(any_overlap)


if __name__ == "__main__":
    run_solution("2022", "dec_04", main)
