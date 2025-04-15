from advent_of_code.shared.utils import run_solution

Lines = list[str]


def main(lines: Lines) -> None:
    towels = {t.strip() for t in lines[0].split(",")}
    prime_towels = set()

    for towel in towels:
        inner_towels = towels.copy()
        inner_towels.remove(towel)

        if is_string_prime(towel, inner_towels):
            prime_towels.add(towel)

    designs = lines[2:]

    result = 0
    for design in designs:
        if not design:
            continue

        if not is_string_prime(design, prime_towels):
            result += 1

    print(f"Result: {result}")


def is_string_prime(given_string: str, other_strings: set[str]) -> bool:
    """Check if the given_string can be composed of any combination of the other_strings."""
    if not given_string:
        return False

    for other_string in other_strings:
        if (given_string.startswith(other_string)) and (
            not is_string_prime(given_string[len(other_string) :], other_strings)
        ):
            return False

    return True


if __name__ == "__main__":
    run_solution("2024", "dec_19", main)
