from random import random
import numpy as np


def get_matrix(n):
    matrix = []
    for i in range(n):
        row = [random() for _ in range(n)]
        s = sum(row)
        matrix.append([x / s for x in row])

    return np.array(matrix)


def get_hitting_matrix(n, hitting_rows):
    matrix = []
    for i in range(hitting_rows):
        hitting_row = [0] * (n - 1)
        hitting_row.insert(i, 1)
        matrix.append(hitting_row)

    for i in range(n - hitting_rows):
        row = [random() for _ in range(n)]
        s = sum(row)
        matrix.append([x / s for x in row])

    return np.array(matrix)


def get_start_probabilities(n):
    row = [random() for _ in range(n)]
    s = sum(row)
    row = [x / s for x in row]
    return np.array(row)


def get_matrix_ranges(matrix):
    n = len(matrix)
    new_matrix = []
    for row in matrix:
        new_matrix.append([sum(row[:i]) for i in range(n + 1)])

    return new_matrix


def model_markov_chains(n=4, condition=None, matrix=None, hitting=False):
    states = []

    if condition is not None:
        row = [0 for _ in range(n)]
        row[condition] = 1
        start_probabilities = np.array(row)
        states.append(condition)
    else:
        start_probabilities = get_start_probabilities(n)
        ranges = [sum(start_probabilities[:i]) for i in range(n + 1)]
        rd = random()
        for i in range(n + 1):
            if rd < ranges[i]:
                states.append(i - 1)
                break

    if matrix is None:
        matrix = get_hitting_matrix(n, 1) if hitting else get_matrix(n)
    else:
        n = len(matrix)
    ranges = get_matrix_ranges(matrix)

    for i in range(n * 3):
        rd = random()
        for j in range(n + 1):
            if rd < ranges[states[-1]][j]:
                states.append(j - 1)
                break

    print('start probabilities:')
    print(start_probabilities)

    return states


if __name__ == '__main__':
    # mt = np.array([[1, 0, 0, 0], [0.2, 0.3, 0.3, 0.2], [0.2, 0.3, 0.4, 0.1], [0.3, 0.2, 0.4, 0.1]])
    n = 5
    matrix = get_matrix(n)
    hitting_matrix = get_hitting_matrix(n, 1)
    state = 1
    print('\nЛанцюг Маркова для заданих перехідних і початкових ймовірностей:')
    print('matrix:')
    print(matrix)
    print('\nПри вибраному початковому стані')
    print(model_markov_chains(n=n, condition=state, matrix=matrix), end='\n\n')
    print('при випадковому початковому стані')
    print(model_markov_chains(n=n, matrix=matrix), end='\n\n')
    print('Ланцюг Маркова з поглинанням для заданих перехідних і початкових ймовірностей:')
    print('matrix:')
    print(hitting_matrix)
    print('\nПри вибраному початковому стані')
    print(model_markov_chains(n=n, condition=state, matrix=hitting_matrix), end='\n\n')
    print('при випадковому початковому стані')
    print(model_markov_chains(n=n, matrix=hitting_matrix), end='\n\n')