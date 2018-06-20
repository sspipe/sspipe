from sspipe.factory import pipe_with_nonfirst_arg_factory, _partial_pipe
from toolz import curried, compose

from sspipe.pipe import Pipe


class Facade():
    def __call__(self, func, *args, **kwargs):
        return _partial_pipe(func, args, kwargs)

    def __getattr__(self, item):
        return compose(Pipe, getattr(curried, item))

    def __getitem__(self, item):
        return pipe_with_nonfirst_arg_factory(item)


p = Facade()
