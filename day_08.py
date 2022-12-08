import timer

GRID = list[list[int]]


def is_edge(grid: GRID, index: tuple[int, int]):
    x, y = index
    return x == 0 or x == len(grid[0]) - 1 or y == 0 or y == len(grid) - 1


def is_visible(grid: GRID, index: tuple[int, int]) -> bool:
    # outer border is always visible, no matter the height
    if is_edge(grid, index):
        return True

    x, y = index
    height = grid[y][x]

    # Consider all trees towards the edge
    is_visible_left = all(j < height for j in grid[y][:x])
    is_visible_right = all(j < height for j in grid[y][x+1:])
    is_visible_top = all(j < height for j in [grid[k][x] for k in range(0, y)])
    is_visible_bottom = all(j < height for j in [grid[k][x] for k in range(y+1, len(grid))])

    is_visible = is_visible_left or is_visible_right or is_visible_top or is_visible_bottom
    return is_visible


def calculate_scenic_score(grid: GRID, index: tuple[int, int]) -> int:
    # outer border will result in a viewing distance of 0, so our end product
    # would be 0 anyways, so we can return it without doing other checks
    if is_edge(grid, index):
        return 0

    x, y = index
    height = grid[y][x]

    def count_viewable_trees(height: int, trees: list[int]) -> int:
        # counts viewable trees in order of the list `trees`.
        count = 0
        for tree in trees:
            if tree < height:
                count += 1
            else:  # while the tree is higher, it can still be seen
                count += 1
                break

        return count

    # Check the trees on all cardinal directions.
    trees_left = count_viewable_trees(height, reversed(grid[y][:x]))
    trees_right = count_viewable_trees(height, grid[y][x+1:])
    trees_top = count_viewable_trees(height, reversed([grid[k][x] for k in range(0, y)]))
    trees_bottom = count_viewable_trees(height, [grid[k][x] for k in range(y+1, len(grid))])

    return trees_left * trees_right * trees_top * trees_bottom


@timer.timer
def puzzle_1(grid: GRID) -> int:
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            count += is_visible(grid, (x, y))

    return count


@timer.timer
def puzzle_2(grid: GRID) -> int:
    biggest_scenic_score = -1
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            scenic_score = calculate_scenic_score(grid, (x, y))
            if scenic_score >= biggest_scenic_score:
                biggest_scenic_score = scenic_score

    return biggest_scenic_score


@timer.timer
def parse_input() -> GRID:
    with open("inputs/day_08.txt", "r") as fp:
        return [[int(j) for j in row.strip()] for row in fp.readlines()]


if __name__ == "__main__":
    grid = parse_input()
    print(puzzle_1(grid))
    print(puzzle_2(grid))
