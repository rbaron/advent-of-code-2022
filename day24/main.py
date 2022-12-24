from collections import deque


def add(p1, p2):
    return tuple(a + b for a, b in zip(p1, p2))


def print_grid(pos, grid):
    H, W = len(grid), len(grid[0])
    print("#" * (W + 2))
    for y, l in enumerate(grid):
        print("#", end="")
        for x, col in enumerate(l):
            if pos == (y, x):
                assert len(col) == 0
                print("E", end="")
            elif len(col) == 0:
                print(".", end="")
            else:
                print(col[0] if len(col) == 1 else len(col), end="")
        print("#")
    print("#" * (W + 2))


def step_grid(grid):
    H, W = len(grid), len(grid[0])
    new_grid = [[[] for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            for e in grid[y][x]:
                if e in "#":
                    new_grid[y][x].append("#")
                    continue
                elif e == ">":
                    new_grid[y][(x + 1) % W].append(e)
                elif e == "<":
                    new_grid[y][(x - 1) % W].append(e)
                elif e == "^":
                    new_grid[(y - 1) % H][x].append(e)
                elif e == "v":
                    new_grid[(y + 1) % H][x].append(e)
    return new_grid


DIRS_FORW = [(1, 0), (0, 1), (0, 0), (0, -1), (-1, 0)]
DIRS_BACK = DIRS_FORW[::-1]


def neighbors(pos, dirs):
    for d in dirs:
        yield add(pos, d)


def find_path(start, grid, goal, dirs):
    H, W = len(grid), len(grid[0])
    queue = deque([(start, grid, 0)])
    seen_states = set()
    while queue:
        pos, grid, time = queue.popleft()
        key = (pos, tuple(tuple(c for c in r) for l in grid for r in l))
        if key in seen_states:
            continue
        seen_states.add(key)
        grid = step_grid(grid)

        for ny, nx in neighbors(pos, dirs):
            new_state = ((ny, nx), grid, time + 1)
            if (ny, nx) == goal:
                return time + 1, goal, step_grid(grid)
            elif 0 <= ny < H and 0 <= nx < W and len(grid[ny][nx]) == 0:
                queue.append(new_state)
            elif (ny, nx) == start:
                queue.append(new_state)


if __name__ == "__main__":
    with open("test-input.txt", "r") as f:
        grid = [
            [[] if c == "." else [c] for c in l.strip()[1:-1]]
            for l in f.read().split("\n")[1:-1]
        ]

    total_steps = 0
    H, W = len(grid), len(grid[0])
    steps, goal, grid = find_path((-1, 0), grid, (H, W - 1), DIRS_FORW)
    print(steps)
    total_steps += steps
    steps, goal, grid = find_path((H, W - 1), grid, (-1, 0), DIRS_BACK)
    total_steps += steps + 1
    steps, goal, grid = find_path((-1, 0), grid, (H, W - 1), DIRS_FORW)
    total_steps += steps + 1
    print(total_steps)
