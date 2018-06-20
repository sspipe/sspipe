from .pipe import Pipe


def _pipe_with_args(func, args, kwargs):
    return Pipe(lambda x: func(x, *args, **kwargs))


def _insert_in_args(args, idx, arg):
    args[idx:idx] = arg
    return args


def _insert_in_kwargs(kwargs, key, arg):
    kwargs[key] = arg
    return kwargs


def _partial_pipe(func, args, kwargs):
    if args or kwargs:
        return _pipe_with_args(func, args, kwargs)
    else:
        return Pipe(func)


def pipe_with_nonfirst_arg_factory(arg_key_or_pos):
    if isinstance(arg_key_or_pos, int):
        def make_p(func, *args, **kwargs):
            return Pipe(lambda x: func(*_insert_in_args(args, arg_key_or_pos, x), **kwargs))

        return make_p
    elif isinstance(arg_key_or_pos, str):
        def make_p(func, *args, **kwargs):
            return Pipe(lambda x: func(*args, **_insert_in_kwargs(kwargs, arg_key_or_pos, x)))

        return make_p
    else:
        raise KeyError(arg_key_or_pos)


def pipe(func, *args, **kwargs):
    return _partial_pipe(func, args, kwargs)
