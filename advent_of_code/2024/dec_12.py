from dataclasses import dataclass

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]


@dataclass
class Plot:
    pos: Position
    char: str
    perimeter: int = 0
    region: set["Plot"] | None = None

    def __hash__(self) -> int:
        return hash(self.pos)


def main(lines: Lines) -> None:
    grid = create_grid(lines)

    process_plots(grid)

    regions: list[set[Plot]] = []
    for plot in grid.values():
        if (region := plot.region) and region not in regions:
            regions.append(region)

    result = 0
    for region in regions:
        region_size = len(region)
        region_perimeter = sum(plot.perimeter for plot in region)
        result += region_size * region_perimeter

    print(result)


def create_grid(lines: Lines) -> dict[Position, Plot]:
    grid: dict[Position, Plot] = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            pos = Position(col, row)
            grid[pos] = Plot(pos, char)
    return grid


def process_plots(grid: dict[Position, Plot]) -> None:
    for pos, plot in grid.items():
        for direction in Direction:
            if neighbour := grid.get(pos + direction):
                if plot.char != neighbour.char:
                    plot.perimeter += 1
                    continue

                process_neighbour(plot, neighbour)
            else:
                plot.perimeter += 1

        if not plot.region:
            plot.region = {plot}


def process_neighbour(plot: Plot, neighbour: Plot) -> None:
    if plot.region is not None:
        if neighbour.region is not None:
            # Combine regions
            neighbour.region.update(plot.region)
            for p in plot.region:
                p.region = neighbour.region
        else:
            neighbour.region = plot.region
    elif neighbour.region is not None:
        plot.region = neighbour.region
    else:
        plot.region = set()
        neighbour.region = plot.region

    plot.region.add(plot)
    plot.region.add(neighbour)


if __name__ == "__main__":
    run_solution("2024", "dec_12", main)
