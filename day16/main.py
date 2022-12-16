import re
from collections import defaultdict
from functools import lru_cache, cache
from itertools import product


def compute_max_release(valves, curr_node, open, time):
    @lru_cache(maxsize=None)
    def compute_max_cached(curr_node, open, time):
        if time <= 1:
            return 0
        options = []
        for child in valves[curr_node]["children"]:
            if child == curr_node:
                continue
            # Either turn on the current valve.
            if curr_node not in open and valves[curr_node]["rate"] > 0:
                options.append(
                    (time - 1) * valves[curr_node]["rate"]
                    + compute_max_cached(child, open | {curr_node}, time - 2)
                )
            # Or go straight to the next valve.
            options.append(compute_max_cached(child, open, time - 1))

        return max(options)

    return compute_max_cached(curr_node, open, time)


def part1(valves):
    return compute_max_release(valves, "AA", frozenset(), 30)


# https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
def all_pairs_shortest_path(valves):
    dists = defaultdict(lambda: float("inf"))
    for valve, attrs in valves.items():
        for child in attrs["children"]:
            dists[child, valve] = 1
    for k, i, j in product(valves.keys(), valves.keys(), valves.keys()):
        dists[i, j] = min(dists[i, j], dists[i, k] + dists[k, j])
    return dists


def part2(valves):
    dists = all_pairs_shortest_path(valves)

    @lru_cache(maxsize=None)
    def compute_max_cached(time, curr_valve, available, is_elephant):
        return max(
            [
                valves[v]["rate"] * (time - dists[curr_valve, v] - 1)
                + compute_max_cached(
                    time - dists[curr_valve, v] - 1, v, available - {v}, is_elephant
                )
                for v in available
                if dists[curr_valve, v] < time
            ]
            + [
                compute_max_cached(
                    26, curr_valve="AA", available=available, is_elephant=False
                )
                if is_elephant
                else 0
            ]
        )

    return compute_max_cached(
        26,
        "AA",
        available=frozenset(v for v, attrs in valves.items() if attrs["rate"] > 0),
        is_elephant=True,
    )


if __name__ == "__main__":

    def parse_line(l):
        parent, *children = re.findall("[A-Z]{2}", l)
        [rate] = re.findall("rate=(\d+)", l)
        return parent, {"rate": int(rate), "children": children}

    with open("input.txt", "r") as f:
        valves = dict(map(parse_line, f))

    print(part1(valves))
    print(part2(valves))
