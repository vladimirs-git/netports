"""Tests ports.py"""

import unittest

from netports import ports, NetportsValueError


class Test(unittest.TestCase):
    """Tests ports.py"""

    def test_valid__inumbers(self):
        """inumbers()"""
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
            result = ports.inumbers(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__inumbers(self):
        """inumbers()"""
        for items, error in [
            ("1-2-3", NetportsValueError),
            ("1-a", NetportsValueError),
            ("2-1", NetportsValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ports.inumbers(items)

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
            result = ports.snumbers(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__sports(self):
        """sports()"""
        for items, error in [
            ([[1]], NetportsValueError),
            (b"a", NetportsValueError),
            ([{}], NetportsValueError),
            ("1 3 to 5", NetportsValueError),  # HP style
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ports.snumbers(items=items)


if __name__ == "__main__":
    unittest.main()
