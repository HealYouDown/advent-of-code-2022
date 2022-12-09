from typing import Literal, Union

import timer

DIRECTION = str
AMOUNT = int
MOVES = list[tuple[DIRECTION, AMOUNT]]


class Knot:
    def __init__(self, predecessor: Union["Knot", None]) -> None:
        self._predecessor = predecessor

        self._x = 0
        self._y = 0

        self._field_visited: list[tuple[int, int]] = [(self._x, self._y)]

    @property
    def position(self) -> tuple[int, int]:
        return self._x, self._y

    @property
    def unique_visited_count(self) -> int:
        return len(set(self._field_visited))

    def move(self, direction: Literal["R", "L", "U", "D"]) -> None:
        if direction == "R":
            self._x += 1
        elif direction == "L":
            self._x += -1
        elif direction == "U":
            self._y += -1
        elif direction == "D":
            self._y += 1

    def follow(self) -> None:
        assert self._predecessor is not None, "Head can't follow any knot"
        px, py = self._predecessor.position

        # Check if adjacent to predecessor knot
        dx = abs(px - self._x)
        dy = abs(py - self._y)
        is_adjacent = dx <= 1 and dy <= 1
        if is_adjacent:
            return

        #                         #
        #          -x, -y         #          +x, -y
        #                         #
        ##########################H#######################
        #                         #
        #          -x, +y         #          +x, +y
        #                         #

        # If the head is ever two steps directly up, down, left, or right
        # from the tail, the tail must also move one step in that
        # direction so it remains close enough
        if dy == 0:  # aligned on horizontal axis
            self._x += (1 if (px - self._x) > 0 else -1)
        elif dx == 0:  # aligned on vertical axis
            self._y += (1 if py - self._y > 0 else -1)
        else:
            # Otherwise, if the head and tail aren't touching
            # and aren't in the same row or column, the tail
            # always moves one step diagonally to keep up:

            # Top left, we have to move down right
            if self._x < px and self._y < py:
                move = (1, 1)
            # Top right, we have to move down left
            elif self._x > px and self._y < py:
                move = (-1, 1)
            # Bottom left, we have to move top right
            elif self._x < px and self._y > py:
                move = (1, -1)
            # Bottom right, we have to move top left
            elif self._x > px and self._y > py:
                move = (-1, -1)
            
            self._x += move[0]
            self._y += move[1]

        self._field_visited.append((self._x, self._y))


@timer.timer
def puzzle_1(moves: MOVES) -> None:
    head = Knot(predecessor=None)
    tail = Knot(predecessor=head)

    for direction, amount in moves:
        for _ in range(amount):
            head.move(direction)
            tail.follow()

    return tail.unique_visited_count


@timer.timer
def puzzle_2(moves: MOVES) -> int:
    head = Knot(predecessor=None)

    in_between_knots: list[Knot] = []
    for _ in range(8):
        previous_knot = head if not in_between_knots else in_between_knots[-1]
        in_between_knots.append(Knot(predecessor=previous_knot))
    
    tail = Knot(predecessor=in_between_knots[-1])

    for direction, amount in moves:
        for _ in range(amount):
            head.move(direction)
            for knot in in_between_knots:
                knot.follow()
            tail.follow()

    return tail.unique_visited_count


@timer.timer
def parse_input() -> MOVES:
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
