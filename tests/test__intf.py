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
        result = intf_o.__hash__()
        req = hash(("interface Ethernet", 1, 2, 3, 4))
        self.assertEqual(result, req, msg=f"{intf1=}")

    def test_valid__eq__(self):
        """Intf.__eq__() __ne__()"""
        intf1 = "interface Ethernet1/2/3.4"
        intf_o = Intf(intf1)
        for other_o, req, in [
            (Intf(intf1), True),
            (Intf("interface Ethernet1.2.3.4"), True),
            (Intf("interface Ethernet1/1"), False),
        ]:
            result = intf_o.__eq__(other_o)
            self.assertEqual(result, req, msg=f"{intf_o=} {other_o=}")
            result = intf_o.__ne__(other_o)
            self.assertEqual(result, not req, msg=f"{intf_o=} {other_o=}")

    def test_valid__lt__(self):
        """Intf.__lt__() __le__() __gt__() __ge__()"""
        intf1 = "interface Eth1/2/3.4"
        for intf_o, other_o, req_lt, req_le, req_gt, req_ge in [
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
            result = intf_o.__lt__(other_o)
            self.assertEqual(result, req_lt, msg=f"{intf_o=} {other_o=}")
            result = intf_o.__le__(other_o)
            self.assertEqual(result, req_le, msg=f"{intf_o=} {other_o=}")
            result = intf_o.__gt__(other_o)
            self.assertEqual(result, req_gt, msg=f"{intf_o=} {other_o=}")
            result = intf_o.__ge__(other_o)
            self.assertEqual(result, req_ge, msg=f"{intf_o=} {other_o=}")

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
            req = items.copy()
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")
            items[0], items[1] = items[1], items[0]
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")

    # =========================== property ===========================

    def test_valid__line(self):
        """Intf.line"""
        intf = "interface Ethernet"
        req1 = dict(line=f"{intf}1", name="Ethernet1", id0=intf, id1=1, id2=0, id3=0, id4=0)
        req2 = dict(line=f"{intf}1/2", name="Ethernet1/2", id0=intf, id1=1, id2=2, id3=0, id4=0)
        req3 = dict(line=f"{intf}1/2/3", name="Ethernet1/2/3", id0=intf, id1=1, id2=2, id3=3, id4=0)
        req4 = dict(line=f"{intf}1/2/3.4", name="Ethernet1/2/3.4",
                    id0=intf, id1=1, id2=2, id3=3, id4=4)
        req5 = dict(line=f"{intf}1.2.3.4", name="Ethernet1.2.3.4",
                    id0=intf, id1=1, id2=2, id3=3, id4=4)
        req6 = dict(line=f"{intf}1,2,3,4", name="Ethernet1,2,3,4",
                    id0=intf, id1=1, id2=2, id3=3, id4=4)
        req7 = dict(line=f"{intf}1:2:3:4", name="Ethernet1:2:3:4",
                    id0=intf, id1=1, id2=2, id3=3, id4=4)
        req8 = dict(line=f"{intf}1-2-3-4", name="Ethernet1-2-3-4",
                    id0=intf, id1=1, id2=2, id3=3, id4=4)
        for kwargs, req_d in [
            (dict(line=""), dict(line="", name="", id0="", id1=0, id2=0, id3=0, id4=0)),
            (dict(line="1"), dict(line="1", name="1", id0="", id1=1, id2=0, id3=0, id4=0)),
            (dict(line="1/2"), dict(line="1/2", name="1/2", id0="", id1=1, id2=2, id3=0, id4=0)),
            (dict(line="port1"), dict(line="port1", name="port1", id0="port",
                                      id1=1, id2=0, id3=0, id4=0)),
            (dict(line="port1.2"), dict(line="port1.2", name="port1.2",
                                        id0="port", id1=1, id2=2, id3=0, id4=0)),
            (dict(line="text"), dict(line="text", name="text",
                                     id0="text", id1=0, id2=0, id3=0, id4=0)),
            (dict(line=intf), dict(line=intf, name="Ethernet",
                                   id0=intf, id1=0, id2=0, id3=0, id4=0)),
            (dict(line=f"{intf}1"), req1),
            (dict(line=f"{intf}1/2"), req2),
            (dict(line=f"{intf}1/2/3"), req3),
            (dict(line=f"{intf}1/2/3.4"), req4),
            (dict(line=f"{intf}1/2/3.4-5"), req4),
            (dict(line=f"{intf}1/2/3.4text"), req4),
            (dict(line=f"{intf}1.2.3.4"), req5),
            (dict(line=f"{intf}1,2,3,4"), req6),
            (dict(line=f"{intf}1:2:3:4"), req7),
            # (dict(line=f"{intf}1-2-3-4", splitter="-"), req8),
        ]:
            intf_o = Intf(**kwargs)
            self._test_attrs(obj=intf_o, req_d=req_d, msg=f"{kwargs=}")

    def test_name_short(self):
        """Intf.name_short"""
        for line, req in [
            ("interface Ethernet1/2/3.4", "Eth1/2/3.4"),
            ("interface FastEthernet1/2", "Fa1/2"),
            ("interface fastethernet1/2", "Fa1/2"),
            ("interface GigabitEthernet1/2", "Gi1/2"),
            ("interface TenGigabitEthernet1/2", "Te1/2"),
            ("interface Loopback0", "Lo0"),
            ("interface Port-channel100", "Po100"),
            ("interface Tunnel1", "Tu1"),
            ("interface Tunnel-ip1", "Tu1"),
            ("interface Vlan1", "Vl1"),
        ]:
            obj = Intf(line)
            result = obj.name_short
            self.assertEqual(result, req, msg=f"{line=}")

    # =========================== methods ============================

    def test_last_idx(self):
        """Intf.last_idx()"""
        for line, req in [
            ("", 0),
            ("Ethernet", 0),
            ("Ethernet1", 1),
            ("Ethernet1/2", 2),
            ("Ethernet1/2/3", 3),
            ("Ethernet1/2/3.4", 4),
            ("Ethernet1/2/3.4-5", 4),
        ]:
            obj = Intf(line)
            result = obj.last_idx()
            self.assertEqual(result, req, msg=f"{line=}")

    def test_names(self):
        """Intf.name_short()"""
        for line, req in [
            ("interface Ethernet1/2/3.4",
             ["interface Ethernet1/2/3.4", "Ethernet1/2/3.4", "Eth1/2/3.4"]),
            ("interface Port-channel100",
             ["interface Port-channel100", "Port-channel100", "Po100"]),
        ]:
            obj = Intf(line)
            result = obj.names()
            self.assertEqual(result, req, msg=f"{line=}")

    def test_valid__parts(self):
        """Intf.parts()"""
        for line, idx, req in [
            ("", -1, ""),
            ("", 0, ""),
            ("", 1, ""),
            ("1", 1, ""),
            ("1", 2, "1"),
            ("1/2", 1, ""),
            ("1/2", 2, "1/"),
            ("1/2", 3, "1/2"),
            # port1
            ("port1", 1, "port"),
            ("port1", 2, "port1"),
            # port1.2
            ("port1.2", 1, "port"),
            ("port1.2", 2, "port1."),
            ("port1.2", 3, "port1.2"),
            # interface Ethernet1/2
            ("interface Ethernet1/2", 1, "interface Ethernet"),
            ("interface Ethernet1/2", 2, "interface Ethernet1/"),
            ("interface Ethernet1/2", 3, "interface Ethernet1/2"),
            # interface Ethernet1/2/3.4
            ("interface Ethernet1/2/3.4", -1, ""),
            ("interface Ethernet1/2/3.4", 0, ""),
            ("interface Ethernet1/2/3.4", 1, "interface Ethernet"),
            ("interface Ethernet1/2/3.4", 2, "interface Ethernet1/"),
            ("interface Ethernet1/2/3.4", 3, "interface Ethernet1/2/"),
            ("interface Ethernet1/2/3.4", 4, "interface Ethernet1/2/3."),
            ("interface Ethernet1/2/3.4", 5, "interface Ethernet1/2/3.4"),
            ("interface Ethernet1/2/3.4", 6, "interface Ethernet1/2/3.4"),
        ]:
            obj = Intf(line)
            result = obj.part(idx)
            self.assertEqual(result, req, msg=f"{line=}")

    # =========================== helpers ============================

    def test_valid__get_ids(self):
        """Intf._get_ids()"""

        for line, req in [
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
            result = obj._get_ids()
            self.assertEqual(result, req, msg=f"{line=}")


if __name__ == "__main__":
    unittest.main()
