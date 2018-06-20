import functools

from sspipe.pipe import Pipe


def patch_cls(cls):
    original = cls.__or__

    @functools.wraps(original)
    def wrapper(self, x):
        if isinstance(x, Pipe):
            return x.__ror__(self)
        return original(self, x)

    cls.__or__ = wrapper
