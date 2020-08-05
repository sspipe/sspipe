import functools

from sspipe.pipe import Pipe


def _patch_cls_method(cls, method):
    original = getattr(cls, method)

    @functools.wraps(original)
    def wrapper(self, x, *args, **kwargs):
        if isinstance(x, Pipe):
            return NotImplemented
        return original(self, x, *args, **kwargs)

    setattr(cls, method, wrapper)


def patch_cls_operator(cls):
    _patch_cls_method(cls, '__or__')
    if hasattr(cls, '__ior__'):
        _patch_cls_method(cls, '__ior__')


def patch_all():
    try:
        import pandas

        patch_cls_operator(pandas.Series)
        patch_cls_operator(pandas.DataFrame)
        patch_cls_operator(pandas.Index)
    except ImportError:
        pass

    try:
        import torch

        patch_cls_operator(torch.Tensor)
    except ImportError:
        pass
    
    try:
        from django.db.models import query

        patch_cls_operator(query.QuerySet)

    except ImportError:
        pass
