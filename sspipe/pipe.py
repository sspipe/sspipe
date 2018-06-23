import functools
import operator

FALLBACK_RTRUEDIV_TYPES = (type(dict().keys()), type(dict().values()))


def _resolve(pipe, x):
    while isinstance(pipe, Pipe):
        pipe = pipe._____func___(x)
    return pipe


def _call_with_resolved_args(func, args, kwargs, x):
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
        assert not isinstance(func, Pipe)
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
    def unwrap(pipe):
        return pipe._____func___

    @staticmethod
    def partial(func, args, kwargs):
        if not args and not kwargs:
            return Pipe(func)
        elif any(isinstance(arg, Pipe) for arg in args) or any(isinstance(arg, Pipe) for arg in kwargs.values()):
            return Pipe(lambda x: _call_with_resolved_args(func, args, kwargs, x))
        else:
            return Pipe(lambda x: func(*args, x, **kwargs))

    @staticmethod
    def partial2(func, args, kwargs):
        return Pipe(lambda x: _call_with_resolved_args(func, args, kwargs, x))

    def __getattr__(self, item):
        return Pipe.partial2(getattr, (self, item), {})

    def __call__(self, *args, **kwargs):
        return Pipe.partial2(self, args, kwargs)


def _override_operator(op):
    def __operator__(self, *args, **kwargs):
        return Pipe.partial2(Pipe.partial2(getattr, (self, op), {}), args, kwargs)

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
