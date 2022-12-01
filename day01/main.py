import itertools


def part1(input_data):
    return max(sum(blk) for blk in input_data)


def part2(input_data):
    return sum(
        s for s in itertools.islice(sorted(map(sum, input_data), reverse=True), 3)
    )


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input_data = [
            [int(l) for l in blk.split("\n")] for blk in f.read().split("\n\n")
        ]

    print(part1(input_data))
    print(part2(input_data))
