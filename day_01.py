def puzzle_1(data: list[list[int]]) -> int:
    return sum(max(data, key=lambda e: sum(e)))


def puzzle_2(data: list[list[int]]) -> int:
    data_sorted = sorted(data, key=lambda e: sum(e), reverse=True)
    return sum(sum(d) for d in data_sorted[:3])


if __name__ == "__main__":
    with open("inputs/day_01.txt", "r") as fp:
        data = [[int(r) for r in group.splitlines(keepends=False)] for group in fp.read().split("\n\n")]

    print(puzzle_1(data))
    print(puzzle_2(data))
