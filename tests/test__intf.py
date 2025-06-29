"""Tests intf.py"""

import difflib

import pytest

from netports import intf as netport_intf, NetportsValueError
from netports.intf import Intf
from netports.types_ import DAny
from tests import params__intf as p


@pytest.fixture
def intf(line: str) -> Intf:
    """Create Intf objects."""
    return Intf(line=line)


@pytest.fixture
def intf_(line: str, kwargs: DAny) -> Intf:
    """Create Intf objects with kwargs."""
    return Intf(line=line, **kwargs)


@pytest.mark.parametrize("line, kwargs, exp_line, exp_id1, exp_id2", [
    ("Eth1/2", {}, "Eth1/2", 1, 2),
    ("Eth1/2", {"device_type": "cisco_ios"}, "Eth1/2", 1, 2),
    ("Eth1-2", {"splitter": "-"}, "Eth1-2", 1, 2),
])
def test__init__(intf_, line, kwargs, exp_line, exp_id1, exp_id2):
    """Intf.__repr__()"""
    assert intf_.line == exp_line
    assert intf_.id1 == exp_id1
    assert intf_.id2 == exp_id2


@pytest.mark.parametrize("line, expected", [
    ("Eth1/2", "Intf('Eth1/2')"),
])
def test__repr__(intf, line, expected):
    """Intf.__repr__()"""
    actual = repr(intf)
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("Eth1/2", "Eth1/2"),
    (" Eth1/2 ", " Eth1/2 "),
    (" interface Eth1/2 ", " interface Eth1/2 "),
    ("", ""),
    (" ", " "),
])
def test__str__(intf, line, expected):
    """Intf.__str__()"""
    actual = str(intf)
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", hash(("", 0, 0, 0, 0, 0, 0))),
    ("Eth1/2/3/4/5.6.7", hash(("Eth", 1, 2, 3, 4, 5, 6))),
])
def test__hash__(intf, line, expected):
    """Intf.__hash__()"""
    actual = hash(intf)
    assert actual == expected


@pytest.mark.parametrize("line1, line2, expected", [
    ("Eth1/2/3.4", "Eth1/2/3.4", True),
    ("Eth1/2/3.4", "Eth1/2/3.5", False),
    ("Eth1/2/3.4", "interface Eth1/2/3.4", False),
    ("Eth1/2/3.4", "Eth1.2.3.4", True),
])
def test__eq__(line1, line2, expected):
    """Intf.__eq__()"""
    actual = Intf(line1) == Intf(line2)
    assert actual == expected


@pytest.mark.parametrize("line1, line2, expected", [
    # name
    ("Eth1/2/3.4", "XXX0/2/3.4", True),
    # id0
    ("Eth0/2/3.4", "Eth1/2/3.4", True),
    ("Eth1/2/3.4", "Eth1/2/3.4", False),
    ("Eth2/2/3.4", "Eth1/2/3.4", False),
    # id1
    ("Eth1/1/3.4", "Eth1/2/3.4", True),
    ("Eth1/2/3.4", "Eth1/2/3.4", False),
    ("Eth1/3/3.4", "Eth1/2/3.4", False),
    # id2
    ("Eth1/2/2.4", "Eth1/2/3.4", True),
    ("Eth1/2/3.4", "Eth1/2/3.4", False),
    ("Eth1/2/3.4", "Eth1/2/3.4", False),
    # id3
    ("Eth1/2/3.3", "Eth1/2/3.4", True),
    ("Eth1/2/3.4", "Eth1/2/3.4", False),
    ("Eth1/2/3.5", "Eth1/2/3.4", False),
    # id4
    ("Eth1/2/3/4.4", "Eth1/2/3/4.5", True),
    ("Eth1/2/3/4.5", "Eth1/2/3/4.5", False),
    ("Eth1/2/3/4.6", "Eth1/2/3/4.5", False),
    # id5
    ("Eth1/2/3/4/5.5", "Eth1/2/3/4/5.6", True),
    ("Eth1/2/3/4/5.6", "Eth1/2/3/4/5.6", False),
    ("Eth1/2/3/4/5.7", "Eth1/2/3/4/5.6", False),
    # id6
    ("Eth1/2/3/4/5/6.6", "Eth1/2/3/4/5/6.7", False),
    ("Eth1/2/3/4/5/6.7", "Eth1/2/3/4/5/6.7", False),
    ("Eth1/2/3/4/5/6.8", "Eth1/2/3/4/5/6.7", False),

])
def test__lt__(line1, line2, expected):
    """Intf.__lt__()"""
    actual = Intf(line1) < Intf(line2)
    assert actual == expected


