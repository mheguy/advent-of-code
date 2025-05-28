from typing import cast

from advent_of_code.shared.utils import run_solution

Lines = list[str]


def main(lines: Lines) -> None:
    charge_map, operations_map = parse_input(lines)

    charge_map = resolve_operations_map(charge_map, operations_map)

    charge_map = {k: v for k, v in charge_map.items() if k.startswith("z")}

    bits = [charge_map[k] for k in sorted(charge_map, reverse=True)]
    bool_num = "".join(["1" if bit else "0" for bit in bits])
    result = int(bool_num, 2)

    print(result)


def resolve_operations_map(
    charge_map: dict[str, bool], operations_map: dict[str, tuple[str, str, str]]
) -> dict[str, bool]:
    if not operations_map:
        return {}

    charge_map = charge_map.copy()
    unsolved_map = {}

    for output_node, operation in operations_map.items():
        if operation[0] in charge_map and operation[2] in charge_map:
            charge_map[output_node] = resolve_operation(charge_map, *operation)
        else:
            unsolved_map[output_node] = operation

    return charge_map | resolve_operations_map(charge_map, unsolved_map)


def resolve_operation(charge_map: dict[str, bool], input_1: str, operand: str, input_2: str) -> bool:
    match operand:
        case "AND":
            return charge_map[input_1] and charge_map[input_2]
        case "OR":
            return charge_map[input_1] or charge_map[input_2]
        case "XOR":
            return charge_map[input_1] ^ charge_map[input_2]
        case _:
            raise ValueError("Unexpected operand value: %s", operand)


def parse_input(lines: Lines) -> tuple[dict[str, bool], dict[str, tuple[str, str, str]]]:
    charge_map: dict[str, bool] = {}
    operations_map: dict[str, tuple[str, str, str]] = {}

    for line in lines:
        if not line:
            continue

        if len(line) == 6:  # noqa: PLR2004
            node, value = line.split(": ")
            charge_map[node] = bool(int(value))
        else:
            *operation, _, out_node = line.split()
            operation = cast("tuple[str,str,str]", operation)
            operations_map[out_node] = operation

    return charge_map, operations_map


if __name__ == "__main__":
    run_solution("2024", "dec_24", main)
