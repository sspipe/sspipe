from .pipe import Pipe

px = Pipe(lambda x: x)


def create_pipe(func, args, kwargs):
    if not args and not kwargs:
        return Pipe(func)
    elif any(
        isinstance(arg, Pipe) for arg in args
    ) or any(
        isinstance(arg, Pipe) for arg in kwargs.values()
    ) or isinstance(func, Pipe):
        return Pipe.partial(func, args, kwargs)
    else:
        return Pipe(lambda x: func(*args, x, **kwargs))


def _insert_in_args(args, idx, arg):
    return args[:idx] + (arg,) + args[idx:]


def _insert_in_kwargs(kwargs, key, arg):
    kwargs[key] = arg
    return kwargs


def pipe_with_nonfirst_arg_factory(arg_key_or_pos):
    if isinstance(arg_key_or_pos, int):
        def make_p(func, *args, **kwargs):
            fixed_args = _insert_in_args(args, arg_key_or_pos, px)
            return Pipe.partial(Pipe.partial, args=(func, fixed_args, kwargs), kwargs={})

        return make_p
    elif isinstance(arg_key_or_pos, str):
        def make_p(func, *args, **kwargs):
            fixed_kwargs = _insert_in_kwargs(kwargs, arg_key_or_pos, px)
            return Pipe.partial(Pipe.partial, args=(func, args, fixed_kwargs), kwargs={})

        return make_p
    else:
        raise KeyError(arg_key_or_pos)
