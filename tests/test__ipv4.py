"""Tests ipv4.py."""

import pytest

from netports import ipv4 as ipv4_
from netports.ipv4 import IPv4
from netports.exceptions import NetportsValueError


@pytest.fixture
def ipv4(addr: str) -> IPv4:
    """Create IPv4 objects."""
    return IPv4(addr=addr)


@pytest.mark.parametrize("addr, strict, expected", [
    ("10.0.0.1", False, "10.0.0.1/32"),
    ("10.0.0.0/24", False, "10.0.0.0/24"),
    ("10.0.0.1/24", False, "10.0.0.1/24"),
    ("10.0.0.0 255.255.255.0", False, "10.0.0.0/24"),
    ("10.0.0.1 255.255.255.0", False, "10.0.0.1/24"),
    ("", False, ValueError),
    # strict
    ("10.0.0.1", True, "10.0.0.1/32"),
    ("10.0.0.0/24", True, "10.0.0.0/24"),
    ("10.0.0.1/24", True, ValueError),
    ("10.0.0.0 255.255.255.0", True, "10.0.0.0/24"),
    ("10.0.0.1 255.255.255.0", True, ValueError),
    ("", True, ValueError),
])
def test__init__(addr, strict, expected):
    """IPv4.__init__()."""
    if isinstance(expected, str):
        obj = IPv4(addr=addr, strict=strict)

        assert obj.addr == addr
        assert obj.ip_len == expected
    else:
        with pytest.raises(expected):
            IPv4(addr=addr, strict=strict)


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1", "IPv4('10.0.0.1')"),
    ("10.0.0.1/24", "IPv4('10.0.0.1/24')"),
])
def test__repr__(ipv4, addr, expected):
    """Test IPv4.__repr__()."""
    actual = repr(ipv4)
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1", "10.0.0.1"),
    ("10.0.0.1/24", "10.0.0.1/24"),
])
def test__str__(ipv4, addr, expected):
    """Test IPv4.__str__()."""
    actual = str(ipv4)
    assert actual == expected


@pytest.mark.parametrize("addr1, addr2, expected", [
    ("10.0.0.0/24", "10.0.0.0/24", True),  # same prefix
    ("10.0.0.1/24", "10.0.0.1/24", True),  # same address
    ("10.0.0.1", "10.0.0.1/32", True),  # same address
    ("10.0.0.1", "10.0.0.1/24", False),  # different address
    ("10.0.0.1/24", "10.0.0.0/24", False),  # different address, same prefix
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


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/24", "10.0.0.1"),
])
def test__ip(ipv4, addr, expected):
    """Test IPv4.ip()."""
    actual = ipv4.ip
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1", "10.0.0.1/32"),
    ("10.0.0.1/24", "10.0.0.1/24"),
])
def test__ip_len(ipv4, addr, expected):
    """Test IPv4.ip_len()."""
    actual = ipv4.ip_len
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/32", "10.0.0.1"),
    ("10.0.0.1/24", "10.0.0.0"),
])
def test__net(ipv4, addr, expected):
    """Test IPv4.net()."""
    actual = ipv4.net
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/24", 24),
])
def test__len(ipv4, addr, expected):
    """Test IPv4.len()."""
    actual = ipv4.len
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/24", "10.0.0.0/24"),
])
def test__prefix(ipv4, addr, expected):
    """Test IPv4.prefix()."""
    actual = ipv4.prefix
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    # host
    ("10.0.0.0", "host"),
    # cidr
    ("10.0.0.1/30", "cidr"),
    # mask
    ("10.0.0.0 255.255.255.0", "mask"),
    ("10.0.0.0 255.255.255.252", "mask"),
    ("10.0.0.0 255.255.255.254", "mask"),
    ("10.0.0.0 255.255.255.255", "mask"),
    # wildcard
    ("10.0.0.0 0.0.0.255", "wildcard"),
    ("10.0.0.0 0.0.0.3", "wildcard"),
    ("10.0.0.0 0.0.0.1", "wildcard"),
    ("10.0.0.0 0.0.0.0", "wildcard"),
])
def test__representations(ipv4, addr, expected):
    """IPv4.representations()."""
    actual = ipv4.representation
    assert actual == expected


