"""unittest vlan.py"""

import unittest

from netports import vlan


class Test(unittest.TestCase):
    """unittest vlan.py"""

    def test_valid__ivlan(self):
        """ivlan()"""
        for kwargs, req in [
            (dict(items=""), []),
            (dict(items=[]), []),
            (dict(items=1), [1]),
            (dict(items=[4094]), [4094]),
            (dict(items=[1, 3, 4, 5]), [1, 3, 4, 5]),
            (dict(items="1,3-5"), [1, 3, 4, 5]),
            (dict(items="1,3-5", splitter=",", range_splitter="-"), [1, 3, 4, 5]),
            (dict(items="1 3 to 5", splitter=" ", range_splitter=" to "), [1, 3, 4, 5]),
        ]:
            result = vlan.ivlan(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_valid__ivlan_hpe(self):
        """ivlan_hpe()"""
        for items, req in [
            ([1, 3, 4, 5], [1, 3, 4, 5]),
            ("1 3 to 5", [1, 3, 4, 5]),
        ]:
            result = vlan.ivlan_hpe(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__ivlan(self):
        """ivlan()"""
        for items, error in [
            ("-1", ValueError),
            ("0", ValueError),
            ("4095", ValueError),
            ([0], ValueError),
            ([-1], ValueError),
            ([4095], ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                vlan.ivlan(items)

    def test_valid__ivlan_all(self):
        """ivlan_all()"""
        result = vlan.ivlan_all()
        req = list(range(1, 4095))
        self.assertEqual(result, req, msg="ivlan_all")

    def test_valid__svlan(self):
        """svlan()"""
        for kwargs, req in [
            (dict(items=""), ""),
            (dict(items=[]), ""),
            (dict(items=1), "1"),
            (dict(items=[4094]), "4094"),
            (dict(items=[1, 3, 4, 5]), "1,3-5"),
            (dict(items="1,3-5"), "1,3-5"),
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
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                vlan.svlan(items)

    def test_valid__svlan_hpe(self):
        """svlan_hpe()"""
        for items, req in [
            ([1, 3, 4, 5], "1 3 to 5"),
            ("1 3 to 5", "1 3 to 5"),
        ]:
            result = vlan.svlan_hpe(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__svlan_all(self):
        """svlan_all()"""
        result = vlan.svlan_all()
        req = "1-4094"
        self.assertEqual(result, req, msg="svlan_all")


if __name__ == "__main__":
    unittest.main()
