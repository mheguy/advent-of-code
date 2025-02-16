# ruff: noqa: S606
import http.client
import os
import re
import subprocess
import sys
import urllib.request
from http.client import OK
from pathlib import Path
from string import Template

import advent_of_code

SOLUTION_TEMPLATE = Template(
    """from advent_of_code.shared.utils import run_solution

Lines=list[str]

def main(lines: Lines) -> None:
    print(get_result(lines))

def get_result(lines: Lines) -> int | str:
    return 0

if __name__ == "__main__":
    run_solution("$year", "$date", main)
"""
)


def open_file(filename: Path | str) -> None:
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])  # noqa: S603


def create_files_for_day(year: int, day: int) -> None:
    print(f"Processing {year}, day {day}")
    aoc_folder = Path(advent_of_code.__file__).parent

    year_folder_name = str(year)

    solutions_folder = aoc_folder / year_folder_name
    solutions_folder.mkdir(parents=True, exist_ok=True)

    real_input_folder = aoc_folder / "input" / year_folder_name / "real"
    real_input_folder.mkdir(parents=True, exist_ok=True)

    sample_input_folder = aoc_folder / "input" / year_folder_name / "sample"
    sample_input_folder.mkdir(parents=True, exist_ok=True)

    date = f"dec_{day:02}"
    base_url = f"https://adventofcode.com/{year}/day/{day}"

    generate_solution_file(solutions_folder, year, date)
    generate_example_input_file(sample_input_folder, date, base_url)
    generate_real_input_file(real_input_folder, date, base_url)


def generate_solution_file(solutions_folder: Path, year: int, date: str) -> None:
    (solutions_folder / "__init__.py").touch()

    solution_file = solutions_folder / f"{date}.py"

    if solution_file.exists():
        print("Solution file exists, will not overwrite.")
    else:
        solution_text = SOLUTION_TEMPLATE.substitute(year=year, date=date)
        solution_file.write_text(solution_text)


def generate_example_input_file(sample_input_folder: Path, date: str, base_url: str) -> None:
    sample_input_file = sample_input_folder / f"{date}.txt"

    if sample_input_file.exists() and sample_input_file.read_text():
        print("Sample input file exists and is not empty. Will not overwrite.")
        return

    sample_input_file.touch()

    with urllib.request.urlopen(base_url, timeout=5) as response:  # noqa: S310
        if not isinstance(response, http.client.HTTPResponse):
            raise TypeError(f"Expected HTTPResponse, got {type(response)}")

        response_text = response.read().decode()

        if response.status == OK:
            match = re.search(r"example.*?:[\s\S]+?<code>([\s\S]+?)</code>", response_text)

            if match is None:
                print("WARNING: Could not find example input")
            else:
                sample_input_file.write_text(match.group(1))
        else:
            print(f"ERROR: Invalid response when trying to obtain example input. Code: {response.status}")
            open_file(base_url)
            open_file(sample_input_file)


def generate_real_input_file(real_input_folder: Path, date: str, base_url: str) -> None:
    real_input_file = real_input_folder / f"{date}.txt"

    if real_input_file.exists() and real_input_file.read_text():
        print("Real input file exists and is not empty. Will not overwrite.")
        return

    real_input_file.touch()
    open_file(real_input_file)
    open_file(f"{base_url}/input")


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
