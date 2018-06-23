from sspipe.factory import pipe_with_nonfirst_arg_factory, create_pipe, px
from toolz import curried
from sspipe.pipe import Pipe


class Facade():
    def __call__(self, func, *args, **kwargs):
        """
        >>> from sspipe import p
        >>> 1 | p('{}'.format)
        '1'
        >>> 2 | p('{}{}'.format, 2)
        '12'
        >>> 2 | p('{}{}{x}'.format, 1, x=3)
        '123'
        """
        return create_pipe(func, args, kwargs)

    def __getattr__(self, item):
        """
        >>> from sspipe import p
        >>> [1,2] | p.map(lambda x: x*2) | p(sum)
        6
        """
        func = getattr(curried, item)

        def make_pipe(*args, **kwargs):
            if args and isinstance(args[0], Pipe):
                args = (Pipe.unpipe(args[0]),) + args[1:]
            return Pipe.partial(func, *args, px, **kwargs)

        setattr(self, item, make_pipe)
        return make_pipe

    def __getitem__(self, item):
        return pipe_with_nonfirst_arg_factory(item)


p = Facade()