# =========================== property ===========================

@pytest.mark.parametrize("line, expected", [
    ("", ("", "", "", "", "")),
    ("interface Eth1/2/3.4", ("/", "/", ".", "", "")),
    ("interface Eth1/2/3/4/5.6", ("/", "/", "/", "/", ".")),
    ("interface Eth1,2.3/4:5/6/7", (",", ".", "/", ":", "/")),
])
def test__delimiters(intf, line, expected):
    """Intf.delimiters"""
    actual = intf.delimiters
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", ""),
    ("Eth", "Eth"),
    ("Eth1", "Eth"),
    ("Eth1/2", "Eth"),
    ("interface", "interface"),
    ("interface ", "interface "),
    ("interface Eth", "interface Eth"),
    ("interface Eth1", "interface Eth"),
    ("interface Eth1/2", "interface Eth"),
    ("interface Eth1/2/3", "interface Eth"),
    ("interface Eth1/2/3/4", "interface Eth"),
    ("interface Eth1/2/3/4/5", "interface Eth"),
    ("interface Eth1/2/3/4/5.6", "interface Eth"),
    ("interface Eth1/2/3/4/5/6.7", "interface Eth"),
])
def test__id0(intf, line, expected):
    """Intf.id0"""
    actual = intf.id0
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", 0),
    ("Eth", 0),
    ("Eth1", 1),
    ("Eth1/2", 1),
    ("interface", 0),
    ("interface ", 0),
    ("interface Eth", 0),
    ("interface Eth1", 1),
    ("interface Eth1/2", 1),
    ("interface Eth1/2/3", 1),
    ("interface Eth1/2/3/4", 1),
    ("interface Eth1/2/3/4/5", 1),
    ("interface Eth1/2/3/4/5.6", 1),
    ("interface Eth1/2/3/4/5/6.7", 1),
])
def test__id1(intf, line, expected):
    """Intf.id1"""
    actual = intf.id1
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", 0),
    ("Eth", 0),
    ("Eth1", 0),
    ("Eth1/2", 2),
    ("interface", 0),
    ("interface ", 0),
    ("interface Eth", 0),
    ("interface Eth1", 0),
    ("interface Eth1/2", 2),
    ("interface Eth1/2/3", 2),
    ("interface Eth1/2/3/4", 2),
    ("interface Eth1/2/3/4/5", 2),
    ("interface Eth1/2/3/4/5.6", 2),
    ("interface Eth1/2/3/4/5/6.7", 2),
])
def test__id2(intf, line, expected):
    """Intf.id2"""
    actual = intf.id2
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", 0),
    ("Eth", 0),
    ("Eth1", 0),
    ("Eth1/2", 0),
    ("interface", 0),
    ("interface ", 0),
    ("interface Eth", 0),
    ("interface Eth1", 0),
    ("interface Eth1/2", 0),
    ("interface Eth1/2/3", 3),
    ("interface Eth1/2/3/4", 3),
    ("interface Eth1/2/3/4/5", 3),
    ("interface Eth1/2/3/4/5.6", 3),
    ("interface Eth1/2/3/4/5/6.7", 3),
])
def test__id3(intf, line, expected):
    """Intf.id3"""
    actual = intf.id3
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", 0),
    ("Eth", 0),
    ("Eth1", 0),
    ("Eth1/2", 0),
    ("interface", 0),
    ("interface ", 0),
    ("interface Eth", 0),
    ("interface Eth1", 0),
    ("interface Eth1/2", 0),
    ("interface Eth1/2/3", 0),
    ("interface Eth1/2/3/4", 4),
    ("interface Eth1/2/3/4/5", 4),
    ("interface Eth1/2/3/4/5.6", 4),
    ("interface Eth1/2/3/4/5/6.7", 4),
])
def test__id4(intf, line, expected):
    """Intf.id4"""
    actual = intf.id4
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", 0),
    ("Eth", 0),
    ("Eth1", 0),
    ("Eth1/2", 0),
    ("interface", 0),
    ("interface ", 0),
    ("interface Eth", 0),
    ("interface Eth1", 0),
    ("interface Eth1/2", 0),
    ("interface Eth1/2/3", 0),
    ("interface Eth1/2/3/4", 0),
    ("interface Eth1/2/3/4/5", 5),
    ("interface Eth1/2/3/4/5.6", 5),
    ("interface Eth1/2/3/4/5/6.7", 5),
])
def test__id5(intf, line, expected):
    """Intf.id5"""
    actual = intf.id5
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", 0),
    ("Eth", 0),
    ("Eth1", 0),
    ("Eth1/2", 0),
    ("interface", 0),
    ("interface ", 0),
    ("interface Eth", 0),
    ("interface Eth1", 0),
    ("interface Eth1/2", 0),
    ("interface Eth1/2/3", 0),
    ("interface Eth1/2/3/4", 0),
    ("interface Eth1/2/3/4/5", 0),
    ("interface Eth1/2/3/4/5.6", 6),
    ("interface Eth1/2/3/4/5/6.7", 6),
])
def test__id6(intf, line, expected):
    """Intf.id6"""
    actual = intf.id6
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", ""),
    ("Eth", "Eth"),
    ("Eth1", "Eth1"),
    ("Eth1/2", "Eth1/2"),
    ("interface", "interface"),
    ("interface ", "interface "),
    ("interface Eth", "interface Eth"),
    ("interface Eth1", "interface Eth1"),
    ("interface Eth1/2", "interface Eth1/2"),
    ("interface Eth1/2/3", "interface Eth1/2/3"),
    ("interface Eth1/2/3/4", "interface Eth1/2/3/4"),
    ("interface Eth1/2/3/4/5", "interface Eth1/2/3/4/5"),
    ("interface Eth1/2/3/4/5.6", "interface Eth1/2/3/4/5.6"),
    ("interface Eth1/2/3/4/5/6.7", "interface Eth1/2/3/4/5/6"),
    ("interface lag 1", "interface lag 1"),
])
def test__line(intf, line, expected):
    """Intf.line"""
    actual = intf.line
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", ""),
    ("Eth", "Eth"),
    ("Eth1", "Eth1"),
    ("Eth1/2", "Eth1/2"),
    ("interface", ""),
    ("interface ", ""),
    ("interface Eth", "Eth"),
    ("interface Eth1", "Eth1"),
    ("interface Eth1/2", "Eth1/2"),
    ("interface Eth1/2/3", "Eth1/2/3"),
    ("interface Eth1/2/3/4", "Eth1/2/3/4"),
    ("interface Eth1/2/3/4/5", "Eth1/2/3/4/5"),
    ("interface Eth1/2/3/4/5.6", "Eth1/2/3/4/5.6"),
    ("interface Eth1/2/3/4/5/6.7", "Eth1/2/3/4/5/6"),
    ("interface lag 1", "lag 1"),
])
def test__name(intf, line, expected):
    """Intf.name"""
    actual = intf.name
    assert actual == expected


