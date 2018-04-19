from time import time

from deps.algorithms import ConstantStepAlgorithm, DividingStepAlgorithm, DecreasingStepAlgorithm, \
    FastestDescendAlgorithm, NewtonAlgorithm, RavineAlgorithm
from deps.utils import ALGORITHMS, Point, Function, dump_config


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


def cli_interface(config):
    input('Начнем программу, нажмите любую кнопку, чтобы продолжить...')
    print('Настроим программу...')
    is_set_up = False
    function = Function(config)
    while not is_set_up:
        print('Текущий конфиг:')
        print(config)
        answer = input('Что введете?\n'
                       '1. Шаг.\n'
                       '2. Точность.\n'
                       '3. Параметр а.\n'
                       '4. Максимальное кол-во шагов.\n'
                       '5. Алгоритм.\n'
                       '6. Начальная точка.\n'
                       '7. Интервал печати.\n'
                       'Либо начать работу алгоритма 0, или закончить работу программы -1.\n'
                       'Ответ: ')
        try:
            answer = int(answer)
            if answer == 1:
                config.step = read_step()
            elif answer == 2:
                config.precision = read_precision()
            elif answer == 3:
                config.a = read_a()
            elif answer == 4:
                config.max_steps = read_max_steps()
            elif answer == 5:
                config.algorithm = read_algorithm()
            elif answer == 6:
                config.starting_point = read_starting_point()
            elif answer == 7:
                config.print_interval = read_print_interval()
            elif answer == -1:
                dump_config(config)
                print('Пока!')
                exit(0)
            elif answer == 0:
                algorithm = None
                if config.algorithm == ALGORITHMS[0]:
                    algorithm = ConstantStepAlgorithm(config, function)
                elif config.algorithm == ALGORITHMS[1]:
                    algorithm = DividingStepAlgorithm(config, function)
                elif config.algorithm == ALGORITHMS[2]:
                    algorithm = DecreasingStepAlgorithm(config, function)
                elif config.algorithm == ALGORITHMS[3]:
                    algorithm = FastestDescendAlgorithm(config, function)
                elif config.algorithm == ALGORITHMS[4]:
                    algorithm = NewtonAlgorithm(config, function)
                elif config.algorithm == ALGORITHMS[5]:
                    algorithm = RavineAlgorithm(config, function)

                start = time()
                algorithm.run()
                print('Заняло времени: {0:> .3}с'.format(time() - start))
            else:
                raise Exception()
        except Exception:
            input('Неверный ввод, для повтора нажмите любую кнопку.')
