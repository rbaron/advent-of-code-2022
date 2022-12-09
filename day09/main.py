DIR = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}


def add(p1, p2):
    return tuple(map(lambda p: p[0] + p[1], zip(p1, p2)))


def diff(p1, p2):
    return add(p1, map(lambda p: -p, p2))


def direction(v):
    y, x = v
    return (y // abs(y or 1), x // abs(x or 1))


def move_tail(h, t):
    d = dy, dx = diff(h, t)
    if abs(dy) <= 1 and abs(dx) <= 1:
        return t
    else:
        return add(t, direction(d))


def part1(moves):
    h = t = (0, 0)
    seen = set([t])
    for dir, steps in moves:
        for _ in range(steps):
            h = add(h, DIR[dir])
            t = move_tail(h, t)
            seen.add(t)
    return len(seen)


def part2(moves):
    knots = [(0, 0) for _ in range(10)]
    seen = set(knots[-1:])
    for dir, steps in moves:
        for _ in range(steps):
            knots[0] = add(knots[0], DIR[dir])
            for i in range(1, len(knots)):
                knots[i] = move_tail(knots[i - 1], knots[i])
            seen.add(knots[-1])
    return len(seen)


if __name__ == "__main__":

    def parse_line(line):
        d, n = line.split(" ")
        return (d, int(n))

    with open("input.txt", "r") as f:
        moves = [parse_line(l) for l in f]

    print(part1(moves))
    print(part2(moves))
