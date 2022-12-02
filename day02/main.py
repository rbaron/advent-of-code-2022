WINNING_COMBS = {
    "R": "S",
    "P": "R",
    "S": "P",
}

LOSING_COMBS = {op: shape for shape, op in WINNING_COMBS.items()}


ENC_TO_SHAPE = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}


def outcome(shape, shape_opponent):
    SHAPE_PTS = {
        "R": 1,
        "P": 2,
        "S": 3,
    }

    return SHAPE_PTS[shape] + (
        3
        if shape == shape_opponent
        else (6 if shape_opponent == WINNING_COMBS[shape] else 0)
    )


def part1(input_data):
    return sum(
        outcome(ENC_TO_SHAPE[shape], ENC_TO_SHAPE[shape_opponent])
        for (shape_opponent, shape) in input_data
    )


def part2(input_data):
    def pick_shape(desired_outcome, shape_opponent):
        match desired_outcome:
            case "X":  # We lose.
                return WINNING_COMBS[shape_opponent]
            case "Y":  # Draw.
                return shape_opponent
            case "Z":  # We win.
                return LOSING_COMBS[shape_opponent]

    return sum(
        outcome(
            pick_shape(desired_outcome, ENC_TO_SHAPE[shape_opponent]),
            ENC_TO_SHAPE[shape_opponent],
        )
        for (shape_opponent, desired_outcome) in input_data
    )


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input_data = [l.strip().split(" ") for l in f]

    print(part1(input_data))
    print(part2(input_data))
