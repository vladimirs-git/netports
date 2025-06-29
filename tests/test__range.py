"""Tests range.py"""

import pytest

from netports import Range, Item, NetportsValueError
from netports.types_ import StrIInt
from tests import helpers_


@pytest.fixture
def range_(items: StrIInt) -> Range:
    """Create Range objects."""
    return Range(items=items)


@pytest.mark.parametrize("items, expected", [
    ("1,3-5", 8499776695296556729),
])
def test__hash__(range_, items, expected):
    """Range.__hash__()."""
    actual = hash(range_)
    assert actual == expected


@pytest.mark.parametrize("items1, items2, expected", [
    ("1,3-5", "1,3-5", True),
    ("1,3-5", "1,3,4,5", True),
    ("1,3-5", "1", False),
])
def test__eq__(items1, items2, expected):
    """Range.__eq__()."""
    actual = Range(items1) == Range(items2)
    assert actual == expected


@pytest.mark.parametrize("items1, items2, expected", [
    ("0", "0", False),
    ("0", "1", True),
    ("0", "", False),
    ("1", "0", False),
    ("1", "1", False),
    ("1", "2", True),
    ("1,3-5", "0", False),
    ("1,3-5", "1", False),
    ("1,3-5", "2", True),
    ("1,3-5", "6", True),
    ("1,3-5", "3-5", True),
    ("1,3-5", "1,3-5", False),
    ("", "", False),
    ("", "0", True),
])
def test__lt__(items1, items2, expected):
    """Range.__lt__()."""
    actual = Range(items1) < Range(items2)
    assert actual == expected


@pytest.mark.parametrize("items, expected", [
    (["0", "1,3-5"], ["0", "1,3-5"]),
    (["1,3-5", "0"], ["0", "1,3-5"]),
    (["0-6", "1,3-5"], ["0-6", "1,3-5"]),
    (["1,3-5", "0-6"], ["0-6", "1,3-5"]),
    (["1", "1,3-5"], ["1", "1,3-5"]),
    (["1,3-5", "1"], ["1", "1,3-5"]),
    (["2", "1,3-5"], ["1,3-5", "2"]),
    (["1,3-5", "2"], ["1,3-5", "2"]),
    (["6", "1,3-5"], ["1,3-5", "6"]),
    (["1,3-5", "6"], ["1,3-5", "6"]),
    (["3-5", "1,3-5"], ["1,3-5", "3-5"]),
    (["1,3-5", "3-5"], ["1,3-5", "3-5"]),
])
def test__lt__sorting(items, expected):
    """Test Range.__lt__() sorting."""
    items_ = [Range(s) for s in items]

    results = sorted(items_)

    actual = [str(o) for o in results]
    assert actual == expected


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0", "0-1,3-5"),
    ("1,3-5", "1", "1,3-5"),
    ("1,3-5", "2", "1-5"),
    ("1,3-5", "3", "1,3-5"),
    ("1,3-5", "4", "1,3-5"),
    ("1,3-5", "5", "1,3-5"),
    ("1,3-5", "6", "1,3-6"),
    ("1,3-5", "7", "1,3-5,7"),
])
def test__add__(range_, items, items2, expected):
    """Range.__add__()."""
    result = range_ + Range(items2)

    actual = result.line
    assert actual == expected


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0", "1,3-5"),
    ("1,3-5", "1", "3-5"),
    ("1,3-5", "2", "1,3-5"),
    ("1,3-5", "3", "1,4-5"),
    ("1,3-5", "4", "1,3,5"),
    ("1,3-5", "5", "1,3-4"),
    ("1,3-5", "6", "1,3-5"),
    ("1,3-5", "7", "1,3-5"),
])
def test__sub__(range_, items, items2, expected):
    """Range.__sub__()."""
    result = range_ - Range(items2)

    actual = result.line
    assert actual == expected


