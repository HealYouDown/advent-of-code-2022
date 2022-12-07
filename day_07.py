from typing import Optional


class Node:
    def __init__(self, parent: Optional["Node"] = None) -> None:
        self.parent = parent
        self.children: list[Node] = []

        if parent is not None:
            self.parent.children.append(self)


class Dir(Node):
    def __init__(self, *, parent: Optional["Node"] = None, name: str) -> None:
        self.name = name
        super().__init__(parent=parent)

    def __repr__(self) -> str:
        return f"Dir(name={repr(self.name)})"


class File(Node):
    def __init__(self, *, parent: Optional["Node"] = None, name: str, size: int) -> None:
        self.name = name
        self.size = size
        super().__init__(parent=parent)

    def __repr__(self) -> str:
        return f"File(name={repr(self.name)}, size={repr(self.size)})"


def get_all_files_for_dir(dir: Node) -> list[File]:
    files = []
    for node in dir.children:
        if isinstance(node, Dir):
            files.extend(get_all_files_for_dir(node))
        elif isinstance(node, File):
            files.append(node)

    return files


def get_all_dirs(root: Node) -> list[Dir]:
    dirs = []
    for node in root.children:
        if isinstance(node, Dir):
            dirs.append(node)
            dirs.extend(get_all_dirs(node))

    return dirs


def puzzle_1(root: Node) -> int:
    total_size = 0
    for dir in [root, *get_all_dirs(root)]:
        dir_size = sum(f.size for f in get_all_files_for_dir(dir))
        if dir_size <= 100_000:
            total_size += dir_size 

    return total_size


def puzzle_2(root: Node) -> int:
    # available space: 70_000_000
    # required space to update: 30_000_000
    total_space_used = sum(f.size for f in get_all_files_for_dir(root))
    unused_space = 70_000_000 - total_space_used
    required_space = 30_000_000 - unused_space

    min_folder_size = float("inf")
    for dir in [root, *get_all_dirs(root)]:
        dir_size = sum(f.size for f in get_all_files_for_dir(dir))
        # Check if dir would free up enough space to run the update
        if dir_size >= required_space and dir_size < min_folder_size:
            min_folder_size = dir_size

    return min_folder_size


if __name__ == "__main__":
    with open("inputs/day_07.txt", "r") as fp:
        root = Dir(parent=None, name="/")
        current_node: Node = None

        for line in fp.read().splitlines(keepends=False):
            if line.startswith("$"):
                cmd, *args = line[2:].split(" ")
                if cmd == "cd":
                    dir_name = args[0]
                    if dir_name == "/":
                        current_node = root
                    elif dir_name == "..":
                        if current_node is None:
                            current_node = root  # Can't go higher than root
                        else:
                            current_node = current_node.parent
                    else:
                        current_node = [c for c in current_node.children if c.name == dir_name][0]
                elif cmd == "ls":
                    pass

            else:
                arg1, arg2 = line.split(" ")
                if arg1 == "dir":
                    Dir(parent=current_node, name=arg2)
                else:
                    File(parent=current_node, name=arg2, size=int(arg1))

        print(puzzle_1(root))
        print(puzzle_2(root))
