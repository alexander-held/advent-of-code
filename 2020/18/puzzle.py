import fileinput
import re

x = [line.strip() for line in fileinput.input()]


def solve(expr, part2=False):
    if "(" in expr:  # brackets have highest precedence
        subexpr = re.findall("\([^()]*\)", expr)
        bracket_sol = solve(subexpr[0][1:-1], part2=part2)  # solve first bracket
        new_expr = expr.replace(subexpr[0], bracket_sol)
        return solve(new_expr, part2=part2)

    elif "+" in expr and expr.count("+") + expr.count("*") > 1 and part2:
        # higher precedence for + in part 2, only needed if more than one operation left
        subexpr = re.findall("\d+ \+ \d+", expr)
        sum_sol = solve(subexpr[0], part2=part2)
        # need to have lookahead / lookbehind here to avoid replacing "5 + 35" by the
        # solution of "5 + 3 = 8", resulting in "85"
        new_expr = re.sub(
            "(?<!\d)" + subexpr[0].replace("+", "\+").replace("*", "\*") + "(?!\d)",
            sum_sol,
            expr,
        )
        return solve(new_expr, part2=part2)

    else:
        expr_split = expr.split()
        if len(expr_split) > 1:
            first_expr = expr_split[:3]
            new_expr = f"{eval(''.join(first_expr))} {' '.join(expr_split[3:])}"
            return solve(new_expr, part2=part2)
        else:
            return expr.strip()


# part 1
sum_ans = 0
for problem in x:
    sum_ans += int(solve(problem))

print(f"part 1: {sum_ans}")


# part 2
sum_ans = 0
for problem in x:
    sum_ans += int(solve(problem, part2=True))

print(f"part 2: {sum_ans}")
