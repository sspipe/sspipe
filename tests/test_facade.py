from sspipe import p, px


def test_normal_args():
    assert (1 | p('{}{}{x}'.format, 2, x=3)) == '123'


def test_pipe_args():
    def f(x, y):
        return x * y

    assert (1 | p(f, px + 1, px + 2)) == 6