@pytest.mark.parametrize("items, number, expected", [
    ("1,3-5", 0, False),
    ("1,3-5", 1, True),
    ("1,3-5", 2, False),
    ("1,3-5", 3, True),
    ("1,3-5", 4, True),
    ("1,3-5", 5, True),
    ("1,3-5", 6, False),
])
def test__contains__(range_, items, number, expected):
    """Range.__contains__()."""
    actual = number in range_
    assert actual == expected


@pytest.mark.parametrize("items, idx, expected", [
    ("1,3-5", 0, "3-5"),
    ("1,3-5", 1, "1,4-5"),
    ("1,3-5", 2, "1,3,5"),
    ("1,3-5", 3, "1,3-4"),
    ("1,3-5", -1, "1,3-4"),
    ("1,3-5", 4, IndexError),
])
def test__delitem__(range_, items, idx, expected):
    """Range.__delitem__()."""
    if isinstance(expected, str):
        del range_[idx]
        actual = range_.line
        assert actual == expected
    else:
        with pytest.raises(expected):
            del range_[idx]


@pytest.mark.parametrize("items, idx, expected", [
    ("1,3-5", 0, 1),
    ("1,3-5", 1, 3),
    ("1,3-5", 2, 4),
    ("1,3-5", 3, 5),
    ("1,3-5", -1, 5),
    ("1,3-5", 4, IndexError),
])
def test__getitem__(range_, items, idx, expected):
    """Range.__getitem__()."""
    if isinstance(expected, int):
        actual = range_[idx]
        assert actual == expected
    else:
        with pytest.raises(expected):
            # noinspection PyStatementEffect
            range_[idx]  # pylint: disable=pointless-statement


def test__iter__():
    """Range.__iter__()."""
    range_o = Range("1,3-5")
    for actual in range_o:
        _ = actual


@pytest.mark.parametrize("items, expected", [
    ("1", 1),
    ("1,3", 2),
    ("3-5", 3),
    ("1,3-5", 4),
])
def test__len__(range_, items, expected):
    """Range.__len__()."""
    actual = len(range_)
    assert actual == expected


def test__next__():
    """Range.__next__()."""
    range_o = Range("1,3-5")
    for expected in [
        1,
        3,
        4,
        5,
    ]:
        actual = next(range_o)
        assert actual == expected


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0", "0-1,3-5"),
    ("1,3-5", "1", "1,3-5"),
    ("1,3-5", "2", "1-5"),
    ("1,3-5", "3", "1,3-5"),
    ("1,3-5", "4", "1,3-5"),
    ("1,3-5", "5", "1,3-5"),
    ("1,3-5", "6", "1,3-6"),
    ("1,3-5", "7", "1,3-5,7"),
])
def test__add(range_, items, items2, expected):
    """Range.add()."""
    range_.add(Range(items2))

    actual = range_.line
    assert actual == expected


@pytest.mark.parametrize("items, number, expected", [
    ("1", 3, "1,3"),
    ("1", "3", "1,3"),
    ("1", [3], TypeError),
])
def test__append(range_, items, number, expected):
    """Range.append()."""
    if isinstance(expected, str):
        range_.append(number)

        actual = range_.line
        assert actual == expected
    else:
        with pytest.raises(expected):
            range_.append(number)


@pytest.mark.parametrize("items, expected, exp_numbers", [
    ("1,3-5", "", []),
])
def test__clear(range_, items, expected, exp_numbers):
    """Range.clear()."""
    range_.clear()

    assert range_.line == expected
    assert range_.numbers() == exp_numbers


