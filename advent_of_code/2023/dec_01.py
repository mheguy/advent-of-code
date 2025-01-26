import re

from advent_of_code.shared.utils import run_solution

number_lookup = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def main(lines: list[str]) -> None:
    p1_regex = re.compile(r"\d")
    p2_regex = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")
    p1_total = 0
    p2_total = 0

    for line in lines:
        p1_match: list[str] = re.findall(p1_regex, line)
        p1_total += int(p1_match[0] + p1_match[-1])

        p2_match: list[str] = re.findall(p2_regex, line)
        first = number_lookup.get(p2_match[0], p2_match[0])
        last = number_lookup.get(p2_match[-1], p2_match[-1])
        p2_total += int(first + last)

    print(p1_total, p2_total)


if __name__ == "__main__":
    run_solution("2023", "dec_01", main)
