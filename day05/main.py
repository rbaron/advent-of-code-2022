from collections import deque
from copy import deepcopy


def part1(state, moves):
    for (n, from_, to) in moves:
        for _ in range(n):
            state[to - 1].append(state[from_ - 1].pop())
    return "".join(stack[-1] for stack in state)


def part2(state, moves):
    for (n, from_, to) in moves:
        tmp_queue = deque()
        for _ in range(n):
            tmp_queue.append(state[from_ - 1].pop())
        for _ in range(n):
            state[to - 1].append(tmp_queue.pop())
    return "".join(stack[-1] for stack in state)


def parse_input(filename):
    with open(filename, "r") as f:
        state_in, moves_in = [blk.split("\n") for blk in f.read().split("\n\n")]
    n_stacks = max(map(int, state_in[-1].strip().split("  ")))
    state = [deque() for _ in range(n_stacks)]
    for l in state_in[:-1]:
        for n in range(n_stacks):
            if (crate := l[1 + 4 * n]) != " ":
                state[n].appendleft(crate)
    moves = []
    for line in moves_in:
        _, n, _, from_, _, to = line.strip().split(" ")
        moves.append((int(n), int(from_), int(to)))
    return state, moves


if __name__ == "__main__":
    state, moves = parse_input("input.txt")
    print(part1(deepcopy(state), moves))
    print(part2(deepcopy(state), moves))
