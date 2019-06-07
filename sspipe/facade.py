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
        if isinstance(func, (list, tuple, dict, set)):
            if args or kwargs:
                raise RuntimeError('You should pass no extra args to Pipe if its first input is list or tuple')
            return Pipe.collection(func)
        if not args and not kwargs:
            return Pipe(func)
        elif func in (map, filter):
            if len(args) == 1:
                f, x = args[0], px
            elif len(args) == 2:
                f, x = args
            else:
                raise RuntimeError('You should pass only one function/pipe to p(map) and p(filter)')
            if kwargs:
                raise RuntimeError('You should pass no kwargs to p(map) and p(filter)')
            return Pipe.partial(func, Pipe.unpipe(f), x)
        elif any(
            isinstance(arg, Pipe) for arg in args
        ) or any(
            isinstance(arg, Pipe) for arg in kwargs.values()
        ) or isinstance(func, Pipe):
            return Pipe.partial(func, *args, **kwargs)
        else:
            return Pipe(lambda x: func(x, *args, **kwargs))


for helper in pipe.__all__:
    if helper != 'Pipe':
        setattr(Facade, helper, convert_pipe(getattr(pipe, helper)))

p = Facade()
px = Pipe(lambda x: x)
