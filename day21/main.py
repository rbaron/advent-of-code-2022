import re

SENTINEL = "x"


def maybe_simplify(expr):
    if not isinstance(expr, int) and SENTINEL not in expr:
        return int(eval(expr))
    return expr


def eval_expr(expr, ast):
    if len(expr) == 1:
        return f"{SENTINEL if expr[0] == SENTINEL else int(expr[0])}"

    operand1, op, operand2 = expr
    return maybe_simplify(
        f"({maybe_simplify(eval_expr(ast[operand1], ast))}) {op} ({maybe_simplify(eval_expr(ast[operand2], ast))})"
    )


def split_expr(expr):
    # Remove opening and closing parens.
    expr = expr[1:-1]
    paren_counter = 0
    for i, chr in enumerate(expr):
        match chr:
            case "(":
                paren_counter += 1
            case ")":
                paren_counter -= 1
            case _:
                continue
        if paren_counter == 0:
            # lhs, op, rhs
            return expr[: i + 1], expr[i + 2], expr[i + 4 :]


def solve_equality_for_x(expr):
    [(lhs, rhs)] = re.findall("^(.+) == (.+)$", expr)
    if SENTINEL in rhs:
        lhs, rhs = rhs, lhs

    def solve_for_x(expr_with_x, equals_to):
        if expr_with_x == f"({SENTINEL})":
            return equals_to
        lhs1, op, lhs2 = split_expr(expr_with_x)
        if SENTINEL in lhs2:
            if op == "/":
                return solve_for_x(lhs2, eval(f"{lhs1} * {equals_to}"))
            elif op == "-":
                return solve_for_x(lhs2, eval(f"{lhs1} - {equals_to}"))
            else:
                # +, *  are commutative.
                lhs1, lhs2 = lhs2, lhs1
        match op:
            case "-":
                return solve_for_x(lhs1, eval(f"{equals_to} + {lhs2}"))
            case "+":
                return solve_for_x(lhs1, eval(f"{equals_to} - {lhs2}"))
            case "*":
                return solve_for_x(lhs1, eval(f"{equals_to} / {lhs2}"))
            case "/":
                return solve_for_x(lhs1, eval(f"{equals_to} * {lhs2}"))
            case _:
                raise RuntimeError(op)

    return int(solve_for_x(lhs, rhs))


def parse_line(l):
    label, op = l.split(": ")
    return label, op.split(" ")


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        ast = dict(parse_line(l.strip()) for l in f)

    print(eval_expr(ast["root"], ast))

    ast["root"][1] = "=="
    ast["humn"][0] = SENTINEL
    expr = eval_expr(ast["root"], ast)
    print(solve_equality_for_x(expr))
