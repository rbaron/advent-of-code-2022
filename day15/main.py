import re

# MAX_X = 20
MAX_X = 4_000_000


def join_intervals(intervals):
    all_points = []
    for begin, end in intervals:
        all_points.extend([(begin, "begin"), (end, "end")])
    all_points.sort()
    open = 0
    last_open_x = 0
    disjoint_intervals = []
    for p, b_or_e in all_points:
        if b_or_e == "begin":
            if open == 0:
                last_open_x = p
            open += 1
        elif b_or_e == "end":
            open -= 1
            if open == 0:
                disjoint_intervals.append((last_open_x, p))
            elif open < 0:
                raise Exception
    return disjoint_intervals


def get_intervals(readings, y):
    intervals = []
    beacons = set()
    for (sy, sx), (by, bx) in readings:
        radius = abs(sy - by) + abs(sx - bx)
        dx_at_y = radius - abs(sy - y)
        if dx_at_y >= 1:
            interval = ((sx - dx_at_y), (sx + dx_at_y))
            intervals.append(interval)
        if by == y:
            beacons.add(bx)
    return join_intervals(intervals), beacons


def part1(readings):
    y = 2000000
    disjoint_intervals, beacons = get_intervals(readings, y)
    return sum(e - s + 1 for s, e in disjoint_intervals) - sum(
        1 for b in beacons if any(s <= b <= e for s, e in disjoint_intervals)
    )


def find_beacon(disjoint_intervals):
    for begin, end in disjoint_intervals:
        if 0 < begin < MAX_X:
            return begin + 1
        elif 0 < end < MAX_X:
            return end + 1


def part2(readings):
    for y in range(MAX_X + 1):
        disjoint_intervals, _ = get_intervals(readings, y)
        if x := find_beacon(disjoint_intervals):
            return y + x * 4000000


if __name__ == "__main__":

    def parse_line(l):
        sx, sy, bx, by = map(int, re.findall("-?\d+", l))
        return ((sy, sx), (by, bx))

    with open("input.txt", "r") as f:
        readings = [parse_line(l) for l in f]

    print(part1(readings))
    print(part2(readings))
