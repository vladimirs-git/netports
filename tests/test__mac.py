"""Tests mac.py"""

from typing import Any

import dictdiffer
import pytest

from netports import NetportsValueError
from netports.mac import Mac
from tests import params__mac as p


# ========================== redefined ===========================

@pytest.mark.parametrize("line, expected", [
    (p.ZERO, p.ZERO_D),
    (p.CISCO, p.CISCO_D),
    (p.COLON, p.COLON_D),
    (f"\t{p.ZERO}", NetportsValueError),
    (0, NetportsValueError),
])
def test__init__(line, expected: Any):
    """Mac.__init__()."""
    if isinstance(expected, dict):
        obj = Mac(line=line)

        actual = obj.model_dump()
        diff = list(dictdiffer.diff(actual, expected))
        assert not diff
    else:
        with pytest.raises(expected):
            Mac(line=line)


@pytest.mark.parametrize("line, expected", [
    (p.ZERO, p.ZERO_D),
])
def test__init__args(line, expected: Any):
    """Mac.__init__(*args)."""
    obj = Mac(line)

    actual = obj.model_dump()

    diff = list(dictdiffer.diff(actual, expected))
    assert not diff


@pytest.mark.parametrize("line, expected", [
    (p.ZERO, p.ZERO),
])
def test__str__(line, expected):
    """Mac.__str__()"""
    obj = Mac(line=line)
    actual = str(obj)
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    (p.ZERO, f"Mac('{p.ZERO}')"),
])
def test__repr__(line, expected):
    """Mac.__repr__()"""
    obj = Mac(line)
    actual = repr(obj)
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    (p.ZERO, 0),
    (p.FFFFFF, 281474976710655),
])
def test__hash__(line, expected):
    """Mac.__hash__()"""
    obj = Mac(line)
    actual = hash(obj)
    assert actual == expected


@pytest.mark.parametrize("line1, line2, expected", [
    (p.ABCDEF, p.ABCDEF, True),
    (p.ABCDEF, p.ZERO, False),
])
def test__eq__(line1, line2, expected):
    """Mac.__eq__()"""
    obj1 = Mac(line1)
    obj2 = Mac(line2)
    actual = bool(obj1 == obj2)
    assert actual == expected


@pytest.mark.parametrize("line1, line2, expected", [
    (p.ABCDEF, p.ABCDEF, True),
    (p.ZERO, p.ABCDEF, True),
    (p.FFFFFF, p.ABCDEF, False),

])
def test__le__(line1, line2, expected):
    """Mac.__le__()"""
    obj1 = Mac(line1)
    obj2 = Mac(line2)
    actual = bool(obj1 <= obj2)
    assert actual == expected


# ============================== parse ===============================


@pytest.mark.parametrize("line, expected", [
    (p.ZERO, p.ZERO),
    (p.CISCO, p.ZERO),
    (p.COLON, p.ZERO),
    (p.ABCDEF, p.ABCDEF),
    (p.ABCDEF.upper(), p.ABCDEF),
])
def test__parse_hex(line, expected: Any):
    """Mac._parse_hex()."""
    obj = Mac(line=p.ZERO)
    obj.line = line

    if isinstance(expected, str):
        obj._parse_hex()

        actual = obj.hex
        assert actual == expected
    else:
        with pytest.raises(expected):
            obj._parse_hex()


@pytest.mark.parametrize("hex_, expected", [
    (p.ZERO, "0000.0000.0000"),
    (p.ABCDEF, "abcd.ef12.3456"),
    (p.FFFFFF, "ffff.ffff.ffff"),
])
def test__parse_cisco(hex_, expected: Any):
    """Mac._parse_cisco()."""
    obj = Mac(line=p.ZERO)
    obj.hex = hex_

    obj._parse_cisco()

    actual = obj.cisco
    assert actual == expected


@pytest.mark.parametrize("hex_, expected", [
    (p.ZERO, "00:00:00:00:00:00"),
    (p.ABCDEF, "ab:cd:ef:12:34:56"),
    (p.FFFFFF, "ff:ff:ff:ff:ff:ff"),
])
def test__parse_colon(hex_, expected):
    """Mac._parse_colon()."""
    obj = Mac(line=p.ZERO)
    obj.hex = hex_

    obj._parse_colon()

    actual = obj.colon
    assert actual == expected


@pytest.mark.parametrize("hex_, expected", [
    (p.ZERO, 0),
    (p.FFFFFF, 281474976710655),
])
def test__parse_integer(hex_, expected):
    """Mac._parse_integer()."""
    obj = Mac(line=p.ZERO)
    obj.hex = hex_

    obj._parse_integer()

    actual = obj.integer
    assert actual == expected