@pytest.mark.parametrize("line, kwargs, expected", [
    ("Eth", {}, ""),
    ("Eth", {"device_type": "cisco_ios"}, "cisco_ios"),
])
def test__device_type(intf_, line, kwargs, expected):
    """Intf.device_type"""
    actual = intf_.device_type
    assert actual == expected


@pytest.mark.parametrize("line, kwargs, expected, id0, id1, id2", [
    ("Eth1-2", {}, ",./:", "Eth", 1, 0),
    ("Eth1-2", {"splitter": "-"}, "-", "Eth", 1, 2),
])
def test__splitter(intf_, line, kwargs, expected, id0, id1, id2):
    """Intf.splitter"""
    actual = intf_.splitter
    assert actual == expected
    assert intf_.id0 == id0
    assert intf_.id1 == id1
    assert intf_.id2 == id2


# =========================== methods ============================


@pytest.mark.parametrize("line, expected", [
    # upper
    ("interface Ethernet1/2", p.ALL_NAMES_ETH),
    ("Ethernet1/2", p.ALL_NAMES_ETH),
    ("Eth1/2", p.ALL_NAMES_ETH),
    ("interface tunnel-ip1", p.ALL_NAMES_TUN_IP),
    ("tunnel-ip1", p.ALL_NAMES_TUN_IP),
    ("interface Tunnel1", p.ALL_NAMES_TUN),
    ("Tunnel1", p.ALL_NAMES_TUN),
    ("Tu1", p.ALL_NAMES_TUN),
    ("interface mgmt0", p.ALL_NAMES_MGMT),
    ("mgmt0", p.ALL_NAMES_MGMT),
    # lower
    ("interface ethernet1/2", p.ALL_NAMES_ETH),
    ("ethernet1/2", p.ALL_NAMES_ETH),
    ("eth1/2", p.ALL_NAMES_ETH),
    ("interface tunnel-ip1", p.ALL_NAMES_TUN_IP),
    ("tunnel-ip1", p.ALL_NAMES_TUN_IP),
    ("interface tunnel1", p.ALL_NAMES_TUN),
    ("tunnel1", p.ALL_NAMES_TUN),
    ("tu1", p.ALL_NAMES_TUN),
    ("interface mgmt0", p.ALL_NAMES_MGMT),
    ("mgmt0", p.ALL_NAMES_MGMT),
    # only lower
    ("interface 1", ["interface 1", "1"]),  # hpc
    ("lag 1", ["interface lag 1", "lag 1"]),  # aruba_os
    ("1", ["interface 1", "1"]),
])
def test__all_names(intf, line, expected):
    """Intf.all_names()"""
    actual = intf.all_names()

    diff = list(difflib.unified_diff(actual, expected))
    diff = [s for s in diff if s.startswith("-") or s.startswith("+")]
    assert not diff


