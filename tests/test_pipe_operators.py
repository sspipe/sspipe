from sspipe import p

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
