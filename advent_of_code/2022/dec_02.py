"""Having done this exercise not long ago, I suspect that the next challenge will be adding 'Lizard' and 'Spock'."""

from enum import IntEnum

from advent_of_code.shared.utils import run_solution


class Choice(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Outcome(IntEnum):
    Win = 6
    Lose = 0
    Draw = 3


defeat_map: dict[Choice, Choice] = {
    Choice.Rock: Choice.Scissors,
    Choice.Paper: Choice.Rock,
    Choice.Scissors: Choice.Paper,
}
reverse_defeat_map = {v: k for k, v in defeat_map.items()}


choice_decryption = {"A": Choice.Rock, "B": Choice.Paper, "C": Choice.Scissors}

reverse_decryption_map: dict[Choice, list[str]] = {
    Choice.Rock: ["A", "X"],
    Choice.Paper: ["B", "Y"],
    Choice.Scissors: ["C", "Z"],
}

decryption_map = {}
for choice, char_list in reverse_decryption_map.items():
    for char in char_list:
        decryption_map[char] = choice

p2_decryption_map = decryption_map.copy()
p2_decryption_map["X"] = Outcome.Lose
p2_decryption_map["Y"] = Outcome.Draw
p2_decryption_map["Z"] = Outcome.Win


def part_1(rps_rounds: list[str]) -> None:
    total_score = 0
    row = 1
    for rps_round in rps_rounds:
        if not rps_round:
            continue

        opponent_str, player_str = rps_round.split(" ")
        opponent, player = decryption_map[opponent_str], decryption_map[player_str]
        round_score = player.value
        if player == opponent:
            round_score += 3
        elif opponent == defeat_map[player]:
            round_score += 6
        total_score += round_score
        print(f"{row} - {round_score}")
        row += 1

    print(total_score)


def part_2(rps_rounds: list[str]) -> None:
    # test_rounds = ["A Y", "B X", "C Z"]
    # rps_rounds = test_rounds

    total_score = 0
    row = 1
    for rps_round in rps_rounds:
        if not rps_round:
            continue

        opponent_str, player_str = rps_round.split(" ")
        opponent, round_outcome = (
            p2_decryption_map[opponent_str],
            p2_decryption_map[player_str],
        )
        round_score = round_outcome.value
        if round_outcome == Outcome.Win:
            player_choice = reverse_defeat_map[opponent]
        elif round_outcome == Outcome.Lose:
            player_choice = defeat_map[opponent]
        elif round_outcome == Outcome.Draw:
            player_choice = opponent
        else:
            raise ValueError

        round_score += player_choice.value
        total_score += round_score
        print(f"{row} - {round_score} - {opponent} v {player_choice}")
        row += 1

    print(total_score)


def main(rps_rounds: list[str]) -> None:
    part_1(rps_rounds)
    part_2(rps_rounds)


if __name__ == "__main__":
    run_solution("2022", "dec_02", main)
