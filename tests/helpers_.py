"""unittest helpers"""

import unittest
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
    "interface Tunnel-ip1",
    "interface tunnel-ip1",
    "interface Tunnel1",
    "interface tunnel1",
    "interface Tu1",
    "interface tu1",
    "Tunnel-ip1",
    "tunnel-ip1",
    "Tunnel1",
    "tunnel1",
    "Tu1",
    "tu1",
]
ALL_NAMES_TUN_IP_ = [
    "interface Tunnel-ip1",
    "interface tunnel-ip1",
    "interface Tu1",
    "interface tu1",
    "Tunnel-ip1",
    "tunnel-ip1",
    "Tu1",
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
ALL_NAMES_1 = [
    "interface 1",
    "1",
]


class Helpers(unittest.TestCase):
    """Address"""

    def _test_attrs(self, obj, exp_d, msg: str):
        """Test obj.line and attributes in req_d
        :param obj: Tested object
        :param exp_d: Valid attributes and values
        :param msg: Message
        """
        actual = obj.line
        expected = exp_d["line"]
        self.assertEqual(expected, actual, msg=f"{msg} line")
        actual = str(obj)
        self.assertEqual(expected, actual, msg=f"{msg} str")
        for attr, expected in exp_d.items():
            if attr == "numbers":
                method: Callable = getattr(obj, attr)
                actual = method()
            else:
                actual = getattr(obj, attr)
            if hasattr(actual, "line"):
                actual = str(actual)
            self.assertEqual(expected, actual, msg=f"{msg} {attr=}")
