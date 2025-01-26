from advent_of_code.shared.utils import run_solution

Position = tuple[int, int]
Point = str

Row = list[Point]
Grid = list[Row]

directional_inverse: dict[str, str] = {"S": "N", "N": "S", "E": "W", "W": "E"}
direction_coordinate_change = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}
opening_lookup: dict[str, str] = {
    "|": "NS",
    "-": "EW",
    "L": "NE",
    "J": "NW",
    "7": "SW",
    "F": "SE",
    ".": "",
    "S": "NSEW",
}


def print_diagram(grid: Grid) -> None:
    diagram_conversion: dict[str, str] = {
        "NS": "│",
        "EW": "─",
        "NE": "└",
        "NW": "┘",
        "SW": "┐",
        "SE": "┌",
        "": " ",
        "NSEW": "\033[41m⁑\033[0m",
    }
    for row in grid:
        r: list[str] = [diagram_conversion[c] for c in row]
        print("".join(r))


def create_grid(lines: list[str]) -> tuple[Position, Grid]:
    starting_pos = None
    grid: Grid = []
    for row_num, line in enumerate(lines):
        row: Row = []
        for column_num, char in enumerate(line):
            if char == "S":
                starting_pos = (row_num, column_num)
            row.append(opening_lookup[char])

        grid.append(row)

    if starting_pos is None:
        raise ValueError
    return starting_pos, grid


class UnidirectionalTraveler:
    def __init__(self, grid: Grid, starting_coordinates: tuple[int, int]) -> None:
        self.grid = grid

        self.y = starting_coordinates[0]
        self.x = starting_coordinates[1]
        self.previous_direction = ""

    def take_step(self) -> Position:
        current_location = self.grid[self.y][self.x]

        for direction in current_location:
            if direction == self.previous_direction:
                continue

            coordinate_change = direction_coordinate_change[direction]
            neighbour_y = self.y + coordinate_change[0]
            neighbour_x = self.x + coordinate_change[1]

            try:
                neighbour = self.grid[neighbour_y][neighbour_x]
            except IndexError:
                # Not that way!
                continue

            opposite_direction = directional_inverse[direction]

            if opposite_direction in neighbour:
                self.y = neighbour_y
                self.x = neighbour_x
                self.previous_direction = opposite_direction
                break

        return (self.y, self.x)


def main(lines: list[str]) -> None:
    starting_pos, grid = create_grid(lines)

    traveler = UnidirectionalTraveler(grid, starting_pos)
    step_counter = 1
    while traveler.take_step() != starting_pos:
        step_counter += 1

    print_diagram(grid)
    print(f"P1 answer: {step_counter / 2}")


if __name__ == "__main__":
    run_solution("2023", "dec_10", main)
