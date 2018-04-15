from copy import copy, deepcopy
from scipy.optimize import minimize_scalar
import numpy as np
from deps.utils import Config, Function, Point


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
            raise Exception('Function was not set in {}'.format(self))
        current_step = deepcopy(self.config.starting_point)  # type: Point
        for i in range(self.config.max_steps):
            point = self.function(current_step)
            if not i % self.config.print_interval:
                print('Шаг: {0:> 7}: x: {1:> 13e}, y: {2:> 13e}, функция: {3:> 13e}, градиент: [{4:> 13e}, {5:> 13e}]'
                      .format(i + 1, current_step.x, current_step.y,
                              point['function'], point['derivative']['x'], point['derivative']['y']))
            if abs(point['function']) < self.config.precision:
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
    __DIVIDING_CONST = 0.5

    def __init__(self, config: Config, function: Function):
        super().__init__(config, function)
        self.__my_step = copy(self.config.step)

    def step(self, current_step, point):
        x, y = current_step.x, current_step.y
        dx, dy = point['derivative']['x'], point['derivative']['y']

        new_position = deepcopy(current_step)
        alpha = self.__my_step
        while point['function'] <= self.function(new_position)['function']:
            new_position.x = x - alpha * dx
            new_position.y = y - alpha * dy
            alpha *= self.__DIVIDING_CONST

        current_step.x = new_position.x
        current_step.y = new_position.y


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

        self.__counter += 1


class FastestDescendAlgorithm(Algorithm):
    def __init__(self, config: Config, function: Function):
        super().__init__(config, function)

    def step(self, current_step, point):
        x, y = current_step.x, current_step.y
        dx, dy = point['derivative']['x'], point['derivative']['y']

        f = lambda x1, x2 : (x2 - x1**2)**2 + self.config.a * (1 - x1)**2
        alpha = minimize_scalar(
            lambda alpha: f(x - alpha * dx, y - alpha * dy)).x

        current_step.x -= alpha * dx
        current_step.y -= alpha * dy


class NewtonAlgorithm(Algorithm):
    def __init__(self, config: Config, function: Function):
        super().__init__(config, function)

    def step(self, current_step, point):
        df = point['derivative']
        df = np.array([df['x'], df['y']])
        d2f = point['second_derivative']
        d2f = np.array([[d2f['xx'], d2f['xy']],
                        [d2f['xy'], d2f['yy']]])
        dx = np.linalg.inv(d2f) @ df

        current_step.x -= dx[0]
        current_step.y -= dx[1]


class RavineAlgorithm(Algorithm):
    def __init__(self, config: Config, function: Function):
        super().__init__(config, function)

        self.fastest_descend = FastestDescendAlgorithm(deepcopy(config), deepcopy(function))
        self.prev_step = None
        self.prev_point = None

    def __sign(self, x):
        if x < 0:
            return -1
        elif x == 0:
            return 0
        else:
            return 1

    def step(self, current_step, point):
        if self.prev_step is None or self.prev_point is None:
            self.prev_step = deepcopy(current_step)
            self.prev_point = deepcopy(point)
            self.fastest_descend.step(current_step, point)
        else:
            dx = current_step.x - self.prev_step.x
            dy = current_step.y - self.prev_step.y
            length = (dx**2 + dy**2)**0.5
            s = self.__sign(self.prev_point['function'] - point['function'])
            direction = Point(s*dx / length, s*dy / length)

            next_step = Point(current_step.x + self.config.step*direction.x,
                              current_step.y + self.config.step*direction.y)
            self.fastest_descend.step(next_step, self.function(next_step))

            self.prev_step = deepcopy(current_step)
            self.prev_point = deepcopy(point)

            current_step.x = next_step.x
            current_step.y = next_step.y