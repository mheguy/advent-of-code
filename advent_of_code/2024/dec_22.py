from advent_of_code.shared.utils import run_solution

Lines = list[str]


def main(lines: Lines) -> None:
    result = 0

    for line in lines:
        if not line:
            continue

        num = int(line)

        for _ in range(2000):
            tmp_num = num * 64
            tmp_num = tmp_num ^ num
            num = tmp_num % 16777216

            tmp_num = num // 32
            tmp_num = tmp_num ^ num
            num = tmp_num % 16777216

            tmp_num = num * 2048
            tmp_num = tmp_num ^ num
            num = tmp_num % 16777216

        result += num

    print(result)


if __name__ == "__main__":
    run_solution("2024", "dec_22", main)
