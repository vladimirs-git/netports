"""unittest helpers.py"""

import unittest

from netports import helpers as h


class Test(unittest.TestCase):
    """unittest helpers.py"""

    # ============================= str ==============================

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

    # ============================= list =============================

    def test_valid__lstr(self):
        """lstr()"""
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
            result = h.lstr(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__lstr(self):
        """lstr()"""
        for items, error in [
            (str, TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.lstr(items=items)

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

    # ============================= int ==============================

    def test_valid__to_int(self):
        """to_int()"""
        for number, req in [
            (0, 0),
            ("0", 0),
        ]:
            result = h.to_int(number)
            self.assertEqual(result, req, msg=f"{number=}")

    def test_invalid__to_int(self):
        """to_int()"""
        for number, error in [
            ("a", TypeError),
            ("-1", TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.to_int(number)

    def test_valid__to_lint(self):
        """to_lint()"""
        for numbers, req in [
            ([0, 1, "2"], [0, 1, 2]),
        ]:
            result = h.to_lint(numbers)
            self.assertEqual(result, req, msg=f"{numbers=}")

    def test_invalid__to_lint(self):
        """to_lint()"""
        for numbers, error in [
            (1, TypeError),
            (["a"], TypeError),
            (["-1"], TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.to_lint(numbers)


if __name__ == "__main__":
    unittest.main()
