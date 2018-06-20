from sspipe.factory import pipe_with_nonfirst_arg_factory, _partial_pipe
from toolz import curried, compose

from sspipe.pipe import Pipe


class Facade():
    def __call__(self, func, *args, **kwargs):
        """
        >>> from sspipe import p
        >>> 1 | p('{}'.format)
        '1'
        >>> 1 | p('{}{}'.format, 2)
        '12'
        >>> 1 | p('{}{}{x}'.format, 2, x=3)
        '123'
        """
        return _partial_pipe(func, args, kwargs)

    def __getattr__(self, item):
        """
        >>> from sspipe import p
        >>> [1,2] | p.map(lambda x: x*2) | p(sum)
        6
        """
        return compose(Pipe, getattr(curried, item))

    def __getitem__(self, item):
        return pipe_with_nonfirst_arg_factory(item)


p = Facade()
