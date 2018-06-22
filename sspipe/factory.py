from .pipe import Pipe


def _insert_in_args(args, idx, arg):
    return args[:idx] + (arg,) + args[idx:]


def _insert_in_kwargs(kwargs, key, arg):
    kwargs[key] = arg
    return kwargs


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
    return Pipe.create(func, args, kwargs)
