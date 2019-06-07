from sspipe import p, px, unpipe

def test_unpipe_active():
    a_pipe = px + 1 | px * 5
    func = unpipe(a_pipe)
    assert func(0) == 5

def test_unpipe_passive():
    func = lambda x: (x + 1) * 5
    func = unpipe(func)
    assert func(0) == 5
    