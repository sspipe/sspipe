import pandas as pd
from sspipe import p, px


def test_px_slice():
    df = pd.DataFrame(dict(x=[1, 2, 0], y=[3, 4, 5]))
    assert (df | px[(px.x > 1) & (px.x < px.y)].y.sum()) == 4


def test_dataframe():
    df = {'x': [0, 1, 2], 'y': [3, 4, 5]} | p(pd.DataFrame)
    assert df.shape == (3, 2)

    df = [{'x': 0, 'y': 3}, {'x': 1, 'y': 4}, {'x': 2, 'y': 5}] | p(pd.DataFrame)
    assert df.shape == (3, 2)


def test_loc_tuple():
    df = (
        {'x': [0, 1, 2], 'y': [3, 4, 5]}
        | p(pd.DataFrame)
        | px.loc[px.x > 1, ['y']]
    )
    assert pd.DataFrame({'y': [5]}, index=[2]).equals(df)
