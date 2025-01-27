from collections import deque

from advent_of_code.shared.utils import run_solution

CYPHER_LENGTH = 4


def main(lines: list[str]) -> None:
    input_text = lines[0]
    cypher = deque([], CYPHER_LENGTH)
    for pos, char in enumerate(input_text, start=1):
        cypher.append(char)
        if len(set(cypher)) == CYPHER_LENGTH:
            print(pos)
        break


if __name__ == "__main__":
    run_solution("2022", "dec_06", main)
