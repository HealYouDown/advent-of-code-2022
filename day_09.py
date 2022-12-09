import timer

class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


@timer.timer
def puzzle_1(moves: list[tuple[str, int]]) -> int:
    head = Point(0, 0)
    tail = Point(0, 0)

    direction_move = {
        "R": 1,
        "L": -1,
        "U": -1,
        "D": 1,
    }

    for direction, amount in moves:
        movement = direction_move[direction]
        if direction in ("R", "L"):
            idx = 0
        else:
            idx = 1

        for _ in range(amount):
            head[idx] += movement
            
            # Check if tails is still adjacent to head -> don't update tails
            dx = abs(head.x - tail.x)
            dy = abs(head.y - tail.y)
            is_adjacent = dx <= 1 or dy <= 1
            if is_adjacent:
                continue

            # If the head is ever two steps directly up, down, left, or right
            # from the tail, the tail must also move one step in that
            # direction so it remains close enough
            if dx == 2:
                if dy == 0:  # aligned on horizontal axis
                    tail.x += (1 if (head.x - tail.x) > 0 else -1)
                elif dx == 0 and dx:  # aligned on vertical axis
                    tail.y += (1 if head.y - tail.y > 0 else -1)
                else:
                    # Otherwise, if the head and tail aren't touching
                    # and aren't in the same row or column, the tail
                    # always moves one step diagonally to keep up:
                    
                    #                         #
                    #          -x, -y         #          +x, -y
                    #                         #
                    ##########################S#######################
                    #                         #
                    #          -x, +y         #          +x, +y
                    #                         #

                    # Top left, we have to move down right
                    if tail.x < head.x and tail.y < head.y:
                        move = (1, 1)
                    # Top right, we have to move down left
                    elif tail.x > head.x and tail.y < head.y:
                        move = (-1, 1)
                    

@timer.timer
def puzzle_2(moves: list[tuple[str, int]]) -> int:
    pass


@timer.timer
def parse_input() -> list[tuple[str, int]]:
    moves = []
    with open("inputs/day_09.txt", "r") as fp:
        for line in fp.readlines():
            direction, amount = line.split(" ")
            moves.append((direction, int(amount)))

    return moves


if __name__ == "__main__":
    moves = parse_input()
    print(puzzle_1(moves))
    print(puzzle_2(moves))
