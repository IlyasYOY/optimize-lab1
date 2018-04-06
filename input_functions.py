from utils import ALGORITHMS, Point


def read_step():
    step = input('Введите начальный шаг алгоритма: ')
    step = float(step)
    if step <= 0:
        raise Exception()
    return step


def read_precision():
    precision = input('Введите точность алгоритма: ')
    precision = float(precision)
    if precision <= 0:
        raise Exception()
    return precision


def read_a():
    a = input('Введите параметр а функции: ')
    a = float(a)
    return a


def read_max_steps():
    max_steps = input('Введите масимальное кол-во шагов алгоритма: ')
    max_steps = int(max_steps)
    if max_steps <= 0:
        raise Exception()
    return max_steps


def read_algorithm():
    algorithm = input(
        '\n'.join(['{}. {}'.format(i, ALGORITHMS[i]) for i in range(len(ALGORITHMS))]) +
        '\nВведите номер алгоритма: '
    )
    algorithm = int(algorithm)
    for i in range(len(ALGORITHMS)):
        if algorithm == i:
            return ALGORITHMS[i]
    raise Exception()


def read_starting_point():
    answer = input('Введите точку начала "x y": ')
    x, y = [float(s.rstrip()) for s in answer.split() if s]
    return Point(x, y)


def read_print_interval():
    print_interval = input('Введите интервал вывода результата: ')
    print_interval = int(print_interval)
    if print_interval <= 0:
        raise Exception()
    return print_interval
