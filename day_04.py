def get_range_from_string(s: str) -> set[int]:
    a, b = [int(i) for i in s.split("-")]
    return set(range(a, b+1))


def puzzle_1(pairs: list[tuple[str, str]]) -> int:
    counter = 0
    for a, b in pairs:
        range_a = get_range_from_string(a)
        range_b = get_range_from_string(b)

        if (range_a.intersection(range_b) == range_a
                or range_b.intersection(range_a) == range_b):
            counter += 1

    return counter


def puzzle_2(pairs: list[tuple[str, str]]) -> int:
    counter = 0
    for a, b in pairs:
        range_a = get_range_from_string(a)
        range_b = get_range_from_string(b)

        is_overlapping = len(range_a.intersection(range_b)) != 0
        if is_overlapping:
            counter += 1

    return counter


if __name__ == "__main__":
    with open("inputs/day_04.txt", "r") as fp:
        pairs = [r.strip().split(",") for r in fp.readlines()]

    print(puzzle_1(pairs))
    print(puzzle_2(pairs))
