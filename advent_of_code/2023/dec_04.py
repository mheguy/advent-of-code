from collections import defaultdict

from advent_of_code.shared.utils import run_solution


def main(cards: list[str]) -> None:
    card_count = defaultdict(lambda: 1)
    p1_total = 0

    for card_num, card in enumerate(cards, 1):
        win_nums, our_nums = card.split(":")[1].split("|")

        win_nums = [int(n) for n in win_nums.split(" ") if n != ""]
        our_nums = [int(n) for n in our_nums.split(" ") if n != ""]

        winning_matches = 0
        for num in our_nums:
            if num in win_nums:
                winning_matches += 1

        if winning_matches:
            p1_total += 2 ** (winning_matches - 1)

            for i in range(1, winning_matches + 1):
                card_count[card_num + i] += card_count[card_num]

    p2_total = 0
    for i in range(1, len(cards) + 1):
        p2_total += card_count[i]

    print(p1_total)
    print(p2_total)


if __name__ == "__main__":
    run_solution("2023", "dec_04", main)
