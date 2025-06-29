"""Tests helpers.py"""

import pytest

from netports import helpers as h

APOSTROPHE = "'"
SPEECH = "\""


# =============================== bool ===============================

@pytest.mark.parametrize("kwargs, expected", [
    ({"all": True}, True),
    ({"all": 1}, True),
    ({"all": False}, False),
    ({"verbose": True}, False),
    ({}, False),
])
def test__is_all(kwargs, expected):
    """helpers.is_all()"""
    actual = h.is_all(**kwargs)
    assert actual == expected


@pytest.mark.parametrize("kwargs, expected", [
    ({"verbose": True}, False),
    ({"verbose": 1}, False),
    ({"verbose": False}, True),
    ({"brief": True}, True),
    ({}, True),
])
def test__is_brief(kwargs, expected):
    """helpers.is_brief()"""
    actual = h.is_brief(**kwargs)
    assert actual == expected


@pytest.mark.parametrize("items, expected", [
    (1, False),
    ("1", False),
    ([], False),
    ([1], False),
    (["0-1"], False),
    (-1, True),
    ("-1", True),
    ([-1], True),
    (["-1"], True),
    ([1, -1], True),
    (["1", "-1"], True),
])
def test__is_brief_in_items(items, expected):
    """helpers.is_brief_in_items()"""
    actual = h.is_brief_in_items(items=items)
    assert actual == expected


@pytest.mark.parametrize("kwargs, expected", [
    ({"verbose": True}, True),
    ({"verbose": 1}, True),
    ({"verbose": False}, False),
    ({"brief": True}, False),
    ({}, False),
])
def test__is_verbose(kwargs, expected):
    """helpers.is_verbose()"""
    actual = h.is_verbose(**kwargs)
    assert actual == expected


@pytest.mark.parametrize("kwargs, expected", [
    ({"strict": True}, True),
    ({"strict": False}, False),
    ({}, True),
])
def test__is_strict(kwargs, expected):
    """helpers.is_strict()"""
    actual = h.is_strict(**kwargs)
    assert actual == expected


# =============================== int ================================

@pytest.mark.parametrize("number, expected", [
    (0, 0),
    ("0", 0),
    ("a", TypeError),
    ("-1", TypeError),
])
def test__to_int(number, expected):
    """helpers.to_int()"""
    if isinstance(expected, int):
        actual = h.to_int(number=number)
        assert actual == expected
    else:
        with pytest.raises(expected):
            h.to_int(number=number)


@pytest.mark.parametrize("numbers, expected", [
    ([0, 1, "2"], [0, 1, 2]),
    (1, TypeError),
    (["a"], TypeError),
    (["-1"], TypeError),
])
def test__to_lint(numbers, expected):
    """helpers.to_lint()"""
    if isinstance(expected, list):
        actual = h.to_lint(numbers=numbers)
        assert actual == expected
    else:
        with pytest.raises(expected):
            h.to_lint(numbers=numbers)


@pytest.mark.parametrize("items, expected", [
    ("", [""]),
    ("1,3-5", ["1,3-5"]),
    (0, ["0"]),
    (1, ["1"]),
    (b"1", ["1"]),
    (0.9, ["0"]),
    (0.5, ["0"]),
    (1.9, ["1"]),
    ([], []),
    ([0, 1, 1.5, "1.5", "2-4"], ["0", "1", "1", "1.5", "2-4"]),
    ((0, 1), ["0", "1"]),
    ({0: "", 1: ""}, ["0", "1"]),
    ([[1]], ["[1]"]),
    (str, TypeError),
])
def test__lstr(items, expected):
    """helpers.lstr()"""
    if isinstance(expected, list):
        actual = h.lstr(items=items)
        assert actual == expected
    else:
        with pytest.raises(expected):
            h.lstr(items=items)


# ============================= list =============================


@pytest.mark.parametrize("items, expected", [
    ("", [""]),
    ([], []),
    ([1], [1]),
    (-1, []),
    ("-1", []),
    ([-1, 1], [1]),
    (["-1", "1"], ["1"]),
])
def test__remove_brief_items(items, expected):
    """helpers.remove_brief_items()"""
    actual = h.remove_brief_items(items=items)
    assert actual == expected


@pytest.mark.parametrize("items, expected", [
    ("", []),
    ("1,3-5,a", ["1", "3-5", "a"]),
    (0, ["0"]),
    (1, ["1"]),
    (b"1", ["1"]),
    (0.9, ["0"]),
    (0.5, ["0"]),
    (1.9, ["1"]),
    ([], []),
    ([0, 1.5, "1.5", "2-4", "a", "b,c"], ["0", "1", "1.5", "2-4", "a", "b", "c"]),
    ((0, 1), ["0", "1"]),
    ({0: "", 1: ""}, ["0", "1"]),
    ([[1]], ["[1]"]),
    (str, TypeError),
])
def test__split(items, expected):
    """helpers.split()"""
    if isinstance(expected, list):
        actual = h.split(items=items)
        assert actual == expected
    else:
        with pytest.raises(expected):
            h.split(items=items)
