from functools import cache
from typing import TYPE_CHECKING

from advent_of_code.shared.utils import run_solution

if TYPE_CHECKING:
    from collections.abc import Iterable

Lines = list[str]


def main(lines: Lines) -> None:
    towels = tuple(t.strip() for t in lines[0].split(","))
    designs = lines[2:]

    prime_towels = tuple(get_prime_strings(set(towels)))

    print(f"Unique towel patterns: {len(towels)}, prime patterns: {len(prime_towels)}")

    p1_result = 0
    p2_result = 0
    for design in designs:
        if not design:
            continue

        if is_string_prime(design, prime_towels):
            continue

        p1_result += 1

        towel_combinations = get_combinations(design, towels)
        p2_result += towel_combinations

    print(f"Result 1: {p1_result}")
    print(f"Result 2: {p2_result}")


def get_prime_strings(strings: set[str]) -> set[str]:
    """Get the subset of prime strings."""
    prime_towels = set()
    for towel in strings:
        inner_strings = strings.copy()
        inner_strings.remove(towel)

        if is_string_prime(towel, tuple(inner_strings)):
            prime_towels.add(towel)
    return prime_towels


@cache
def is_string_prime(given_string: str, other_strings: "Iterable[str]") -> bool:
    """Check if the given_string can be composed of any combination of the other_strings."""
    if not given_string:
        return False

    for other_string in other_strings:
        if (given_string.startswith(other_string)) and (
            not is_string_prime(given_string[len(other_string) :], other_strings)
        ):
            return False

    return True


@cache
def get_combinations(given_string: str, other_strings: "Iterable[str]") -> int:
    """Get the number of ways given_string can be constructed by the strings in other_strings."""
    combinations = 0
    for other_string in other_strings:
        if given_string == other_string:
            combinations += 1

        if given_string.startswith(other_string):
            combinations += get_combinations(given_string[len(other_string) :], other_strings)

    return combinations


if __name__ == "__main__":
    run_solution("2024", "dec_19", main)
