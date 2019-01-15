from sspipe import p, px

pinc = p(lambda x: x + 1)
pcdr = p(lambda x: x[1:])


def test_level1():
    cases = [
        [True, 1 not in [1, 2] | pcdr],
        [True, 2 | pinc > 2],
        [False, 2 | pinc < 3],
        [1, 2 | pinc & 5],
        [7, 2 | (pinc | 4)],
        [1 | pinc + 2, 4],
        # TODO: write test for rest
    ]
    for expected, result in cases:
        assert expected == result


def test_level2():
    result = 1 | (px == px)
    assert result == True


def test_divide():
    pipeline = 1 / px
    assert (2 | pipeline) == 0.5

    pipeline = (px + 1) / (px + 2)
    assert (2 | pipeline) == 0.75


def test_reverse():
    assert (1 | 2 + px) == 3
    assert (1 | 2 << px) == 4


def test_order():
    assert ('a' | px + 'b') == 'ab'
    assert ('a' | 'b' + px) == 'ba'
