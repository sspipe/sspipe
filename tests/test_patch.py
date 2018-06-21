import pytest

from sspipe import p
import pandas as pd


def test_pd_series():
    assert (pd.Series([1, 2]) | p(list)) == [1, 2]
