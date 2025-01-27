from collections import Counter

from advent_of_code.shared.utils import run_solution


def main(lines: list[str]) -> None:
    lefts: list[int] = []
    rights: list[int] = []
    for line in lines:
        left, right = line.split()
        lefts.append(int(left))
        rights.append(int(right))

    sorted_lefts = sorted(lefts)
    rights.sort()

    total = 0
    for left, right in zip(sorted_lefts, rights, strict=False):
        total += abs(left - right)

    print(total)

    counted_rights = Counter(rights)

    p2_total = 0
    for num in lefts:
        p2_total += num * counted_rights[num]

    print(p2_total)


if __name__ == "__main__":
    run_solution("2024", "dec_01", main)
