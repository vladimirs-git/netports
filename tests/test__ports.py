"""Tests ports.py"""

import pytest

from netports import ports, NetportsValueError


@pytest.mark.parametrize("items, expected", [
    ("", []),
    (0, [0]),
    (b"1", [1]),
    ("0", [0]),
    ("1,1", [1]),
    ("1,2", [1, 2]),
    (" 1\t, 2\n", [1, 2]),
    ("1-1", [1]),
    ("1-2", [1, 2]),
    ("1-3", [1, 2, 3]),
    ("1,3-5", [1, 3, 4, 5]),
    ("1\t, \t3\t- 5\n", [1, 3, 4, 5]),
    ("3-5,1", [1, 3, 4, 5]),
    ("1,3-5,1,3-5", [1, 3, 4, 5]),

    ([], []),
    ([1], [1]),
    ([1, 1], [1]),
    (["1"], [1]),
    ({1: ""}, [1]),

    ([1, 2], [1, 2]),
    ({1, 2}, [1, 2]),
    ((1, 2), [1, 2]),
    ([2, 1], [1, 2]),
    ([5, 1, 3, 4, 5], [1, 3, 4, 5]),
    # error
    ("1-2-3", NetportsValueError),
    ("1-a", NetportsValueError),
    ("2-1", NetportsValueError),
])
def test__inumbers(items, expected):
    """ports.inumbers()"""
    if isinstance(expected, list):
        actual = ports.inumbers(items=items)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ports.inumbers(items=items)


@pytest.mark.parametrize("items, expected", [
    ("", ""),
    (0, "0"),
    (b"1", "1"),
    (0.9, "0"),
    (1.9, "1"),
    ([], ""),
    ([1], "1"),
    (["1"], "1"),
    ({1: ""}, "1"),

    ([1, 2], "1-2"),
    ({1, 2}, "1-2"),
    ((1, 2), "1-2"),
    ([2, 1], "1-2"),
    ([1, 3, 4, 5], "1,3-5"),
    ([5, 1, 4, 3], "1,3-5"),
    (["1", 2.9, b"3"], "1-3"),

    ("1,3-5", "1,3-5"),
    (" 1\t , 3\t - 5\n", "1,3-5"),
    ("1,3-5,1,3-5", "1,3-5"),
    # error
    ([[1]], NetportsValueError),
    (b"a", NetportsValueError),
    ([{}], NetportsValueError),
    ("1 3 to 5", NetportsValueError),  # HP style
])
def test__snumbers(items, expected):
    """ports.snumbers()"""
    if isinstance(expected, str):
        actual = ports.snumbers(items=items)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ports.snumbers(items=items)
