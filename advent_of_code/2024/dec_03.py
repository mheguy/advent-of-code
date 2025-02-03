import re

from advent_of_code.shared.utils import run_solution

PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def main(lines: list[str]) -> None:
    input_text = "".join(lines)
    print(part_1(input_text))
    print(part_2(input_text))


def part_1(input_text: str) -> int:
    result = 0

    matches = PATTERN.findall(input_text)

    for match in matches:
        result += int(match[0]) * int(match[1])

    return result


def part_2(input_text: str) -> int:
    parts_to_keep = []

    enabled = True

    for idx, char in enumerate(input_text):
        if input_text[idx:].startswith("don't()"):
            enabled = False
            continue

        if input_text[idx:].startswith("do()"):
            enabled = True
            continue

        if enabled:
            parts_to_keep.append(char)

    kept_string = "".join(parts_to_keep)

    return part_1(kept_string)


if __name__ == "__main__":
    run_solution("2024", "dec_03", main)
