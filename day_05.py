# DISCLAIMER:
# I was challenged to produce the most useless code around the problem.
# Also I was bored.
import math
import re
from dataclasses import dataclass
from typing import Any, Generic, Literal, Type, TypeVar

import timer

T = TypeVar("T")


@dataclass
class Stack(Generic[T]):
    # The id of the stack
    id: int

    # The current items on the stack. The last element is the top one.
    current_items: list[T]

    @property
    def first(self) -> T:
        """Top most element of the stack.

        Returns:
            T: Top most element.
        """
        return self.current_items[-1]

    def pop(self, n: int = 1) -> list[T]:
        """Removes `n` items from the top of the stack.

        Args:
            n (int, optional): Items to remove. Defaults to 1.

        Returns:
            list[T]: Items removed.
        """
        items = self.current_items[-n:]
        self.current_items = self.current_items[:-n]
        return items

    def add(self, items: list[T]) -> None:
        """Adds the given `items` to the top of the stack in the
        same order as given.

        Args:
            items (list[T]): Items to add to the stack.
        """
        self.current_items.extend(items)

    def add_reversed(self, items: list[T]) -> None:
        """Adds the given `items` to the top of the stack
        in reversed order.

        Args:
            items (list[T]): Items to add to the stack.
        """
        self.current_items.extend(items[::-1])


@dataclass
class StackList(Generic[T]):
    # The stacks that should be re-arranged
    stacks: list[Stack[T]]

    @classmethod
    def parse_from_input(cls: Type["StackList"], block: str) -> "StackList[str]":
        # Removes the numbering row below
        rows = block.splitlines()[:-1]

        # Parses each stack vertically
        stacks = []
        number_of_columns = math.ceil(len(rows[0])/4)
        for i in range(number_of_columns):
            stack: list[str] = []
            for row in rows:
                char = row[i*4 + 1 : i*4 + 2].strip()
                if char:
                    stack.append(char)
            
            # Reverse the items so that the top parsed on is at the end of
            # the list
            stacks.append(Stack[str](id=i+1, current_items=stack[::-1]))

        return cls[str](stacks=stacks)

    def get_stack(self, stack_id: int) -> Stack[T]:
        """Returns the stack with the given `stack_id`

        Args:
            stack_id (int): `stack_id` to search for.

        Returns:
            Stack[T]: Stack with the given id.

        Raises:
            ValueError: The stack could not be found.
        """
        stack = [s for s in self.stacks if s.id == stack_id]
        if not stack:
            raise ValueError(f"Stack with the id {stack_id} could not be found.")
        return stack[0]

    def apply_instruction(
        self,
        instruction: "Instruction",
        crane_model: Literal["CrateMover 9000", "CrateMover 9001"]
    ) -> None:
        """Applies the given instruction to the stack list.

        Args:
            instruction (Instruction): The instruction to apply
            crane_model (Literal['CrateMover 9000', 'CrateMover 9001']):
                The model of the crane. Depending on the model, the crane
                will re-apply the picked up items in different order.

        Raises:
            ValueError: Unknown crane model given.
        """
        stack_from = self.get_stack(instruction.from_)
        stack_to = self.get_stack(instruction.to)

        items = stack_from.pop(n=instruction.amount)

        if crane_model == "CrateMover 9000":
            stack_to.add_reversed(items)
        elif crane_model == "CrateMover 9001":
            stack_to.add(items)
        else:
            raise ValueError(f"Unknown crane model {crane_model}.")


@dataclass
class Instruction:
    # The amount of items to remove
    amount: int

    # From which stack to remove the items
    from_: Stack

    # To which stack to add the removed items
    to: Stack

    @classmethod
    def parse_from_row(cls: Type["Instruction"], row: str) -> "Instruction":
        pattern = r"move (?P<amount>\d{1,}) from (?P<from>\d{1,}) to (?P<to>\d{1,})"
        parsed = re.match(pattern, row).groupdict()
        return cls(amount=int(parsed["amount"]), from_=int(parsed["from"]), to=int(parsed["to"]))


@timer.timer
def puzzle_1(stack_list: StackList[Any], instructions: list[Instruction]) -> int:
    for instruction in instructions:
        stack_list.apply_instruction(instruction, "CrateMover 9000")

    return "".join(s.first for s in stack_list.stacks)


@timer.timer
def puzzle_2(stack_list: StackList[Any], instructions: list[Instruction]) -> int:
    for instruction in instructions:
        stack_list.apply_instruction(instruction, "CrateMover 9001")

    return "".join(s.first for s in stack_list.stacks)


@timer.timer
def parse_input() -> tuple[StackList, list[Instruction]]:
    with open("inputs/day_05.txt", "r") as fp:
        raw_stacks, raw_instructions = fp.read().split("\n\n")

    instructions = [Instruction.parse_from_row(row) for row in raw_instructions.splitlines()]
    stack = StackList.parse_from_input(raw_stacks)

    return stack, instructions


if __name__ == "__main__":
    stack, instructions = parse_input()
    print(puzzle_1(stack, instructions))
    
    # Parse again because the first stack object was modified
    stack, instructions = parse_input()
    print(puzzle_2(stack, instructions))
