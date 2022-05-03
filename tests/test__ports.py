"""unittest ports.py"""

import unittest

from netports import ports


class Test(unittest.TestCase):
    """unittest ports.py"""

    # ============================== ports ===============================

    def test_valid__iports(self):
        """iports()"""
        for items, req in [
            ("", []),
            (0, [0]),
            (b"1", [1]),
            ("0", [0]),
            ("1,1", [1]),
            ("1,2", [1, 2]),
            (" 1\t, 2\n", [1, 2]),
            ("1-1", [1]),
            ("1-2", [1, 2]),
            ("1-3", [1, 2, 3]),
            ("1,3-5", [1, 3, 4, 5]),
            ("1\t, \t3\t- 5\n", [1, 3, 4, 5]),
            ("3-5,1", [1, 3, 4, 5]),
            ("1,3-5,1,3-5", [1, 3, 4, 5]),

            ([], []),
            ([1], [1]),
            ([1, 1], [1]),
            (["1"], [1]),
            ({1: ""}, [1]),

            ([1, 2], [1, 2]),
            ({1, 2}, [1, 2]),
            ((1, 2), [1, 2]),
            ([2, 1], [1, 2]),
            ([5, 1, 3, 4, 5], [1, 3, 4, 5]),
        ]:
            result = ports.iports(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__iports(self):
        """iports()"""
        for items, error in [
            ("1-2-3", ValueError),
            ("1-a", ValueError),
            ("2-1", ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ports.iports(items)

    def test_valid__sports(self):
        """sports()"""
        for items, req in [
            ("", ""),
            (0, "0"),
            (b"1", "1"),
            (0.9, "0"),
            (1.9, "1"),
            ([], ""),
            ([1], "1"),
            (["1"], "1"),
            ({1: ""}, "1"),

            ([1, 2], "1-2"),
            ({1, 2}, "1-2"),
            ((1, 2), "1-2"),
            ([2, 1], "1-2"),
            ([1, 3, 4, 5], "1,3-5"),
            ([5, 1, 4, 3], "1,3-5"),
            (["1", 2.9, b"3"], "1-3"),

            ("1,3-5", "1,3-5"),
            (" 1\t , 3\t - 5\n", "1,3-5"),
            ("1,3-5,1,3-5", "1,3-5"),
        ]:
            result = ports.sports(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__sports(self):
        """sports()"""
        for items, error in [
            ([[1]], ValueError),
            (b"a", ValueError),
            ([{}], ValueError),
            ("1 3 to 5", ValueError),  # HP style
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ports.sports(items=items)

    # =============================== tcp ================================

    def test_valid__itcp(self):
        """itcp()"""
        for items, req in [
            ("", []),
            ([], []),
            (1, [1]),
            ([65535], [65535]),
            ([1, 3, 4, 5], [1, 3, 4, 5]),
            ("1,3-5", [1, 3, 4, 5]),
        ]:
            result = ports.itcp(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__itcp(self):
        """itcp()"""
        for items, error in [
            ("-1", ValueError),
            ("0", ValueError),
            ("65536", ValueError),
            ([0], ValueError),
            ([-1], ValueError),
            ([65536], ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ports.itcp(items)

    def test_valid__all_itcp(self):
        """all_itcp()"""
        result = ports.all_itcp()
        req = list(range(1, 65536))
        self.assertEqual(result, req, msg="all_itcp")

    def test_valid__stcp(self):
        """stcp()"""
        for items, req in [
            ("", ""),
            ([], ""),
            (1, "1"),
            ([65535], "65535"),
            ([1, 3, 4, 5], "1,3-5"),
            ("1,3-5", "1,3-5"),
        ]:
            result = ports.stcp(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__stcp(self):
        """stcp()"""
        for items, error in [
            ("-1", ValueError),
            ("0", ValueError),
            ("65536", ValueError),
            ([0], ValueError),
            ([-1], ValueError),
            ([65536], ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ports.stcp(items)

    def test_valid__all_stcp(self):
        """all_stcp()"""
        result = ports.all_stcp()
        req = "1-65535"
        self.assertEqual(result, req, msg="all_stcp")

    # =============================== vlan ===============================

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
            result = ports.ivlan(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_valid__ivlan_hpe(self):
        """ivlan_hpe()"""
        for items, req in [
            ([1, 3, 4, 5], [1, 3, 4, 5]),
            ("1 3 to 5", [1, 3, 4, 5]),
        ]:
            result = ports.ivlan_hpe(items)
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
                ports.ivlan(items)

    def test_valid__all_ivlan(self):
        """all_ivlan()"""
        result = ports.all_ivlan()
        req = list(range(1, 4095))
        self.assertEqual(result, req, msg="all_ivlan")

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
            result = ports.svlan(**kwargs)
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
                ports.svlan(items)

    def test_valid__svlan_hpe(self):
        """svlan_hpe()"""
        for items, req in [
            ([1, 3, 4, 5], "1 3 to 5"),
            ("1 3 to 5", "1 3 to 5"),
        ]:
            result = ports.svlan_hpe(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__all_svlan(self):
        """all_svlan()"""
        result = ports.all_svlan()
        req = "1-4094"
        self.assertEqual(result, req, msg="all_svlan")


if __name__ == "__main__":
    unittest.main()
