# ruff: noqa: PLR2004
from collections import Counter
from operator import itemgetter

from advent_of_code.shared.utils import run_solution

CARD_FACES = "123456789TJQKA"
CARD_VALUES = {k: i for i, k in enumerate(CARD_FACES, 1)}
CARD_VALUES_WITH_JOKERS = CARD_VALUES.copy()
CARD_VALUES_WITH_JOKERS["J"] = 0

Hand = tuple[int, int, int, int, int]
HandType = int
Bet = int
HandInfo = tuple[HandType, Hand, Bet]

HandStrength = tuple[int, *Hand]


def main(lines: list[str]) -> None:
    hand_infos = convert_to_hand_info(lines, False)

    p1_total = 0
    for rank, hand in enumerate(sorted(hand_infos, key=itemgetter(0, 1)), start=1):
        p1_total += rank * hand[2]

    hand_infos = convert_to_hand_info(lines, True)
    p2_total = 0
    for rank, hand in enumerate(sorted(hand_infos, key=itemgetter(0, 1)), start=1):
        p2_total += rank * hand[2]

    print(f"{p1_total=}")
    print(f"{p2_total=}")


def convert_to_hand_info(lines: list[str], jokers_enabled: bool) -> list[HandInfo]:
    hand_bets = []
    for line in lines:
        hand, bet = line.split()

        if jokers_enabled:
            numerical_hand = Hand(CARD_VALUES_WITH_JOKERS[c] for c in hand)
        else:
            numerical_hand = Hand(CARD_VALUES[c] for c in hand)

        hand_type, *_ = calculate_hand_strength(numerical_hand, jokers_enabled)
        hand_bets.append([hand_type, numerical_hand, int(bet)])
    return hand_bets


def calculate_hand_strength(hand: Hand, jokers_enabled: bool) -> HandStrength:
    counter = Counter(hand)

    if jokers_enabled:
        # Deal with jokers
        joker_count = counter[0]
        counter[0] = 0
        most_freq_value = counter.most_common(1)[0][0]
        counter[most_freq_value] += joker_count

    frequency = counter.most_common()
    sorted_freq = sorted(frequency, key=itemgetter(1, 0), reverse=True)

    # I implemented this because I read the instructions too quickly and thought
    # we needed to follow the real rules for evaluating poker hands.
    sorted_hand = []
    for card, freq in sorted_freq:
        sorted_hand.extend([card for _ in range(freq)])

    top_freq = frequency[0][1]

    try:
        second_freq = frequency[1][1]
    except IndexError:
        second_freq = 0

    hand_power = 0  # High card

    if top_freq == 5:
        hand_power = 6  # Five of a kind
    elif top_freq == 4:
        hand_power = 5  # Four of a kind
    elif top_freq == 3:
        if second_freq == 2:
            hand_power = 4  # Full house
        else:
            hand_power = 3  # Three of a kind
    elif top_freq == 2:
        if second_freq == 2:
            hand_power = 2  # Two pairs
        else:
            hand_power = 1  # One pair

    return (hand_power, *sorted_hand)


if __name__ == "__main__":
    run_solution("2023", "dec_07", main)
