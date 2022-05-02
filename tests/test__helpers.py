"""unittest helpers.py"""

import unittest

from netports import helpers as h


class Test(unittest.TestCase):
    """unittest helpers.py"""

    def test_valid__list_of_str(self):
        """_list_of_str()"""
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
        """_list_of_str()"""
        for items, error in [
            (str, TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.list_of_str(items=items)


if __name__ == "__main__":
    unittest.main()
