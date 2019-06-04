from sspipe import p, px


def test_list_creation():
    assert (2 | p([1, px, px + 1])) == [1, 2, 3]


def test_tuple_creation():
    assert (2 | p((1, px, px + 1))) == (1, 2, 3)


def test_set_creation():
    assert (2 | p({1, px, px + 1})) == {1, 2, 3}


def test_dict_creation():
    assert (2 | p({1: px, px: 3, px + 1: px + 2, 4: 5})) == {i: i + 1 for i in range(1, 5)}
