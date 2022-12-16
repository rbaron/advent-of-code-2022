import re
from collections import defaultdict
from functools import lru_cache
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


def all_pairs_shortest_path(valves):
    dists = defaultdict(lambda: float("inf"))
    for v, attrs in valves.items():
        for child in v["children"]:
            dists[v, child] = 1
    return dists


def part2(valves):
    dists = all_pairs_shortest_path(valves)
    print(dists)
    # @lru_cache(maxsize=None)
    # def search(t, u="AA", vs=frozenset(F), e=False):
    #     return max(
    #         [
    #             F[v] * (t - D[u, v] - 1) + search(t - D[u, v] - 1, v, vs - {v}, e)
    #             for v in vs
    #             if D[u, v] < t
    #         ]
    #         + [search(26, vs=vs) if e else 0]
    #     )


if __name__ == "__main__":

    def parse_line(l):
        parent, *children = re.findall("[A-Z]{2}", l)
        [rate] = re.findall("rate=(\d+)", l)
        return parent, {"rate": int(rate), "children": children}

    with open("input.txt", "r") as f:
        valves = dict(map(parse_line, f))

    print(part1(valves))
    print(part2(valves))
