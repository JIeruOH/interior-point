from fractions import Fraction


def print_tableau(table, header_variables, basic_variables):
    row_format = "{:<12}" * (len(header_variables) + 3)
    print(row_format.format("BV", *header_variables, "Solution", "Ratio"))
    print('-' * len(header_variables) * 12)

    pivot_col_idx = None
    if any(value < 0 for value in table[-1][:-1]):
        pivot_col_idx = table[-1].index(min(table[-1][:-1]))

    for idx, row in enumerate(table[:-1]):
        ratio = str(row[-1] / row[pivot_col_idx]) if pivot_col_idx is not None and row[pivot_col_idx] > 0 else "∞"
        print(row_format.format(basic_variables[idx], *[str(val) for val in row], ratio))
    print(row_format.format("Objective", *[str(val) for val in table[-1]], "∞"))
    print('=' * len(header_variables) * 12)


def pivot(table, pivot_row_idx, pivot_col_idx):
    pivot_element = table[pivot_row_idx][pivot_col_idx]
    table[pivot_row_idx] = [val / pivot_element for val in table[pivot_row_idx]]

    for idx, row in enumerate(table):
        if idx == pivot_row_idx:
            continue
        factor = row[pivot_col_idx]
        table[idx] = [elem - factor * table[pivot_row_idx][i] for i, elem in enumerate(row)]


def simplex(c, A, b):
    m, n = len(A), len(c)
    non_basic_variables = ["x" + str(i) for i in range(1, n + 1)] + ["s" + str(i) for i in range(1, m + 1)]
    basic_variables = ["s" + str(i) for i in range(1, m + 1)]

    header_variables = non_basic_variables.copy()

    table = [row + [0] * m + [b[idx]] for idx, row in enumerate(A)]
    for i in range(m):
        table[i][n + i] = Fraction(1)

    table.append([Fraction(i * -1) for i in c] + [Fraction(0)] * m + [Fraction(0)])

    iteration = 1
    while any(value < 0 for value in table[-1][:-1]):
        print(f"Iteration {iteration}")
        print_tableau(table, header_variables, basic_variables)

        pivot_col_idx = table[-1].index(min(table[-1][:-1]))
        pivot_row_idx = None
        min_ratio = float('inf')
        for i, row in enumerate(table[:-1]):
            if row[pivot_col_idx] <= 0:
                continue
            ratio = row[-1] / row[pivot_col_idx]
            if ratio < min_ratio:
                min_ratio, pivot_row_idx = ratio, i

        if pivot_row_idx is None:
            print("No feasible solution exists.")
            exit()

        basic_variables[pivot_row_idx], non_basic_variables[pivot_col_idx] = non_basic_variables[pivot_col_idx], \
            basic_variables[pivot_row_idx]
        pivot(table, pivot_row_idx, pivot_col_idx)
        iteration += 1

    print("Final Tableau:")
    print_tableau(table, header_variables, basic_variables)

    solution = [Fraction(0)] * n
    for idx, variable in enumerate(basic_variables):
        if variable[0] == 'x':
            solution[int(variable[1:]) - 1] = table[idx][-1]

    return solution, table[-1][-1]


def run(c, A, b):
    c = [Fraction(i) for i in c]
    A = [[Fraction(j) for j in i] for i in A]
    b = [Fraction(i) for i in b]
    solution, objective_value = simplex(c, A, b)
    print(f"Optimal Solution: [{' '.join([f'{val.numerator}/{val.denominator}' for val in solution])}]")
    print(f"Optimal Value: {objective_value.numerator}/{objective_value.denominator}")
