"""unittest interface.py"""

import unittest

from netports.interface4 import Interface4
from tests.helpers_test import Helpers


# noinspection DuplicatedCode
class Test(Helpers):
    """Interface"""

    # ========================== redefined ===========================

    def test_valid__hash__(self):
        """Interface.__hash__()"""
        intf1 = "interface Ethernet1/2/3.4"
        intf_o = Interface4(intf1)
        result = intf_o.__hash__()
        req = hash(("interface Ethernet", 1, 2, 3, 4))
        self.assertEqual(result, req, msg=f"{intf1=}")

    def test_valid__eq__(self):
        """Interface.__eq__() __ne__()"""
        intf1 = "interface Ethernet1/2/3.4"
        intf_o = Interface4(intf1)
        for other_o, req, in [
            (Interface4(intf1), True),
            (Interface4("interface Ethernet1.2.3.4"), True),
            (Interface4("interface Ethernet1/1"), False),
        ]:
            result = intf_o.__eq__(other_o)
            self.assertEqual(result, req, msg=f"{intf_o =} {other_o=}")
            result = intf_o.__ne__(other_o)
            self.assertEqual(result, not req, msg=f"{intf_o =} {other_o=}")

    def test_valid__lt__(self):
        """Interface.__lt__() __le__() __gt__() __ge__()"""
        intf1 = "interface Eth1/2/3.4"
        for intf_o, other_o, req_lt, req_le, req_gt, req_ge in [
            (Interface4(intf1), intf1, False, False, True, True),
            (Interface4(intf1), Interface4("1"), False, False, True, True),
            (Interface4(intf1), Interface4("a 9"), False, False, True, True),
            (Interface4(intf1), Interface4("z 0"), True, True, False, False),
            (Interface4(intf1), Interface4("interface Eth"), False, False, True, True),
            (Interface4(intf1), Interface4("interface Eth1"), False, False, True, True),
            (Interface4(intf1), Interface4("interface Eth1/2"), False, False, True, True),
            (Interface4(intf1), Interface4("interface Eth1/2/3"), False, False, True, True),
            (Interface4(intf1), Interface4(intf1), False, True, False, True),
            (Interface4(intf1), Interface4("interface Eth1.2.3.4"), False, True, False, True),
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
        """Ace.__lt__(), Ace.__le__()"""
        intf1 = "interface Ethernet1/2/3.4"
        for items in [
            [intf1, Interface4(intf1)],
            [Interface4(intf1), Interface4(intf1)],
            [Interface4("1"), Interface4(intf1)],
            [Interface4("a 9"), Interface4(intf1)],
            [Interface4("interface Ethernet"), Interface4(intf1)],
            [Interface4("interface Ethernet1"), Interface4(intf1)],
            [Interface4(intf1), Interface4("interface Ethernet2")],
            [Interface4("interface Ethernet1/1"), Interface4(intf1)],
            [Interface4("interface Ethernet1/2"), Interface4(intf1)],
            [Interface4(intf1), Interface4("interface Ethernet1/3")],
            [Interface4("interface Ethernet1/2/1"), Interface4(intf1)],
            [Interface4("interface Ethernet1/2/3"), Interface4(intf1)],
            [Interface4(intf1), Interface4("interface Ethernet1/2/4")],
            [Interface4("interface Ethernet1/2/3.1"), Interface4(intf1)],
            [Interface4("interface Ethernet1/2/3.4"), Interface4(intf1)],
            [Interface4(intf1), Interface4("interface Ethernet1/2/3.5")],
            [Interface4("interface Ethernet1.2.3.1"), Interface4(intf1)],
            [Interface4("interface Ethernet1.2.3.4"), Interface4(intf1)],
            [Interface4(intf1), Interface4("interface Ethernet1.2.3.5")],
        ]:
            req = items.copy()
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")
            items[0], items[1] = items[1], items[0]
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")

    # =========================== property ===========================

    def test_valid__line(self):
        """Interface.line"""
        intf = "interface Ethernet"
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
            (dict(line=f"{intf}1"), dict(line=f"{intf}1", name="Ethernet1",
                                         id0=intf, id1=1, id2=0, id3=0, id4=0)),
            (dict(line=f"{intf}1/2"), dict(line=f"{intf}1/2", name="Ethernet1/2",
                                           id0=intf, id1=1, id2=2, id3=0, id4=0)),
            (dict(line=f"{intf}1/2/3"), dict(line=f"{intf}1/2/3", name="Ethernet1/2/3",
                                             id0=intf, id1=1, id2=2, id3=3, id4=0)),
            (dict(line=f"{intf}1/2/3.4"), dict(line=f"{intf}1/2/3.4", name="Ethernet1/2/3.4",
                                               id0=intf, id1=1, id2=2, id3=3, id4=4)),
            (dict(line=f"{intf}1.2.3.4"), dict(line=f"{intf}1.2.3.4", name="Ethernet1.2.3.4",
                                               id0=intf, id1=1, id2=2, id3=3, id4=4)),
            (dict(line=f"{intf}1,2,3,4"), dict(line=f"{intf}1,2,3,4", name="Ethernet1,2,3,4",
                                               id0=intf, id1=1, id2=2, id3=3, id4=4)),
            (dict(line=f"{intf}1:2:3:4"), dict(line=f"{intf}1:2:3:4", name="Ethernet1:2:3:4",
                                               id0=intf, id1=1, id2=2, id3=3, id4=4)),
            (dict(line=f"{intf}1-2-3-4", splitter="-"), dict(line=f"{intf}1-2-3-4",
                                                             name="Ethernet1-2-3-4",
                                                             id0=intf, id1=1, id2=2, id3=3, id4=4)),
        ]:
            # getter
            intf_o = Interface4(**kwargs)
            self._test_attrs(obj=intf_o, req_d=req_d, msg=f"getter {kwargs=}")
            # setter
            intf_o.line = kwargs["line"]
            self._test_attrs(obj=intf_o, req_d=req_d, msg=f"setter {kwargs=}")
        # deleter
        with self.assertRaises(AttributeError, msg="deleter line"):
            # noinspection PyPropertyAccess
            del intf_o.line

    # =========================== helpers ============================

    def test_valid__parse_interface(self):
        """Interface._parse_interface()"""
        intf_o = Interface4()
        for interface, req in [
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
            result = intf_o._parse_interface(interface)
            self.assertEqual(result, req, msg=f"{interface=}")


if __name__ == "__main__":
    unittest.main()