@pytest.mark.parametrize("line, expected", [
    ("", 0),
    ("Eth", 0),
    ("Eth1", 1),
    ("Eth1/2", 2),
    ("interface", 0),
    ("interface ", 0),
    ("interface Eth", 0),
    ("interface Eth1", 1),
    ("interface Eth1/2", 2),
    ("interface Eth1/2/3", 3),
    ("interface Eth1/2/3/4", 4),
    ("interface Eth1/2/3/4/5", 5),
    ("interface Eth1/2/3/4/5.6", 6),
    ("interface Eth1/2/3/4/5/6.7", 6),
    # hp_procurve
    ("interface 1", 1),
    ("1", 1),
    # aruba_os
    ("interface lag 1", 1),
    ("lag 1", 1),
])
def test__last_idx(intf, line, expected):
    """Intf.last_idx()"""
    actual = intf.last_idx()
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", ""),
    ("Eth", "Eth"),
    ("Eth1", "Eth"),
    ("Eth1/2/3/4/5/6.7", "Eth"),
    ("Ethernet", "Ethernet"),
    ("Ethernet1", "Ethernet"),
    ("Ethernet1/2/3/4/5/6.7", "Ethernet"),
    ("interface", ""),
    ("interface ", ""),
    ("interface Eth", "Eth"),
    ("interface  Eth", "Eth"),
    ("interface Eth1", "Eth"),
    ("interface Eth1/2/3/4/5/6.7", "Eth"),
    ("interface Ethernet", "Ethernet"),
    ("interface Ethernet1", "Ethernet"),
    ("interface Ethernet1/2/3/4/5/6.7", "Ethernet"),
    # hp_procurve
    ("interface 1", ""),
    ("1", ""),
    # aruba_os
    ("interface lag 1", "lag"),
    ("lag 1", "lag"),
])
def test__name_base(intf, line, expected):
    """Intf.name_base()"""
    actual = intf.name_base()
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", "interface"),
    ("Eth", "interface Ethernet"),
    ("Eth1", "interface Ethernet1"),
    ("Eth1/2/3/4/5/6.7", "interface Ethernet1/2/3/4/5/6"),
    ("Ethernet", "interface Ethernet"),
    ("Ethernet1", "interface Ethernet1"),
    ("Ethernet1/2/3/4/5/6.7", "interface Ethernet1/2/3/4/5/6"),
    ("interface", "interface"),
    ("interface ", "interface"),
    ("interface Eth", "interface Ethernet"),
    ("interface  Eth", "interface Ethernet"),
    ("interface Eth1", "interface Ethernet1"),
    ("interface Eth1/2/3/4/5/6.7", "interface Ethernet1/2/3/4/5/6"),
    ("interface Ethernet", "interface Ethernet"),
    ("interface Ethernet1", "interface Ethernet1"),
    ("interface Ethernet1/2/3/4/5/6.7", "interface Ethernet1/2/3/4/5/6"),
    # hp_procurve
    ("interface 1", "interface 1"),
    ("1", "interface 1"),
    # aruba_os
    ("interface lag 1", "interface lag 1"),
    ("lag 1", "interface lag 1"),
    ("interface lag  1", "interface lag  1"),
    ("lag  1", "interface lag  1"),
])
def test__name_full(intf, line, expected):
    """Intf.name_full()"""
    actual = intf.name_full()
    assert actual == expected


