import re
import sys

sys.setrecursionlimit(10000)

ROT = {
    "R": {"u": "r", "r": "d", "d": "l", "l": "u"},
    "L": {"u": "l", "l": "d", "d": "r", "r": "u"},
}


def walk(y, x, dir, instrs, tiles):
    # print(y, x, dir)
    if not instrs:
        return y, x, dir

    # print(instrs)

    next_instr, *remaining = instrs
    if next_instr in ROT:
        # print(f"Turn {next_instr}, now facing {ROT[next_instr][dir]}")
        return walk(y, x, ROT[next_instr][dir], remaining, tiles)

    # print(f"Will try to walk {next_instr} in direction {dir}")
    match dir:
        case "u":
            for _ in range(next_instr):
                nxt_pos = (y - 1) % len(tiles)
                while tiles[nxt_pos][x] == " ":
                    nxt_pos = (nxt_pos - 1) % len(tiles)
                if tiles[nxt_pos][x] == "#":
                    break
                y = nxt_pos
            return walk(y, x, dir, remaining, tiles)
        case "d":
            for _ in range(next_instr):
                nxt_pos = (y + 1) % len(tiles)
                while tiles[nxt_pos][x] == " ":
                    nxt_pos = (nxt_pos + 1) % len(tiles)
                if tiles[nxt_pos][x] == "#":
                    break
                y = nxt_pos
            return walk(y, x, dir, remaining, tiles)
        case "r":
            for _ in range(next_instr):
                nxt_pos = (x + 1) % len(tiles[0])
                while tiles[y][nxt_pos] == " ":
                    nxt_pos = (nxt_pos + 1) % len(tiles[0])
                if tiles[y][nxt_pos] == "#":
                    break
                x = nxt_pos
            return walk(y, x, dir, remaining, tiles)
        case "l":
            for _ in range(next_instr):
                nxt_pos = (x - 1) % len(tiles[0])
                while tiles[y][nxt_pos] == " ":
                    nxt_pos = (nxt_pos - 1) % len(tiles[0])
                if tiles[y][nxt_pos] == "#":
                    break
                x = nxt_pos
            return walk(y, x, dir, remaining, tiles)


def part1(tiles, instrs):
    x = next(i for i, x in enumerate(tiles[0]) if x == ".")
    y, x, dir = walk(0, x, "r", instrs, tiles)
    DIR_SCORE = {"u": 3, "d": 1, "l": 2, "r": 0}
    return 1000 * (y + 1) + 4 * (x + 1) + DIR_SCORE[dir]


FACE_MAP = {
    0: {
        "u": (3, "d", lambda y, x, W: (0, W - 1 - x)),
        "r": (5, "l", lambda y, x, W: (y, W - 1)),
        "l": (2, "d", lambda y, x, W: (0, y)),
        "d": (1, "d", lambda y, x, W: (0, x)),
    },
    1: {
        "u": (0, "u", lambda y, x, W: (W - 1, x)),
        "r": (5, "d", lambda y, x, W: (0, W - 1 - y)),
        "l": (2, "l", lambda y, x, W: (y, W - 1)),
        "d": (4, "d", lambda y, x, W: (0, x)),
    },
    2: {
        "u": (0, "r", lambda y, x, W: (x, 0)),
        "r": (1, "r", lambda y, x, W: (y, 0)),
        "l": (3, "l", lambda y, x, W: (y, W - 1)),
        "d": (4, "r", lambda y, x, W: (W - 1 - x, 0)),
    },
    3: {
        "u": (0, "d", lambda y, x, W: (0, W - 1 - x)),
        "r": (2, "r", lambda y, x, W: (y, 0)),
        "l": (5, "u", lambda y, x, W: (W - 1, W - 1 - y)),
        "d": (4, "u", lambda y, x, W: (W - 1, W - 1 - x)),
    },
    4: {
        "u": (1, "u", lambda y, x, W: (W - 1, x)),
        "r": (5, "r", lambda y, x, W: (y, 0)),
        "l": (2, "u", lambda y, x, W: (W - 1, W - 1 - y)),
        "d": (3, "u", lambda y, x, W: (W - 1, W - 1 - x)),
    },
    5: {
        "u": (1, "l", lambda y, x, W: (W - 1 - x, W - 1)),
        "r": (0, "l", lambda y, x, W: (W - 1 - y, W - 1)),
        "l": (4, "l", lambda y, x, W: (y, W - 1)),
        "d": (3, "r", lambda y, x, W: (W - 1 - x, 0)),
    },
}


