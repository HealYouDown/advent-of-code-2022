# Enemy:
# A = Rock
# B = Paper
# C = Scissors

# Me:
# X = Rock
# Y = Paper
# Z = Scissors

# Part 2: Ending
# X = Lose
# Y = Draw
# Z = Win


def puzzle_1(rounds: list[tuple[str, str]]) -> int:
    score = 0
    for round in rounds:
        enemy_move, my_move = round

        is_win = (
            enemy_move == "A" and my_move == "Y" or
            enemy_move == "B" and my_move == "Z" or
            enemy_move == "C" and my_move == "X"
        )
        is_draw = (
            enemy_move == "A" and my_move == "X" or
            enemy_move == "B" and my_move == "Y" or
            enemy_move == "C" and my_move == "Z"
        )

        if my_move == "X":
            score += 1
        elif my_move == "Y":
            score += 2
        elif my_move == "Z":
            score += 3

        if is_win:
            score += 6
        elif is_draw:
            score += 3

    return score


def puzzle_2(rounds: list[tuple[str, str]]) -> int:
    score = 0
    for round in rounds:
        enemy_move, required_ending = round

        score_winning = {
            # Rock vs Paper
            "A": 2,
            # Paper vs Scissors
            "B": 3,
            # Scissors vs Rock
            "C": 1,
        }
        score_drawing = {
            "A": 1,
            "B": 2,
            "C": 3,
        }
        score_losing = {
            "A": 3,
            "B": 1,
            "C": 2,
        }

        if required_ending == "X":
            score += score_losing[enemy_move]
        elif required_ending == "Y":
            score += score_drawing[enemy_move]
            score += 3
        elif required_ending == "Z":
            score += score_winning[enemy_move]
            score += 6

    return score


if __name__ == "__main__":
    with open("inputs/day_02.txt", "r") as fp:
        rounds = [tuple(row.strip().split(" ")) for row in fp.readlines()]

    print(puzzle_1(rounds))
    print(puzzle_2(rounds))
