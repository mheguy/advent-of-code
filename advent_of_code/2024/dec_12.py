import itertools
from collections import defaultdict
from dataclasses import dataclass, field

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]

AXIS_INVERSION_MAP = {"x": "y", "y": "x"}


@dataclass
class Plot:
    pos: Position
    char: str
    region: set["Plot"] | None = None
    open_sides: set[Direction] = field(init=False, default_factory=set)

    def __hash__(self) -> int:
        return hash(self.pos)


def main(lines: Lines) -> None:
    grid = create_grid(lines)

    process_plots(grid)

    regions: list[set[Plot]] = []
    for plot in grid.values():
        if (region := plot.region) and region not in regions:
            regions.append(region)

    result_1 = 0
    result_2 = 0
    for region in regions:
        region_size = len(region)
        region_perimeter = sum(len(plot.open_sides) for plot in region)
        result_1 += region_perimeter * region_size

        result_2 += get_region_sides(region) * region_size

    print(result_1, result_2)


def get_region_sides(region: set[Plot]) -> int:
    # Create a map so that we know which plots are open for each direction/face.
    open_side_map = create_side_map(region)

    sides = 0

    # For each direction and level, sort plots by their location on the opposite axis.
    for k, plots in open_side_map.items():
        opposite_axis = AXIS_INVERSION_MAP[k[0].value.axis]

        # With plots sorted, we can form "chains" to establish walls
        plots.sort(key=lambda x: getattr(x.pos, opposite_axis))

        sides += 1
        for left, right in itertools.pairwise(plots):
            left_pos: int = getattr(left.pos, opposite_axis)
            right_pos: int = getattr(right.pos, opposite_axis)

            if right_pos - left_pos > 1:
                sides += 1

    return sides


def create_side_map(region: set[Plot]) -> dict[tuple[Direction, int], list[Plot]]:
    open_side_map: dict[tuple[Direction, int], list[Plot]] = defaultdict(list)

    for plot in region:
        for open_side in plot.open_sides:
            key: tuple[Direction, int] = (open_side, getattr(plot.pos, open_side.value.axis))
            open_side_map[key].append(plot)

    return open_side_map


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
                    plot.open_sides.add(direction)
                    continue

                process_neighbour(plot, neighbour)
            else:
                plot.open_sides.add(direction)

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