@pytest.mark.parametrize("line, kwargs, expected", [
    # cisco_xr
    ("interface tunnel-ip1", {"device_type": "cisco_xr"}, "interface tunnel-ip1"),
    ("tunnel-ip1", {"device_type": "cisco_xr"}, "interface tunnel-ip1"),
    ("Tu1", {"device_type": "cisco_xr"}, "interface tunnel-ip1"),
    ("tu1", {"device_type": "cisco_xr"}, "interface tunnel-ip1"),
    ("ti1", {"device_type": "cisco_xr"}, "interface tunnel-ip1"),
])
def test__name_full__cisco_xr(intf_, line, kwargs, expected):
    """Intf.name_full(device_type="cisco_xr")"""
    actual = intf_.name_full()
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", ""),
    ("Eth", "Ethernet"),
    ("Eth1", "Ethernet1"),
    ("Eth1/2/3/4/5/6.7", "Ethernet1/2/3/4/5/6"),
    ("Ethernet", "Ethernet"),
    ("Ethernet1", "Ethernet1"),
    ("Ethernet1/2/3/4/5/6.7", "Ethernet1/2/3/4/5/6"),
    ("interface", ""),
    ("interface ", ""),
    ("interface Eth", "Ethernet"),
    ("interface  Eth", "Ethernet"),
    ("interface Eth1", "Ethernet1"),
    ("interface Eth1/2/3/4/5/6.7", "Ethernet1/2/3/4/5/6"),
    ("interface Ethernet", "Ethernet"),
    ("interface Ethernet1", "Ethernet1"),
    ("interface Ethernet1/2/3/4/5/6.7", "Ethernet1/2/3/4/5/6"),
    # hp_procurve
    ("interface 1", "1"),
    ("1", "1"),
    # aruba_os
    ("interface lag 1", "lag 1"),
    ("lag 1", "lag 1"),
    ("interface lag  1", "lag  1"),
    ("lag  1", "lag  1"),
])
def test__name_long(intf, line, expected):
    """Intf.name_long()"""
    actual = intf.name_long()
    assert actual == expected


