import re

from advent_of_code.shared.utils import run_solution


def main(lines: list[str]) -> None:
    part_1_validity_thresholds = {"red": 12, "green": 13, "blue": 14}
    part_1_total = part_2_total = 0

    for line in lines:
        game_info, hint = line.split(":")
        game_running_total = 1

        valid_game = True
        for color_name, color_value in part_1_validity_thresholds.items():
            color_values = [int(num) for num in re.findall(rf"(\d+) {color_name}", hint)]
            color_max = max(color_values)
            game_running_total *= color_max

            if color_max > color_value:
                valid_game = False

        part_2_total += game_running_total
        if valid_game:
            part_1_total += int(game_info.split(" ")[1])

    print("Part 1:", part_1_total)
    print("Part 2:", part_2_total)


if __name__ == "__main__":
    run_solution("2023", "dec_02", main)
