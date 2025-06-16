"""Tests ipv4.py."""
from ipaddress import IPv4Network, IPv4Address

import pytest

from netports.ipv4 import IPv4


def test__init__():
    """IPv4.__init__()."""
    # cidr format
    ipv4 = IPv4("10.0.0.1/24")
    assert ipv4.addr == "10.0.0.1/24"
    assert ipv4.ip == "10.0.0.1"
    assert ipv4.net == "10.0.0.0/24"
    assert ipv4.net_ == "10.0.0.0"
    assert ipv4.prefixlen == 24

    assert ipv4.is_global is False
    assert ipv4.is_link_local is False
    assert ipv4.is_loopback is False
    assert ipv4.is_multicast is False
    assert ipv4.is_private is True
    assert ipv4.is_reserved is False
    assert ipv4.is_unspecified is False

    assert ipv4.hostmask == IPv4Address("0.0.0.255")
    assert ipv4.hostmask == IPv4Address("0.0.0.255")
    assert ipv4.netmask == IPv4Address("255.255.255.0")
    assert ipv4.network == IPv4Network("10.0.0.0/24")

    assert ipv4.addr_wildcard == "10.0.0.1 0.0.0.255"
    assert ipv4.addr_mask == "10.0.0.1 255.255.255.0"
    assert ipv4.net_wildcard == "10.0.0.0 0.0.0.255"
    assert ipv4.net_mask == "10.0.0.0 255.255.255.0"

    ipv4 = IPv4("10.0.0.1/32")
    assert ipv4.ip == "10.0.0.1"
    assert ipv4.addr == "10.0.0.1/32"
    assert ipv4.net == "10.0.0.1/32"
    assert ipv4.prefixlen == 32
    assert ipv4.is_private is True


@pytest.mark.parametrize("cidr, strict, expected", [
    ("10.0.0.0/24", False, "10.0.0.0/24"),
    ("10.0.0.1/24", False, "10.0.0.1/24"),
    ("10.0.0.0 255.255.255.0", False, "10.0.0.0/24"),
    ("10.0.0.1 255.255.255.0", False, "10.0.0.1/24"),
    # strict
    ("10.0.0.0/24", True, "10.0.0.0/24"),
    ("10.0.0.1/24", True, ValueError),
    ("10.0.0.0 255.255.255.0", True, "10.0.0.0/24"),
    ("10.0.0.1 255.255.255.0", True, ValueError),
])
def test__init__formats(cidr, strict, expected):
    """IPv4.__init__() cidr, network mask formats."""
    if isinstance(expected, str):
        actual = str(IPv4(cidr=cidr, strict=strict))

        assert actual == expected
    else:
        with pytest.raises(expected):
            IPv4(cidr=cidr, strict=strict)


@pytest.mark.parametrize("cidr1, cidr2, expected", [
    ("10.0.0.0/24", "10.0.0.0/24", True),  # same prefix
    ("10.0.0.1/24", "10.0.0.1/24", True),  # same address
    ("10.0.0.1/24", "10.0.0.0/24", False),  # different IPs, same prefix
    ("10.0.0.0/24", "10.0.0.0/25", False),  # different prefix
    ("10.0.0.1/24", "10.0.0.1/25", False),  # different prefix
    ("10.0.1.0/24", "10.0.0.0/24", False),  # different prefix
])
def test__eq__(cidr1, cidr2, expected):
    """Test IPv4.__eq__()."""
    actual = IPv4(cidr1) == IPv4(cidr2)
    assert actual is expected


@pytest.mark.parametrize("cidr1, cidr2, expected", [
    ("10.0.0.0/23", "10.0.0.0/24", True),  # network < network
    ("10.0.0.0/23", "10.0.0.1/24", True),  # network < host IP
    ("10.0.0.0/24", "10.0.0.1/24", True),  # network < host IP
    ("10.0.0.1/24", "10.0.0.2/24", True),  # IP .1 < IP .2
    ("10.0.0.2/24", "10.0.0.1/24", False),  # IP .2 !< IP .1
])
def test__lt__(cidr1, cidr2, expected):
    """Test IPv4.__lt__()."""
    actual = IPv4(cidr1) < IPv4(cidr2)
    assert actual is expected


@pytest.mark.parametrize("cidr1, expected", [
    (["10.0.0.0/24", "10.0.0.0/23", "10.0.0.1/24", "10.0.0.1/23"],
     ["10.0.0.0/23", "10.0.0.0/24", "10.0.0.1/23", "10.0.0.1/24"]),
])
def test__lt__sorting(cidr1, expected):
    """Test IPv4.__lt__() sorting."""
    results = sorted(cidr1)

    actual = [str(o) for o in results]
    assert actual == expected


@pytest.mark.parametrize("subnet, supernet, expected", [
    ("10.0.0.0/24", "10.0.0.0/23", True),
    ("10.0.0.1/24", "10.0.0.0/23", True),
    ("10.0.0.0/24", "10.0.0.0/24", True),
    ("10.0.0.1/24", "10.0.0.0/24", True),
    ("10.0.0.0/24", "10.0.0.0/25", False),
    ("10.0.0.1/24", "10.0.0.0/25", False),
    ("10.0.0.0/32", "10.0.0.0/32", True),
    ("10.0.0.1/32", "10.0.0.0/32", False),

])
def test__contains__(subnet, supernet, expected):
    """IPv4.__contains__()."""
    actual = IPv4(subnet) in IPv4(supernet)
    assert actual == expected
