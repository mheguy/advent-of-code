from collections import defaultdict
from dataclasses import dataclass, field
from math import inf

from advent_of_code.shared.utils import run_solution

map_names = (
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
)


@dataclass
class LookupRule:
    destination: int
    source: int
    value_range: int

    max_source: int = field(init=False)
    conversion_factor: int = field(init=False)

    def __post_init__(self):
        self.max_source = self.source + self.value_range
        self.conversion_factor = self.destination - self.source

    def convert(self, value: int) -> int | None:
        if self.max_source >= value >= self.source:
            return value + self.conversion_factor

        return None


def main(lines: list[str]) -> None:
    seed_map = create_map(lines)

    seeds = [int(i) for i in lines[0].split(" ")[1:]]
    destinations = [get_seed_destination_value(seed_map, seed) for seed in seeds]

    print("p1 answer:", min(destinations))

    # Part 2 will never finish running as-is.
    # Do it in rust!

    p2_lowest_destination = inf
    seed_maps = deduplicate_seed_maps(seeds)

    for start, length in seed_maps:
        for seed in range(start, start + length + 1):
            destination = get_seed_destination_value(seed_map, seed)
            p2_lowest_destination = min(destination, p2_lowest_destination)

    print("p2 answer:", p2_lowest_destination)


def deduplicate_seed_maps(seeds: list[int]) -> list[tuple[int, int]]:
    seed_ranges: list[tuple[int, int]] = list(zip(seeds[::2], seeds[1::2], strict=False))

    total_seeds = 0
    for _, length in seed_ranges:
        total_seeds += length
    print(f"{total_seeds=}")

    seed_ranges: list[tuple[int, int]] = [(start, start + length) for start, length in seed_ranges]

    deduplicated_ranges = []
    sorted_ranges = sorted(seed_ranges, key=lambda x: x[0])

    for current_range in sorted_ranges:
        if not deduplicated_ranges or current_range[0] > deduplicated_ranges[-1][1]:
            deduplicated_ranges.append(current_range)
        else:
            deduplicated_ranges[-1] = (
                deduplicated_ranges[-1][0],
                max(current_range[1], deduplicated_ranges[-1][1]),
            )

    deduplicated_seeds = 0
    for start, end in seed_ranges:
        deduplicated_seeds += end - start
    print(f"{deduplicated_seeds=}")

    return deduplicated_ranges


def get_seed_destination_value(
    seed_map: defaultdict[str, list[LookupRule]],
    seed: int,
) -> int:
    current_value = seed

    for map_name in map_names:
        current_value = perform_map_layer_lookup(seed_map, map_name, current_value)

    return current_value


def perform_map_layer_lookup(
    seed_map: defaultdict[str, list[LookupRule]],
    map_name: str,
    current_value: int,
) -> int:
    lookup_matches: list[int] = []

    for lookup_rule in seed_map[map_name]:
        lookup_value = lookup_rule.convert(current_value)
        if lookup_value is not None:
            lookup_matches.append(lookup_value)

    if lookup_matches:
        current_value = min(lookup_matches)
    return current_value


def create_map(lines: list[str]) -> defaultdict[str, list[LookupRule]]:
    seed_map = defaultdict(list)
    map_index = 0

    for line in lines[2:]:
        if not line[0].isdigit():
            map_index += 1
            continue

        seed_map[map_names[map_index]].append(LookupRule(*[int(i) for i in line.split(" ")]))

    return seed_map


if __name__ == "__main__":
    run_solution("2023", "dec_05", main)
