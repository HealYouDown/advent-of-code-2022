import timer


@timer.timer
def puzzle_1(stream: str) -> int:
    for i in range(len(stream) - 3):
        chars = set(stream[i:i+4])
        if len(chars) == 4:
            return i + 4


@timer.timer
def puzzle_2(stream: str) -> int:
    for i in range(len(stream) - 13):
        chars = set(stream[i:i+14])
        if len(chars) == 14:
            return i + 14


@timer.timer
def parse_input() -> str:
    with open("inputs/day_06.txt", "r") as fp:
        return fp.read().strip()


if __name__ == "__main__":
    stream = parse_input()
    print(puzzle_1(stream))
    print(puzzle_2(stream))
