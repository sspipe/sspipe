from sspipe.factory import pipe_with_nonfirst_arg_factory
from toolz import curried
import toolz
from sspipe.pipe import Pipe, _call_with_resolved_args


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
        return Pipe.create(func, args, kwargs)

    def __getattr__(self, item):
        """
        >>> from sspipe import p
        >>> [1,2] | p.map(lambda x: x*2) | p(sum)
        6
        """
        func = getattr(curried, item)

        def make_pipe(*args, **kwargs):
            if isinstance(args[0], Pipe):
                args = (Pipe.unwrap(args[0]),) + args[1:]
            return Pipe(lambda x: _call_with_resolved_args(func, args + (x,), kwargs, x))

        setattr(self, item, make_pipe)
        return make_pipe

    def __getitem__(self, item):
        return pipe_with_nonfirst_arg_factory(item)


p = Facade()
