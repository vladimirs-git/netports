"""unittest ports.py"""

import unittest

from netports import ports


class Test(unittest.TestCase):
    """unittest ports.py"""

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
            result = ports.inumbers(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__iports(self):
        """iports()"""
        for items, error in [
            ("1-2-3", ValueError),
            ("1-a", ValueError),
            ("2-1", ValueError),
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
            ([[1]], ValueError),
            (b"a", ValueError),
            ([{}], ValueError),
            ("1 3 to 5", ValueError),  # HP style
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ports.snumbers(items=items)


if __name__ == "__main__":
    unittest.main()
