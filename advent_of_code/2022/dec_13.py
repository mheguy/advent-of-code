from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

from advent_of_code.shared.utils import run_solution

if TYPE_CHECKING:
    from collections.abc import Callable

PACKET_PAIR = 0

PacketDataType = int | list["PacketDataType"]


@dataclass
class Packet:
    data: list[PacketDataType]

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Packet):
            raise NotImplementedError
        return self.compare_packets(other)

    def compare_packets(self: Packet, other: Packet) -> bool:
        calc = PacketCalculator()
        result = calc.compare_lists(self.data, other.data)

        return bool(result.value)


class Result(Enum):
    WRONG = False
    RIGHT = True
    NO_RESULT = -1000000


class PacketCalculator:
    def compare_integers(self, left: int, right: int) -> Result:
        if left < right:
            return Result.RIGHT
        if left > right:
            return Result.WRONG
        return Result.NO_RESULT

    def compare_lists(self, left_list: list[Any], right_list: list[Any]) -> Result:
        for left, right in zip(left_list, right_list, strict=False):
            comparison_function = self.get_comparison_method_from_types(type(left), type(right))

            result = comparison_function(left, right)
            if result is not Result.NO_RESULT:
                return result

        left_len = len(left_list)
        right_len = len(right_list)

        if left_len < right_len:
            return Result.RIGHT
        if left_len > right_len:
            return Result.WRONG

        return Result.NO_RESULT

    def compare_mixed(self, left: Any, right: Any) -> Result:
        """Compare a list and an int."""
        if isinstance(left, int):
            left = [left]
        else:
            right = [right]

        return self.compare_lists(left, right)

    def get_comparison_method_from_types(self, left: type, right: type) -> Callable[[Any, Any], Result]:
        """Get the correct method based on the types."""
        if left is int and right is int:
            return self.compare_integers

        if left is list and right is list:
            return self.compare_lists

        return self.compare_mixed


def main(lines: list[str]) -> None:
    left_packets = list(map(Packet, map(json.loads, lines[0::2])))
    right_packets = list(map(Packet, map(json.loads, lines[1::2])))
    packet_score = sum(
        packet_index
        for packet_index, (left, right) in enumerate(zip(left_packets, right_packets, strict=False), start=1)
        if left < right
    )
    print(f"Sum of correct packet pair indices: {packet_score}")
    assert packet_score in [13, 5340]

    divider_packets = [Packet([[2]]), Packet([[6]])]
    all_packets = left_packets + right_packets + divider_packets
    all_packets.sort()
    divider_indices = [index for index, packet in enumerate(all_packets, start=1) if packet in divider_packets]
    decoder_key = divider_indices[0] * divider_indices[1]
    print(f"Decoder key: {decoder_key}")
    assert decoder_key in [140, 21276]


if __name__ == "__main__":
    run_solution("2022", "dec_13", main)
