import itertools

from advent_of_code.shared.utils import run_solution

Lines = list[str]


def main(lines: Lines) -> None:
    print(get_result(lines))


def get_result(lines: Lines) -> int:
    line = lines[0]

    full_sequence: list[int | None] = []
    for file_id, batch in enumerate(itertools.batched(line, 2)):
        file = batch[0]

        if len(batch) == 1:
            space = 0
        else:
            space = batch[-1]

        subseq = [file_id] * int(file) + [None] * int(space)
        full_sequence += subseq

    first_none_index = 0
    while None in full_sequence[first_none_index:]:
        last_val = full_sequence.pop()

        if last_val is None:
            continue

        first_none_index = full_sequence.index(None)
        full_sequence[first_none_index] = last_val

    result = 0
    for block_id, val in enumerate(full_sequence):
        if val is None:
            raise TypeError

        result += block_id * val

    return result


if __name__ == "__main__":
    run_solution("2024", "dec_09", main)
