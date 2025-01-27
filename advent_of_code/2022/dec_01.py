from itertools import groupby

from advent_of_code.shared.utils import run_solution


def get_sum_of_top_n(nums: list[int], n: int) -> int:
    total = 0
    for _ in range(n):
        current_max = max(nums)
        total += current_max
        nums.remove(current_max)

    return total


def main(lines: list[str]) -> None:
    calorie_counts = [sum(map(int, group)) for key, group in groupby(lines, bool) if key]
    print(max(calorie_counts))
    print(get_sum_of_top_n(calorie_counts, 3))


if __name__ == "__main__":
    run_solution("2022", "dec_01", main)
