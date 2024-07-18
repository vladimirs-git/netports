"""Tests intfs.py"""

import pytest
import difflib
from netports.intf import Intf
from tests import params__intf as p


# ========================== redefined ===========================

@pytest.mark.parametrize("line, expected, id0, id1, id2", [
    ("", "", "", 0, 0),
    (" ", " ", " ", 0, 0),
    ("Eth1/2", "Eth1/2", "Eth", 1, 2),
    (" Eth1/2 ", " Eth1/2 ", " Eth", 1, 2),
    ("interface Eth1/2", "interface Eth1/2", "interface Eth", 1, 2),
    (" interface Eth1/2 ", " interface Eth1/2 ", " interface Eth", 1, 2),
])
def test____str__(line, expected, id0, id1, id2):
    """Intf.__str__()"""
    intf = Intf(line)
    actual = str(intf)
    assert actual == expected
    assert intf.id0 == id0
    assert intf.id1 == id1
    assert intf.id2 == id2


@pytest.mark.parametrize("line, expected", [
    ("Eth1/2", "Intf('Eth1/2')"),
])
def test____repr__(line, expected):
    """Intf.__repr__()"""
    intf = Intf(line)
    actual = repr(intf)
    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    ("", hash(("", 0, 0, 0, 0, 0, 0))),
    ("Eth1/2/3/4/5.6.7", hash(("Eth", 1, 2, 3, 4, 5, 6))),
])
def test____hash__(line, expected):
    """Intf.__hash__()"""
    intf = Intf(line)
    actual = hash(intf)
    assert actual == expected


@pytest.mark.parametrize("line1, line2, expected", [
    ("Eth1/2/3.4", "Eth1/2/3.4", True),
    ("Eth1/2/3.4", "Eth1/2/3.5", False),
    ("Eth1/2/3.4", "interface Eth1/2/3.4", False),
    ("Eth1/2/3.4", "Eth1.2.3.4", True),
])
def test____eq__(line1, line2, expected):
    """Intf.__eq__()"""
    Intf(line1)
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
def test____eq__(line1, line2, expected):
    """Intf.__eq__()"""
    Intf(line1)
    actual = Intf(line1) < Intf(line2)
    assert actual == expected


# =========================== property ===========================

@pytest.mark.parametrize("line, expected", [
    ("", ('', '', '', '', '')),
    ("interface Eth1/2/3.4", ('/', '/', '.', '', '')),
    ("interface Eth1/2/3/4/5.6", ('/', '/', '/', '/', '.')),
    ("interface Eth1,2.3/4:5/6/7", (',', '.', '/', ':', '/')),
])
def test__delimiters(line, expected):
    """Intf.delimiters"""
    intf = Intf(line)
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
def test__id0(line, expected):
    """Intf.id0"""
    intf = Intf(line)
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
def test__id1(line, expected):
    """Intf.id1"""
    intf = Intf(line)
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
def test__id2(line, expected):
    """Intf.id2"""
    intf = Intf(line)
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
def test__id3(line, expected):
    """Intf.id3"""
    intf = Intf(line)
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
def test__id4(line, expected):
    """Intf.id4"""
    intf = Intf(line)
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
def test__id5(line, expected):
    """Intf.id5"""
    intf = Intf(line)
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
def test__id6(line, expected):
    """Intf.id6"""
    intf = Intf(line)
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
def test__line(line, expected):
    """Intf.line"""
    intf = Intf(line)
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
def test__name(line, expected):
    """Intf.name"""
    intf = Intf(line)
    actual = intf.name
    assert actual == expected


@pytest.mark.parametrize("line, device_type", [
    ("Eth", ""),
    ("Eth", "cisco_ios"),
])
def test__device_type(line, device_type):
    """Intf.device_type"""
    intf = Intf(line=line, device_type=device_type)
    actual = intf.device_type
    assert actual == device_type


