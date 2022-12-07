import fileinput
import json


def parse_tree(cmds, i):
    tree = dict()
    while i < len(cmds):
        _, *parts = cmds[i].split(" ")
        if parts[0] == "cd":
            if parts[1] == "..":
                return i + 1, tree
            i, tree[parts[1]] = parse_tree(cmds, i + 1)
        elif parts[0] == "ls":
            i += 1
            while i < len(cmds) and cmds[i][0] != "$":
                maybe_size, name = cmds[i].split()
                if maybe_size != "dir":
                    tree[name] = int(maybe_size)
                i += 1
    return i, tree


def traverse(tree, f):
    if isinstance(tree, int):
        f("file", tree)
        return tree
    else:
        siz = sum(traverse(c, f) for c in tree.values())
        f("dir", siz)
        return siz


def sum_dirs(tree, max_size=float("Inf")):
    sizes = []
    traverse(tree, lambda type, size: sizes.append((type, size)))
    return sum(size for type, size in sizes if size <= max_size if type == "dir")


def find_dir(tree):
    sizes = []
    total_size = traverse(tree, lambda type, size: sizes.append((type, size)))
    return min(
        s
        for type, s in sizes
        if type == "dir" and 70_000_000 - total_size + s > 30_000_000
    )


if __name__ == "__main__":
    cmds = [l.strip() for l in fileinput.input()]
    i, tree = parse_tree(cmds, 0)
    print(json.dumps(tree, indent=2))
    print(sum_dirs(tree["/"], max_size=100000))
    print(find_dir(tree["/"]))
