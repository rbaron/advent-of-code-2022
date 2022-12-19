import itertools


def gen_rocks():
    while True:
        yield [0b0011110]
        yield [0b0001000, 0b0011100, 0b0001000]
        yield [0b0000100, 0b0000100, 0b0011100]
        yield [0b0010000, 0b0010000, 0b0010000, 0b0010000]
        yield [0b0011000, 0b0011000]


def print_stack(stack):
    for l in reversed(stack):
        print(f"{l:>07b}")
    print()


def gen_moves_stream(moves):
    while True:
        for i, move in enumerate(moves):
            yield i, move


def simulate(moves, n, cache):
    stack = [0b1111111]
    s = gen_moves_stream(moves)
    step = -1
    offset = 0
    rock_n = 0
    jumped_into_overdrive = False
    for rock in gen_rocks():
        if rock_n == n:
            return offset + len(stack) - 1
        rock_n += 1
        d = 4

        # Assume that if the last 50 stack elements are the same, we're in a repeated state.
        state = (tuple(rock), tuple(stack[-50:]), step)
        if rock == [0b0011110] and state in cache and not jumped_into_overdrive:
            jumped_into_overdrive = True
            prev_height, prev_rock_n = cache[state]
            height_diff = len(stack) - prev_height
            rocks_diff = rock_n - prev_rock_n
            rock_blocks = (n - rock_n) // rocks_diff
            offset = rock_blocks * height_diff
            extra_rocks = rock_blocks * rocks_diff
            rock_n += extra_rocks
        else:
            cache[state] = (len(stack), rock_n)
        while True:
            d -= 1
            k = -d
            # If there's any collision.
            n_avail = min(k, len(rock), len(stack))
            if any(stack[-k + pos] & rock[-pos - 1] for pos in range(n_avail)):
                # Merge min(k, len(rock)) at position stack[-k -n_merge + i].
                n_merge = min(k - 1, len(rock))
                for i in range(n_merge):
                    stack[-k + i + 1] |= rock[-i - 1]
                    if stack[-k + i + 1] == 0b1111111:
                        # print("TETRIS BABY")
                        pass

                # Push remaining rocks on new stack elements.
                n_push = len(rock) - n_merge
                for i in range(n_push):
                    stack.append(rock[-n_merge - 1 - i])

                # print_stack(stack)
                break
            step, ss = next(s)
            match ss:
                case ">":
                    if all(l & (1 << 0) == 0 for l in rock) and not any(
                        (rock[-pos - 1] >> 1) & stack[-k + pos]
                        for pos in range(n_avail)
                    ):
                        rock = [l >> 1 for l in rock]
                case "<":
                    if all(l & (1 << 6) == 0 for l in rock) and not any(
                        (rock[-pos - 1] << 1) & stack[-k + pos]
                        for pos in range(n_avail)
                    ):
                        rock = [l << 1 for l in rock]


def part2(input_data):
    pass


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        stream = f.read().strip()

    print(simulate(stream, 2022, {}))
    print(simulate(stream, 1000000000000, {}))
