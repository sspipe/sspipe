from sspipe import p, px


def test_plmap():
    def plmap(func):
        return p(lambda x: map(func, x)) | p(list)

    result = [1, 2] | plmap(lambda x: x + 1)
    print(result)
    assert result == [2, 3]
