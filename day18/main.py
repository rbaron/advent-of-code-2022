from collections import deque


def add(p1, p2):
    return tuple(a + b for a, b in zip(p1, p2))


def neighbors(cube):
    for delta in [-1, 1]:
        yield add(cube, (delta, 0, 0))
        yield add(cube, (0, delta, 0))
        yield add(cube, (0, 0, delta))


def part1(cubes):
    return sum(n not in cubes for cube in cubes for n in neighbors(cube))


def flood_fill(cubes, z0, z1, y0, y1, x0, x1):
    queue = deque([(z0 - 1, y0, x0)])
    seen = set()
    touches = 0
    while queue:
        p = queue.popleft()
        assert p not in cubes
        if p in seen:
            continue
        seen.add(p)
        touches += sum(1 for n in neighbors(p) if n in cubes)
        for n in neighbors(p):
            nz, ny, nx = n
            if (
                z0 - 1 <= nz <= z1 + 1
                and y0 - 1 <= ny <= y1 + 1
                and x0 - 1 <= nx <= x1 + 1
                and n not in cubes
                and n not in seen
            ):
                queue.append(n)
    return touches


def part2(cubes):
    z0, y0, x0 = map(min, zip(*cubes))
    z1, y1, x1 = map(max, zip(*cubes))
    return flood_fill(cubes, z0, z1, y0, y1, x0, x1)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        cubes = set(tuple(int(n) for n in l.split(",")) for l in f)

    print(part1(cubes))
    print(part2(cubes))