def test__copy():
    """Range.copy()"""
    range1 = Range("1")
    range2 = range1.copy()

    range2.append("2")

    actual = range1.line
    assert actual == "1"
    assert range2.line == "1-2"


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0", "1,3-5"),
    ("1,3-5", "1", "3-5"),
    ("1,3-5", "2", "1,3-5"),
    ("1,3-5", "3", "1,4-5"),
    ("1,3-5", "4", "1,3,5"),
    ("1,3-5", "5", "1,3-4"),
    ("1,3-5", "6", "1,3-5"),
])
def test__difference(range_, items, items2, expected):
    """Range.difference()."""
    range2 = Range(items2)

    range3 = range_.difference(range2)

    actual = range3.line
    assert actual == expected
    assert range_.line == items
    assert range2.line == items2


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0", "1,3-5"),
    ("1,3-5", "1", "3-5"),
    ("1,3-5", "2", "1,3-5"),
    ("1,3-5", "3", "1,4-5"),
    ("1,3-5", "4", "1,3,5"),
    ("1,3-5", "5", "1,3-4"),
    ("1,3-5", "6", "1,3-5"),
])
def test__difference_update(range_, items, items2, expected):
    """Range.difference_update()."""
    range2 = Range(items2)

    range_.difference_update(range2)

    actual = range_.line
    assert actual == expected
    actual = range2.line
    assert actual == items2


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "1", "3-5"),
    ("1,3-5", 2, "1,3-5"),
    ("1,3-5", 3, "1,4-5"),
])
def test__discard(range_, items, items2, expected):
    """Range.discard()."""
    range_.discard(items2)

    actual = range_.line
    assert actual == expected


@pytest.mark.parametrize("items, numbers, expected", [
    ("1", [3], "1,3"),
    ("1", [3], "1,3"),
    ("1", ["3"], "1,3"),
    ("1", [3, 4, 5], "1,3-5"),
    # error
    ("1", 3, TypeError),
    ("1", "3", TypeError),
    ("1", ["a"], NetportsValueError),
])
def test__extend(range_, items, numbers, expected):
    """Range.extend()."""
    if isinstance(expected, str):
        range_.extend(numbers)

        actual = range_.line
        assert actual == expected
    else:
        with pytest.raises(expected):
            range_.extend(numbers)


def test__index():
    """Range.index()."""
    range1 = Range("1,3-5")
    for item, expected in [
        (1, 0),
        ("3", 1),
        (4, 2),
        (5, 3),
        (2, ValueError),
    ]:
        if isinstance(expected, int):
            actual = range1.index(item)
            assert actual == expected
        else:
            with pytest.raises(expected):
                range1.index(item)


def test__intersection():
    """Range.intersection()."""
    range1 = Range("1,3-5")
    for line, expected, in [
        ("0,6", ""),
        ("0-3", "1,3"),
        ("5-7", "5"),
    ]:
        range2 = Range(line)
        range3 = range1.intersection(range2)

        actual = range3.line
        assert actual == expected
        assert range1.line == "1,3-5"
        assert range2.line == line


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0,6", ""),
    ("1,3-5", "0-3", "1,3"),
    ("1,3-5", "5-7", "5"),
])
def test__intersection_update(range_, items, items2, expected):
    """Range.intersection_update()."""
    range2 = Range(items2)

    range_.intersection_update(range2)

    actual = range_.line
    assert actual == expected
    assert range2.line == items2


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0,6", True),
    ("1,3-5", "1", False),
    ("1,3-5", "5-7", False),
])
def test__isdisjoint(range_, items, items2, expected):
    """Range.isdisjoint()."""
    range2 = Range(items2)

    actual = range_.isdisjoint(range2)

    assert actual == expected


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0,6", False),
    ("1,3-5", "1", False),
    ("1,3-5", "5-7", False),
    ("1,3-5", "1,3-5", True),
    ("1,3-5", "1-5", True),
])
def test__issubset(range_, items, items2, expected):
    """Range.issubset()."""
    range2 = Range(items2)

    actual = range_.issubset(range2)

    assert actual == expected


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0,6", False),
    ("1,3-5", "1", True),
    ("1,3-5", "5-7", False),
    ("1,3-5", "1,3-5", True),
    ("1,3-5", "1-5", False),
])
def test__issuperset(range_, items, items2, expected):
    """Range.issuperset()."""
    range2 = Range(items2)

    actual = range_.issuperset(range2)

    assert actual == expected