@pytest.mark.parametrize("line, kwargs, expected", [
    # cisco_xr
    ("interface tunnel-ip1", {"device_type": "cisco_xr"}, "tunnel-ip1"),
    ("tunnel-ip1", {"device_type": "cisco_xr"}, "tunnel-ip1"),
    ("Tu1", {"device_type": "cisco_xr"}, "tunnel-ip1"),
    ("tu1", {"device_type": "cisco_xr"}, "tunnel-ip1"),
    ("ti1", {"device_type": "cisco_xr"}, "tunnel-ip1"),
])
def test__name_long__cisco_xr(intf_, line, kwargs, expected):
    """Intf.name_long(device_type="cisco_xr")"""
    actual = intf_.name_long()
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", ""),
    ("Eth", "Eth"),
    ("Eth1", "Eth1"),
    ("Eth1/2/3/4/5/6.7", "Eth1/2/3/4/5/6"),
    ("Ethernet", "Eth"),
    ("Ethernet1", "Eth1"),
    ("Ethernet1/2/3/4/5/6.7", "Eth1/2/3/4/5/6"),
    ("interface", ""),
    ("interface ", ""),
    ("interface Eth", "Eth"),
    ("interface  Eth", "Eth"),
    ("interface Eth1", "Eth1"),
    ("interface Eth1/2/3/4/5/6.7", "Eth1/2/3/4/5/6"),
    ("interface Ethernet", "Eth"),
    ("interface Ethernet1", "Eth1"),
    ("interface Ethernet1/2/3/4/5/6.7", "Eth1/2/3/4/5/6"),
    # hp_procurve
    ("interface 1", "1"),
    ("1", "1"),
    # aruba_os
    ("interface lag 1", "lag 1"),
    ("lag 1", "lag 1"),
    ("interface lag  1", "lag  1"),
    ("lag  1", "lag  1"),
])
def test__name_short(intf, line, expected):
    """Intf.name_short()"""
    actual = intf.name_short()
    assert actual == expected


@pytest.mark.parametrize("line, kwargs, expected", [
    # vlan
    ("interface Vlan1", {}, "V1"),
    ("interface Vlan1", {"device_type": "cisco_ios"}, "Vlan1"),
    ("interface Vlan1", {"device_type": "cisco_nxos"}, "Vlan1"),
    ("interface Vlan1", {"device_type": "cisco_xr"}, "Vlan1"),
    ("interface Vlan1", {"device_type": "hp_comware"}, "V1"),
    ("interface Vlan1", {"device_type": "hp_procurve"}, "Vlan1"),
    # GigabitEthernet
    ("interface GigabitEthernet1", {}, "Gi1"),
    ("interface GigabitEthernet1", {"device_type": "cisco_ios"}, "Gi1"),
    ("interface GigabitEthernet1", {"device_type": "cisco_nxos"}, "Gi1"),
    ("interface GigabitEthernet1", {"device_type": "cisco_xr"}, "Gi1"),
    ("interface GigabitEthernet1", {"device_type": "hp_comware"}, "GE1"),
    ("interface GigabitEthernet1", {"device_type": "hp_procurve"}, "Gi1"),
    # cisco_xr
    ("interface tunnel-ip1", {"device_type": "cisco_xr"}, "ti1"),
    ("tunnel-ip1", {"device_type": "cisco_xr"}, "ti1"),
    ("Tu1", {"device_type": "cisco_xr"}, "ti1"),
    ("tu1", {"device_type": "cisco_xr"}, "ti1"),
    ("ti1", {"device_type": "cisco_xr"}, "ti1"),
])
def test__name_short__device_type(intf_, line, kwargs, expected):
    """Intf.name_short(device_type)"""
    actual = intf_.name_short()
    assert actual == expected


