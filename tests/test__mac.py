"""Tests mac.py"""

import dictdiffer  # type: ignore[import-untyped]
import pytest

from netports import NetportsValueError
from netports import mac as mac_
from netports.mac import Mac


@pytest.fixture
def mac(addr: str) -> Mac:
    """Create IPv4 objects."""
    return Mac(addr=addr)


@pytest.mark.parametrize("addr, expected", [
    ("000000-000000", "000000000000"),
    ("FF:FF:FF:FF:FF:FF", "FFFFFFFFFFFF"),
    ("", NetportsValueError),
])
def test__init__(addr, expected):
    """Mac.__init__()."""
    if isinstance(expected, str):
        obj = Mac(addr)

        assert obj.addr == addr
        assert obj.hex == expected
    else:
        with pytest.raises(expected):
            Mac(addr=addr)


@pytest.mark.parametrize("addr, expected", [
    ("0000.0000.0000", "Mac('0000.0000.0000')"),
])
def test__repr__(mac, addr, expected):
    """Mac.__repr__()"""
    actual = repr(mac)
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("0000.0000.0000", "0000.0000.0000"),
])
def test__str__(mac, addr, expected):
    """Mac.__str__()"""
    actual = str(mac)
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("0000.0000.0000", 0),
    ("FFFF.FFFF.FFFF", 281474976710655),
])
def test__hash__(mac, addr, expected):
    """Mac.__hash__()"""
    actual = hash(mac)
    assert actual == expected


@pytest.mark.parametrize("addr1, addr2, expected", [
    ("abcd.ef12.3456", "abcdef123456", True),
    ("000000000000", "000000000001", False),
])
def test__eq__(addr1, addr2, expected):
    """Mac.__eq__()"""
    actual = Mac(addr1) == Mac(addr2)
    assert actual == expected


@pytest.mark.parametrize("addr1, addr2, expected", [
    ("abcd.ef12.3456", "abcdef123456", False),
    ("000000000000", "abcdef123456", True),
    ("ffffffffffff", "abcdef123456", False),

])
def test__le__(addr1, addr2, expected):
    """Mac.__le__()"""
    actual = Mac(addr1) < Mac(addr2)
    assert actual == expected


# ============================= methods ==============================

@pytest.mark.parametrize("addr, size, splitter, expected", [
    ("000000000000", 2, ":", "00:00:00:00:00:00"),
    ("000000000000", 4, ".", "0000.0000.0000"),
    ("000000000000", 6, "-", "000000-000000"),
    ("000000000000", 1, ":", NetportsValueError),
])
def test__format(mac, addr, size, splitter, expected):
    """Mac.format()."""
    if isinstance(expected, str):
        actual = mac.format(size=size, splitter=splitter)
        assert actual == expected
    else:
        with pytest.raises(expected):
            mac.format(size=size, splitter=splitter)


@pytest.mark.parametrize("addr, expected", [
    ("000000000000", "00-00-00-00-00-00"),
])
def test__windows(mac, addr, expected):
    """Mac.windows()."""
    actual = mac.windows
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("000000000000", "0000.0000.0000"),
])
def test__cisco(mac, addr, expected):
    """Mac.cisco()."""
    actual = mac.cisco
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("000000000000", "0000-0000-0000"),
])
def test__hp_comware(mac, addr, expected):
    """Mac.hp_comware()."""
    actual = mac.hp_comware
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("000000000000", "000000-000000"),
])
def test__hp_procurve(mac, addr, expected):
    """Mac.hp_procurve()."""
    actual = mac.hp_procurve
    assert actual == expected


# ============================== parse ===============================


@pytest.mark.parametrize("args, kwargs, expected", [
    # args
    (["Abcdef123456"], {}, ("Abcdef123456", "Abcdef123456")),
    (["000000000000"], {}, ("000000000000", "000000000000")),
    (["000000.000000"], {}, ("000000.000000", "000000000000")),
    (["000000:000000"], {}, ("000000:000000", "000000000000")),
    (["000000-000000"], {}, ("000000-000000", "000000000000")),
    (["0000.0000.0000"], {}, ("0000.0000.0000", "000000000000")),
    (["0000:0000:0000"], {}, ("0000:0000:0000", "000000000000")),
    (["0000-0000-0000"], {}, ("0000-0000-0000", "000000000000")),
    (["00.00.00.00.00.00"], {}, ("00.00.00.00.00.00", "000000000000")),
    (["00:00:00:00:00:00"], {}, ("00:00:00:00:00:00", "000000000000")),
    (["00-00-00-00-00-00"], {}, ("00-00-00-00-00-00", "000000000000")),
    # kwargs
    ([], {"addr": "0000.0000.0000"}, ("0000.0000.0000", "000000000000")),
    # error
    ([], {}, NetportsValueError),  # empty
    (["000000_000000"], {}, NetportsValueError),  # splitter
    (["000000.000000A"], {}, NetportsValueError),  # len
])
def test__validate_addr(args, kwargs, expected):
    """mac._validate_addr()."""
    if isinstance(expected, tuple):
        actual = mac_._validate_addr(*args, **kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            mac_._validate_addr(*args, **kwargs)
