def snafu_to_dec(snafu):
    N = dict(zip("=-012", range(-2, 3)))
    return sum(N[n] * 5**i for i, n in enumerate(reversed(snafu)))


def dec_to_snafu(dec):
    N = dict(zip([0, 1, 2, 3, 4], "012=-"))
    res = []
    while dec > 0:
        k, rest = divmod(dec, 5)
        val = N[rest]
        res.append(val)
        dec = k
        if val in "-=":
            # Carry one.
            dec += 1
    return "".join(reversed(res))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        snafus = [l.strip() for l in f]

    s = sum(snafu_to_dec(n) for n in snafus)
    print(s)
    print(dec_to_snafu(s))