@pytest.mark.parametrize("line, replace, expected", [
    ("interface Ethernet1", None, "Eth1"),
    ("interface Ethernet1", [], "Eth1"),
    ("interface Ethernet1", [("Eth", "Fa")], "Fa1"),
    ("interface Ethernet1", [("typo", "Fa")], "Eth1"),
    ("interface Ethernet1", [("Eth", "Fa"), ("typo", "Fa")], "Fa1"),
    ("interface Ethernet1", [("typo", "Fa"), ("Eth", "Fa")], "Fa1"),
    ("interface Ethernet1", [("Eth", "FA"), ("Eth", "Fa")], "FA1"),
])
def test__name_short__replace(intf, line, replace, expected):
    """Intf.name_short(replace)"""
    actual = intf.name_short(replace=replace)
    assert actual == expected


@pytest.mark.parametrize("line, idx, expected", [
    ("", -1, ""),
    ("", 0, ""),
    ("", 1, ""),
    ("1", -1, "1"),
    ("1", 0, "1"),
    ("1", 1, ""),
    ("1", 2, ""),
    ("1/2", -1, "1/2"),
    ("1/2", 0, "1/2"),
    ("1/2", 1, "/2"),
    ("1/2", 2, ""),
    ("1/2", 3, ""),
    # lag 1
    ("lag 1", -1, "lag 1"),
    ("lag 1", 0, "1"),
    ("lag 1", 1, ""),
    ("lag 1", 2, ""),
    # port1
    ("port1", -1, "port1"),
    ("port1", 0, "1"),
    ("port1", 1, ""),
    ("port1", 2, ""),
    # port1.2
    ("port1.2", -1, "port1.2"),
    ("port1.2", 0, "1.2"),
    ("port1.2", 1, ".2"),
    ("port1.2", 2, ""),
    ("port1.2", 3, ""),
    ("port1.2", 4, ""),
    # interface Ethernet1/2/3/4/5.6
    ("interface Ethernet1/2/3/4/5.6", -1, "interface Ethernet1/2/3/4/5.6"),
    ("interface Ethernet1/2/3/4/5.6", 0, "1/2/3/4/5.6"),
    ("interface Ethernet1/2/3/4/5.6", 1, "/2/3/4/5.6"),
    ("interface Ethernet1/2/3/4/5.6", 2, "/3/4/5.6"),
    ("interface Ethernet1/2/3/4/5.6", 3, "/4/5.6"),
    ("interface Ethernet1/2/3/4/5.6", 4, "/5.6"),
    ("interface Ethernet1/2/3/4/5.6", 5, ".6"),
    ("interface Ethernet1/2/3/4/5.6", 6, ""),
    ("interface Ethernet1/2/3/4/5/6.7", 7, ""),
])
def test__part_after(intf, line, idx, expected):
    """Intf.part_after()"""
    actual = intf.part_after(idx=idx)
    assert actual == expected


