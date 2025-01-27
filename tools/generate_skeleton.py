from pathlib import Path

import advent_of_code

SOLUTION_TEMPLATE = """"""


def create_files_for_day(year: int, day: int) -> None:
    print(f"Processing {year}, day {day}")
    aoc_folder = Path(advent_of_code.__file__).parent

    year_folder_name = str(year)
    solutions_folder = aoc_folder / year_folder_name
    real_input_folder = aoc_folder / "input" / year_folder_name / "real"
    sample_input_folder = aoc_folder / "input" / year_folder_name / "sample"

    solutions_folder.mkdir(parents=True, exist_ok=True)
    real_input_folder.mkdir(parents=True, exist_ok=True)
    sample_input_folder.mkdir(parents=True, exist_ok=True)

    date = f"dec_{day:02}"
    (real_input_folder / f"{date}.txt").touch()
    (sample_input_folder / f"{date}.txt").touch()

    solution_file = solutions_folder / f"{date}.py"

    if solution_file.exists():
        print("Solution file exists, will not overwrite.")
    else:
        solution_file.write_text(SOLUTION_TEMPLATE)


def process_day_input(day_input: str) -> list[int]:
    if "," in day_input:
        return [int(day) for day in day_input.split(",")]

    if "-" in day_input:
        start, end = day_input.split("-")
        return list(range(int(start), int(end) + 1))

    return [int(day_input)]


def main() -> None:
    print("This will generate the solution and input files for the given year and days.")
    year = int(input("Year (4 digits): "))

    day_input = input("Days (single, comma-separated, or range): ")

    days = process_day_input(day_input)

    for day in days:
        create_files_for_day(year, day)


if __name__ == "__main__":
    main()
