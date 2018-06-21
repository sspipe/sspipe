from sspipe import p, px

pinc = p(lambda x: x + 1)
pcdr = p(lambda x: x[1:])


def test_level1():
    cases = [
        [True, 1 not in [1, 2] | pcdr],
        [True, 2 | pinc > 2],
        [False, 2 | pinc < 3],
        [2 | pinc + 1, 4],
        # TODO: write test for rest
    ]
    for expected, result in cases:
        assert result == expected


def test_divide():
    pipeline = 1 / px
    assert (2 | pipeline) == 0.5


def test_divide_fallback():
    assert (dict(x=2, y=3).keys() / p(list) | p(set)) == {'x', 'y'}
    assert (dict(x=2, y=3).values() / p(list) | p(set)) == {2, 3}
