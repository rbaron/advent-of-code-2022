from collections import Counter, deque
from math import prod
from copy import deepcopy


def calc_mokey_business(monkeys, n_rounds, lower_worry_fn):
    activity = Counter()
    for _ in range(n_rounds):
        for monkey_n, monkey in enumerate(monkeys):
            while len(monkey["items"]) != 0:
                activity[monkey_n] += 1
                val = monkey["items"].popleft()
                operand = monkey["op"]["operand"]
                rhs = int(operand) if operand != "old" else val
                match monkey["op"]["op"]:
                    case "+":
                        val += rhs
                    case "*":
                        val *= rhs
                    case _:
                        raise Exception
                val = lower_worry_fn(val)
                if val % monkey["test"]["div"] == 0:
                    monkeys[monkey["test"]["conseq"]]["items"].append(val)
                else:
                    monkeys[monkey["test"]["alt"]]["items"].append(val)
    (_, v1), (_, v2) = activity.most_common(2)
    return v1 * v2


def part1(monkeys):
    return calc_mokey_business(monkeys, 20, lambda val: val // 3)


def part2(monkeys):
    k = prod(m["test"]["div"] for m in monkeys)
    return calc_mokey_business(monkeys, 10_000, lambda val: val % k)


def parse_monkey(blk):
    lines = blk.split("\n")
    op = lines[2].split(" ")
    return {
        "items": deque(map(int, lines[1].split(":")[1].split(","))),
        "op": {
            "op": op[-2],
            "operand": op[-1],
        },
        "test": {
            "div": int(lines[3].split(" ")[-1]),
            "conseq": int(lines[4].split(" ")[-1]),
            "alt": int(lines[5].split(" ")[-1]),
        },
    }


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        monkeys = [parse_monkey(blk) for blk in f.read().split("\n\n")]

    print(part1(deepcopy(monkeys)))
    print(part2(deepcopy(monkeys)))
