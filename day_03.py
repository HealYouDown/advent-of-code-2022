import string

import timer

CHAR_TO_SCORE = {char: i for i, char in enumerate(string.ascii_letters, start=1)}


@timer.timer
def puzzle_1(backpacks: list[str]) -> int:
    score = 0
    for backpack in backpacks:

        c1 = set(backpack[:len(backpack)//2])
        c2 = set(backpack[len(backpack)//2:])

        duplicate = c1.intersection(c2).pop()
        score += CHAR_TO_SCORE[duplicate]

    return score


@timer.timer
def puzzle_2(backpacks: list[str]) -> int:
    score = 0
    for i in range(len(backpacks)//3):
        a, b, c = [set(b) for b in backpacks[i*3:i*3+3]]

        duplicate = a.intersection(b).intersection(c).pop()
        score += CHAR_TO_SCORE[duplicate]

    return score


@timer.timer
def parse_input() -> list[str]:
    with open("inputs/day_03.txt", "r") as fp:
        return [r.strip() for r in fp.readlines()]


if __name__ == "__main__":
    backpacks = parse_input()
    print(puzzle_1(backpacks))
    print(puzzle_2(backpacks))
