import functools

from sspipe.pipe import Pipe


def patch_cls(cls):
    original = cls.__or__

    @functools.wraps(original)
    def wrapper(self, x):
        if isinstance(x, Pipe):
            return x.__or__(self)
        return original(self, x)

    cls.__or__ = wrapper


def patch_pandas():
    import pandas
    patch_cls(pandas.Series)
    patch_cls(pandas.DataFrame)


def patch_all():
    for patch in [patch_pandas]:
        try:
            patch()
        except ImportError:
            pass