def test__pop():
    """Range.pop()."""
    range1 = Range("1,3-5")
    for number, expected in [
        (5, "1,3-4"),
        (4, "1,3"),
    ]:
        actual_ = range1.pop()
        assert actual_ == number
        actual = range1.line
        assert actual == expected


def test__remove():
    """Range.remove()."""
    range1 = Range("1,3-5")
    for number, expected in [
        (4, "1,3,5"),
        ("3", "1,5"),
        (6, ValueError),
    ]:
        if isinstance(expected, str):
            range1.remove(number)
            actual = range1.line
            assert actual == expected
        else:
            with pytest.raises(expected):
                range1.remove(number)


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0,6", "0-1,3-6"),
    ("1,3-5", "1", "3-5"),
    ("1,3-5", "2", "1-5"),
    ("1,3-5", "1,3-5", ""),
])
def test__symmetric_difference(range_, items, items2, expected):
    """Range.symmetric_difference()."""
    range2 = Range(items2)

    range3 = range_.symmetric_difference(range2)

    actual = range3.line
    assert actual == expected


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0,6", "0-1,3-6"),
    ("1,3-5", "1", "3-5"),
    ("1,3-5", "2", "1-5"),
    ("1,3-5", "1,3-5", ""),
])
def test__symmetric_difference_update(range_, items, items2, expected):
    """Range.symmetric_difference_update()."""
    range2 = Range(items2)

    range_.symmetric_difference_update(range2)

    actual = range_.line
    assert actual == expected


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0,6", "0-1,3-6"),
    ("1,3-5", "1", "1,3-5"),
    ("1,3-5", "2", "1-5"),
    ("1,3-5", "1,3-5", "1,3-5"),
])
def test__union(range_, items, items2, expected):
    """Range.union()."""
    range2 = Range(items2)

    range3 = range_.union(range2)

    actual = range3.line
    assert actual == expected


@pytest.mark.parametrize("items, items2, expected", [
    ("1,3-5", "0,6", "0-1,3-6"),
    ("1,3-5", "1", "1,3-5"),
    ("1,3-5", "2", "1-5"),
    ("1,3-5", "1,3-5", "1,3-5"),
])
def test__update(range_, items, items2, expected):
    """Range.update()"""
    range2 = Range(items2)

    range_.update(range2)

    actual = range_.line
    assert actual == expected


@pytest.mark.parametrize("params, expected", [
    # line
    ({}, {"line": "", "numbers": []}),
    ({"items": ""}, {"line": "", "numbers": []}),
    ({"items": "0"}, {"line": "0", "numbers": [0]}),
    ({"items": "0,1"}, {"line": "0-1", "numbers": [0, 1]}),
    ({"items": "0,2"}, {"line": "0,2", "numbers": [0, 2]}),
    ({"items": "0 1", "splitter": " "}, {"line": "0-1", "numbers": [0, 1]}),
    ({"items": "0 2", "splitter": " "}, {"line": "0 2", "numbers": [0, 2]}),
    ({"items": "0-1"}, {"line": "0-1", "numbers": [0, 1]}),
    ({"items": "0 to 1", "range_splitter": " to "}, {"line": "0 to 1", "numbers": [0, 1]}),
    ({"items": "1,3-5"}, {"line": "1,3-5", "numbers": [1, 3, 4, 5]}),
    ({"items": "1,3,4,5,3-4,4-5,3-5"}, {"line": "1,3-5", "numbers": [1, 3, 4, 5]}),
    ({"items": "1 3 to 5", "splitter": " ", "range_splitter": " to "},
     {"line": "1 3 to 5", "numbers": [1, 3, 4, 5]}),
    ({"items": "1 3 to 5 7 9 to 10 1 4 to 5", "splitter": " ", "range_splitter": " to "},
     {"line": "1 3 to 5 7 9 to 10", "numbers": [1, 3, 4, 5, 7, 9, 10]}),
    ({"items": "1,3-5,a,7-a,a-7", "strict": False}, {"line": "1,3-5", "numbers": [1, 3, 4, 5]}),
    # numbers
    ({"items": 0}, {"line": "0", "numbers": [0]}),
    ({"items": 1}, {"line": "1", "numbers": [1]}),
    ({"items": [0]}, {"line": "0", "numbers": [0]}),
    ({"items": [0, 1]}, {"line": "0-1", "numbers": [0, 1]}),
    ({"items": ["0", "1"]}, {"line": "0-1", "numbers": [0, 1]}),
    ({"items": [0, 2]}, {"line": "0,2", "numbers": [0, 2]}),
    ({"items": {0, 2}}, {"line": "0,2", "numbers": [0, 2]}),
    ({"items": (0, 2)}, {"line": "0,2", "numbers": [0, 2]}),
    ({"items": [1, 3, 4, 5]}, {"line": "1,3-5", "numbers": [1, 3, 4, 5]}),
    ({"items": [5, 1, 1, 3, 4]}, {"line": "1,3-5", "numbers": [1, 3, 4, 5]}),
    ({"items": [1, 3, 4, 5], "splitter": " ", "range_splitter": " to "},
     {"line": "1 3 to 5", "numbers": [1, 3, 4, 5]}),
])
def test__line(params, expected):
    """Range.line."""
    range1 = Range(**params)
    # getter
    helpers_.test_attrs(obj=range1, exp_d=expected)
    # setter
    if params and isinstance(params["items"], str):
        range1.line = params["items"]
        helpers_.test_attrs(obj=range1, exp_d=expected)


