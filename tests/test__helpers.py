"""unittest helpers.py"""

import unittest

from netports import helpers as h


class Test(unittest.TestCase):
    """unittest helpers.py"""

    def test_valid__join(self):
        """join()"""
        for items, req in [
            ([], ""),
            (["0", "1"], "0,1"),
            ([0, 1], "0,1"),
            ([[1]], "[1]"),
        ]:
            result = h.join(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__list_of_str(self):
        """list_of_str()"""
        for items, req in [
            ("", [""]),
            ("1,3-5", ["1,3-5"]),
            (0, ["0"]),
            (1, ["1"]),
            (b"1", ["1"]),
            (0.9, ["0"]),
            (0.5, ["0"]),
            (1.9, ["1"]),
            ([], []),
            ([0, 1, 1.5, "1.5", "2-4"], ["0", "1", "1", "1.5", "2-4"]),
            ((0, 1), ["0", "1"]),
            ({0: "", 1: ""}, ["0", "1"]),
            ([[1]], ["[1]"]),
        ]:
            result = h.list_of_str(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__list_of_str(self):
        """list_of_str()"""
        for items, error in [
            (str, TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.list_of_str(items=items)

    def test_valid__split(self):
        """split()"""
        for items, req in [
            ("", []),
            ("1,3-5,a", ["1", "3-5", "a"]),
            (0, ["0"]),
            (1, ["1"]),
            (b"1", ["1"]),
            (0.9, ["0"]),
            (0.5, ["0"]),
            (1.9, ["1"]),
            ([], []),
            ([0, 1.5, "1.5", "2-4", "a", "b,c"], ["0", "1", "1.5", "2-4", "a", "b", "c"]),
            ((0, 1), ["0", "1"]),
            ({0: "", 1: ""}, ["0", "1"]),
            ([[1]], ["[1]"]),
        ]:
            result = h.split(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__split(self):
        """split()"""
        for items, error in [
            (str, TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.split(items=items)


if __name__ == "__main__":
    unittest.main()
