import operator

FALLBACK_RTRUEDIV_TYPES = (type(dict().keys()), type(dict().values()), type(dict().items()))


def _resolve(pipe, x):
    while isinstance(pipe, Pipe):
        pipe = pipe._____func___(x)
    return pipe


class Pipe(object):
    """
    >>> [lambda : '{}'] | (Pipe(lambda x: x)[0]().format(2) | Pipe(int)**3)
    8
    """
    __slots__ = ('_____func___',)

    def __init__(self, func):
        self._____func___ = func

    def __ror__(self, other):
        ret = _resolve(self, other)
        return ret

    def __or__(self, other):
        if isinstance(other, Pipe):
            return Pipe(lambda x: _resolve(other, _resolve(self, x)))

        return Pipe(lambda x: _resolve(self, x) | other)

    def __rtruediv__(self, other):
        if isinstance(other, FALLBACK_RTRUEDIV_TYPES):
            return _resolve(self, other)

        return Pipe(lambda x: _resolve(other, x) / _resolve(self, x))

    def __getattr__(self, item):
        return Pipe.partial(getattr, self, item)

    def __call__(self, *args, **kwargs):
        return Pipe.partial(self, *args, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, tuple) and len(item) < 20:  # do not iterate over too large tuples!
            item = Pipe.collection(item)
        return Pipe.partial(operator.getitem, self, item)

    __array_priority__ = -10

    @staticmethod
    def __array_ufunc__(func, method, *args, **kwargs):
        import numpy
        if callable(method) and args[0] == '__call__':
            if method is numpy.bitwise_or:
                if isinstance(args[1], Pipe):
                    return Pipe.partial(_resolve, args[2], args[1])
                else:
                    return _resolve(args[2], args[1])
            return Pipe.partial(method, *args[1:], **kwargs)
        elif method == '__call__':
            if func.name == 'bitwise_or':
                if isinstance(args[0], Pipe):
                    return Pipe.partial(_resolve, args[1], args[0])
                else:
                    return _resolve(args[1], args[0])
            return Pipe.partial(func, *args, **kwargs)
        return NotImplemented

    @staticmethod
    def unpipe(pipe):
        if isinstance(pipe, Pipe):
            return pipe._____func___
        else:
            return pipe

    @staticmethod
    def partial(func, *args, **kwargs):
        # Code duplication in this function is intentional to increase performance.
        if isinstance(func, Pipe):
            if kwargs:
                def _resolve_function_call(x):
                    resolved_func = _resolve(func, x)
                    resolved_args = (_resolve(arg, x) for arg in args)
                    resolved_kwargs = {k: _resolve(v, x) for k, v in kwargs.items()}
                    return resolved_func(*resolved_args, **resolved_kwargs)
            else:
                def _resolve_function_call(x):
                    resolved_func = _resolve(func, x)
                    resolved_args = (_resolve(arg, x) for arg in args)
                    return resolved_func(*resolved_args)

            return Pipe(_resolve_function_call)
        else:
            if kwargs:
                def _resolve_function_call(x):
                    resolved_args = (_resolve(arg, x) for arg in args)
                    resolved_kwargs = {k: _resolve(v, x) for k, v in kwargs.items()}
                    return func(*resolved_args, **resolved_kwargs)
            else:
                def _resolve_function_call(x):
                    resolved_args = (_resolve(arg, x) for arg in args)
                    return func(*resolved_args)

            return Pipe(_resolve_function_call)

    @staticmethod
    def collection(items):
        if isinstance(items, dict):
            def _resolve_collection_creation(x):
                resolved_items = {_resolve(key, x): _resolve(val, x) for key, val in items.items()}
                return dict(resolved_items)
        else:
            def _resolve_collection_creation(x):
                resolved_items = (_resolve(item, x) for item in items)
                return type(items)(resolved_items)

        return Pipe(_resolve_collection_creation)


def _override_operator(op, impl):
    def __operator__(*args):
        return Pipe.partial(impl, *args)

    setattr(Pipe, op, __operator__)


def _reverse_args(func):
    def wrapper(*args):
        return func(*args[::-1])

    return wrapper


for _op in [
    'len', 'abs',
    'contains', 'await',
    'lt', 'le', 'gt', 'ge', 'eq', 'ne',
    'xor', 'and',
    'rxor', 'rand',
    'rshift', 'lshift',
    'rrshift', 'rlshift',
    'add', 'sub', 'mul', 'matmul', 'pow',
    'radd', 'rsub', 'rmul', 'rmatmul', 'rpow',
    'truediv', 'floordiv', 'mod',
    'rfloordiv', 'rmod',  # skipped rtruediv because it is implemented in Pipe class
    'pos', 'neg', 'invert',
    ]:
    _name = '__{}__'.format(_op)

    if _op in ['and', 'rand']:
        _impl = operator.and_
    elif _op == 'len':
        _impl = len
    elif _op == 'await':
        async def _impl(x):
            return await x
    else:
        try:
            _impl = getattr(operator, _op)
        except AttributeError:  # radd, rrshift, rsub, rmul, ...
            _op = _op[1:]  # remove the first 'r' letter
            _impl = _reverse_args(getattr(operator, _op))

    _override_operator(_name, _impl)
