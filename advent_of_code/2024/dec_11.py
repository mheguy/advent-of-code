from collections import Counter

from advent_of_code.shared.utils import run_solution

Lines = list[str]


def main(lines: Lines) -> None:
    raw_stones = [int(v) for v in lines[0].split()]
    stones = Counter(raw_stones)

    for _ in range(25):
        stones = blink(stones)

    print(sum(stones.values()))

    for _ in range(50):
        stones = blink(stones)

    print(sum(stones.values()))


def blink(stones: Counter[int]) -> Counter[int]:
    new_stones = Counter()

    for stone, count in stones.items():
        if stone == 0:
            new_stones[1] += count
        else:
            stone_str = str(stone)
            if len(stone_str) % 2 == 0:
                midpoint = len(stone_str) // 2
                first_half = int(stone_str[:midpoint])
                second_half = int(stone_str[midpoint:])

                new_stones[first_half] += count
                new_stones[second_half] += count
            else:
                new_stones[stone * 2024] += count

    return new_stones


if __name__ == "__main__":
    run_solution("2024", "dec_11", main)
