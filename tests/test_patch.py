from sspipe import p, px
import pandas as pd


def test_pd_series():
    result = pd.Series([1, 2]) | p(list)
    assert result == [1, 2]


def test_pd_dataframe():
    result = pd.DataFrame({'x': [1, 2], 'y': [3, 4]}) | px.size
    assert result == 4


def test_pd_index():
    result = pd.date_range('2017', '2018') | px.size
    assert result == 366
