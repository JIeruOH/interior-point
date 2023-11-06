import numpy as np
from numpy.linalg import inv

EPS = 1e-9


def no_solution():
    print('The problem does not have solution!')
    exit()


def not_applicable():
    print('The method is not applicable!')
    exit()


def simple(A, b):
    """
    Simplificate matrix by pivots, remove useless rows
    :param A: matrix
    :param b: vector
    :return: (matrix_, vector_)
    """
    n, m = A.shape
    orders = set(range(n))
    for j in range(m):
        if not orders: break
        p = max(orders, key=lambda p: abs(A[p][j]))
        if abs(A[p][j]) < EPS: continue
        orders.discard(p)
        for i in range(n):
            if i == p: continue
            k = A[i][j] / A[p][j]
            A[i] -= A[p] * k
            b[i] -= b[p] * k
    deleted = set()
    for i in range(n):
        if np.max(np.abs(A[i])) < EPS:
            if abs(b[i][0]) > EPS:
                no_solution()
            deleted.add(i)
    A = np.array([A[i] for i in range(n) if i not in deleted])
    b = np.array([b[i] for i in range(n) if i not in deleted])
    return A, b


def find_particular_solution(A, b):
    """
    Finds the particular solution
    :param A: matrix
    :param b: vector
    :return: particular solution: vector
    """
    n, m = A.shape
    orders = set(range(m))
    for i in range(n):
        for j in range(m):
            if A[i][j] and j in orders:
                orders.remove(j)
                break
    if n != m:
        additional = np.array([[float(i == j) for j in range(m)] for i in orders])
        A = np.concatenate((A, additional))
        b = np.concatenate((b, np.ones((m - n, 1))))
    A = inv(A)
    x = A @ b
    delta = np.concatenate((np.zeros((n, 1)), np.ones((m - n, 1))))
    while delta[-1][0] > EPS ** 2:
        x = A @ b
        if np.min(x) >= delta[-1][0]:
            break
        delta /= 2
        if np.min(A @ (b - delta)) > np.min(A @ (b + delta)):
            b -= delta
        else:
            b += delta
    return x


def projected_gradient(A, c):
    """
    Finds the projected gradient
    :param A: matrix
    :param c: vector
    :return:
    """
    I = np.identity(A.shape[1])
    P = I - A.T @ np.linalg.inv(A @ A.T) @ A
    return P @ c


def print_solution(x, rnd=3):
    """
    Prints the current solution
    :param x: solution: vector
    :param rnd: round parameter: int
    :return: None
    """
    print('\n'.join(f'x{i} = {round(v, rnd)}' for (i, v) in enumerate(x.T[0])))


def interior_point(A: np.ndarray, c: np.ndarray, b: np.ndarray, eps: float, alpha: float = 0.5) -> np.ndarray:
    """
    Solving the problem with interior point algorithm
    :param A: A matrix of coefficients of constraint function
    :param c: A vector of coefficients of objective function
    :param b: A vector of right-hand side numbers
    :param eps: The approximation accuracy
    :param alpha: gradient coefficient
    :return:
    """
    x = find_particular_solution(A, b)
    if np.min(x.T) < -EPS:
        no_solution()
    if np.min(np.abs(x.T)) < EPS:
        not_applicable()
    iteration = 1
    while True:
        print(f'Iteration {iteration}')
        print_solution(x)
        D = np.diag(x.T[0])
        x_ = inv(D) @ x
        A_ = A @ D
        c_ = D @ c
        cp = projected_gradient(A_, c_)
        v = np.min(cp)
        # the gradient is too small
        if v > -eps:
            return x
        x_ -= alpha / v * cp
        x = D @ x_
        iteration += 1


def run(c, A, b, eps, alpha=0.5):
    """
    Solve the problem by interior point algorithm.
    :param c: A vector of coefficients of objective function
    :param A: A matrix of coefficients of constraint function
    :param b: A vector of right-hand side numbers
    :param eps: The approximation accuracy
    :param alpha: gradient coefficient
    :return: None
    """
    # convert input data to matrices
    c = np.array([[float(i) for i in c]]).T
    A = np.array([[float(j) for j in i] for i in A])
    b = np.array([[float(i) for i in b]]).T
    # simplification of matrix
    A, b = simple(A, b)
    # solve the problem
    x = interior_point(A, c, b, eps, alpha)
    # print the result
    print('Optimal Solution:')
    print_solution(x)
    print('Optimal Value:')
    print(round((c.T @ x)[0][0], 3))
