import itertools

from advent_of_code.shared.utils import run_solution

Lines = list[str]
BATCH_LEN = 7
MAX_HEIGHT = 5


def main(lines: Lines) -> None:
    locks, keys = parse_input(lines)

    result = 0
    for lock, key in itertools.product(locks, keys):
        for lock_height, key_height in zip(lock, key, strict=True):
            if lock_height + key_height > MAX_HEIGHT:
                break
        else:
            result += 1

    print(result)


def parse_input(lines: Lines) -> tuple[list[list[int]], list[list[int]]]:
    locks: list[list[int]] = []
    keys: list[list[int]] = []

    for line_batch in itertools.batched(filter(None, lines), BATCH_LEN, strict=False):
        if len(line_batch) < BATCH_LEN:
            continue

        lock_or_key = parse_height_map(line_batch)

        if line_batch[0] == "#####":
            locks.append(lock_or_key)
        else:
            keys.append(lock_or_key)

    return locks, keys


def parse_height_map(lines: tuple[str, ...]) -> list[int]:
    height_map = [0, 0, 0, 0, 0]
    for line in lines[1:6]:
        for idx, char in enumerate(line):
            if char == "#":
                height_map[idx] += 1

    return height_map


if __name__ == "__main__":
    run_solution("2024", "dec_25", main)
