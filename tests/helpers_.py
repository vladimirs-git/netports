"""Tests helpers"""

from typing import Callable

ALL_NAMES_ETH = [
    "interface Ethernet1/2",
    "interface ethernet1/2",
    "interface Eth1/2",
    "interface eth1/2",
    "Ethernet1/2",
    "ethernet1/2",
    "Eth1/2",
    "eth1/2",
]
ALL_NAMES_TUN_IP = [
    "interface tunnel-ip1",
    "interface ti1",
    "tunnel-ip1",
    "ti1",
]
ALL_NAMES_TUN_IP_LOWER = [
    "interface tunnel-ip1",
    "interface ti1",
    "interface tu1",
    "tunnel-ip1",
    "ti1",
    "tu1",
]
ALL_NAMES_TUN_IP_UPPER = [
    "interface Tunnel-ip1",
    "interface tunnel-ip1",
    "interface ti1",
    "Tunnel-ip1",
    "tunnel-ip1",
    "ti1",
]
ALL_NAMES_TUN_IP_UPPER2 = [
    "interface tunnel-ip1",
    "interface Tu1",
    "interface ti1",
    "interface tu1",
    "tunnel-ip1",
    "Tu1",
    "ti1",
    "tu1",
]
ALL_NAMES_TUN = [
    "interface Tunnel1",
    "interface tunnel1",
    "interface Tu1",
    "interface tu1",
    "Tunnel1",
    "tunnel1",
    "Tu1",
    "tu1",
]
ALL_NAMES_MGMT = [
    "interface mgmt0",
    "mgmt0",
]
ALL_NAMES_HPC = [
    "interface 1",
    "1",
    "interface 1/1",
]


def test_attrs(obj, exp_d):
    """Test obj.line and attributes in req_d
    :param obj: Tested object
    :param exp_d: Valid attributes and values
    """
    actual = obj.line
    expected = exp_d["line"]
    assert expected == actual

    actual = str(obj)
    assert expected == actual

    for attr, expected in exp_d.items():
        if attr == "numbers":
            method: Callable = getattr(obj, attr)
            actual = method()
        else:
            actual = getattr(obj, attr)
        if hasattr(actual, "line"):
            actual = str(actual)
        assert expected == actual
