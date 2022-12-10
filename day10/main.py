OP_CYCLES = {"addx": 2, "noop": 1}


def part1(ops):
    SS_CYCLES = list(range(20, 240 + 1, 40))
    signal_strength = 0
    X = 1
    cycle = 1
    next_signal_cycle_ptr = 0
    for op, *args in ops:
        if (
            next_signal_cycle_ptr < len(SS_CYCLES)
            and cycle <= SS_CYCLES[next_signal_cycle_ptr] < cycle + OP_CYCLES[op]
        ):
            signal_strength += X * SS_CYCLES[next_signal_cycle_ptr]
            next_signal_cycle_ptr += 1
        if op == "addx":
            X += int(args[0])
        cycle += OP_CYCLES[op]
    return signal_strength


def part2(ops):
    W = 40
    H = 6
    buff = [[" " for _ in range(W)] for _ in range(H)]
    X = 1
    cycle = 0
    for op, *args in ops:
        for _ in range(OP_CYCLES[op]):
            for sprite_pos in range(X - 1, X + 2):
                if cycle % W == sprite_pos:
                    row, col = divmod(cycle, W)
                    buff[row][col] = "#"
            cycle += 1
        if op == "addx":
            X += int(args[0])
    return "\n".join(["".join(row) for row in buff])


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        ops = [tuple(p for p in l.strip().split(" ")) for l in f]
    print(part1(ops))
    print(part2(ops))
