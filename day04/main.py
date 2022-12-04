import fileinput


def contains(p1, p2):
    s1, e1 = p1
    s2, e2 = p2
    return (s2 >= s1 and e2 <= e1) or (s1 >= s2 and e1 <= e2)


def part1(pairs):
    return sum(1 if contains(pa, pb) else 0 for (pa, pb) in pairs)


def part2(pairs):
    def overlaps(p1, p2):
        s1, e1 = p1
        s2, e2 = p2
        return (s1 <= s2 and e1 >= s2) or (s1 <= e2 and e1 >= e2) or contains(p1, p2)

    return sum(1 if overlaps(pa, pb) else 0 for (pa, pb) in pairs)


def parse_line(l):
    def parse_pair(p):
        s, e = map(int, p.split("-"))
        return (s, e)

    p1, p2 = l.split(",")
    return (parse_pair(p1), parse_pair(p2))


if __name__ == "__main__":
    pairs = [parse_line(l) for l in fileinput.input()]
    print(part1(pairs))
    print(part2(pairs))
