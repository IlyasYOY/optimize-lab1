from copy import copy, deepcopy

from utils import Config, Function, Point


class Algorithm:
    _config = None
    _function = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, function):
        self._function = function

    def __init__(self, config: Config, function: Function):
        self.config = config
        self.function = function
        self.function.config = config

    def step(self, current_step, point):
        raise NotImplementedError()

    def run(self):
        if self.config is None:
            raise Exception('Config was not set in {}.'.format(self))
        elif self.function is None:
            raise Exception('Function was ot set in {}'.format(self))
        current_step = deepcopy(self.config.starting_point)  # type: Point
        for i in range(self.config.max_steps):
            point = self.function(current_step)
            if not i % self.config.print_interval:
                print('Шаг: {0:> 7}: x: {1:> 13e}, y: {2:> 13e}, функция: {3:> 13e}, градиент: [{4:> 13e}, {5:> 13e}]'
                      .format(i + 1, current_step.x, current_step.y,
                              point['function'], point['derivative']['x'], point['derivative']['y']))
            if (point['derivative']['x'] ** 2 + point['derivative']['y'] ** 2) ** 0.5 < self.config.precision:
                print('Минимум достигнут.')
                return True
            self.step(current_step, point)


class ConstantStepAlgorithm(Algorithm):
    def __init__(self, config: Config, function: Function):
        super().__init__(config, function)

    def step(self, current_step, point):
        x, y = point['derivative']['x'], point['derivative']['y']
        length = (x ** 2 + y ** 2) ** 0.5
        x, y = x / length, y / length
        current_step.x -= self.config.step * x
        current_step.y -= self.config.step * y


class DividingStepAlgorithm(Algorithm):
    __my_step = None

    def __init__(self, config: Config, function: Function):
        super().__init__(config, function)
        self.__my_step = copy(self.config.step)

    def step(self, current_step, point):
        x, y = point['derivative']['x'], point['derivative']['y']
        length = (x ** 2 + y ** 2) ** 0.5
        x, y = x / length, y / length
        current_step.x -= self.__my_step * x
        current_step.y -= self.__my_step * y
        self.__my_step /= 1.1


class DecreasingStepAlgorithm(Algorithm):
    __counter = None

    def __init__(self, config: Config, function: Function):
        super().__init__(config, function)
        self.__counter = 1

    def step(self, current_step, point):
        x, y = point['derivative']['x'], point['derivative']['y']
        length = (x ** 2 + y ** 2) ** 0.5
        x, y = x / length, y / length
        current_step.x -= self.config.step / self.__counter * x
        current_step.y -= self.config.step / self.__counter * y


class FastestDescendAlgorithm(Algorithm):
    def __init__(self, config: Config, function: Function):
        super().__init__(config, function)

    def step(self, current_step, point):
        x, y = point['derivative']['x'], point['derivative']['y']
        length = (x ** 2 + y ** 2) ** 0.5
        x, y = x / length, y / length
        current_step.x -= self.config.step * x
        current_step.y -= self.config.step * y
