from manim import Integer, Mobject, Square

from manim_data_structures import LinearCollection


def test_constructor():
    data = [i + 1 for i in range(10)]
    lc = LinearCollection(data)
    assert type(lc) == LinearCollection
    assert type(lc._LinearCollection__data) == list
    assert isinstance(lc, Mobject)
    assert isinstance(lc._LinearCollection__data[0], Mobject)
    assert isinstance(lc.submobjects[0], Mobject)
    assert type(lc._LinearCollection__data[0]) == Integer
    assert type(lc.submobjects[0]) == Square

    for i in range(len(data)):
        assert lc._LinearCollection__data[i].get_value() == i + 1
        assert lc.submobjects[i].submobjects[0].get_value() == i + 1


def test_insertion():
    pass


def test_removal():
    pass


def test_getitem():
    data = [i + 1 for i in range(10)]
    lc = LinearCollection(data)

    for i in range(len(data)):
        assert lc[i] == data[i]


def test_setitem():
    data = [i + 1 for i in range(10)]
    lc = LinearCollection(data)

    for i in range(len(data)):
        assert lc[i] == data[i]
        lc[i] = data[-(1 + i)]

    for i in range(len(data)):
        assert lc[i] == data[-(1 + i)]


def test_iteration():
    data = [i + 1 for i in range(10)]
    lc = LinearCollection(data)

    for lc_value, data_value in zip(lc, data):
        assert lc_value == data_value


def test_add():
    data = [i + 1 for i in range(10)]
    lc1 = LinearCollection(data)
    lc2 = LinearCollection(data[::-1])

    for i in range(len(data)):
        assert lc1[i] == data[i]
        assert lc2[i] == data[-(1 + i)]

    for i, value in enumerate(lc1 + lc2):
        if i < len(data):
            assert value == lc1[i]
        else:
            assert value == lc2[i - len(data)]
