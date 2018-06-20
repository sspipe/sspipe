import pandas as pd
from sspipe import p, px


def test_px_slice():
    df = pd.DataFrame(dict(x=[1, 2, 0], y=[3, 4, 5]))
    assert (df | px[(px.x > 1) & (px.x < px.y)].y.sum()) == 4