@pytest.mark.parametrize("line, splitter, expected, id0, id1, id2", [
    ("Eth1-2", "", ",./:", "Eth", 1, 0),
    ("Eth1-2", "-", "-", "Eth", 1, 2),
])
def test__splitter(line, splitter, expected, id0, id1, id2):
    """Intf.splitter"""
    intf = Intf(line=line, splitter=splitter)
    actual = intf.splitter
    assert actual == expected
    assert intf.id0 == id0
    assert intf.id1 == id1
    assert intf.id2 == id2


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
def test__all_names(line, expected):
    """Intf.all_names()"""
    intf = Intf(line=line)

    actual = intf.all_names()

    diff = list(difflib.unified_diff(actual, expected, lineterm=""))
    diff = [s for s in diff if s.startswith("-") or s.startswith("+")]
    assert not diff


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
def test__all_names(line, expected):
    """Intf.all_names()"""
    intf = Intf(line=line)

    actual = intf.all_names()

    diff = list(difflib.unified_diff(actual, expected, lineterm=""))
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
def test__last_idx(line, expected):
    """Intf.last_idx()"""
    intf = Intf(line=line)

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
def test__name_base(line, expected):
    """Intf.name_base()"""
    intf = Intf(line=line)

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
def test__name_full(line, expected):
    """Intf.name_full()"""
    intf = Intf(line=line)

    actual = intf.name_full()

    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    # cisco_xr
    ("interface tunnel-ip1", "interface tunnel-ip1"),
    ("tunnel-ip1", "interface tunnel-ip1"),
    ("Tu1", "interface tunnel-ip1"),
    ("tu1", "interface tunnel-ip1"),
    ("ti1", "interface tunnel-ip1"),
])
def test__name_full__cisco_xr(line, expected):
    """Intf.name_full(device_type="cisco_xr")"""
    intf = Intf(line=line, device_type="cisco_xr")

    actual = intf.name_full()

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
def test__name_long(line, expected):
    """Intf.name_long()"""
    intf = Intf(line=line)

    actual = intf.name_long()

    assert actual == expected


@pytest.mark.parametrize("line, expected", [
    # cisco_xr
    ("interface tunnel-ip1", "tunnel-ip1"),
    ("tunnel-ip1", "tunnel-ip1"),
    ("Tu1", "tunnel-ip1"),
    ("tu1", "tunnel-ip1"),
    ("ti1", "tunnel-ip1"),
])
def test__name_long__cisco_xr(line, expected):
    """Intf.name_long(device_type="cisco_xr")"""
    intf = Intf(line=line, device_type="cisco_xr")

    actual = intf.name_long()

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
def test__name_short(line, expected):
    """Intf.name_short()"""
    intf = Intf(line=line)

    actual = intf.name_short()

    assert actual == expected


@pytest.mark.parametrize("line, device_type, expected", [
    # vlan
    ("interface Vlan1", "", "V1"),
    ("interface Vlan1", "cisco_ios", "Vlan1"),
    ("interface Vlan1", "cisco_nxos", "Vlan1"),
    ("interface Vlan1", "cisco_xr", "Vlan1"),
    ("interface Vlan1", "hp_comware", "V1"),
    ("interface Vlan1", "hp_procurve", "Vlan1"),
    # GigabitEthernet
    ("interface GigabitEthernet1", "", "Gi1"),
    ("interface GigabitEthernet1", "cisco_ios", "Gi1"),
    ("interface GigabitEthernet1", "cisco_nxos", "Gi1"),
    ("interface GigabitEthernet1", "cisco_xr", "Gi1"),
    ("interface GigabitEthernet1", "hp_comware", "GE1"),
    ("interface GigabitEthernet1", "hp_procurve", "Gi1"),
    # cisco_xr
    ("interface tunnel-ip1", "cisco_xr", "ti1"),
    ("tunnel-ip1", "cisco_xr", "ti1"),
    ("Tu1", "cisco_xr", "ti1"),
    ("tu1", "cisco_xr", "ti1"),
    ("ti1", "cisco_xr", "ti1"),
])
def test__name_short__device_type(line, device_type, expected):
    """Intf.name_short(device_type)"""
    intf = Intf(line=line, device_type=device_type)

    actual = intf.name_short()

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
def test__name_short__replace(line, replace, expected):
    """Intf.name_short(replace)"""
    intf = Intf(line=line)

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
def test__part_after(line, idx, expected):
    """Intf.part_after()"""
    intf = Intf(line=line)

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
def test__part_before(line, idx, expected):
    """Intf.part_before()"""
    intf = Intf(line=line)

    actual = intf.part_before(idx=idx)

    assert actual == expected
