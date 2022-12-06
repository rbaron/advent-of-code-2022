from collections import Counter

START_OF_PACKET_MARKER_WINDOW_SIZE = 4
START_OF_MESSAGE_MARKER_WINDOW_SIZE = 14


def find_marker(stream, window_size):
    buff = Counter(stream[:window_size])
    for i, signal in enumerate(stream[window_size:]):
        buff[stream[i]] -= 1
        buff[signal] += 1
        if sum(1 for v in buff.values() if v == 1) == window_size:
            return i + window_size + 1
    return -1


def part1(stream):
    return find_marker(stream, START_OF_PACKET_MARKER_WINDOW_SIZE)


def part2(stream):
    return find_marker(stream, START_OF_MESSAGE_MARKER_WINDOW_SIZE)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        stream = f.read().strip()

    print(part1(stream))
    print(part2(stream))
