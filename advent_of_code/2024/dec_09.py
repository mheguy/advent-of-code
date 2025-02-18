import itertools
from dataclasses import dataclass

from advent_of_code.shared.utils import run_solution

Lines = list[str]


@dataclass
class Blob:
    size: int
    file_id: int | None = None

    def get_hash_value(self, block_id: int) -> int:
        if self.file_id is None:
            return 0

        return self.file_id * block_id

    def copy(self) -> "Blob":
        return Blob(self.size, self.file_id)


def main(lines: Lines) -> None:
    print(get_p1_result(lines))
    print(get_p2_result(lines))


def get_p1_result(lines: Lines) -> int:
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


def get_p2_result(lines: Lines) -> int:
    line = lines[0]

    disk: list[Blob] = []
    for file_id, batch in enumerate(itertools.batched(line, 2)):
        disk.append(Blob(int(batch[0]), file_id))

        if len(batch) > 1:
            disk.append(Blob(int(batch[-1])))

    counter = len(disk) - 1

    while counter > 0:
        file = disk[counter]

        if file.file_id:
            for index, empty_space in enumerate(disk):
                if index >= counter:
                    break

                if empty_space.file_id is None and empty_space.size >= file.size:
                    empty_space.size = empty_space.size - file.size

                    disk.insert(index, file.copy())

                    file.file_id = None

                    break

        counter -= 1

    result = 0
    end_id = 0

    for blob in disk:
        start_id = end_id
        end_id = start_id + blob.size

        for block_id in range(start_id, end_id):
            result += blob.get_hash_value(block_id)

    return result


if __name__ == "__main__":
    run_solution("2024", "dec_09", main)
