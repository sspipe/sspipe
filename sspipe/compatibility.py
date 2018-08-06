import functools
from sspipe.pipe import Pipe


def convert_pipe(original_pipe):
    @functools.wraps(original_pipe)
    def method(self, *args, **kwargs):
        args = (Pipe.unpipe(arg) if isinstance(arg, Pipe) else arg for arg in args)
        kwargs = {k: Pipe.unpipe(v) if isinstance(v, Pipe) else v for k, v in kwargs.items()}
        return Pipe(original_pipe(*args, **kwargs).function)

    return method
