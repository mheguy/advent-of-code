import re

from advent_of_code.shared.utils import run_solution

PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def main(lines: list[str]) -> None:
    input_text = "".join(lines)
    result = 0

    matches = PATTERN.findall(input_text)

    for match in matches:
        result += int(match[0]) * int(match[1])

    print(result)


if __name__ == "__main__":
    run_solution("2024", "dec_03", main)
