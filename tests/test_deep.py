from sspipe import p, px


def test_simple():
    def f(x, y):
        return x * y

    result = 1 | p(f, px + 1, px + 2)
    assert result == 6


def test_plmap():
    result = [1, 2] | p(map, lambda x: x+1) | p(list)
    print(result)
    assert result == [2, 3]
