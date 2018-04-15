from copy import copy, deepcopy

ALGORITHMS = (
    'Градиентный спуск с постоянным шагом',
    'Градиентный спуск с дроблением шага',
    'Градиентный спуск с убывающим шагом',
    'Найскорейший спуск',
    'Метод Ньютона-Рафсона',
    'Овражный метод',
)


class Point:
    _x = None
    _y = None

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, x: float):
        self._x = x

    @y.setter
    def y(self, y: float):
        self._y = y

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)


class Config:
    _step = None
    _precision = None
    _a = None
    _max_steps = None
    _algorithm = None
    _starting_point = None
    _print_interval = None

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step: float):
        self._step = step

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, precision: float):
        self._precision = precision

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, a):
        self._a = a

    @property
    def max_steps(self):
        return self._max_steps

    @max_steps.setter
    def max_steps(self, max_steps: int):
        self._max_steps = max_steps

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: str):
        self._algorithm = algorithm

    @property
    def starting_point(self):
        return self._starting_point

    @starting_point.setter
    def starting_point(self, starting_point: Point):
        self._starting_point = starting_point

    @property
    def print_interval(self):
        return self._print_interval

    @print_interval.setter
    def print_interval(self, print_interval):
        self._print_interval = print_interval

    def create_algorithm_from_config(self):
        function = Function(self)
        if self.algorithm == ALGORITHMS[0]:
            return ConstantStepAlgorithm(self, function)
        elif self.algorithm == ALGORITHMS[1]:
            return DividingStepAlgorithm(self, function)
        elif self.algorithm == ALGORITHMS[2]:
            return DecreasingStepAlgorithm(self, function)
        elif self.algorithm == ALGORITHMS[3]:
            return FastestDescendAlgorithm(self, function)
        else:
            return None

    def __init__(self, step: float, precision: float,
                 a: float, max_steps: int, algorithm: str,
                 starting_point: Point, print_interval: int):
        self.step = step
        self.precision = precision
        self.a = a
        self.max_steps = max_steps
        self.algorithm = algorithm
        self.starting_point = starting_point
        self.print_interval = print_interval

    def __str__(self):
        return ('Шаг: {},\n'
                'Точность: {}, \n'
                'Параметр а: {}, \n'
                'Максимальное кол-во шагов: {}, \n'
                'Алгоритм: {}, \n'
                'Начальная точка: {}, \n'
                'Интервал печати: {}, \n').format(self.step, self.precision, self.a, self.max_steps,
                                                  self.algorithm, self.starting_point, self.print_interval)


class Function:
    _config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config: Config):
        self._config = config

    def __init__(self, config: Config):
        self.config = config

    def __call__(self, point: Point):
        return {
            'function': (point.y - point.x ** 2) ** 2 + self.config.a * (point.x - 1) ** 2,
            'derivative': {
                'x': 2 * self.config.a * (point.x - 1) - 4 * point.x * (point.y - point.x ** 2),
                'y': 2 * (point.y - point.x ** 2)
            },
            'second_derivative': {
                'xx': 12*point.x**2 - 4*point.y + 2*self.config.a,
                'yy': 2,
                'xy': -4*point.x,
                'yx': -4*point.x,
            }
        }