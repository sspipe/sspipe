from sspipe import p, px
import numpy as np


def test_scalar_rhs():
    assert np.int32(1) | p(lambda x: x + 1) | (px == 2)


def test_scalar_lhs():
    assert 2 | px + np.int32(1)


def test_rhs():
    assert np.array([1, 2]) | p(lambda x: x.sum()) | (px == 3)


def test_rhs_px():
    assert np.array([1, 2]) | (px.sum() == 3)


def test_lhs():
    assert 2 | p(np.log2) | (px == 1)


def test_lhs_px():
    assert 2 | np.power(px, px + 1) | (px == 8)
