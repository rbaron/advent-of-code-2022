from collections import defaultdict


def add(p1, p2):
    return tuple(a + b for a, b in zip(p1, p2))


POS = {
    "N": [(-1, -1), (-1, 0), (-1, 1)],
    "S": [(1, -1), (1, 0), (1, 1)],
    "W": [(-1, -1), (0, -1), (1, -1)],
    "E": [(-1, 1), (0, 1), (1, 1)],
}

DIRS = "NSWE"


def count_empty_ground(elves):
    miny, maxy = min(y for y, _ in elves), max(y for y, _ in elves)
    minx, maxx = min(x for _, x in elves), max(x for _, x in elves)
    return sum(
        (y, x) not in elves
        for y in range(miny, maxy + 1)
        for x in range(minx, maxx + 1)
    )


def simulate(elves, rounds):
    for round in range(rounds):
        any_proposed = False
        # Old positions by new positions
        proposals = defaultdict(list)
        for ey, ex in sorted(elves):
            # If no elves in eight neighboring positions, this elf does not move.
            if not any(add((ey, ex), n) in elves for dir in DIRS for n in POS[dir]):
                proposals[(ey, ex)].append((ey, ex))
                continue

            # Pick a direction.
            proposed = False
            for i in range(len(DIRS)):
                dir = DIRS[(round + i) % 4]
                # If all free, move there.
                if all(add((ey, ex), n) not in elves for n in POS[dir]):
                    proposals[add((ey, ex), POS[dir][1])].append((ey, ex))
                    proposed = True
                    any_proposed = True
                    break

            if not proposed:
                proposals[(ey, ex)].append((ey, ex))

        if not any_proposed:
            return count_empty_ground(elves), round + 1

        elves = set()
        for new_pos, old_elves in proposals.items():
            if len(old_elves) == 1:
                elves.add(new_pos)
            else:
                elves.update(old_elves)

    return count_empty_ground(elves), round + 1


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        elves = {(y, x) for y, l in enumerate(f) for x, c in enumerate(l) if c == "#"}

    print(simulate(elves, 10)[0])
    print(simulate(elves, 1000000)[1])
