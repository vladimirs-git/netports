"""Tests item.py"""

import pytest

from netports import Item
from tests import helpers_


@pytest.fixture
def item__(line: str) -> Item:
    """Create Item objects."""
    return Item(line=line)


@pytest.mark.parametrize("line, expected", [
    ("1-2", hash((1, 2))),
])
def test__hash__(line, expected):
    """Item.__hash__()."""
    item = Item(line=line)
    actual = hash(item)
    assert actual == expected


@pytest.mark.parametrize("line1, line2, expected", [
    ("1-2", "1-2", True),
    ("1-2", "0-2", False),
    ("1-2", "1", False),
    ("1-2", "2", False),
])
def test__eq__(line1, line2, expected):
    """Item.__eq__()."""
    actual = Item(line1) == Item(line2)
    assert actual == expected


@pytest.mark.parametrize("line1, line2, expected", [
    ("1-2", "1-2", False),
    ("1-2", "0", False),
    ("1-2", "1", False),
    ("1-2", "2", True),
    ("1-2", "0-3", False),
    ("1-2", "2-3", True),
    ("1-2", "1-1", False),
    ("1-2", "1-3", True),
])
def test__lt__(line1, line2, expected):
    """Item.__lt__()."""
    actual = Item(line1) < Item(line2)
    assert actual == expected


@pytest.mark.parametrize("lines, expected", [
    (["1-2", "0"], ["0", "1-2"]),
    (["0", "1-2"], ["0", "1-2"]),
    (["1-2", "2"], ["1-2", "2"]),
    (["2", "1-2"], ["1-2", "2"]),
])
def test__lt__sorting(lines, expected):
    """Item.__lt__() sorting."""
    items = [Item(s) for s in lines]

    results = sorted(items)

    actual = [str(o) for o in results]
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("0", {"line": "0", "min": 0, "max": 0, "range": range(0, 1)}),
    ("1", {"line": "1", "min": 1, "max": 1, "range": range(1, 2)}),
    ("0-1", {"line": "0-1", "min": 0, "max": 1, "range": range(0, 2)}),
])
def test__line(line, expected):
    """Item.line"""
    # getter
    item = Item(line)
    helpers_.test_attrs(obj=item, exp_d=expected)
    # setter
    item.line = line
    helpers_.test_attrs(obj=item, exp_d=expected)
