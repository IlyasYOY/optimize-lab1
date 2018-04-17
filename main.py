from sys import exit
from time import time

from deps.algorithms import *
from deps.input_functions import read_step, read_precision, read_a, read_max_steps, read_algorithm, read_starting_point, \
    read_print_interval
from deps.utils import Config, ALGORITHMS, Point, Function


def main():
    input('Начнем программу, нажмите любую кнопку, чтобы продолжить...')
    print('Настроим программу...')
    is_set_up = False
    # config = Config(0.1, 0.01, 1, 100, ALGORITHMS[0], Point(0.0, 0.0), 1)
    config = Config(0.1, 10**(-5), 0.01, 100, ALGORITHMS[5], Point(-9.0, 0.0), 1)
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
            raise
            input('Неверный ввод, для повтора нажмите любую кнопку.')


if __name__ == '__main__':
    main()
