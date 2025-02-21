from advent_of_code.shared.utils import run_solution

Lines = list[str]


def main(lines: Lines) -> None:
    print(get_result(lines))


def get_result(lines: Lines) -> int:
    stones = [int(v) for v in lines[0].split()]

    for _ in range(25):
        stones = blink(stones)

    return len(stones)


def blink(stones: list[int]) -> list[int]:
    new_stones: list[int] = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            stone_text = str(stone)
            midpoint = len(stone_text) // 2

            new_stones.extend([int(stone_text[:midpoint]), int(stone_text[midpoint:])])
        else:
            new_stones.append(stone * 2024)

    return new_stones


if __name__ == "__main__":
    run_solution("2024", "dec_11", main)
