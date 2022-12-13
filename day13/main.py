import functools
import math


def compare(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return p1 - p2
    elif isinstance(p1, int):
        return compare([p1], p2)
    elif isinstance(p2, int):
        return compare(p1, [p2])
    elif len(p1) == 0 or len(p2) == 0:
        return len(p1) - len(p2)
    return compare(p1[0], p2[0]) or compare(p1[1:], p2[1:])


def part1(pairs):
    return sum(index + 1 for index, pair in enumerate(pairs) if compare(*pair) < 0)


def part2(pairs):
    sorted_pairs = sorted(
        [el for pair in pairs for el in pair] + [[[2]], [[6]]],
        key=functools.cmp_to_key(compare),
    )
    return math.prod(
        i + 1
        for i, el in enumerate(sorted_pairs)
        if compare(el, [[2]]) == 0 or compare(el, [[6]]) == 0
    )


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        pairs = [
            # Yolo
            tuple(eval(el, None, None) for el in pair.split("\n"))
            for pair in f.read().split("\n\n")
        ]

    print(part1(pairs))
    print(part2(pairs))
