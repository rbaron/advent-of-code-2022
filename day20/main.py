from __future__ import annotations
import copy
import dataclasses


@dataclasses.dataclass
class Node:
    val: int
    prev: Node
    next: Node


def decrypt(numbers, repeat, decryption_key):
    N = len(numbers)

    nodes = [
        Node(val=n * decryption_key, prev=None, next=None)
        for i, n in enumerate(numbers)
    ]
    for i, _ in enumerate(nodes):
        nodes[i].prev = nodes[i - 1]
        nodes[i].next = nodes[(i + 1) % N]

    for _ in range(repeat):
        for curr in nodes:

            # Number of steps (we will remove the current node, so N - 1 is the length
            # of the remaining list).
            steps = curr.val % (N - 1)

            if steps == 0:
                continue

            # Remove current node
            curr.next.prev = curr.prev
            curr.prev.next = curr.next

            next = curr
            for _ in range(steps):
                next = next.next

            curr.next = next.next
            curr.next.prev = curr
            curr.prev = next
            curr.prev.next = curr

    # Find index 0.
    zero = None
    for curr in nodes:
        if curr.val == 0:
            zero = curr

    s = 0
    for offset in [1000, 2000, 3000]:
        curr = zero
        for _ in range(offset % N):
            curr = curr.next
        s += curr.val
    return s


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        numbers = [int(l) for l in f]

    print(decrypt(numbers, repeat=1, decryption_key=1))
    print(decrypt(numbers, repeat=10, decryption_key=811589153))
