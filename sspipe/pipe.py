import functools

FALLBACK_RTRUEDIV_TYPES = (type(dict().keys()), type(dict().values()))


def _resolve(pipe, x):
    while isinstance(pipe, Pipe):
        pipe = pipe._____func___(x)
    return pipe


def _resolve_function_call(func, args, kwargs, x):
    func = _resolve(func, x)
    resolved_args = (_resolve(arg, x) for arg in args)
    resolved_kwargs = {k: _resolve(v, x) for k, v in kwargs.items()}
    return func(*resolved_args, **resolved_kwargs)


class Pipe(object):
    """
    >>> [lambda : '{}'] | (Pipe(lambda x: x)[0]().format(2) | Pipe(int)**3)
    8
    """
    # __slots__ = ('_____func___',)
    __array_ufunc__ = None

    def __init__(self, func):
        self._____func___ = func

    def __ror__(self, other):
        return _resolve(self, other)

    def __or__(self, other):
        if isinstance(other, Pipe):
            return Pipe(lambda x: _resolve(other, _resolve(self, x)))

        return Pipe(lambda x: _resolve(self, x) | other)

    def __rtruediv__(self, other):
        if isinstance(other, FALLBACK_RTRUEDIV_TYPES):
            return _resolve(self, other)

        return Pipe(lambda x: _resolve(other, x) / _resolve(self, x))

    @staticmethod
    def unpipe(pipe):
        return pipe._____func___

    @staticmethod
    def partial(func, args, kwargs):
        return Pipe(functools.partial(_resolve_function_call, func, args, kwargs))

    def __getattr__(self, item):
        return Pipe.partial(getattr, (self, item), {})

    def __call__(self, *args, **kwargs):
        return Pipe.partial(self, args, kwargs)


def _override_operator(op):
    def __operator__(self, *args, **kwargs):
        # `Pipe.partial` resolves `self` before calling `getattr`:
        resolved_operator = Pipe.partial(getattr, (self, op), {})
        return Pipe.partial(resolved_operator, args, kwargs)

    setattr(Pipe, op, __operator__)


for op in [
    'len', 'abs',
    'contains', 'await',
    'lt', 'le', 'gt', 'ge', 'eq', 'ne',
    'xor', 'and',
    'rshift', 'lshift',
    'add', 'sub', 'mul', 'matmul', 'pow',
    'truediv', 'floordiv', 'mod',
    'pos', 'neg', 'invert',
    'getitem']:
    _override_operator('__{}__'.format(op))
