from advent_of_code.shared.utils import run_solution


def main(lines: list[str]) -> None:
    total = 0
    for chars in lines[0].split(","):
        value = 0
        for char in chars:
            value = ((value + ord(char)) * 17) % 256

        total += value

    print(total)


if __name__ == "__main__":
    run_solution("2023", "dec_15", main)
