from numpy.random import uniform
from math import log, exp, factorial
import matplotlib.pyplot as pyplot


def model_poisson_process(amount_of_numbers, _lambda):
    random_numbers = uniform(size=amount_of_numbers)
    x_n = [-log(random_numbers[i]) / _lambda for i in range(amount_of_numbers)]
    distr = [sum(x_n[:i]) for i in range(amount_of_numbers)]

    return distr, x_n


def get_realizations(amount_of_realizations, amount_of_numbres, _lambda):
    processes = []
    for i in range(amount_of_realizations):
        processes.append(model_poisson_process(amount_of_numbres, _lambda)[0])

    return processes


def find_time_of_first_event_appearance(realizations, number_of_event):
    times = [sum(realizations[i][:number_of_event + 1]) for i in range(len(realizations))]

    return times


def find_interval_within_events(realizations, start, end):
    intervals = [sum(realizations[i][start: end + 1]) for i in range(len(realizations))]
    return intervals


def find_probabilities_of_n_events_appearance(realizations, n, t):
    t_min = min([sum(realizations[i]) for i in range(len(realizations))])
    if t > t_min:
        raise ValueError("T is too big")

    probabilities = []
    for k in range(100):
        size = int(len(realizations) / 100)
        amount_of_events = []
        length = len(realizations[0])

        for i in range(k * size, (k + 1) * size):
            time = 0
            amount = 0
            for j in range(length):
                if time > t:
                    break
                amount = j
                time += realizations[i][j]
            amount_of_events.append(amount)

        probabilities.append(amount_of_events.count(n) / size)
    return probabilities


def analyse_process(_lambda, amount_of_processes, amount_of_numbers, number_of_event, start, end, n, t):
    realizations = get_realizations(amount_of_processes, amount_of_numbers, _lambda)

    times = find_time_of_first_event_appearance(realizations, number_of_event)
    intervals = find_interval_within_events(realizations, start, end)
    pr = find_probabilities_of_n_events_appearance(realizations, n, t)

    realization = (model_poisson_process(amount_of_numbers, _lambda), model_poisson_process(amount_of_numbers, _lambda))

    # print(exp(-_lambda * t) * (_lambda * t) ** n / factorial(n))

    return {
        'realizations': realization,
        'times': times,
        'intervals': intervals,
        'pr': pr
    }

    # height = [i for i in range(amount_of_numbers)]



_lambda = 100
amount_of_processes = 1000
amount_of_numbers = 100
number_of_event = 100
start = 2
end = 3
n = 100
t = 15


data = analyse_process(_lambda, amount_of_processes, amount_of_numbers, number_of_event, start, end, n, t)

height = [i for i in range(len(data['realizations'][0][0]))]

pyplot.bar(data['realizations'][0][0], height)
pyplot.bar(data['realizations'][1][0], height)
pyplot.show()

pyplot.hist(data['times'])
pyplot.show()

pyplot.hist(data['intervals'])
pyplot.show()

pyplot.hist(data['pr'])
pyplot.show()
