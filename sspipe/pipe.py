FALLBACK_RTRUEDIV_TYPES = (type(dict().keys()), type(dict().values()))


class Pipe(object):
    """
    >>> [lambda : '{}'] | (Pipe(lambda x: x)[0]().format(2) | Pipe(int)**3)
    8
    """

    __array_ufunc__ = None

    def __init__(self, func):
        if isinstance(func, Pipe):
            func = func._____func___
        self._____func___ = func

    def __ror__(self, other):
        return self._____func___(other)

    def __rtruediv__(self, other):
        if isinstance(other, FALLBACK_RTRUEDIV_TYPES):
            return self._____func___(other)
        return Pipe(lambda x: other / self._____func___(x))

    def __or__(self, other):
        return Pipe(lambda x: self._____func___(x) | other)

    def __getattr__(self, attr):
        return Pipe(lambda x: getattr(self._____func___(x), attr))


def _override_operator(operator):
    def implementation(self, *args, **kwargs):
        def func(x):
            resolved_args = (arg._____func___(x) if isinstance(arg, Pipe) else arg for arg in args)
            for k, v in tuple(kwargs.items()):
                if isinstance(v, Pipe):
                    kwargs[k] = v._____func___(x)
            return getattr(self._____func___(x), operator)(*resolved_args, **kwargs)

        return Pipe(func)

    setattr(Pipe, operator, implementation)


for op in [
    'len', 'abs',
    'contains', 'await',
    'lt', 'le', 'gt', 'ge', 'eq', 'ne',
    'xor', 'and',
    'rshift', 'lshift',
    'add', 'sub', 'mul', 'matmul', 'pow',
    'truediv', 'floordiv', 'mod',
    'pos', 'neg', 'invert',
    'call', 'getitem']:
    _override_operator('__{}__'.format(op))
