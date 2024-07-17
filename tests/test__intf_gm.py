"""Tests intf_gm.py"""

import random
import unittest

from netports.intf import Intf
from netports.intf_gm import IntfGM
from tests.helpers_ import Helpers


# noinspection DuplicatedCode
class Test(Helpers):
    """IntfGM"""

    # =========================== property ===========================

    def test_valid__items(self):
        """IntfGM.items"""
        for items, req in [
            (None, []),
            ("", []),
            ([], []),
            ("p1", ["p1"]),
            (["p1", "p2"], ["p1", "p2"]),
            (("p1", "p2"), ["p1", "p2"]),
            ({"p1", "p2"}, ["p1", "p2"]),
            (["p2", "p1"], ["p1", "p2"]),  # unsorted
            (Intf("p1"), ["p1"]),
            ([Intf("p1"), Intf("p2")], ["p1", "p2"]),
        ]:
            obj = IntfGM(items=items)
            result = [str(o) for o in obj.items]
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__items(self):
        """IntfGM.items"""
        for items, error in [
            (1, TypeError),
            ([1], TypeError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                IntfGM(items=items)

    def test_valid__range(self):
        """IntfGM.range()"""
        intfs = ["interface Ethernet1", "interface Ethernet2", "interface Ethernet3",
                 "interface Ethernet1/4", "interface Ethernet1/5", "interface Ethernet1/6"]
        long = ["interface Ethernet1-3", "interface Ethernet1/4-6"]
        short = ["Eth1-3", "Eth1/4-6"]
        for fmt, items, req in [
            ("long", intfs, long),
            ("short", intfs, short),
        ]:
            obj = IntfGM(items)
            random.shuffle(obj.items)
            result = obj.ranges(fmt=fmt)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__range(self):
        """IntfGM.range"""
        for fmt, error in [
            ("typo", ValueError),
        ]:
            obj = IntfGM("p1")
            with self.assertRaises(error, msg=f"{fmt=}"):
                obj.ranges(fmt=fmt)

    def test_valid__ranges__long(self):
        """IntfGM._ranges__long()"""
        ports1 = ["p1/1", "p1/2", "p1/3", "p1/5", "p1/6", "p1/7", "p1/9",
                  "p2/1", "p2/2", "p2/3", "p2/5", "p2/6", "p2/7", "p2/9"]
        ports2 = ["p1", "p2", "p3", "p1/1", "p1/2", "p1/3",
                  "p1/2.3", "p1/2.4", "p1/2.5", "p1/2.7",
                  "p2/3.4", "p2/3.6", "p2/3.7", "p2/3.8"]
        for items, req in [
            ([], []),
            (["p1"], ["p1"]),
            (["p1", "p2"], ["p1-2"]),
            (["p1", "p2", "p3"], ["p1-3"]),
            (["p1", "p2", "p3", "p5"], ["p1-3", "p5"]),
            (["interface Ethernet1", "interface Ethernet2"], ["interface Ethernet1-2"]),
            (["p1", "p2", "p3", "p5", "p6", "p7", "p9"], ["p1-3", "p5-7", "p9"]),
            (ports1, ["p1/1-3", "p1/5-7", "p1/9", "p2/1-3", "p2/5-7", "p2/9"]),
            (ports2, ["p1-3", "p1/1-3", "p1/2.3-5", "p1/2.7", "p2/3.4", "p2/3.6-8"]),
        ]:
            obj = IntfGM(items)
            random.shuffle(obj.items)
            result = obj._ranges__long()
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__ranges__short(self):
        """IntfGM._ranges__short()"""
        eth0 = ["interface Ethernet1", "interface Ethernet2",
                "interface Ethernet3", "interface Ethernet5"]
        eth1 = ["interface FastEthernet1/2/3.4", "interface FastEthernet1/2/3.5",
                "interface FastEthernet1/2/3.6", "interface FastEthernet1/2/3.8"]
        for items, req in [
            (eth0, ["Eth1-3", "Eth5"]),
            (eth1, ["Fa1/2/3.4-6", "Fa1/2/3.8"]),
        ]:
            obj = IntfGM(items)
            random.shuffle(obj.items)
            result = obj._ranges__short()
            self.assertEqual(result, req, msg=f"{items=}")


if __name__ == "__main__":
    unittest.main()
