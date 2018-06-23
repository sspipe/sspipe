from .facade import p, px
from .version import __version__
from .patch import patch_all
from .pipe import Pipe

unpipe = Pipe.unpipe

patch_all()
del patch_all
