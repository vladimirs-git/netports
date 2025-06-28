"""Tests ipv4.py."""

import pytest

from netports import ipv4 as ipv4_
from netports.ipv4 import IPv4


@pytest.fixture
def ipv4(addr: str) -> IPv4:
    """Create IPv4 objects."""
    return IPv4(addr=addr)


@pytest.mark.parametrize("addr, strict, expected", [
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
def test__init__formats(addr, strict, expected):
    """IPv4.__init__() cidr, network mask formats."""
    if isinstance(expected, str):
        actual = str(IPv4(addr=addr, strict=strict))

        assert actual == expected
    else:
        with pytest.raises(expected):
            IPv4(addr=addr, strict=strict)


@pytest.mark.parametrize("addr1, addr2, expected", [
    ("10.0.0.0/24", "10.0.0.0/24", True),  # same prefix
    ("10.0.0.1/24", "10.0.0.1/24", True),  # same address
    ("10.0.0.1/24", "10.0.0.0/24", False),  # different IPs, same prefix
    ("10.0.0.0/24", "10.0.0.0/25", False),  # different prefix
    ("10.0.0.1/24", "10.0.0.1/25", False),  # different prefix
    ("10.0.1.0/24", "10.0.0.0/24", False),  # different prefix
])
def test__eq__(addr1, addr2, expected):
    """Test IPv4.__eq__()."""
    actual = IPv4(addr1) == IPv4(addr2)

    assert actual is expected


@pytest.mark.parametrize("addr1, addr2, expected", [
    ("10.0.0.0/23", "10.0.0.0/24", True),  # network < network
    ("10.0.0.0/23", "10.0.0.1/24", True),  # network < host IP
    ("10.0.0.0/24", "10.0.0.1/24", True),  # network < host IP
    ("10.0.0.1/24", "10.0.0.2/24", True),  # IP .1 < IP .2
    ("10.0.0.2/24", "10.0.0.1/24", False),  # IP .2 !< IP .1
])
def test__lt__(addr1, addr2, expected):
    """Test IPv4.__lt__()."""
    actual = IPv4(addr1) < IPv4(addr2)
    assert actual is expected


@pytest.mark.parametrize("addrs, expected", [
    (["10.0.0.0/24", "10.0.0.0/23", "10.0.0.1/24", "10.0.0.1/23"],
     ["10.0.0.0/23", "10.0.0.0/24", "10.0.0.1/23", "10.0.0.1/24"]),
])
def test__lt__sorting(addrs, expected):
    """Test IPv4.__lt__() sorting."""
    results = sorted(addrs)

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


# ================================ is ================================

@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0/32", True),
    ("10.0.0.1/24", True),
    ("10.0.0.0/24", False),
])
def test__is_address(ipv4, addr, expected):
    """IPv4.is_address()."""
    actual = ipv4.is_address()
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0/32", False),
    ("10.0.0.1/24", False),
    ("10.0.0.0/24", True),
])
def test__is_prefix(ipv4, addr, expected):
    """IPv4.is_prefix()."""
    actual = ipv4.is_prefix()
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("0.0.0.0", False),
    ("1.0.0.0", True),  # public
    ("10.0.0.0", False),
    ("127.0.0.0", False),
    ("169.254.0.0", False),
    ("172.16.0.0", False),
    ("192.168.0.0", False),
    ("224.0.0.0", True),  # multicast
])
def test__is_global(ipv4, addr, expected):
    """IPv4.is_global()."""
    actual = ipv4.is_global()
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0", False),
    ("127.0.0.0", False),
    ("169.254.0.0", True),  # first
    ("169.254.255.255", True),  # last
    ("172.16.0.0", False),
    ("192.168.0.0", False),
    ("224.0.0.0", False),
])
def test__is_link_local(ipv4, addr, expected):
    """IPv4.is_link_local()."""
    actual = ipv4.is_link_local()
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0", False),
    ("127.0.0.0", True),  # first
    ("127.255.255.255", True),  # last
    ("224.0.0.0", False),
])
def test__is_loopback(ipv4, addr, expected):
    """IPv4.is_loopback()."""
    actual = ipv4.is_loopback()
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0", False),
    ("127.0.0.0", False),
    ("224.0.0.0", True),  # first
    ("239.255.255.255", True),  # last
])
def test__is_multicast(ipv4, addr, expected):
    """IPv4.is_multicast()."""
    actual = ipv4.is_multicast()
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("0.0.0.0", True),
    ("1.0.0.0", False),  # public
    ("10.0.0.0", True),
    ("127.0.0.0", True),
    ("172.16.0.0", True),
    ("192.168.0.0", True),
])
def test__is_private(ipv4, addr, expected):
    """IPv4.is_private()."""
    actual = ipv4.is_private()
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("240.0.0.0", True),
    ("192.168.0.0", False),
])
def test__is_reserved(ipv4, addr, expected):
    """IPv4.is_reserved()."""
    actual = ipv4.is_reserved()
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("0.0.0.0", True),
    ("0.0.0.1", False),
])
def test__is_unspecified(ipv4, addr, expected):
    """IPv4.is_unspecified()."""
    actual = ipv4.is_unspecified()
    assert actual == expected


# ============================= objects ==============================

