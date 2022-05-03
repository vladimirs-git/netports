"""unittest vlan.py"""

import unittest

import dictdiffer  # type: ignore

from netports import vlan

ALL_VLANS = list(range(1, 4095))


class Test(unittest.TestCase):
    """unittest vlan.py"""

    def test_valid__ivlan(self):
        """ivlan()"""
        for kwargs, req in [
            (dict(), []),
            (dict(items=""), []),
            (dict(items=[]), []),
            (dict(items=1), [1]),
            (dict(items="1"), [1]),
            (dict(items=[1]), [1]),
            (dict(items=[4094]), [4094]),
            (dict(items=[5, 5, 1, 3, 4]), [1, 3, 4, 5]),
            (dict(items="3-5,1,3-5,1"), [1, 3, 4, 5]),
            (dict(all=True), ALL_VLANS),
            (dict(items="1", all=True), ALL_VLANS),
            (dict(items="1,3-5", platform="cisco"), [1, 3, 4, 5]),
            (dict(items="1 3 to 5", platform="hpe"), [1, 3, 4, 5]),
            (dict(items="1,3-5", splitter=",", range_splitter="-"), [1, 3, 4, 5]),
            (dict(items="1 3 to 5", splitter=" ", range_splitter=" to "), [1, 3, 4, 5]),
        ]:
            result = vlan.ivlan(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_invalid__ivlan(self):
        """ivlan()"""
        for kwargs, error in [
            (dict(items="-1"), ValueError),
            (dict(items="0"), ValueError),
            (dict(items="4095"), ValueError),
            (dict(items=[0]), ValueError),
            (dict(items=[-1]), ValueError),
            (dict(items=[4095]), ValueError),
            (dict(items="1,3-5", platform="hpe"), ValueError),
            (dict(items="1 3 to 5", platform="cisco"), ValueError),
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                vlan.ivlan(**kwargs)

    def test_valid__svlan(self):
        """svlan()"""
        for kwargs, req in [
            (dict(), ""),
            (dict(items=""), ""),
            (dict(items=[]), ""),
            (dict(items=1), "1"),
            (dict(items="1"), "1"),
            (dict(items=[1]), "1"),
            (dict(items=[4094]), "4094"),
            (dict(items=[5, 5, 1, 3, 4]), "1,3-5"),
            (dict(items="3-5,1,3-5,1"), "1,3-5"),
            (dict(items=[1, 3, 4, 5], platform="cisco"), "1,3-5"),
            (dict(items=[1, 3, 4, 5], platform="hpe"), "1 3 to 5"),
            (dict(items=[1, 3, 4, 5], splitter=",", range_splitter="-"), "1,3-5"),
            (dict(items=[1, 3, 4, 5], splitter=" ", range_splitter=" to "), "1 3 to 5"),
        ]:
            result = vlan.svlan(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_invalid__svlan(self):
        """svlan()"""
        for items, error in [
            ("-1", ValueError),
            ("0", ValueError),
            ("4095", ValueError),
            ([0], ValueError),
            ([-1], ValueError),
            ([4095], ValueError),
            (dict(items="1,3-5", platform="hpe"), ValueError),
            (dict(items="1 3 to 5", platform="cisco"), ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                vlan.svlan(items)

    # =========================== helpers ============================

    def test_valid__update_splitters(self):
        """_update_splitters()"""
        for kwargs, req_d in [
            (dict(), dict()),
            (dict(splitter="a", range_splitter="a"), dict(splitter="a", range_splitter="a")),
            (dict(platform="cisco"), dict(platform="cisco", splitter=",", range_splitter="-")),
            (dict(platform="cisco", splitter="a", range_splitter="a"),
             dict(platform="cisco", splitter=",", range_splitter="-")),
            (dict(platform="hpe", splitter="a", range_splitter="a"),
             dict(platform="hpe", splitter=" ", range_splitter=" to ")),
        ]:
            result = vlan._update_splitters(**kwargs)
            diff = list(dictdiffer.diff(first=result, second=req_d))
            self.assertEqual(diff, [], msg=f"{kwargs=}")


if __name__ == "__main__":
    unittest.main()
