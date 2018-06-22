from sspipe import p, px


def test_map():
    result = [1, 2] | p.map(px + 1) | p(list)
    assert result == [2, 3]
