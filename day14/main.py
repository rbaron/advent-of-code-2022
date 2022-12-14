def part1(grid):
    maxy = max(y for y, _ in grid)
    while True:
        sy, sx = 0, 500
        while True:
            if (p := (sy + 1, sx)) not in grid:
                sy, sx = p
                if sy > maxy:
                    return sum(v == "o" for v in grid.values())
            elif (p := (sy + 1, sx - 1)) not in grid:
                sy, sx = p
            elif (p := (sy + 1, sx + 1)) not in grid:
                sy, sx = p
            else:
                grid[(sy, sx)] = "o"
                break


class FlooredGrid(dict):
    def __init__(self, grid):
        self.maxy = max(y for y, _ in grid)
        super().__init__(grid)

    def __contains__(self, key):
        return key[0] == self.maxy + 2 or super().__contains__(key)


def part2(grid):
    grid = FlooredGrid(grid)
    while True:
        sy, sx = 0, 500
        while True:
            if (p := (sy + 1, sx)) not in grid:
                sy, sx = p
            elif (p := (sy + 1, sx - 1)) not in grid:
                sy, sx = p
            elif (p := (sy + 1, sx + 1)) not in grid:
                sy, sx = p
            else:
                if sy == 0:
                    return sum(v == "o" for v in grid.values())
                grid[(sy, sx)] = "o"
                break


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = [
            [tuple(int(p) for p in pair.split(",")) for pair in l.split(" -> ")]
            for l in f
        ]

    def range_inc(a, b):
        return range(a, b + 1) if a <= b else range(b, a + 1)

    grid = {
        (y, x): "#"
        for line in lines
        for (p1x, p1y), (p2x, p2y) in zip(line, line[1:])
        for y in range_inc(p1y, p2y)
        for x in range_inc(p1x, p2x)
    }

    print(part1(grid))
    print(part2(grid))