@pytest.mark.parametrize("line, idx, expected", [
    ("", -1, ""),
    ("", 0, ""),
    ("", 1, ""),
    ("1", -1, ""),
    ("1", 0, ""),
    ("1", 1, ""),
    ("1", 2, "1"),
    ("1/2", -1, ""),
    ("1/2", 0, ""),
    ("1/2", 1, ""),
    ("1/2", 2, "1/"),
    ("1/2", 3, "1/2"),
    # lag 1
    ("lag 1", -1, ""),
    ("lag 1", 0, ""),
    ("lag 1", 1, "lag "),
    ("lag 1", 2, "lag 1"),
    # port1
    ("port1", -1, ""),
    ("port1", 0, ""),
    ("port1", 1, "port"),
    ("port1", 2, "port1"),
    ("port1", 3, "port1"),
    ("port1", 4, "port1"),
    ("port1", 5, "port1"),
    ("port1", 6, "port1"),
    ("port1", 7, "port1"),
    # port1.2
    ("port1.2", -1, ""),
    ("port1.2", 0, ""),
    ("port1.2", 1, "port"),
    ("port1.2", 2, "port1."),
    ("port1.2", 3, "port1.2"),
    ("port1.2", 4, "port1.2"),
    ("port1.2", 5, "port1.2"),
    ("port1.2", 6, "port1.2"),
    ("port1.2", 7, "port1.2"),
    # interface Ethernet1/2/3/4/5.6
    ("interface Ethernet1/2/3/4/5.6", -1, ""),
    ("interface Ethernet1/2/3/4/5.6", 0, ""),
    ("interface Ethernet1/2/3/4/5.6", 1, "interface Ethernet"),
    ("interface Ethernet1/2/3/4/5.6", 2, "interface Ethernet1/"),
    ("interface Ethernet1/2/3/4/5.6", 3, "interface Ethernet1/2/"),
    ("interface Ethernet1/2/3/4/5.6", 4, "interface Ethernet1/2/3/"),
    ("interface Ethernet1/2/3/4/5.6", 5, "interface Ethernet1/2/3/4/"),
    ("interface Ethernet1/2/3/4/5.6", 6, "interface Ethernet1/2/3/4/5."),
    ("interface Ethernet1/2/3/4/5/6.7", 7, "interface Ethernet1/2/3/4/5/6"),
])
def test__part_before(intf, line, idx, expected):
    """Intf.part_before()"""
    actual = intf.part_before(idx=idx)
    assert actual == expected


# ============================ functions =============================

@pytest.mark.parametrize("params, expected", [
    ({"port": "Eth1", "required": ["Eth"]}, True),
    ({"port": "Eth1/2.3", "required": ["Eth"]}, True),
    ({"port": "Tu1", "required": ["Eth"]}, False),
    ({"port": "Tu1", "required": ["Eth", "Tu"]}, True),
    # ignore
    ({"port": "Eth1", "required": ["Eth"], "ignore": ["Tu"]}, True),
    ({"port": "Tun1", "required": ["Eth"], "ignore": ["Tu"]}, False),
])
def test__is_port_base(params, expected):
    """intf.is_port_base()"""
    actual = netport_intf.is_port_base(**params)

    assert actual == expected


@pytest.mark.parametrize("names, reverse, expected", [
    (["p1/1", "p1/10", "p1/2"], False, ["p1/1", "p1/2", "p1/10"]),
    (["p1/1", "p1/10", "p1/2"], True, ["p1/10", "p1/2", "p1/1"]),
    ([], False, []),
])
def test__sort_names(names, reverse, expected):
    """intf.sort_names()"""
    actual = netport_intf.sort_names(names=names, reverse=reverse)

    assert actual == expected


# ============================= helpers ==============================

@pytest.mark.parametrize("kwargs, expected", [
    ({"device_type": "cisco_ios"}, "cisco_ios"),
    ({"device_type": "cisco_nxos"}, "cisco_nxos"),
    ({"device_type": "cisco_xr"}, "cisco_xr"),
    ({"device_type": "hp_comware"}, "hp_comware"),
    ({"device_type": "hp_procurve"}, "hp_procurve"),
    ({"device_type": "fortinet"}, NetportsValueError),
    ({}, ""),
])
def test__validate_device_type(kwargs, expected):
    """intf._validate_device_type()"""
    if isinstance(expected, str):
        actual = netport_intf._init_device_type(**kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            netport_intf._init_device_type(**kwargs)


@pytest.mark.parametrize("kwargs, expected", [
    ({"splitter": "."}, "."),
    ({}, ",./:"),
])
def test__validate_splitter(kwargs, expected):
    """intf._validate_splitter()"""
    actual = netport_intf._init_splitter(**kwargs)
    assert actual == expected
