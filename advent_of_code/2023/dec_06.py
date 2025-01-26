import math

from advent_of_code.shared.utils import run_solution


def main(lines: list[str]) -> None:
    times = [int(i) for i in lines[0].split()[1:]]
    distances = [int(i) for i in lines[1].split()[1:]]

    winning_ways_per_race = []
    for time, distance_to_beat in zip(times, distances, strict=False):
        ways_to_win = get_ways_to_win(time, distance_to_beat)

        winning_ways_per_race.append(ways_to_win)

    print("p1 total:", math.prod(winning_ways_per_race))

    time = int("".join([str(i) for i in times]))
    distance_to_beat = int("".join([str(i) for i in distances]))

    print("p2 total:", get_ways_to_win(time, distance_to_beat))


def get_ways_to_win(time: int, distance_to_beat: int) -> int:
    ways_to_win = 0
    for i in range(time + 1):
        distance_traveled = i * (time - i)

        if distance_traveled > distance_to_beat:
            ways_to_win += 1
            continue

        if ways_to_win > 0:
            break
    return ways_to_win


if __name__ == "__main__":
    run_solution("2023", "dec_06", main)
