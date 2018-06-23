import functools

from sspipe import p, px


def test_plmap():
    def plmap(func):
        return p(map, func) | p(list)

    result = [1, 2] | plmap(lambda x: x + 1)
    print(result)
    assert result == [2, 3]
