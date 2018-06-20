from .facade import p
from .version import __version__
from .patch import patch_cls

px = p(lambda x: x)

try:
    import pandas

    patch_cls(pandas.Series)
    patch_cls(pandas.DataFrame)
except ImportError:
    pass
