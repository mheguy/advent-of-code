import importlib.resources as pkg_resources
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import advent_of_code

if TYPE_CHECKING:
    from collections.abc import Callable

INPUT_FOLDER = "input"


def run_solution(year: str, date: str, func: "Callable[[list[str]], None]") -> None:
    filename = f"{date}.txt"
    partial_path = f"input/{year}/"

    print("Running sample...")

    try:
        sample_data = get_input_file_lines(f"{partial_path}/sample/{filename}")
    except FileNotFoundError:
        print(f"No sample file found for year ({year}) and date ({date}). Exiting.")
        sys.exit(1)

    func(sample_data)

    print("Sample completed.")
    print("Running real...")

    try:
        real_data = get_input_file_lines(f"{partial_path}/real/{filename}")
    except FileNotFoundError:
        print("File with real data missing. Create the missing file with the data.")

        init_file = advent_of_code.__file__
        package_path = Path(init_file).parent
        full_path = package_path / f"{partial_path}/real/{filename}"
        print("Location:", full_path)

        sys.exit(1)

    func(real_data)

    print("Real completed.")


def get_input_file_lines(file_path: str) -> list[str]:
    file = pkg_resources.open_text(advent_of_code, file_path)

    input_text = file.read()
    lines = input_text.split("\n")
    return [line for line in lines if line]
