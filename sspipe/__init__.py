from .facade import p
from .version import __version__
from .patch import patch_all

px = p(lambda x: x)

patch_all()
del patch_all
