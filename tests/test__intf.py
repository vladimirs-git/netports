"""unittest intfs.py"""

import unittest

from netports.intf import Intf
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

    def test_valid__line(self):
        """Intf.line"""
        id0 = "interface Ethernet"
        exp1 = dict(line=f"{id0}1", name="Ethernet1", id0=id0, id1=1, id2=0, id3=0, id4=0)
        exp2 = dict(line=f"{id0}1/2", name="Ethernet1/2", id0=id0, id1=1, id2=2, id3=0, id4=0)
        exp3 = dict(line=f"{id0}1/2/3", name="Ethernet1/2/3", id0=id0, id1=1, id2=2, id3=3, id4=0)
        exp4 = dict(line=f"{id0}1/2/3.4", name="Ethernet1/2/3.4",
                    id0=id0, id1=1, id2=2, id3=3, id4=4)
        exp5 = dict(line=f"{id0}1.2.3.4", name="Ethernet1.2.3.4",
                    id0=id0, id1=1, id2=2, id3=3, id4=4)
        exp6 = dict(line=f"{id0}1,2,3,4", name="Ethernet1,2,3,4",
                    id0=id0, id1=1, id2=2, id3=3, id4=4)
        exp7 = dict(line=f"{id0}1:2:3:4", name="Ethernet1:2:3:4",
                    id0=id0, id1=1, id2=2, id3=3, id4=4)
        exp8 = dict(line=f"{id0}1-2-3-4", name="Ethernet1-2-3-4",
                    id0=id0, id1=1, id2=2, id3=3, id4=4)
        for kwargs, exp_d in [
            (dict(line=""), dict(line="", name="", id0="", id1=0, id2=0, id3=0, id4=0)),
            (dict(line="1"), dict(line="1", name="1", id0="", id1=1, id2=0, id3=0, id4=0)),
            (dict(line="1/2"), dict(line="1/2", name="1/2", id0="", id1=1, id2=2, id3=0, id4=0)),
            (dict(line="port1"), dict(line="port1", name="port1", id0="port",
                                      id1=1, id2=0, id3=0, id4=0)),
            (dict(line="port1.2"), dict(line="port1.2", name="port1.2",
                                        id0="port", id1=1, id2=2, id3=0, id4=0)),
            (dict(line="text"), dict(line="text", name="text",
                                     id0="text", id1=0, id2=0, id3=0, id4=0)),
            (dict(line=id0), dict(line=id0, name="Ethernet",
                                  id0=id0, id1=0, id2=0, id3=0, id4=0)),
            (dict(line=f"{id0}1"), exp1),
            (dict(line=f"{id0}1/2"), exp2),
            (dict(line=f"{id0}1/2/3"), exp3),
            (dict(line=f"{id0}1/2/3.4"), exp4),
            (dict(line=f"{id0}1/2/3.4-5"), exp4),
            (dict(line=f"{id0}1/2/3.4text"), exp4),
            (dict(line=f"{id0}1.2.3.4"), exp5),
            (dict(line=f"{id0}1,2,3,4"), exp6),
            (dict(line=f"{id0}1:2:3:4"), exp7),
            (dict(line=f"{id0}1-2-3-4", splitter="-"), exp8),
        ]:
            intf_o = Intf(**kwargs)
            self._test_attrs(obj=intf_o, exp_d=exp_d, msg=f"{kwargs=}")

    # =========================== methods ============================

    def test_valid__all_names(self):
        """Intf.all_names()"""
        all_eth = [
            "interface Ethernet1/2",
            "interface ethernet1/2",
            "interface Eth1/2",
            "interface eth1/2",
            "Ethernet1/2",
            "ethernet1/2",
            "Eth1/2",
            "eth1/2",
        ]
        all_tun_ip = [
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
        all_tun = [
            "interface Tunnel1",
            "interface tunnel1",
            "interface Tu1",
            "interface tu1",
            "Tunnel1",
            "tunnel1",
            "Tu1",
            "tu1",
        ]
        all_mgmt = [
            "interface mgmt0",
            "mgmt0",
        ]
        all_1 = [
            "interface 1",
            "1",
        ]
        for line, expected in [
            ("interface Ethernet1/2", all_eth),
            ("Eth1/2", all_eth),
            ("interface Tunnel-ip1", all_tun_ip),
            ("Tunnel1", all_tun),
            ("interface mgmt0", all_mgmt),
            ("mgmt0", all_mgmt),
            ("1", all_1),
        ]:
            obj = Intf(line)
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
            # ("interface Tunnel-ip1", "interface Tunnel-ip1"),  # TODO platform
            ("interface Vlan1", "interface Vlan1"),
            # long to full
            ("interface Ethernet1/2/3.4", "interface Ethernet1/2/3.4"),
            ("interface FastEthernet1/2", "interface FastEthernet1/2"),
            ("interface GigabitEthernet1/2", "interface GigabitEthernet1/2"),
            ("interface TenGigabitEthernet1/2", "interface TenGigabitEthernet1/2"),
            ("interface Loopback0", "interface Loopback0"),
            ("interface Port-channel100", "interface Port-channel100"),
            ("interface Tunnel1", "interface Tunnel1"),
            # ("interface Tunnel-ip1", "interface Tunnel-ip1"),  # TODO platform
            ("interface Vlan1", "interface Vlan1"),
            # short to full
            ("Eth1/2/3.4", "interface Ethernet1/2/3.4"),
            ("Fa1/2", "interface FastEthernet1/2"),
            ("Gi1/2", "interface GigabitEthernet1/2"),
            ("Te1/2", "interface TenGigabitEthernet1/2"),
            ("Lo0", "interface Loopback0"),
            ("Po100", "interface Port-channel100"),
            ("Tu1", "interface Tunnel1"),
            # ("Tu1", "interface Tunnel-ip1"),  # TODO platform
            ("Vl1", "interface Vlan1"),
            ("V1", "interface Vlan1"),
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

    def test_valid__name_long(self):  # TODO
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
            # ("interface Tunnel-ip1", "Tunnel-ip1"),  # TODO platform
            ("interface Vlan1", "Vlan1"),
            # long to long
            ("interface Ethernet1/2/3.4", "Ethernet1/2/3.4"),
            ("interface FastEthernet1/2", "FastEthernet1/2"),
            ("interface GigabitEthernet1/2", "GigabitEthernet1/2"),
            ("interface TenGigabitEthernet1/2", "TenGigabitEthernet1/2"),
            ("interface Loopback0", "Loopback0"),
            ("interface Port-channel100", "Port-channel100"),
            ("interface Tunnel1", "Tunnel1"),
            # ("interface Tunnel-ip1", "Tunnel-ip1"),  # TODO platform
            ("interface Vlan1", "Vlan1"),
            # short to long
            ("Eth1/2/3.4", "Ethernet1/2/3.4"),
            ("Fa1/2", "FastEthernet1/2"),
            ("Gi1/2", "GigabitEthernet1/2"),
            ("Te1/2", "TenGigabitEthernet1/2"),
            ("Lo0", "Loopback0"),
            ("Po100", "Port-channel100"),
            ("Tu1", "Tunnel1"),
            # ("Tu1", "Tunnel-ip1"),  # TODO platform
            ("Vl1", "Vlan1"),
            ("V1", "Vlan1"),
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
            # ("interface Tunnel-ip1", "Tu1"),  # TODO platform
            ("interface Vlan1", "V1"),
            # long to short
            ("Ethernet1/2/3.4", "Eth1/2/3.4"),
            ("FastEthernet1/2", "Fa1/2"),
            ("GigabitEthernet1/2", "Gi1/2"),
            ("TenGigabitEthernet1/2", "Te1/2"),
            ("Loopback0", "Lo0"),
            ("Port-channel100", "Po100"),
            ("Tunnel1", "Tu1"),
            # ("Tunnel-ip1", "Tu1"),  # TODO platform
            ("Vlan1", "V1"),
            # short to short
            ("Eth1/2/3.4", "Eth1/2/3.4"),
            ("Fa1/2", "Fa1/2"),
            ("Gi1/2", "Gi1/2"),
            ("Te1/2", "Te1/2"),
            ("Lo0", "Lo0"),
            ("Po100", "Po100"),
            ("Tu1", "Tu1"),
            # ("Tu1", "Tu1"),  # TODO platform
            ("Vl1", "V1"),
            ("V1", "V1"),
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
