from random import random

import numpy as np

from Lab412 import get_matrix_ranges, get_hitting_matrix, get_matrix


def print_table(table):
    print()
    for row in table:
        for cel in row:
            cel_value = str(cel)[:8]
            cel_len = len(cel_value)
            cel_end = ' ' * (10 - cel_len)
            print(cel_value, end=cel_end)
        print()


def get_probabilities_on_nth_step(matrix, start_probabilities, n):
    prs = [start_probabilities]
    matrix_len = len(matrix)
    for i in range(matrix_len):
        prs.append(np.matmul(prs[-1], np.linalg.matrix_power(matrix, n)))

    return prs[n]


def find_experimental_probabilities(matrix, state, n, amount_of_tries=1000):
    final_states = []
    ranges = get_matrix_ranges(matrix)
    matrix_len = len(matrix)

    for i in range(amount_of_tries):
        states = [state]

        for _ in range(n):
            rd = random()
            for j in range(matrix_len + 1):
                if rd < ranges[states[-1]][j]:
                    states.append(j - 1)
                    break
        final_states.append(states[-1])
    prs = []
    size = len(final_states)
    for i in range(len(matrix)):
        prs.append(final_states.count(i) / size)

    return prs


def get_q_matrix(matrix, n):
    q_matrix = []
    matrix_len = len(matrix)
    for i in range(n, matrix_len):
        q_matrix.append(list(matrix[i][n:]))

    return q_matrix


def get_n_matrix(q_matrix):
    return np.linalg.inv(np.identity(len(q_matrix)) - q_matrix)


def get_r_matrix(matrix, n):
    new_matrix = []
    for j in range(n):
        row = []
        for i in range(n, len(matrix)):
            row.append(matrix[i][j])

        new_matrix.append(row)
    return new_matrix


def get_average_time_in_all_states(p_0, q_matrix):
    tau = np.matmul(p_0, get_n_matrix(q_matrix))
    return tau


def get_probability_of_absorption(n_matrix, r_matrix):
    prob = np.matmul(n_matrix, np.transpose(r_matrix))
    return prob


mt = get_hitting_matrix(5, 2)
print('matrix')
print_table(mt)
print(find_experimental_probabilities(matrix=mt, state=2, n=5))
print(get_probabilities_on_nth_step(mt, [0, 0, 1, 0, 0], 5))
p = np.array([0.3, 0.2, 0.5])
q_matrix = get_q_matrix(mt, 2)
print('\n\nq_matrix')
print_table(q_matrix)
r_matrix = get_r_matrix(mt, 2)
n_matrix = get_n_matrix(q_matrix)
print('\n\nn_matrix')
print_table(n_matrix)
print('\nr_matrix')
print(r_matrix)
print('p_0', p)
print('Час перебування в заданому стані')
print(get_average_time_in_all_states(p, q_matrix))
print('ймовірність поглинання')
print(get_probability_of_absorption(n_matrix, r_matrix), '\n\n\n\n\n')

mt = get_matrix(5)
print_table(mt)

f_matrix = np.linalg.matrix_power(mt, 12)
print(f_matrix)
n_matrix = np.linalg.inv(np.identity(len(mt)) - (mt - f_matrix))
p_0 = np.array([0.1, 0.2, 0.2, 0.2, 0.3])
r_matrix = f_matrix[-1]
print('Час перебування в заданому стані')
print(np.matmul(p_0, n_matrix))