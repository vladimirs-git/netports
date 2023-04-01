"""unittest intfs.py"""

import unittest

from netports.intf import Intf
from tests import helpers_ as th
from tests.helpers_ import Helpers


# noinspection DuplicatedCode
class Test(Helpers):
    """Intf"""

    # ========================== redefined ===========================

    def test_valid__hash__(self):
        """Intf.__hash__()"""
        intf1 = "interface Ethernet1/2/3.4"
        intf_o = Intf(intf1)
        actual = intf_o.__hash__()
        expected = hash(("interface Ethernet", 1, 2, 3, 4))
        self.assertEqual(expected, actual, msg=f"{intf1=}")

    def test_valid__eq__(self):
        """Intf.__eq__() __ne__()"""
        intf1 = "interface Ethernet1/2/3.4"
        intf_o = Intf(intf1)
        for other_o, expected, in [
            (Intf(intf1), True),
            (Intf("interface Ethernet1.2.3.4"), True),
            (Intf("interface Ethernet1/1"), False),
        ]:
            actual = intf_o.__eq__(other_o)
            self.assertEqual(expected, actual, msg=f"{intf_o=} {other_o=}")
            actual = intf_o.__ne__(other_o)
            self.assertEqual(not expected, actual, msg=f"{intf_o=} {other_o=}")

    def test_valid__lt__(self):
        """Intf.__lt__() __le__() __gt__() __ge__()"""
        intf1 = "interface Eth1/2/3.4"
        for intf_o, other_o, exp_lt, exp_le, exp_gt, exp_ge in [
            (Intf(intf1), intf1, False, False, True, True),
            (Intf(intf1), Intf("1"), False, False, True, True),
            (Intf(intf1), Intf("a 9"), False, False, True, True),
            (Intf(intf1), Intf("z 0"), True, True, False, False),
            (Intf(intf1), Intf("interface Eth"), False, False, True, True),
            (Intf(intf1), Intf("interface Eth1"), False, False, True, True),
            (Intf(intf1), Intf("interface Eth1/2"), False, False, True, True),
            (Intf(intf1), Intf("interface Eth1/2/3"), False, False, True, True),
            (Intf(intf1), Intf(intf1), False, True, False, True),
            (Intf(intf1), Intf("interface Eth1.2.3.4"), False, True, False, True),
        ]:
            actual = intf_o.__lt__(other_o)
            self.assertEqual(exp_lt, actual, msg=f"{intf_o=} {other_o=}")
            actual = intf_o.__le__(other_o)
            self.assertEqual(exp_le, actual, msg=f"{intf_o=} {other_o=}")
            actual = intf_o.__gt__(other_o)
            self.assertEqual(exp_gt, actual, msg=f"{intf_o=} {other_o=}")
            actual = intf_o.__ge__(other_o)
            self.assertEqual(exp_ge, actual, msg=f"{intf_o=} {other_o=}")

    def test_valid__lt__sort(self):
        """Intf.__lt__(), Intf.__le__()"""
        intf1 = "interface Ethernet1/2/3.4"
        for items in [
            [intf1, Intf(intf1)],
            [Intf(intf1), Intf(intf1)],
            [Intf("1"), Intf(intf1)],
            [Intf("a 9"), Intf(intf1)],
            [Intf("interface Ethernet"), Intf(intf1)],
            [Intf("interface Ethernet1"), Intf(intf1)],
            [Intf(intf1), Intf("interface Ethernet2")],
            [Intf("interface Ethernet1/1"), Intf(intf1)],
            [Intf("interface Ethernet1/2"), Intf(intf1)],
            [Intf(intf1), Intf("interface Ethernet1/3")],
            [Intf("interface Ethernet1/2/1"), Intf(intf1)],
            [Intf("interface Ethernet1/2/3"), Intf(intf1)],
            [Intf(intf1), Intf("interface Ethernet1/2/4")],
            [Intf("interface Ethernet1/2/3.1"), Intf(intf1)],
            [Intf("interface Ethernet1/2/3.4"), Intf(intf1)],
            [Intf(intf1), Intf("interface Ethernet1/2/3.5")],
            [Intf("interface Ethernet1.2.3.1"), Intf(intf1)],
            [Intf("interface Ethernet1.2.3.4"), Intf(intf1)],
            [Intf(intf1), Intf("interface Ethernet1.2.3.5")],
        ]:
            expected = items.copy()
            actual = sorted(items)
            self.assertEqual(expected, actual, msg=f"{items=}")
            items[0], items[1] = items[1], items[0]
            actual = sorted(items)
            self.assertEqual(expected, actual, msg=f"{items=}")

    # =========================== property ===========================

    def test_valid__init__(self):
        """Intf.__init__()"""
        id0 = "interface Ethernet"
        exp_a1 = dict(line="1", name="1", id0="", id1=1, id2=0, id3=0, id4=0)
        exp_a2 = dict(line="1/2", name="1/2", id0="", id1=1, id2=2, id3=0, id4=0)
        exp_a3 = dict(line="port1", name="port1", id0="port", id1=1, id2=0, id3=0, id4=0)
        exp_a4 = dict(line="port1.2", name="port1.2", id0="port", id1=1, id2=2, id3=0, id4=0)
        exp_a5 = dict(line="text", name="text", id0="text", id1=0, id2=0, id3=0, id4=0)
        exp_a6 = dict(line=id0, name="Ethernet", id0=id0, id1=0, id2=0, id3=0, id4=0)

        exp_b1 = dict(line=f"{id0}1", name="Ethernet1", id0=id0, id1=1, id2=0, id3=0, id4=0)
        exp_b2 = dict(line=f"{id0}1/2", name="Ethernet1/2", id0=id0, id1=1, id2=2, id3=0, id4=0)
        exp_b3 = dict(line=f"{id0}1/2/3", name="Ethernet1/2/3", id0=id0, id1=1, id2=2, id3=3, id4=0)
        exp_b4 = dict(line=f"{id0}1/2/3.4", name="Ethernet1/2/3.4",
                      id0=id0, id1=1, id2=2, id3=3, id4=4)
        exp_b5 = dict(line=f"{id0}1.2.3.4", name="Ethernet1.2.3.4", _splitter=",./:",
                      id0=id0, id1=1, id2=2, id3=3, id4=4)
        exp_b6 = dict(line=f"{id0}1,2,3,4", name="Ethernet1,2,3,4", _splitter=",./:",
                      id0=id0, id1=1, id2=2, id3=3, id4=4)
        exp_b7 = dict(line=f"{id0}1:2:3:4", name="Ethernet1:2:3:4", _splitter=",./:",
                      id0=id0, id1=1, id2=2, id3=3, id4=4)
        exp_b8 = dict(line=f"{id0}1-2-3-4", name="Ethernet1-2-3-4", _splitter="-",
                      id0=id0, id1=1, id2=2, id3=3, id4=4)

        exp_c1 = dict(line=f"{id0}1/1", name="Ethernet1/1", id0=id0, id1=1, id2=1, id3=0, id4=0)
        for kwargs, exp_d in [
            (dict(line="1"), exp_a1),
            (dict(line="1/2"), exp_a2),
            (dict(line="port1"), exp_a3),
            (dict(line="port1.2"), exp_a4),
            (dict(line="text"), exp_a5),
            (dict(line=id0), exp_a6),
            # splitter
            (dict(line=f"{id0}1"), exp_b1),
            (dict(line=f"{id0}1/2"), exp_b2),
            (dict(line=f"{id0}1/2/3"), exp_b3),
            (dict(line=f"{id0}1/2/3.4"), exp_b4),
            (dict(line=f"{id0}1/2/3.4-5"), exp_b4),
            (dict(line=f"{id0}1/2/3.4text"), exp_b4),
            (dict(line=f"{id0}1.2.3.4"), exp_b5),
            (dict(line=f"{id0}1,2,3,4"), exp_b6),
            (dict(line=f"{id0}1:2:3:4"), exp_b7),
            (dict(line=f"{id0}1-2-3-4", splitter="-"), exp_b8),
            # platform
            (dict(line="interface Ethernet1/1", platform=""), exp_c1),
            (dict(line="interface Ethernet1/1", platform="cisco_asr"), exp_c1),
        ]:
            intf_o = Intf(**kwargs)
            self._test_attrs(obj=intf_o, exp_d=exp_d, msg=f"{kwargs=}")

    def test_invalid__init__(self):
        """Intf.__init__()"""
        for kwargs, error in [
            (dict(line="Ethernet1/1", platform="typo"), ValueError),
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                Intf(**kwargs)

    # =========================== methods ============================

    def test_valid__all_names(self):
        """Intf.all_names()"""
        for line, expected in [
            # upper
            ("interface Ethernet1/2", th.ALL_NAMES_ETH),
            ("Ethernet1/2", th.ALL_NAMES_ETH),
            ("Eth1/2", th.ALL_NAMES_ETH),
            ("interface tunnel-ip1", th.ALL_NAMES_TUN_IP),
            ("tunnel-ip1", th.ALL_NAMES_TUN_IP),
            ("interface Tunnel1", th.ALL_NAMES_TUN),
            ("Tunnel1", th.ALL_NAMES_TUN),
            ("Tu1", th.ALL_NAMES_TUN),
            ("interface mgmt0", th.ALL_NAMES_MGMT),
            ("mgmt0", th.ALL_NAMES_MGMT),
            ("1", th.ALL_NAMES_1),
            # lower
            ("interface ethernet1/2", th.ALL_NAMES_ETH),
            ("ethernet1/2", th.ALL_NAMES_ETH),
            ("eth1/2", th.ALL_NAMES_ETH),
            ("interface tunnel-ip1", th.ALL_NAMES_TUN_IP),
            ("tunnel-ip1", th.ALL_NAMES_TUN_IP),
            ("interface tunnel1", th.ALL_NAMES_TUN),
            ("tunnel1", th.ALL_NAMES_TUN),
            ("tu1", th.ALL_NAMES_TUN),
            ("interface mgmt0", th.ALL_NAMES_MGMT),
            ("mgmt0", th.ALL_NAMES_MGMT),
            ("1", th.ALL_NAMES_1),
        ]:
            obj = Intf(line)
            actual = obj.all_names()
            self.assertEqual(expected, actual, msg=f"{line=}")

    def test_valid__all_names__cisco_asr(self):
        """Intf.all_names() platform="cisco_asr" """
        for line, expected in [
            # upper
            ("interface Tunnel-ip1", th.ALL_NAMES_TUN_IP_UPPER),
            ("Tunnel-ip1", th.ALL_NAMES_TUN_IP_UPPER),
            ("Tu1", th.ALL_NAMES_TUN_IP_UPPER2),
            # lower
            ("interface tunnel-ip1", th.ALL_NAMES_TUN_IP),
            ("tunnel-ip1", th.ALL_NAMES_TUN_IP),
            ("tu1", th.ALL_NAMES_TUN_IP_LOWER),
            ("ti1", th.ALL_NAMES_TUN_IP),
        ]:
            obj = Intf(line=line, platform="cisco_asr")
            actual = obj.all_names()
            self.assertEqual(expected, actual, msg=f"{line=}")

    def test_valid__last_idx(self):
        """Intf.last_idx()"""
        for line, expected in [
            ("", 0),
            ("Ethernet", 0),
            ("Ethernet1", 1),
            ("Ethernet1/2", 2),
            ("Ethernet1/2/3", 3),
            ("Ethernet1/2/3.4", 4),
            ("Ethernet1/2/3.4-5", 4),
        ]:
            obj = Intf(line)
            actual = obj.last_idx()
            self.assertEqual(expected, actual, msg=f"{line=}")

    def test_valid__name_full(self):
        """Intf.name_full()"""
        for line, expected in [
            # full to full
            ("interface Ethernet1/2/3.4", "interface Ethernet1/2/3.4"),
            ("interface FastEthernet1/2", "interface FastEthernet1/2"),
            ("interface GigabitEthernet1/2", "interface GigabitEthernet1/2"),
            ("interface TenGigabitEthernet1/2", "interface TenGigabitEthernet1/2"),
            ("interface Loopback0", "interface Loopback0"),
            ("interface Port-channel100", "interface Port-channel100"),
            ("interface Tunnel1", "interface Tunnel1"),
            ("interface Vlan1", "interface Vlan1"),
            ("interface mgmt0", "interface mgmt0"),  # nxos
            # long to full
            ("Ethernet1/2/3.4", "interface Ethernet1/2/3.4"),
            ("FastEthernet1/2", "interface FastEthernet1/2"),
            ("GigabitEthernet1/2", "interface GigabitEthernet1/2"),
            ("TenGigabitEthernet1/2", "interface TenGigabitEthernet1/2"),
            ("Loopback0", "interface Loopback0"),
            ("Port-channel100", "interface Port-channel100"),
            ("Tunnel1", "interface Tunnel1"),
            ("Vlan1", "interface Vlan1"),
            ("mgmt0", "interface mgmt0"),  # nxos
            # short to full
            ("Eth1/2/3.4", "interface Ethernet1/2/3.4"),
            ("Fa1/2", "interface FastEthernet1/2"),
            ("Gi1/2", "interface GigabitEthernet1/2"),
            ("Te1/2", "interface TenGigabitEthernet1/2"),
            ("Lo0", "interface Loopback0"),
            ("Po100", "interface Port-channel100"),
            ("Tu1", "interface Tunnel1"),
            ("V1", "interface Vlan1"),
            ("mgmt0", "interface mgmt0"),  # nxos
            # lower
            ("interface ethernet1/2/3.4", "interface Ethernet1/2/3.4"),
            ("interface fastethernet1/2", "interface FastEthernet1/2"),
            ("ethernet1/2/3.4", "interface Ethernet1/2/3.4"),
            ("fastethernet1/2", "interface FastEthernet1/2"),
            ("eth1/2/3.4", "interface Ethernet1/2/3.4"),
            ("fa1/2", "interface FastEthernet1/2"),
            ("v1", "interface Vlan1"),
        ]:
            obj = Intf(line)
            actual = obj.name_full()
            self.assertEqual(expected, actual, msg=f"{line=}")

    def test_valid__name_full__cisco_asr(self):
        """Intf.name_full() platform="cisco_asr" """
        platform = "cisco_asr"
        for line, expected in [
            ("interface tunnel-ip1", "interface tunnel-ip1"),
            ("tunnel-ip1", "interface tunnel-ip1"),
            ("Tu1", "interface tunnel-ip1"),
            ("tu1", "interface tunnel-ip1"),
            ("ti1", "interface tunnel-ip1"),
        ]:
            obj = Intf(line=line, platform=platform)
            actual = obj.name_full()
            self.assertEqual(expected, actual, msg=f"{line=} {platform=}")

    def test_valid__name_long(self):
        """Intf.name_long()"""
        for line, expected in [
            # full to long
            ("interface Ethernet1/2/3.4", "Ethernet1/2/3.4"),
            ("interface FastEthernet1/2", "FastEthernet1/2"),
            ("interface GigabitEthernet1/2", "GigabitEthernet1/2"),
            ("interface TenGigabitEthernet1/2", "TenGigabitEthernet1/2"),
            ("interface Loopback0", "Loopback0"),
            ("interface Port-channel100", "Port-channel100"),
            ("interface Tunnel1", "Tunnel1"),
            ("interface Vlan1", "Vlan1"),
            ("interface mgmt0", "mgmt0"),  # nxos
            # long to long
            ("Ethernet1/2/3.4", "Ethernet1/2/3.4"),
            ("FastEthernet1/2", "FastEthernet1/2"),
            ("GigabitEthernet1/2", "GigabitEthernet1/2"),
            ("TenGigabitEthernet1/2", "TenGigabitEthernet1/2"),
            ("Loopback0", "Loopback0"),
            ("Port-channel100", "Port-channel100"),
            ("Tunnel1", "Tunnel1"),
            ("Vlan1", "Vlan1"),
            ("mgmt0", "mgmt0"),  # nxos
            # short to long
            ("Eth1/2/3.4", "Ethernet1/2/3.4"),
            ("Fa1/2", "FastEthernet1/2"),
            ("Gi1/2", "GigabitEthernet1/2"),
            ("Te1/2", "TenGigabitEthernet1/2"),
            ("Lo0", "Loopback0"),
            ("Po100", "Port-channel100"),
            ("Tu1", "Tunnel1"),
            ("V1", "Vlan1"),
            ("mgmt0", "mgmt0"),  # nxos
            # lower
            ("interface ethernet1/2/3.4", "Ethernet1/2/3.4"),
            ("interface fastethernet1/2", "FastEthernet1/2"),
            ("ethernet1/2/3.4", "Ethernet1/2/3.4"),
            ("fastethernet1/2", "FastEthernet1/2"),
            ("eth1/2/3.4", "Ethernet1/2/3.4"),
            ("fa1/2", "FastEthernet1/2"),
            ("v1", "Vlan1"),
        ]:
            obj = Intf(line)
            actual = obj.name_long()
            self.assertEqual(expected, actual, msg=f"{line=}")

    def test_valid__name_long__cisco_asr(self):
        """Intf.name_long() platform="cisco_asr" """
        platform = "cisco_asr"
        for line, expected in [
            ("interface tunnel-ip1", "tunnel-ip1"),
            ("tunnel-ip1", "tunnel-ip1"),
            ("Tu1", "tunnel-ip1"),
            ("tu1", "tunnel-ip1"),
            ("ti1", "tunnel-ip1"),
        ]:
            obj = Intf(line=line, platform=platform)
            actual = obj.name_long()
            self.assertEqual(expected, actual, msg=f"{line=} {platform=}")

    def test_valid__name_short(self):
        """Intf.name_short()"""
        for line, expected in [
            # full to short
            ("interface Ethernet1/2/3.4", "Eth1/2/3.4"),
            ("interface FastEthernet1/2", "Fa1/2"),
            ("interface GigabitEthernet1/2", "Gi1/2"),
            ("interface TenGigabitEthernet1/2", "Te1/2"),
            ("interface Loopback0", "Lo0"),
            ("interface Port-channel100", "Po100"),
            ("interface Tunnel1", "Tu1"),
            ("interface Vlan1", "V1"),
            ("interface mgmt0", "mgmt0"),  # nxos
            # long to short
            ("Ethernet1/2/3.4", "Eth1/2/3.4"),
            ("FastEthernet1/2", "Fa1/2"),
            ("GigabitEthernet1/2", "Gi1/2"),
            ("TenGigabitEthernet1/2", "Te1/2"),
            ("Loopback0", "Lo0"),
            ("Port-channel100", "Po100"),
            ("Tunnel1", "Tu1"),
            ("Vlan1", "V1"),
            ("mgmt0", "mgmt0"),  # nxos
            # short to short
            ("Eth1/2/3.4", "Eth1/2/3.4"),
            ("Fa1/2", "Fa1/2"),
            ("Gi1/2", "Gi1/2"),
            ("Te1/2", "Te1/2"),
            ("Lo0", "Lo0"),
            ("Po100", "Po100"),
            ("Tu1", "Tu1"),
            ("V1", "V1"),
            ("mgmt0", "mgmt0"),  # nxos
            # lower
            ("interface ethernet1/2/3.4", "Eth1/2/3.4"),
            ("interface fastethernet1/2", "Fa1/2"),
            ("ethernet1/2/3.4", "Eth1/2/3.4"),
            ("fastethernet1/2", "Fa1/2"),
            ("eth1/2/3.4", "Eth1/2/3.4"),
            ("fa1/2", "Fa1/2"),
            ("v1", "V1"),
        ]:
            obj = Intf(line)
            actual = obj.name_short()
            self.assertEqual(expected, actual, msg=f"{line=}")

    def test_valid__name_short__cisco_asr(self):
        """Intf.name_short() platform="cisco_asr" """
        platform = "cisco_asr"
        for line, expected in [
            ("interface tunnel-ip1", "ti1"),
            ("tunnel-ip1", "ti1"),
            ("Tu1", "ti1"),
            ("tu1", "ti1"),
            ("ti1", "ti1"),
        ]:
            obj = Intf(line=line, platform=platform)
            actual = obj.name_short()
            self.assertEqual(expected, actual, msg=f"{line=} {platform=}")

    def test_valid__part_after(self):
        """Intf.part_after()"""
        for line, kwargs, expected in [
            # splitter=True
            ("", dict(idx=-1, splitter=True), ""),
            ("", dict(idx=0, splitter=True), ""),
            ("", dict(idx=1, splitter=True), ""),
            ("1", dict(idx=-1, splitter=True), "1"),
            ("1", dict(idx=0, splitter=True), "1"),
            ("1", dict(idx=1, splitter=True), ""),
            ("1", dict(idx=2, splitter=True), ""),
            ("1/2", dict(idx=-1, splitter=True), "1/2"),
            ("1/2", dict(idx=0, splitter=True), "1/2"),
            ("1/2", dict(idx=1, splitter=True), "/2"),
            ("1/2", dict(idx=2, splitter=True), ""),
            ("1/2", dict(idx=3, splitter=True), ""),
            # port1
            ("port1", dict(idx=-1, splitter=True), "port1"),
            ("port1", dict(idx=0, splitter=True), "1"),
            ("port1", dict(idx=1, splitter=True), ""),
            ("port1", dict(idx=2, splitter=True), ""),
            # port1.2
            ("port1.2", dict(idx=-1, splitter=True), "port1.2"),
            ("port1.2", dict(idx=0, splitter=True), "1.2"),
            ("port1.2", dict(idx=1, splitter=True), ".2"),
            ("port1.2", dict(idx=2, splitter=True), ""),
            ("port1.2", dict(idx=3, splitter=True), ""),
            ("port1.2", dict(idx=4, splitter=True), ""),
            # interface Ethernet1/2
            ("interface Ethernet1/2", dict(idx=-1, splitter=True), "interface Ethernet1/2"),
            ("interface Ethernet1/2", dict(idx=0, splitter=True), "1/2"),
            ("interface Ethernet1/2", dict(idx=1, splitter=True), "/2"),
            ("interface Ethernet1/2", dict(idx=2, splitter=True), ""),
            ("interface Ethernet1/2", dict(idx=3, splitter=True), ""),
            ("interface Ethernet1/2", dict(idx=4, splitter=True), ""),
            # interface Ethernet1/2/3.4
            ("interface Ethernet1/2/3.4", dict(idx=-1, splitter=True), "interface Ethernet1/2/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=0, splitter=True), "1/2/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=1, splitter=True), "/2/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=2, splitter=True), "/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=3, splitter=True), ".4"),
            ("interface Ethernet1/2/3.4", dict(idx=4, splitter=True), ""),
            ("interface Ethernet1/2/3.4", dict(idx=5, splitter=True), ""),

            # splitter=False
            ("", dict(idx=-1, splitter=False), ""),
            ("", dict(idx=0, splitter=False), ""),
            ("", dict(idx=1, splitter=False), ""),
            ("1", dict(idx=-1, splitter=False), "1"),
            ("1", dict(idx=0, splitter=False), "1"),
            ("1", dict(idx=1, splitter=False), ""),
            ("1", dict(idx=2, splitter=False), ""),
            ("1/2", dict(idx=-1, splitter=False), "1/2"),
            ("1/2", dict(idx=0, splitter=False), "1/2"),
            ("1/2", dict(idx=1, splitter=False), "2"),
            ("1/2", dict(idx=2, splitter=False), ""),
            ("1/2", dict(idx=3, splitter=False), ""),
            # port1
            ("port1", dict(idx=-1, splitter=False), "port1"),
            ("port1", dict(idx=0, splitter=False), "1"),
            ("port1", dict(idx=1, splitter=False), ""),
            ("port1", dict(idx=2, splitter=False), ""),
            # port1.2
            ("port1.2", dict(idx=-1, splitter=False), "port1.2"),
            ("port1.2", dict(idx=0, splitter=False), "1.2"),
            ("port1.2", dict(idx=1, splitter=False), "2"),
            ("port1.2", dict(idx=2, splitter=False), ""),
            ("port1.2", dict(idx=3, splitter=False), ""),
            ("port1.2", dict(idx=4, splitter=False), ""),
            # interface Ethernet1/2
            ("interface Ethernet1/2", dict(idx=-1, splitter=False), "interface Ethernet1/2"),
            ("interface Ethernet1/2", dict(idx=0, splitter=False), "1/2"),
            ("interface Ethernet1/2", dict(idx=1, splitter=False), "2"),
            ("interface Ethernet1/2", dict(idx=2, splitter=False), ""),
            ("interface Ethernet1/2", dict(idx=3, splitter=False), ""),
            ("interface Ethernet1/2", dict(idx=4, splitter=False), ""),
            # interface Ethernet1/2/3.4
            ("interface Ethernet1/2/3.4",
             dict(idx=-1, splitter=False), "interface Ethernet1/2/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=0, splitter=False), "1/2/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=1, splitter=False), "2/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=2, splitter=False), "3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=3, splitter=False), "4"),
            ("interface Ethernet1/2/3.4", dict(idx=4, splitter=False), ""),
            ("interface Ethernet1/2/3.4", dict(idx=5, splitter=False), ""),
        ]:
            obj = Intf(line)
            actual = obj.part_after(**kwargs)
            self.assertEqual(expected, actual, msg=f"{line=} {kwargs=}")

    def test_valid__part_before(self):
        """Intf.part_before()"""
        for line, kwargs, expected in [
            # splitter=True
            ("", dict(idx=-1, splitter=True), ""),
            ("", dict(idx=0, splitter=True), ""),
            ("", dict(idx=1, splitter=True), ""),
            ("1", dict(idx=-1, splitter=True), ""),
            ("1", dict(idx=0, splitter=True), ""),
            ("1", dict(idx=1, splitter=True), ""),
            ("1", dict(idx=2, splitter=True), "1"),
            ("1/2", dict(idx=-1, splitter=True), ""),
            ("1/2", dict(idx=0, splitter=True), ""),
            ("1/2", dict(idx=1, splitter=True), ""),
            ("1/2", dict(idx=2, splitter=True), "1/"),
            ("1/2", dict(idx=3, splitter=True), "1/2"),
            # port1
            ("port1", dict(idx=-1, splitter=True), ""),
            ("port1", dict(idx=0, splitter=True), ""),
            ("port1", dict(idx=1, splitter=True), "port"),
            ("port1", dict(idx=2, splitter=True), "port1"),
            # port1.2
            ("port1.2", dict(idx=-1, splitter=True), ""),
            ("port1.2", dict(idx=0, splitter=True), ""),
            ("port1.2", dict(idx=1, splitter=True), "port"),
            ("port1.2", dict(idx=2, splitter=True), "port1."),
            ("port1.2", dict(idx=3, splitter=True), "port1.2"),
            # interface Ethernet1/2
            ("interface Ethernet1/2", dict(idx=-1, splitter=True), ""),
            ("interface Ethernet1/2", dict(idx=0, splitter=True), ""),
            ("interface Ethernet1/2", dict(idx=1, splitter=True), "interface Ethernet"),
            ("interface Ethernet1/2", dict(idx=2, splitter=True), "interface Ethernet1/"),
            ("interface Ethernet1/2", dict(idx=3, splitter=True), "interface Ethernet1/2"),
            # interface Ethernet1/2/3.4
            ("interface Ethernet1/2/3.4", dict(idx=-1, splitter=True), ""),
            ("interface Ethernet1/2/3.4", dict(idx=0, splitter=True), ""),
            ("interface Ethernet1/2/3.4", dict(idx=1, splitter=True), "interface Ethernet"),
            ("interface Ethernet1/2/3.4", dict(idx=2, splitter=True), "interface Ethernet1/"),
            ("interface Ethernet1/2/3.4", dict(idx=3, splitter=True), "interface Ethernet1/2/"),
            ("interface Ethernet1/2/3.4", dict(idx=4, splitter=True), "interface Ethernet1/2/3."),
            ("interface Ethernet1/2/3.4", dict(idx=5, splitter=True), "interface Ethernet1/2/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=6, splitter=True), "interface Ethernet1/2/3.4"),

            # splitter=False
            ("", dict(idx=-1, splitter=False), ""),
            ("", dict(idx=0, splitter=False), ""),
            ("", dict(idx=1, splitter=False), ""),
            ("1", dict(idx=-1, splitter=False), ""),
            ("1", dict(idx=0, splitter=False), ""),
            ("1", dict(idx=1, splitter=False), ""),
            ("1", dict(idx=2, splitter=False), "1"),
            ("1/2", dict(idx=-1, splitter=False), ""),
            ("1/2", dict(idx=0, splitter=False), ""),
            ("1/2", dict(idx=1, splitter=False), ""),
            ("1/2", dict(idx=2, splitter=False), "1"),
            ("1/2", dict(idx=3, splitter=False), "1/2"),
            # port1
            ("port1", dict(idx=-1, splitter=False), ""),
            ("port1", dict(idx=0, splitter=False), ""),
            ("port1", dict(idx=1, splitter=False), "port"),
            ("port1", dict(idx=2, splitter=False), "port1"),
            # port1.2
            ("port1.2", dict(idx=-1, splitter=False), ""),
            ("port1.2", dict(idx=0, splitter=False), ""),
            ("port1.2", dict(idx=1, splitter=False), "port"),
            ("port1.2", dict(idx=2, splitter=False), "port1"),
            ("port1.2", dict(idx=3, splitter=False), "port1.2"),
            # interface Ethernet1/2
            ("interface Ethernet1/2", dict(idx=-1, splitter=False), ""),
            ("interface Ethernet1/2", dict(idx=0, splitter=False), ""),
            ("interface Ethernet1/2", dict(idx=1, splitter=False), "interface Ethernet"),
            ("interface Ethernet1/2", dict(idx=2, splitter=False), "interface Ethernet1"),
            ("interface Ethernet1/2", dict(idx=3, splitter=False), "interface Ethernet1/2"),
            # interface Ethernet1/2/3.4
            ("interface Ethernet1/2/3.4", dict(idx=-1, splitter=False), ""),
            ("interface Ethernet1/2/3.4", dict(idx=0, splitter=False), ""),
            ("interface Ethernet1/2/3.4", dict(idx=1, splitter=False), "interface Ethernet"),
            ("interface Ethernet1/2/3.4", dict(idx=2, splitter=False), "interface Ethernet1"),
            ("interface Ethernet1/2/3.4", dict(idx=3, splitter=False), "interface Ethernet1/2"),
            ("interface Ethernet1/2/3.4", dict(idx=4, splitter=False), "interface Ethernet1/2/3"),
            ("interface Ethernet1/2/3.4", dict(idx=5, splitter=False), "interface Ethernet1/2/3.4"),
            ("interface Ethernet1/2/3.4", dict(idx=6, splitter=False), "interface Ethernet1/2/3.4"),
        ]:
            obj = Intf(line)
            actual = obj.part_before(**kwargs)
            self.assertEqual(expected, actual, msg=f"{line=} {kwargs=}")

    # =========================== helpers ============================

    def test_valid__get_ids(self):
        """Intf._get_ids()"""
        for line, expected in [
            ("1", ("", "1", "", "", "")),
            ("1/2", ("", "1", "2", "", "")),
            ("port1", ("port", "1", "", "", "")),
            ("port1.2", ("port", "1", "2", "", "")),
            ("interface", ("interface", "", "", "", "")),
            ("interface Ethernet", ("interface Ethernet", "", "", "", "")),
            ("interface Ethernet1", ("interface Ethernet", "1", "", "", "")),
            ("interface Ethernet1/2", ("interface Ethernet", "1", "2", "", "")),
            ("interface Ethernet1/2/3", ("interface Ethernet", "1", "2", "3", "")),
            ("interface Ethernet1/2/3.4", ("interface Ethernet", "1", "2", "3", "4")),
            ("interface Ethernet1.2.3.4", ("interface Ethernet", "1", "2", "3", "4")),
            ("interface Ethernet1,2,3,4", ("interface Ethernet", "1", "2", "3", "4")),
            ("interface Ethernet1:2:3:4", ("interface Ethernet", "1", "2", "3", "4")),
        ]:
            obj = Intf(line)
            actual = obj._get_ids()
            self.assertEqual(expected, actual, msg=f"{line=}")


if __name__ == "__main__":
    unittest.main()