@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/32", "0.0.0.0"),
    ("10.0.0.1/24", "0.0.0.255"),
])
def test__hostmask(ipv4, addr, expected):
    """IPv4.hostmask()."""
    hostmask = ipv4.hostmask()

    actual = hostmask.compressed
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/32", "255.255.255.255"),
    ("10.0.0.1/24", "255.255.255.0"),
])
def test__netmask(ipv4, addr, expected):
    """IPv4.netmask()."""
    netmask = ipv4.netmask()

    actual = netmask.compressed
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/32", "10.0.0.1/32"),
    ("10.0.0.1/24", "10.0.0.0/24"),
])
def test__network(ipv4, addr, expected):
    """IPv4.network()."""
    network = ipv4.network()

    actual = network.compressed
    assert actual == expected


# ============================== masks ===============================

@pytest.mark.parametrize("addr, splitter, expected", [
    ("10.0.0.1/32", " ", "10.0.0.1 255.255.255.255"),
    ("10.0.0.1/24", " ", "10.0.0.1 255.255.255.0"),
    ("10.0.0.0/32", "/", "10.0.0.0/255.255.255.255"),
])
def test__addr_mask(ipv4, addr, splitter, expected):
    """IPv4.addr_mask()."""
    actual = ipv4.addr_mask(splitter=splitter)
    assert actual == expected


@pytest.mark.parametrize("addr, splitter, expected", [
    ("10.0.0.1/32", " ", "10.0.0.1 0.0.0.0"),
    ("10.0.0.1/24", " ", "10.0.0.1 0.0.0.255"),
    ("10.0.0.0/32", "/", "10.0.0.0/0.0.0.0"),
])
def test__addr_wildcard(ipv4, addr, splitter, expected):
    """IPv4.addr_wildcard()."""
    actual = ipv4.addr_wildcard(splitter=splitter)
    assert actual == expected


@pytest.mark.parametrize("addr, splitter, expected", [
    ("10.0.0.1/32", " ", "10.0.0.1 255.255.255.255"),
    ("10.0.0.1/24", " ", "10.0.0.0 255.255.255.0"),
    ("10.0.0.0/32", "/", "10.0.0.0/255.255.255.255"),
])
def test__net_mask(ipv4, addr, splitter, expected):
    """IPv4.net_mask()."""
    actual = ipv4.net_mask(splitter=splitter)
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/32", "10.0.0.1"),
    ("10.0.0.1/24", "10.0.0.0"),
])
def test__net(ipv4, addr, expected):
    """IPv4.net_wildcard()."""
    actual = ipv4.net()
    assert actual == expected


@pytest.mark.parametrize("addr, splitter, expected", [
    ("10.0.0.1/32", " ", "10.0.0.1 0.0.0.0"),
    ("10.0.0.1/24", " ", "10.0.0.0 0.0.0.255"),
    ("10.0.0.0/32", "/", "10.0.0.0/0.0.0.0"),
])
def test__net_wildcard(ipv4, addr, splitter, expected):
    """IPv4.net_wildcard()."""
    actual = ipv4.net_wildcard(splitter=splitter)
    assert actual == expected


@pytest.mark.parametrize("args, kwargs, expected", [
    (["10.0.0.0"], {}, "10.0.0.0/32"),  # address
    (["10.0.0.0/24"], {}, "10.0.0.0/24"),  # prefix
    (["10.0.0.1/24"], {}, "10.0.0.1/24"),  # address with prefixlen
    (["10.0.0.0/255.255.255.0"], {}, "10.0.0.0/24"),  # net mask
    (["10.0.0.0 255.255.255.0"], {}, "10.0.0.0/24"),  # net mask
    (["10.0.0.1/255.255.255.0"], {}, "10.0.0.1/24"),  # address mask
    (["10.0.0.1/0.0.0.255"], {}, "10.0.0.1/24"),  # wildcard
    (["10.0.0.1/0.1.0.255"], {}, ValueError),  # complex wildcard
    ([], {}, ValueError),
    # addr
    ([], {"addr": "10.0.0.0"}, "10.0.0.0/32"),  # address
    ([], {"addr": "10.0.0.1/24"}, "10.0.0.1/24"),  # address with prefixlen
    # strict
    (["10.0.0.0"], {"strict": True}, "10.0.0.0/32"),  # address
    (["10.0.0.0/24"], {"strict": True}, "10.0.0.0/24"),  # prefix
    (["10.0.0.1/24"], {"strict": True}, ValueError),  # address with prefix
    (["10.0.0.0/255.255.255.0"], {"strict": True}, "10.0.0.0/24"),  # net mask
    (["10.0.0.0 255.255.255.0"], {"strict": True}, "10.0.0.0/24"),  # net mask
    (["10.0.0.1/255.255.255.0"], {"strict": True}, ValueError),  # address mask
    (["10.0.0.1/0.0.0.255"], {"strict": True}, ValueError),  # wildcard
    (["10.0.0.1/0.1.0.255"], {"strict": True}, ValueError),  # complex wildcard
    ([], {"strict": True}, ValueError),
    # addr strict
    ([], {"addr": "10.0.0.0", "strict": True}, "10.0.0.0/32"),  # address
    ([], {"addr": "10.0.0.1/24", "strict": True}, ValueError),  # address with prefixlen
])
def test__validate_addr(args, kwargs, expected):
    """ipv4._validate_addr()."""
    if isinstance(expected, str):
        actual = ipv4_._validate_addr(*args, **kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ipv4_._validate_addr(*args, **kwargs)
