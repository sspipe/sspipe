from .facade import p
from .version import __version__
from .patch import patch_cls_operator

px = p(lambda x: x)

try:
    import pandas

    patch_cls_operator(pandas.Series)
    patch_cls_operator(pandas.DataFrame)
except ImportError:
    pass
