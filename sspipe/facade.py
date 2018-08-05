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
        if not args and not kwargs:
            return Pipe(func)
        elif any(
            isinstance(arg, Pipe) for arg in args
        ) or any(
            isinstance(arg, Pipe) for arg in kwargs.values()
        ) or isinstance(func, Pipe):
            return Pipe.partial(func, *args, **kwargs)
        else:
            return Pipe(lambda x: func(*args, x, **kwargs))

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


p = Facade()
px = Pipe(lambda x: x)
