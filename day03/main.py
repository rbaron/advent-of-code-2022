def priority(item):
    return (
        ord(item) - ord("A") + 27 if ord(item) < ord("a") else ord(item) - ord("a") + 1
    )


def chunkify(list, chunk_size):
    return (list[i : i + chunk_size] for i in range(0, len(list), chunk_size))


def part1(input_data):
    sum = 0
    for rucksack in input_data:
        l = len(rucksack)
        [intersection] = set(rucksack[: l // 2]) & set(rucksack[l // 2 :])
        sum += priority(intersection)
    return sum


def part2(input_data):
    sum = 0
    for chunk in chunkify(input_data, 3):
        (first, *others) = map(set, chunk)
        [group] = first.intersection(*others)
        sum += priority(group)
    print(sum)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input_data = [l.strip() for l in f]

    print(part1(input_data))
    print(part2(input_data))
