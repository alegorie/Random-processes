from math import sqrt
from numpy import random
from numpy.random import random_integers

from form import m, mg, n, sample_size

#Punkt B

def sum_population_by_sample(x):
    return sample_size * sum(x) / m

def average_population_by_sample(x):
    Ys = sum(x) / m
    return Ys

def dispertion_population_by_sample(x, Ys, m):
    S2 = 0
    for i in range(m):
        S2 += (x[i] - Ys) ** 2
    S2 = S2 / (m - 1)
    return S2


x = random_integers(10+m, mg + 2 * m, n)
sum_population_by_sample(x)
average_population_by_sample(x)
dispertion_population_by_sample()

print(sum_population_by_sample())

# if __name__ == "__main__":
#     x = []
