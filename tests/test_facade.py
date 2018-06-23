from sspipe import p, px


def test_normal_args():
    assert (2 | p('{}{}{x}'.format, 1, x=3)) == '123'


def test_pipe_args():
    def f(x, y):
        return x * y

    assert (1 | p(f, px + 1, px + 2)) == 6


def test_nonfirst_arg():
    def f(x, y):
        return x + 2 * y

    assert (1 | p[1](f, 2)) == 4


# def test_nonfirst_pipe_arg():
#     def f(x, y):
#         return x + 2 * y
#
#     assert (1 | p[1](f, px * 3)) == 5
