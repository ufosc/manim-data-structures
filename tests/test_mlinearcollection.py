import pytest
from manim import *
from manim.utils.testing.frames_comparison import frames_comparison

__module_test__ = "mlinearcollection"

from manim_data_structures import LinearCollection

__module_test__ = "mlinearcollection"


@pytest.fixture(
    params=[
        [],
        [i + 1 for i in range(10)],
        [hash(i) for i in range(50)],
    ],
)
def lc_data(request):
    return request.param


@pytest.fixture(
    params=[
        (Integer, Square, None),
        (Integer, Circle, None),
        (Integer, Circle, Square()),
        (Integer, Square, Arrow()),
    ],
)
def lc(request, lc_data):
    return LinearCollection(lc_data, *request.param)


def is_valid(lc):
    assert type(lc) == LinearCollection
    assert type(lc._LinearCollection__values) == list
    assert type(lc._LinearCollection__datas) == list
    assert type(lc._LinearCollection__containers) == list
    assert isinstance(lc, Mobject)
    assert all(isinstance(data, Mobject) for data in lc._LinearCollection__datas)
    assert all(
        isinstance(container, Mobject) for container in lc._LinearCollection__containers
    )

    assert (
        len(lc._LinearCollection__values)
        == len(lc._LinearCollection__datas)
        == len(lc._LinearCollection__containers)
    )
    if lc._LinearCollection__delimiter is not None:
        assert (len(lc.submobjects) + 1) // 2 == len(lc._LinearCollection__containers)
    else:
        assert len(lc.submobjects) == len(lc._LinearCollection__containers)

    if lc._LinearCollection__delimiter is not None:
        for i in range(len(lc.submobjects)):
            if i % 2 == 1:
                assert isinstance(
                    lc.submobjects[i], type(lc._LinearCollection__delimiter)
                )
            else:
                assert lc.submobjects[i] == lc._LinearCollection__containers[i // 2]
    else:
        for i in range(len(lc.submobjects)):
            assert lc.submobjects[i] == lc._LinearCollection__containers[i]


def test_constructor(lc, lc_data):
    is_valid(lc)
    assert lc._LinearCollection__values == lc_data


def test_insert(lc):
    lc.insert(2, 222)
    try:
        assert lc[2] == 222
    except IndexError:
        assert lc[-1] == 222
    is_valid(lc)

    lc.insert(-3, 333)
    try:
        assert lc[-4] == 333
    except IndexError:
        assert lc[0] == 333
    is_valid(lc)


def test_insert_front(lc):
    lc.insert(0, 222)
    assert lc[0] == 222
    is_valid(lc)


def test_insert_front_negative(lc):
    lc.insert(-len(lc), 222)
    assert lc[0] == 222
    is_valid(lc)


def test_insert_super_negative(lc):
    lc.insert(-len(lc) - 10, 222)
    assert lc[0] == 222
    is_valid(lc)


def test_insert_back(lc):
    lc.insert(len(lc), 222)
    assert lc[-1] == 222
    is_valid(lc)


def test_insert_super_positive(lc):
    lc.insert(len(lc) + 10, 222)
    assert lc[-1] == 222
    is_valid(lc)


def test_remove(lc):
    lc_data = lc._LinearCollection__values.copy()
    original_count = lc.count(3)
    try:
        lc.remove(3)
        lc_data.remove(3)
        assert lc.count(3) == original_count - 1
    except ValueError:
        assert original_count == 0

    assert lc._LinearCollection__values == lc_data
    is_valid(lc)


def test_pop(lc):
    lc_data = lc._LinearCollection__values.copy()
    try:
        assert lc.pop(len(lc_data) // 2) == lc_data.pop(len(lc_data) // 2)
    except IndexError:
        assert len(lc_data) // 2 >= len(lc)
    is_valid(lc)

    try:
        assert lc.pop(-len(lc_data) // 2) == lc_data.pop(-len(lc_data) // 2)
    except IndexError:
        assert -len(lc_data) // 2 < -len(lc) or len(lc) == 0
    is_valid(lc)


def test_clear(lc):
    lc.clear()
    assert len(lc) == 0
    is_valid(lc)


def test_index(lc):
    lc_data = lc._LinearCollection__values.copy()
    try:
        assert lc.index(7) == lc_data.index(7)
    except ValueError:
        assert 7 not in lc_data


def test_sort(lc):
    lc_data = lc._LinearCollection__values.copy()
    lc.sort()
    lc_data.sort()
    for lc_value, data_value in zip(lc, lc_data):
        assert lc_value == data_value


def test_reverse(lc):
    lc_reversed = lc.copy().reverse()

    for i in range(len(lc)):
        assert lc_reversed[i] == lc[-(1 + i)]
    is_valid(lc_reversed)


@pytest.mark.parametrize(
    "other_data",
    [
        [10, 9, 8, 7, 6],
        [1, 2, 3, 4, 5],
        [10000000, 99999999],
    ],
)
def test_comparisons(lc, lc_data, other_data):
    # Mirror list comparison
    other_lc = LinearCollection(other_data)

    assert (lc < other_data) == (lc_data < other_data) == (lc < other_lc)
    assert (lc <= other_data) == (lc_data <= other_data) == (lc <= other_lc)
    assert (lc == other_data) == (lc_data == other_data) == (lc == other_lc)
    assert (lc >= other_data) == (lc_data >= other_data) == (lc >= other_lc)
    assert (lc > other_data) == (lc_data > other_data) == (lc > other_lc)

    # Mathematically consistent
    assert (lc < other_data) != (lc >= other_data)
    assert (lc <= other_data) != (lc > other_data)
    assert (lc == other_data) != (lc != other_data)
    assert (lc >= other_data) != (lc < other_data)
    assert (lc > other_data) != (lc <= other_data)

    try:
        _ = lc < tuple(other_data)
        assert "Should have raised TypeError"
    except TypeError:
        pass
    try:
        _ = lc <= tuple(other_data)
        assert "Should have raised TypeError"
    except TypeError:
        pass

    assert lc == tuple(other_data) is False
    assert lc != tuple(other_data)

    try:
        _ = lc >= tuple(other_data)
        assert "Should have raised TypeError"
    except TypeError:
        pass
    try:
        _ = lc > tuple(other_data)
        assert "Should have raised TypeError"
    except TypeError:
        pass


def test_getitem(lc):
    lc_data = lc._LinearCollection__values.copy()
    for i in range(len(lc_data)):
        assert lc[i] == lc._LinearCollection__values[i]
        assert lc[i] == lc_data[i]


def test_setitem(lc):
    lc_data = lc._LinearCollection__values.copy()
    for i in range(len(lc_data)):
        assert lc[i] == lc_data[i]
        lc[i] = lc_data[-(1 + i)]

    for i in range(len(lc_data)):
        assert lc[i] == lc_data[-(1 + i)]
    is_valid(lc)


def test_delitem_front(lc):
    lc_data = lc._LinearCollection__values.copy()
    for i in range(len(lc_data)):
        del lc[0]
        del lc_data[0]
        assert lc._LinearCollection__values == lc_data
        is_valid(lc)


def test_delitem_back(lc):
    lc_data = lc._LinearCollection__values.copy()
    for _ in range(len(lc_data)):
        del lc[-1]
        del lc_data[-1]
        assert lc._LinearCollection__values == lc_data
        is_valid(lc)


def test_iteration(lc):
    lc_data = lc._LinearCollection__values.copy()
    for lc_value, data_value in zip(lc, lc_data):
        assert lc_value == data_value


def test_add(lc):
    lc1 = lc.copy()
    lc2 = lc.copy().reverse()
    lc += lc2

    for i, value in enumerate(lc1 + lc2):
        if i < len(lc1):
            assert value == lc1[i]
        else:
            assert value == lc2[i % len(lc2)]
        assert value == lc[i]
    is_valid(lc)


def test_mul(lc):
    lc1 = lc.copy()
    lc *= 3

    supports_index_3 = type("_", (), {"__index__": lambda self: 3})()

    for i, (value, ivalue, rvalue) in enumerate(
        zip(lc1 * 3, lc1 * supports_index_3, supports_index_3 * lc1)
    ):
        assert value == lc1[i % len(lc1)]
        assert value == ivalue == rvalue
        assert value == lc[i]
    is_valid(lc)


def test_copy(lc):
    lc_copy = lc.copy()
    assert lc_copy is not lc
    assert lc_copy == lc
    is_valid(lc_copy)

    if len(lc) > 0:
        lc.clear()
        assert lc_copy != lc

@frames_comparison
def test_add_to_scene(scene, lc):
    scene.play(Create(lc))
