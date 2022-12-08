def part1(trees):
    output = [[False for _ in row] for row in trees]
    H, W = len(trees), len(trees[0])
    for row_n in range(H):
        # left-right.
        max_ = -1
        for col_n in range(W):
            output[row_n][col_n] |= trees[row_n][col_n] > max_
            max_ = max(max_, trees[row_n][col_n])
        # right-left.
        max_ = -1
        for col_n in range(W - 1, -1, -1):
            output[row_n][col_n] |= trees[row_n][col_n] > max_
            max_ = max(max_, trees[row_n][col_n])
    for col_n in range(len(trees[0])):
        # top-bottom.
        max_ = -1
        for row_n in range(H):
            output[row_n][col_n] |= trees[row_n][col_n] > max_
            max_ = max(max_, trees[row_n][col_n])
        # bottom-top.
        max_ = -1
        for row_n in range(H - 1, -1, -1):
            output[row_n][col_n] |= trees[row_n][col_n] > max_
            max_ = max(max_, trees[row_n][col_n])

    return sum(c for row in output for c in row)


def count_while_shorter(grid, row, col, dy, dx):
    H, W = len(trees), len(trees[0])
    count = 0
    i, j = row + dy, col + dx
    while i >= 0 and i < H and j >= 0 and j < W:
        count += 1
        if grid[i][j] >= grid[row][col]:
            return count
        i, j = i + dy, j + dx
    return count


def part2(trees):
    H, W = len(trees), len(trees[0])
    out = [[1 for _ in row] for row in trees]
    for row in range(H):
        for col in range(W):
            prod = 1
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                prod *= count_while_shorter(trees, row, col, dy, dx)
            out[row][col] = prod
    return max(c for row in out for c in row)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        trees = [[int(d) for d in l.strip()] for l in f]

    print(part1(trees))
    print(part2(trees))
