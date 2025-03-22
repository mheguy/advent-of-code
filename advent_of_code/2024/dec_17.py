from dataclasses import dataclass, field

from advent_of_code.shared.utils import run_solution

Lines = list[str]


@dataclass
class Processor:
    register_a: int
    register_b: int
    register_c: int

    output: list[int] = field(default_factory=list, init=False)

    def perform_operation(self, instruction_idx: int, instruction: int, operand: int) -> int:
        """Return the instruction to jump to."""
        match instruction:
            case 0:
                # adv
                self.register_a = int(self.register_a / (2 ** self.get_combo(operand)))
            case 1:
                # bxl
                self.register_b = self.register_b ^ operand
            case 2:
                # bst
                self.register_b = self.get_combo(operand) % 8
            case 3:
                # jnz
                if self.register_a != 0:
                    return operand
            case 4:
                # bxc
                self.register_b = self.register_b ^ self.register_c
            case 5:
                # out
                self.output.append(self.get_combo(operand) % 8)
            case 6:
                # bdv
                self.register_b = int(self.register_a / (2 ** self.get_combo(operand)))
            case 7:
                # cdv
                self.register_c = int(self.register_a / (2 ** self.get_combo(operand)))
            case _:
                raise ValueError(f"Invalid input value: {instruction}")

        return instruction_idx + 2

    def print(self) -> None:
        print(",".join(str(num) for num in self.output))

    def get_combo(self, val: int) -> int:  # noqa: PLR0911
        match val:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case _:
                raise ValueError(f"Invalid input value: {val}")


def main(lines: Lines) -> None:
    p = Processor(
        int(lines[0].split(":")[-1]),
        int(lines[1].split(":")[-1]),
        int(lines[2].split(":")[-1]),
    )

    instructions = [int(num) for num in (lines[4].split(":")[-1].split(","))]

    cur_instruction_idx = 0
    while True:
        cur_instruction_idx = p.perform_operation(
            cur_instruction_idx, instructions[cur_instruction_idx], instructions[cur_instruction_idx + 1]
        )
        if cur_instruction_idx + 1 > len(instructions):
            break

    p.print()


if __name__ == "__main__":
    run_solution("2024", "dec_17", main)