# ================================ is ================================

@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0/32", True),
    ("10.0.0.1/24", True),
    ("10.0.0.0/24", False),
])
def test__is_address(ipv4, addr, expected):
    """IPv4.is_address()."""
    actual = ipv4.is_address
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0/32", False),
    ("10.0.0.1/24", False),
    ("10.0.0.0/24", True),
])
def test__is_prefix(ipv4, addr, expected):
    """IPv4.is_prefix()."""
    actual = ipv4.is_prefix
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
    actual = ipv4.is_global
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
    actual = ipv4.is_link_local
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0", False),
    ("127.0.0.0", True),  # first
    ("127.255.255.255", True),  # last
    ("224.0.0.0", False),
])
def test__is_loopback(ipv4, addr, expected):
    """IPv4.is_loopback()."""
    actual = ipv4.is_loopback
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.0", False),
    ("127.0.0.0", False),
    ("224.0.0.0", True),  # first
    ("239.255.255.255", True),  # last
])
def test__is_multicast(ipv4, addr, expected):
    """IPv4.is_multicast()."""
    actual = ipv4.is_multicast
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
    actual = ipv4.is_private
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("240.0.0.0", True),
    ("192.168.0.0", False),
])
def test__is_reserved(ipv4, addr, expected):
    """IPv4.is_reserved()."""
    actual = ipv4.is_reserved
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("0.0.0.0", True),
    ("0.0.0.1", False),
])
def test__is_unspecified(ipv4, addr, expected):
    """IPv4.is_unspecified()."""
    actual = ipv4.is_unspecified
    assert actual == expected


# ============================= objects ==============================

@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/32", "0.0.0.0"),
    ("10.0.0.1/24", "0.0.0.255"),
])
def test__hostmask(ipv4, addr, expected):
    """IPv4.hostmask()."""
    hostmask = ipv4.hostmask

    actual = hostmask.compressed
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/32", "255.255.255.255"),
    ("10.0.0.1/24", "255.255.255.0"),
])
def test__netmask(ipv4, addr, expected):
    """IPv4.netmask()."""
    netmask = ipv4.netmask

    actual = netmask.compressed
    assert actual == expected


