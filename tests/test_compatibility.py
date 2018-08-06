from sspipe import p, px


def test_simple():
    assert range(3) | p.select(lambda x: x + 1) | p(list) | (px == [1, 2, 3])


def test_integration_with_px():
    assert range(3) | p.select(px + 1) | p(list) | (px == [1, 2, 3])
