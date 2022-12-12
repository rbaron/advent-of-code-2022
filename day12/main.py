from collections import defaultdict


def loc(grid, pos):
    y, x = pos
    return grid[y][x]


def height(grid, pos):
    l = loc(grid, pos)
    return ord("z" if l == "E" else "a" if l == "S" else l)


def neighbors(grid, pos):
    y, x = pos
    H, W = len(grid), len(grid[0])
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        ny, nx = neighbor_pos = (y + dy, x + dx)
        if 0 <= ny < H and 0 <= nx < W:
            yield neighbor_pos


def lo_neighbors(grid, pos):
    return (n for n in neighbors(grid, pos) if height(grid, n) <= height(grid, pos) + 1)


def hi_neighbors(grid, pos):
    return (n for n in neighbors(grid, pos) if height(grid, n) + 1 >= height(grid, pos))


def shortest_path(grid, pos, target, gen_neighbors):
    dist = defaultdict(lambda: float("inf"), {pos: 0})
    q = {(y, x) for y in range(len(grid)) for x in range(len(grid[0]))}
    while q:
        u = min(q, key=lambda n: dist[n])
        q.remove(u)
        if loc(grid, u) == target:
            return dist[u]
        for n in gen_neighbors(grid, u):
            if n not in q:
                continue
            alt = dist[u] + 1
            if alt < dist[n]:
                dist[n] = alt

    raise Exception("No path exists")


def find_pos(pos):
    return next(
        (row, col)
        for row, line in enumerate(grid)
        for col, c in enumerate(line)
        if c == pos
    )


def part1(grid):
    return shortest_path(grid, find_pos("S"), "E", lo_neighbors)


def part2(grid):
    return shortest_path(grid, find_pos("E"), "a", hi_neighbors)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        grid = [l.strip() for l in f]

    print(part1(grid))
    print(part2(grid))
