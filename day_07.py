from anytree import Node, RenderTree, AsciiStyle, PreOrderIter


def puzzle_1(root: Node) -> int:
    folder_to_size = {}
    for root_node in PreOrderIter(root, filter_=lambda n: n.type == "dir"):
        folder_to_size[root_node.name] = sum(
            n.size for n in PreOrderIter(root_node, filter_=lambda n: n.type == "file")
        )

    return sum(v for v in folder_to_size.values() if v <= 100_000)


def puzzle_2(root: Node) -> int:
    pass


with open("inputs/day_07.txt", "r") as fp:
    root = Node("/", type="dir")
    current_node: Node = None

    for line in fp.read().splitlines(keepends=False):
        if line.startswith("$"):
            cmd, *args = line[2:].split(" ")
            if cmd == "cd":
                folder_name = args[0]
                if folder_name == "/":
                    current_node = root
                elif folder_name == "..":
                    if current_node is None:
                        current_node = root  # Can't go higher than root
                    else:
                        current_node = current_node.parent
                else:
                    current_node = [c for c in current_node.children if c.name == folder_name][0]
            elif cmd == "ls":
                pass

        else:
            arg1, arg2 = line.split(" ")
            if arg1 == "dir":
                kwargs = {"type": "dir"}
            else:
                kwargs = {"type": "file", "size": int(arg1)}

            Node(name=arg2, parent=current_node, **kwargs)

    # print(RenderTree(root, style=AsciiStyle()).by_attr())
    print(puzzle_1(root))
