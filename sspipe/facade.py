from __future__ import absolute_import
import pipe
from sspipe.compatibility import convert_pipe
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
        if not args and not kwargs:
            return Pipe(func)
        elif any(
            isinstance(arg, Pipe) for arg in args
        ) or any(
            isinstance(arg, Pipe) for arg in kwargs.values()
        ) or isinstance(func, Pipe):
            return Pipe.partial(func, *args, **kwargs)
        elif func in (map, filter):
            return Pipe(lambda x: func(*args, x, **kwargs))
        else:
            return Pipe(lambda x: func(x, *args, **kwargs))


for helper in pipe.__all__:
    if helper != 'Pipe':
        setattr(Facade, helper, convert_pipe(getattr(pipe, helper)))

p = Facade()
px = Pipe(lambda x: x)
