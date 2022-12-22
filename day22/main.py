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


def part2(input_data):
    pass


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        tiles, instrs = f.read().split("\n\n")
    instrs = [int(i) if i not in "LR" else i for i in re.findall("(\d+|\w)", instrs)]
    tiles = [[c for c in line.strip("\n")] for line in tiles.split("\n")]

    # Pad rows with ' ' to match the max length.
    n = max(len(row) for row in tiles)
    for row in tiles:
        row.extend(" " for _ in range(n - len(row)))

    # for l in tiles:
    #     print(l)

    print(part1(tiles, instrs))
    # print(part2(input_data))
