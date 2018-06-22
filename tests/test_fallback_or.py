from sspipe import p, px


def test_divide_fallback():
    assert (dict(x=2, y=3).keys() / p(list) | p(set)) == {'x', 'y'}
    assert (dict(x=2, y=3).values() / p(list) | p(set)) == {2, 3}

