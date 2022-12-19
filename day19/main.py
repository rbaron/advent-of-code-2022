import functools
import re


def run_blueprint(blueprint, steps):
    (
        _,
        or_ore_cost,
        cr_ore_cost,
        obr_ore_cost,
        obr_clay_cost,
        gr_ore_cost,
        gr_ob_cost,
    ) = blueprint

    @functools.cache
    def dfs(state):
        time, ore, clay, ob, g, o_r, c_r, ob_r, g_r = state

        # Prune excess ore and ore robots.
        ore = min(ore, (steps - time) * max(or_ore_cost, cr_ore_cost, gr_ore_cost))
        o_r = min(o_r, max(or_ore_cost, cr_ore_cost, gr_ore_cost))

        if time == steps:
            return g
        children = []

        # Can we build an geode robot?
        if ore >= gr_ore_cost and ob >= gr_ob_cost:
            # children.append(
            return dfs(
                (
                    time + 1,
                    ore + o_r - gr_ore_cost,
                    clay + c_r,
                    ob + ob_r - gr_ob_cost,
                    g + g_r,
                    o_r,
                    c_r,
                    ob_r,
                    g_r + 1,
                )
            )
            # )
        # Can we build an ore robot?
        if ore >= or_ore_cost:
            children.append(
                dfs(
                    (
                        time + 1,
                        ore + o_r - or_ore_cost,
                        clay + c_r,
                        ob + ob_r,
                        g + g_r,
                        o_r + 1,
                        c_r,
                        ob_r,
                        g_r,
                    )
                )
            )
        # Can we build a clay robot?
        if ore >= cr_ore_cost:
            children.append(
                dfs(
                    (
                        time + 1,
                        ore + o_r - cr_ore_cost,
                        clay + c_r,
                        ob + ob_r,
                        g + g_r,
                        o_r,
                        c_r + 1,
                        ob_r,
                        g_r,
                    )
                )
            )
        # Can we build an obsidian robot?
        if ore >= obr_ore_cost and clay >= obr_clay_cost:
            children.append(
                dfs(
                    (
                        time + 1,
                        ore + o_r - obr_ore_cost,
                        clay + c_r - obr_clay_cost,
                        ob + ob_r,
                        g + g_r,
                        o_r,
                        c_r,
                        ob_r + 1,
                        g_r,
                    )
                )
            )

        children.append(
            dfs(
                (
                    time + 1,
                    ore + o_r,
                    clay + c_r,
                    ob + ob_r,
                    g + g_r,
                    o_r,
                    c_r,
                    ob_r,
                    g_r,
                )
            )
        )
        return max(children)

    # (time, ore, clay, ob, g, o_r, c_r, ob_r, g_r)
    return dfs((0, 0, 0, 0, 0, 1, 0, 0, 0))


def part1(blueprints):
    s = 0
    for i, bp in enumerate(blueprints):
        res = run_blueprint(bp, steps=24)
        # print(f"Finished blueprint {i + 1}: {res}")
        s += (i + 1) * res
    return s


def part2(blueprints):
    p = 1
    for bp in blueprints[:3]:
        res = run_blueprint(bp, steps=32)
        print(f"Finished blueprint: {res}")
        p *= res
    return p


def parse_blueprint(blueprint):
    return tuple(int(n) for n in re.findall("\d+", blueprint))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        blueprints = [parse_blueprint(l) for l in f]

    print(part1(blueprints))
    print(part2(blueprints))