def get_face_offset(face, W):
    match face:
        case 0:
            return 0, 2 * W
        case 1:
            return W, 2 * W
        case 2:
            return W, W
        case 3:
            return W, 0
        case 4:
            return 2 * W, 2 * W
        case 5:
            return 2 * W, 3 * W


def get_tile(face, y, x, tiles, W):
    off_y, off_x = get_face_offset(face, W)
    return tiles[off_y + y][off_x + x]


def move(y, x, dir):
    match dir:
        case "u":
            return y - 1, x
        case "d":
            return y + 1, x
        case "r":
            return y, x + 1
        case "l":
            return y, x - 1


def walk2(y, x, face, dir, instrs, tiles, W):
    print(f"Face {face} {dir} @ ({y}, {x})")
    if not instrs:
        return y, x, face, dir

    next_instr, *remaining = instrs
    if next_instr in ROT:
        print(f"Turn {next_instr}, now facing {ROT[next_instr][dir]}")
        return walk2(y, x, face, ROT[next_instr][dir], remaining, tiles, W)

    print(f"Steps: {next_instr}")
    # print(f"Will try to walk {next_instr} in direction {dir}")
    for i in range(next_instr):
        # print(f"pos {y, x}")
        ny, nx = move(y, x, dir)
        # print("Move to ", ny, nx)

        # Out of bounds? Switch face.
        if not (0 <= ny < W) or not (0 <= nx < W):
            next_face, next_dir, pos_fn = FACE_MAP[face][dir]
            fy, fx = pos_fn(y, x, W)

            # If would hit a '#', stop here.
            if get_tile(next_face, fy, fx, tiles, W) == "#":
                return walk2(y, x, face, dir, remaining, tiles, W)
            else:
                remaining_steps = next_instr - i - 1
                # print(f"Switched from face {face} ({dir}) to {next_face} ({next_dir})")
                return walk2(
                    fy, fx, next_face, next_dir, [remaining_steps] + remaining, tiles, W
                )

        # In bounds.
        # print("will get tile ", ny, nx)
        if get_tile(face, ny, nx, tiles, W) == "#":
            # print("Hit wall on same face")
            return walk2(y, x, face, dir, remaining, tiles, W)

        y, x = ny, nx

    return walk2(y, x, face, dir, remaining, tiles, W)


def part2(tiles, instrs):
    # x = next(i for i, x in enumerate(tiles[0]) if x == ".")
    W = len(tiles) // 3
    y, x, face, dir = walk2(0, 0, 0, "r", instrs, tiles, W)
    print(f"Part 2: face {face} {dir} @ {(y, x)}")
    y0, x0 = get_face_offset(face, W)
    DIR_SCORE = {"u": 3, "d": 1, "l": 2, "r": 0}
    return 1000 * (y0 + y + 1) + 4 * (x0 + x + 1) + DIR_SCORE[dir]


if __name__ == "__main__":
    with open("test-input.txt", "r") as f:
        tiles, instrs = f.read().split("\n\n")
    instrs = [int(i) if i not in "LR" else i for i in re.findall("(\d+|\w)", instrs)]
    tiles = [[c for c in line.strip("\n")] for line in tiles.split("\n")]

    # Pad rows with ' ' to match the max length.
    n = max(len(row) for row in tiles)
    for row in tiles:
        row.extend(" " for _ in range(n - len(row)))

    # for l in tiles:
    #     print(l)

    # print(part1(tiles, instrs))
    print(part2(tiles, instrs))