@pytest.mark.parametrize("addr, expected", [
    ("10.0.0.1/32", "10.0.0.1/32"),
    ("10.0.0.1/24", "10.0.0.0/24"),
])
def test__network(ipv4, addr, expected):
    """IPv4.network()."""
    network = ipv4.network

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
    (["10.0.0.0"], {}, ("10.0.0.0", "10.0.0.0/32")),  # address
    (["10.0.0.0/24"], {}, ("10.0.0.0/24", "10.0.0.0/24")),  # prefix
    (["10.0.0.1/24"], {}, ("10.0.0.1/24", "10.0.0.1/24")),  # address with prefixlen
    (["10.0.0.0/255.255.255.0"], {}, ("10.0.0.0/255.255.255.0", "10.0.0.0/24")),  # net mask
    (["10.0.0.1/255.255.255.0"], {}, ("10.0.0.1/255.255.255.0", "10.0.0.1/24")),  # address mask
    (["10.0.0.1/0.0.0.255"], {}, ("10.0.0.1/0.0.0.255", "10.0.0.1/24")),  # wildcard
    (["10.0.0.1/0.1.0.255"], {}, ValueError),  # complex wildcard
    ([], {}, ValueError),  # empty
    # splitter
    (["10.0.0.0 255.255.255.0"], {}, ("10.0.0.0 255.255.255.0", "10.0.0.0/24")),  # splitter
    ([r"10.0.0.0\255.255.255.0"], {}, (r"10.0.0.0\255.255.255.0", "10.0.0.0/24")),  # splitter
    (["10.0.0.0.255.255.255.0"], {}, ValueError),  # splitter
    (["10.0.0.0  255.255.255.0"], {}, ValueError),  # splitter
    # kwargs
    ([], {"addr": "10.0.0.0"}, ("10.0.0.0", "10.0.0.0/32")),  # address
    ([], {"addr": "10.0.0.1/24"}, ("10.0.0.1/24", "10.0.0.1/24")),  # address with prefixlen
    # strict
    (["10.0.0.0"], {"strict": True}, ("10.0.0.0", "10.0.0.0/32")),  # address
    (["10.0.0.0/24"], {"strict": True}, ("10.0.0.0/24", "10.0.0.0/24")),  # prefix
    (["10.0.0.1/24"], {"strict": True}, ValueError),  # address with prefix
    (["10.0.0.0/255.255.255.0"], {"strict": True}, ("10.0.0.0/255.255.255.0", "10.0.0.0/24")),
    (["10.0.0.0 255.255.255.0"], {"strict": True}, ("10.0.0.0 255.255.255.0", "10.0.0.0/24")),
    (["10.0.0.1/255.255.255.0"], {"strict": True}, ValueError),  # address mask
    (["10.0.0.1/0.0.0.255"], {"strict": True}, ValueError),  # wildcard
    (["10.0.0.1/0.1.0.255"], {"strict": True}, ValueError),  # complex wildcard
    ([], {"strict": True}, ValueError),  # empty
    # kwargs strict
    ([], {"addr": "10.0.0.0", "strict": True}, ("10.0.0.0", "10.0.0.0/32")),  # address
    ([], {"addr": "10.0.0.1/24", "strict": True}, ValueError),  # address with prefixlen
])
def test__validate_addr(args, kwargs, expected):
    """ipv4._validate_addr()."""
    if isinstance(expected, tuple):
        actual = ipv4_._validate_addr(*args, **kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            ipv4_._validate_addr(*args, **kwargs)


# ============================== other ===============================

@pytest.mark.parametrize("addr, expected", [
    # host
    ("10.0.0.0", ["10.0.0.0"]),
    # cidr
    ("10.0.0.0/30", ['10.0.0.1/30', '10.0.0.2/30']),
    ("10.0.0.0/31", ['10.0.0.0/31', '10.0.0.1/31']),
    ("10.0.0.0/32", ["10.0.0.0/32"]),
    # mask network
    ("10.0.0.0 255.255.255.252", ['10.0.0.1 255.255.255.252', '10.0.0.2 255.255.255.252']),
    ("10.0.0.0 255.255.255.254", ['10.0.0.0 255.255.255.254', '10.0.0.1 255.255.255.254']),
    ("10.0.0.0 255.255.255.255", ['10.0.0.0 255.255.255.255']),
    # mask host
    ("10.0.0.1 255.255.255.252", ['10.0.0.1 255.255.255.252', '10.0.0.2 255.255.255.252']),
    ("10.0.0.1 255.255.255.254", ['10.0.0.0 255.255.255.254', '10.0.0.1 255.255.255.254']),
    ("10.0.0.1 255.255.255.255", ['10.0.0.1 255.255.255.255']),
    # wildcard network
    ("10.0.0.0 0.0.0.3", NetportsValueError),
    ("10.0.0.0 0.0.0.0", NetportsValueError),
    # wildcard host
    ("10.0.0.1 0.0.0.3", NetportsValueError),
    ("10.0.0.1 0.0.0.0", NetportsValueError),
])
def test__hosts(ipv4, addr, expected):
    """IPv4.hosts()."""
    if isinstance(expected, list):
        result = ipv4.hosts()

        actual = [o.addr for o in result]
        assert actual == expected
    else:
        with pytest.raises(expected):
            list(ipv4.hosts())