@pytest.mark.parametrize("items, items_, strict, expected", [
    # strict=True
    ("1", [], True, []),
    ("1", [""], True, []),
    ("1", ["1", "3-5"], True, ["1", "3-5"]),
    ("1", ["1", "3-5", "1", "3-4", "4-5"], True, ["1", "3-5"]),
    ("1", ["a"], True, ValueError),
    # strict=False
    ("1", [], False, []),
    ("1", [""], False, []),
    ("1", ["1", "3-5"], False, ["1", "3-5"]),
    ("1", ["1", "3-5", "1", "3-4", "4-5"], False, ["1", "3-5"]),
    ("1", ["3-"], False, []),
    ("1", ["-5"], False, []),
    ("1", ["1-3-5"], False, []),
    ("1", ["a"], False, []),
    ("1", ["3-a"], False, []),
    ("1", ["a-3"], False, []),
    ("1", ["1", "3-5", "a"], False, ["1", "3-5"]),
])
def test__create_items(items, items_, strict, expected):
    """Range._create_items()."""
    range1 = Range("1", strict=strict)

    if isinstance(expected, list):
        results = range1._create_items(items=items_)
        actual = [o.line for o in results]
        assert actual == expected
    else:
        with pytest.raises(expected):
            range1._create_items(items=items_)


@pytest.mark.parametrize("items_, kwargs, expected", [
    ([], {}, ""),
    ([Item("1")], {}, "1"),
    ([Item("3-5")], {}, "3-5"),
    ([Item("1"), Item("3-5")], {}, "1,3-5"),
    ([Item("1"), Item("3-5")], {"splitter": " ", "range_splitter": " to "}, "1 3 to 5"),
])
def test__items_to_line(items_, kwargs, expected):
    """Range._items_to_line()"""
    range1 = Range(item="1", **kwargs)

    actual = range1._items_to_line(items=items_)

    assert actual == expected


@pytest.mark.parametrize("items, items_, expected", [
    ("1", [], []),
    ("1", [Item("1")], [Item("1")]),
    ("1", [Item("3-5")], [Item("3-5")]),
    ("1", [Item("3-5"), Item("1")], [Item("1"), Item("3-5")]),
    ("1", [Item("1"), Item("3-5"), Item("1"), Item("3-4")], [Item("1"), Item("3-5")]),
])
def test__items_wo_duplicates(range_, items, items_, expected):
    """Range._items_wo_duplicates()"""
    actual = range_._items_wo_duplicates(items=items_)
    assert actual == expected
