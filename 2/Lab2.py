from math import sqrt, pi, cos, sin, log
from random import uniform, random
import matplotlib.pyplot as pyplot


def model_first_process(t, amount_of_numbers, r1, r2):
    xi = []
    for i in range(amount_of_numbers):
        eta = 1 / (1 + pi * i ** 2)
        arg = i * pi * t
        xi.append((cos(arg) * r1[i] + sin(arg) * r2[i]) * eta)
    return sum(xi)


def model_second_process(t, amount_of_numbers, r1, r2, r3):
    xi = []
    for i in range(amount_of_numbers):
        eta = 1 / sqrt(1 + pi * i ** 2) ** 2
        arg = r3[i] * t
        xi.append((cos(arg) * r1[i] + sin(arg) * r2[i]) * eta)

    return sum(xi)

amount_of_processes = 300
step = 0.1
amount_of_numbers = 100
amount_of_realizations = 200

def analyse_processes(amount_of_processes, step, amount_of_numbers, amount_of_realizations):
    processes1 = []
    processes2 = []
    for _ in range(amount_of_realizations):
        r1 = [sqrt(-2 * log(random())) * cos(2 * pi * random()) for _ in range(amount_of_numbers)]
        r2 = [sqrt(-2 * log(random())) * sin(2 * pi * random()) for _ in range(amount_of_numbers)]
        r3 = [uniform(i * pi, (i + 1) * pi) for i in range(amount_of_numbers)]
        t = 0
        xi1 = []
        xi2 = []
        while t < amount_of_processes * step:
            xi1.append(model_first_process(t, amount_of_numbers, r1, r2))
            xi2.append(model_second_process(t, amount_of_numbers, r1, r2, r3))
            t += step

        processes1.append(xi1)
        processes2.append(xi2)

    means1 = []
    means2 = []
    variance1 = []
    variance2 = []
    for i in range(amount_of_processes):
        mean1 = sum(processes1[j][i] for j in range(amount_of_realizations)) / amount_of_realizations
        means1.append(mean1)
        variance1.append(
            sum((processes1[j][i] - mean1) ** 2 for j in range(amount_of_realizations)) / amount_of_realizations)

        mean2 = sum(processes2[j][i] for j in range(amount_of_realizations)) / amount_of_realizations
        means2.append(mean2)
        variance2.append(
            sum((processes2[j][i] - mean2) ** 2 for j in range(amount_of_realizations)) / amount_of_realizations)

    return {
        'first_process': (means1, variance1),
        'second_process': (means2, variance2),
        'first_processes_realizations': (processes1[0], processes1[-1]),
        'second_processes_realizations': (processes2[0], processes2[-1]),
    }


x = list(range(amount_of_processes))
data = analyse_processes(amount_of_processes, step, amount_of_numbers, amount_of_realizations)

realization1_0, = pyplot.plot(x, data['first_processes_realizations'][0])
realization1_1, = pyplot.plot(x, data['first_processes_realizations'][1])
realization2_0, = pyplot.plot(x, data['second_processes_realizations'][0])
realization2_1, = pyplot.plot(x, data['second_processes_realizations'][1])
pyplot.legend([realization1_0, realization1_1, realization2_0, realization2_1],
              ['realization1_0', 'realization1_1', 'realization2_0', 'realization2_1'], loc=3)

pyplot.figure()
mean1, = pyplot.plot(x, data['first_process'][0])
variance1, = pyplot.plot(x, data['first_process'][1])
mean2, = pyplot.plot(x, data['second_process'][0])
variance2, = pyplot.plot(x, data['second_process'][1])
pyplot.legend([mean1, variance1, mean2, variance2], ['mean1', 'variance1', 'mean2', 'variance2'])

pyplot.show()